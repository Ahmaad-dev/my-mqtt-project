resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_log_analytics_workspace" "log" {
  name                = "log-${random_string.suffix.result}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                       = var.container_env_name
  location                   = var.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log.id
}

resource "azurerm_container_registry" "acr" {
  name                = "acr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_container_app" "app" {
  name                         = var.container_app_name
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name         = azurerm_resource_group.main.name
  location                    = var.location
  revision_mode               = "Single"

  template {
    container {
      name   = "mqttclient"
      image  = var.image_name
      cpu    = 0.5
      memory = "1.0Gi"
      
      env {
        name  = "ACCESS_TOKEN"
        value = var.access_token
      }

      env {
        name  = "BROKER"
        value = var.broker_url
      }
      
      env {
        name  = "CA_FILE"
        value = var.ca_file
      }
    }
  }

  identity {
    type = "SystemAssigned"
  }

  ingress {
    external_enabled = false
    target_port      = 80
    transport        = "auto"
    
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}

