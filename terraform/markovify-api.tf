terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}


resource "docker_container" "markovify-api" {
  image = "markovify-api:latest"
  name  = "markovify-api"
  ports {
    internal = 5000
    external = 6680
  }
  mounts {
      type = "volume"
      target = "/data"
      source = "markovify"
  }
}
