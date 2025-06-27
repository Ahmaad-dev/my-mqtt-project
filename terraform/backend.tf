terraform {
  backend "azurerm" {
    resource_group_name  = "fh-smdo"
    storage_account_name = "terraform01manual"
    container_name       = "tfstate"
    key                  = "terraform-infra.tfstate"
  }
}
