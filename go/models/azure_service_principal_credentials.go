// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// AzureServicePrincipalCredentials azure service principal credentials
// swagger:model AzureServicePrincipalCredentials
type AzureServicePrincipalCredentials struct {

	// Application Id created for Avi Controller. Required for application id based authentication only. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	ApplicationID *string `json:"application_id,omitempty"`

	// Client Secret value created for the Avi Controller application. Required for application id based authentication only. . Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.
	ClientSecretValue *string `json:"client_secret_value,omitempty"`

	// Tenant ID for the subscription. Required for application id based authentication only. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	TenantID *string `json:"tenant_id,omitempty"`
}
