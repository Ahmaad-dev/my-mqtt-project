variable "location" {
  type        = string
  default     = "westeurope"
  description = "Azure Region"
}

variable "resource_group_name" {
  type        = string
  description = "Name der Resource Group"
}

variable "access_token" {
  type        = string
  description = "Zugangstoken für den MQTT Broker"
  sensitive   = true
}

variable "broker_url" {
  type        = string
  description = "MQTT Broker URL (z. B. demo.thingsboard.io)"
}

variable "image_name" {
  type        = string
  description = "Image-Name ohne Registry (z. B. mqttclient:v1)"
}

variable "ca_file" {
  type        = string
  default     = "ca-root.pem"
  description = "Pfad zur Root-CA-Datei"
}
