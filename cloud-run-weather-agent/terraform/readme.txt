The following is required before the initial terraform apply

- increment the github_actions_pool name (due to previous deletion being soft)

- this new p


The following manual tasks after first terraform apply is made

- manually push agent docker image:

docker build -t europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent:v1 .
docker run -p 8080:8080 europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent
docker push europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent:v1

- manually give Gemini-API-Key Secret a value (excluded for security reasons)

After the second terraform apply succeeds create the following repository secrets in GitHub Actions (referenced in repo workflow files)

- WIF_PROVIDER = workload_identity_provider output by terraform
- WIF_SERVICE_ACCOUNT = github_deployer_email output by terraform


