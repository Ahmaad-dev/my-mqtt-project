terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.5"
    }
  }
  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}
}