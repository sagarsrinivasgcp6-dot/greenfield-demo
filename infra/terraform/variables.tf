variable "project_id" {
  type        = string
  description = "Google Cloud Project ID"
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
  default     = "task-manager"
}

variable "image" {
  type        = string
  description = "Full container image reference (immutable URL)"
}
