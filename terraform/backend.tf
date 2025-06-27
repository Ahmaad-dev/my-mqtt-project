terraform {
  backend "azurerm" {
    container_name       = "tfstate"
    key                  = "terraform-infra.tfstate"
    resource_group_name  = "fh-smdo"
    storage_account_name = "terraform01manual"
    subscription_id      = "7c21e53b-0e8a-4cd9-8d45-c5905f358e7e"
    use_azuread_auth     = true
  }
}
