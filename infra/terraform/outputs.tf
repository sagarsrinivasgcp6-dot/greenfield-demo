output "service_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.service.uri
}

output "repository_url" {
  description = "URL of Artifact Registry repository"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}"
}

output "service_account_email" {
  description = "Email of the service account for Cloud Run"
  value       = google_service_account.cloud_run_sa.email
}
