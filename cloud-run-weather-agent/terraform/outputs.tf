
output "cloud_run_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.weather_agent.uri
}

# output the requried workload identity provider and its associated google sevice account email to setup federated access in Github

output "workload_identity_provider" {
  description = "The Workload Identity Provider for GitHub"
  value       = google_iam_workload_identity_pool_provider.github_provider.name
}

output "github_deployer_email" {
  description = "The email of the GitHub Actions deployment service account"
  value       = google_service_account.github_deployer.email
}