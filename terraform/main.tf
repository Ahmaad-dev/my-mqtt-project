resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = "acr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_container_group" "mqtt_client" {
  name                = "mqttclient-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  ip_address_type     = "Public"
  restart_policy      = "Always"

  container {
    name   = "mqttclient"
    image  = var.image_name
    cpu    = "0.5"
    memory = "1.0"

    environment_variables = {
      ACCESS_TOKEN = var.access_token
      BROKER       = var.broker_url
      CA_FILE      = var.ca_file
    }

    ports {
      port     = 8883
      protocol = "TCP"
    }
  }

  tags = {
    environment = "mqtt"
  }
}
