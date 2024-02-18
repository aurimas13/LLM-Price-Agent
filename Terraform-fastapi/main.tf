provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "FastApiAppResourceGroup"
  location = "East US"
}

resource "azurerm_container_registry" "acr" {
  name                     = "registrasbandymas"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"
  admin_enabled            = false
}

resource "azurerm_container_group" "app" {
  name                = "fastapi-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  ip_address_type     = "Public" # Corrected to "Public"
  dns_name_label      = "fastapiapp${random_string.dns_safe_label.result}"

  container {
    name   = "fastapi"
    image  = "registrasbandymas.azurecr.io/fastapi-app:latest"
    cpu    = 0.5
    memory = 1.5

    ports {
      port     = 8000
      protocol = "TCP"
    }

    environment_variables = {
      DATABASE_URL = "postgresql://user:password@db:5432/dbname"
    }
  }

  image_registry_credential {
    server   = "registrasbandymas.azurecr.io"
    username = "2fc234b2-f5c5-4707-b418-96cece298e5e" // replace with your service principal's appId
    password = "Sil8Q~anOyiQlgiInkJBf-LAOmowz~r0qxLA9dzi" // replace with your service principal's password
  }
}

resource "random_string" "dns_safe_label" {
  length  = 8
  special = false
  upper   = false
}

output "app_url" {
  value = "http://${azurerm_container_group.app.fqdn}/"
}


