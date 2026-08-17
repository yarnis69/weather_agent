# Weather Agent — AI agent on Google Cloud

An AI agent built with Google's Agent Development Kit (ADK), deployed to GCP two different ways: as a container on Cloud Run with Terraform-managed infrastructure and a GitHub Actions pipeline, and as a managed deployment on Agent Runtime.

Built independently to get hands-on with agentic AI security — agent identity, tool-use risk, and the supply-chain questions that come with agent tooling.

---

## What it does

A conversational agent that answers weather questions. The model decides when to call a tool, the tool fetches real data, and the agent explains the forecast and any precautions worth taking.

The tool geocodes a place name and then fetches current conditions from [Open-Meteo](https://open-meteo.com/) — a free API requiring no key or account.

---

## Architecture

```
User → ADK Agent (Gemini) → get_weather tool → Open-Meteo API
                │
                └── deployed to:
                      ├── Cloud Run  (container, Terraform + GitHub Actions)
                      └── Agent Runtime  (managed, deployed via Python SDK)
```

**Cloud Run path**
- Python + ADK in a Docker container
- Image in Artifact Registry
- Infrastructure defined in Terraform
- API key in Secret Manager, mounted as an environment variable at runtime
- Deployed by GitHub Actions on push to `main`, authenticated with Workload Identity Federation

**Agent Runtime path**
- Same agent code, no Dockerfile
- Deployed via the Vertex AI Python SDK
- Model access through Vertex AI rather than an API key
- Managed sessions and Cloud Trace observability

---

## Design decisions

### Keyless CI/CD with Workload Identity Federation

The pipeline authenticates to GCP using Workload Identity Federation rather than a downloaded service account JSON key stored as a GitHub secret.

Most tutorials use the key file. It doesn't expire, doesn't rotate, and if it leaks — repo made public by accident, secret exposed in a build log — it's usable indefinitely by whoever finds it.

With WIF, GitHub issues a short-lived OIDC token per workflow run. GCP verifies the signature against GitHub's public keys, checks an attribute condition restricting trust to this specific repository, and only then issues temporary credentials. No long-lived credential exists to steal.

The attribute condition is the part doing the real work — without it, any GitHub Actions workflow from any repository could authenticate through the provider.

### Separate deploy-time and run-time identities

Two service accounts, not one:

- `github-actions-deployer` — pushes images and deploys. Holds `roles/artifactregistry.writer` and `roles/run.developer`, deliberately not `run.admin`.
- `weather-agent-runtime` — the identity the running service acts as. Holds only `roles/secretmanager.secretAccessor` on one secret.

If the container is compromised, its identity can read a single secret and do nothing else. The deployer's broader permissions aren't available to it.

Deploying a service that runs as another identity also requires `roles/iam.serviceAccountUser` on that identity — GCP's guard against privilege escalation via deployment.

### Direct API call over a third-party MCP server

An earlier version used a community MCP server via `npx`, connected through ADK's `McpToolset`.

It worked, but `npx -y <package>@latest` fetches and executes third-party code from the npm registry on every start, with no review step and no version pin. Given the run of npm supply-chain compromises through 2025–26 — Shai-Hulud, the Axios hijack, the Mastra postinstall payload — that's a real trust surface for a tool whose entire job is fetching public weather data.

The current version calls Open-Meteo directly from a Python function. Fewer moving parts, no third-party code execution, and the code that runs is code in this repository.

The MCP work is retained on a branch. It was worth building — understanding the client/server split, stdio versus HTTP transport, and the runtime tool-discovery handshake is the point, not shipping it.

### Cloud Run over GKE

A single stateless service doesn't justify cluster management overhead. Cloud Run scales to zero, costs nothing idle, and requires no networking, RBAC, or node configuration.

GKE would earn its complexity with several interdependent services, node-level control requirements, or an existing cluster to sit alongside. None applied here.

### Immutable image tags

Images are tagged with the commit SHA rather than `:latest`. Every deployed revision traces to exact source, and rollback targets a specific known build rather than whatever `latest` happened to point at.

### Pinned dependency versions

`requirements.txt` pins exact versions. This isn't theoretical — a major release of the `mcp` package broke ADK's MCP imports silently, with the module exporting nothing rather than raising an error. Diagnosing that cost more time than pinning ever would.

---

### Pipeline

Push to `main`. The workflow authenticates via WIF, builds, pushes to Artifact Registry, and deploys the new revision.

