variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west2"
}     

variable "service_name" {
    description = "Name of the Cloud Run service"
    type        = string
    default     = "weather-agent"
}

variable "container_image" {
    description = "Full path to the container image in Artifact Registry"
    type        = string
}