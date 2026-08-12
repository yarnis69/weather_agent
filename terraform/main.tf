# setup GCP terraform provider

terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "~> 6.0"
        }
    }
}

provider "google" {
    project = var.project_id
    region  = var.region
}


# enable requried GCP APIs

resource "google_project_service" "cloud_run" {
    service = "run.googleapis.com"
    disable_on_destroy = false
}

resource "google_project_service" "artifact_registry" {
    service = "artifactregistry.googleapis.com"
    disable_on_destroy = false
}

resource "google_project_service" "secret_manager" {
    service = "secretmanager.googleapis.com"
    disable_on_destroy = false
}


# create Google Artifact Registry repository for container images

resource "google_artifact_registry_repository" "weather_agent_repo" {
    location = var.region
    repository_id = "weather-agent-repo"
    format = "DOCKER"

    depends_on = [google_project_service.artifact_registry]
}

#create Secret Manager secret for the Gemini API key

resource "google_secret_manager_secret" "gemini_api_key" {
    secret_id = "gemini-api-key"
    replication {
        auto {}
    }
    
    depends_on = [google_project_service.secret_manager]
}

# create a dedicated service account for the Cloud Run service and grant it access to the Gemini API key secret

resource "google_service_account" "weather_agent_runtime" {
    account_id   = "weather-agent-runtime"
    display_name = "Service Account for Weather Agent Cloud Run Service"
}


resource "google_secret_manager_secret_iam_member" "runtime_secret_access" {
  secret_id = google_secret_manager_secret.gemini_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.weather_agent_runtime.email}"
}

# create the Cloud Run service and grant public access to it

resource "google_cloud_run_v2_service" "weather_agent" {
  name     = var.service_name
  location = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.weather_agent_runtime.email

    scaling {
      min_instance_count = 0
    }

    containers {
      image = var.container_image

      env {
        name  = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "False"
      }

      env {
        name = "GOOGLE_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_api_key.secret_id
            version = "latest"
          }
        }
      }
    }
  }

  depends_on = [google_project_service.cloud_run]
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.weather_agent.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}




# Setup WIF for Github, first creating a Workload Identity Pool, github provider and attribute mapping to allow federated access from a specific Github repository

resource "google_iam_workload_identity_pool" "github_actions_pool2" {
  provider                  = google
  workload_identity_pool_id = "github-actions-pool2"
  display_name              = "GitHub Workload Identity Pool"
  description               = "Workload Identity Pool for GitHub"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id = google_iam_workload_identity_pool.github_actions_pool2.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name = "GitHub WIF Provider"
  description = "Workload Identity Provider for GitHub"

  attribute_mapping = {
    "google.subject" = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }

  attribute_condition = "attribute.repository == 'yarnis69/weather_agent'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Setup and grant access to a dedicated Google service account for the Github identity pool

resource "google_service_account" "github_deployer" {
  account_id   = "github-actions-deployer"
  display_name = "GitHub Actions deployment identity"
}

resource "google_service_account_iam_member" "wif_impersonation" {
  service_account_id = google_service_account.github_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions_pool2.name}/attribute.repository/yarnis69/weather_agent"
}

# Grant the Google service account that will be impersonated by the Github identity pool access to the Google Artifact Registry repository, Cloud Run service and Cloud Run service account

resource "google_project_iam_member" "deployer_artifact_registry" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "deployer_cloud_run" {
  project = var.project_id
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_service_account_iam_member" "deployer_act_as_runtime" {
  service_account_id = google_service_account.weather_agent_runtime.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_deployer.email}"
}