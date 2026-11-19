variable "project_id" {
  type        = string
  description = "Google Cloud Project ID"
  default     = "bfstg-1e63363696974f759a3545"
}

variable "region" {
  type        = string
  description = "Google Cloud Region"
  default     = "us-central1"
}

variable "service_name" {
  type        = string
  description = "Cloud Run service name"
  default     = "task-manager-backend"
}

variable "repository_id" {
  type        = string
  description = "Artifact Registry repository ID"
  default     = "task-manager-repo"
}

variable "container_image" {
  type        = string
  description = "Immutable container image URI with tag or digest"
  default     = "us-central1-docker.pkg.dev/bfstg-1e63363696974f759a3545/task-manager-repo/task-manager-backend:latest"
}
