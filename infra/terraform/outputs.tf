output "service_url" {
  value       = google_cloud_run_v2_service.service.uri
  description = "The URL of the deployed Cloud Run service"
}

output "artifact_registry_repository" {
  value       = google_artifact_registry_repository.repo.name
  description = "The Artifact Registry repository name"
}

output "service_account_email" {
  value       = google_service_account.cloud_run_sa.email
  description = "The service account email running the Cloud Run service"
}
