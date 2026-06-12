terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.36.0"
    }
  }
}

provider "google" {
  credentials = "./keys/project_key.json"
  project     = "project-a5192a8b-0149-40ea-b1c"
  region      = "europe-west6"
}

resource "google_storage_bucket" "auto-expire" {
  name          = "project-a5192a8b-0149-40ea-b1c-terra-bucket"
  location      = "US"
  force_destroy = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}