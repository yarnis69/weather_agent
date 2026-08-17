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


resource "google_project_service" "aiplatform" {
  service            = "aiplatform.googleapis.com"
  disable_on_destroy = false
}

