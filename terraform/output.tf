output "mqtt_container_group_ip" {
  value = azurerm_container_group.mqtt_client.ip_address
}
