// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// NsxtSIEndpointDetails nsxt s i endpoint details
// swagger:model NsxtSIEndpointDetails
type NsxtSIEndpointDetails struct {

	// VirtualEndpoint Path. Field introduced in 20.1.8.
	Endpoint *string `json:"endpoint,omitempty"`

	// Error message. Field introduced in 20.1.8.
	ErrorString *string `json:"error_string,omitempty"`

	// ServiceEngineGroup name. Field introduced in 20.1.8.
	Segroup *string `json:"segroup,omitempty"`

	// Services where endpoint refers. Field introduced in 20.1.8.
	Services []string `json:"services,omitempty"`

	// Endpoint Target IPs. Field introduced in 20.1.8.
	TargetIps []string `json:"targetIps,omitempty"`

	// Tier1 path. Field introduced in 20.1.8.
	Tier1 *string `json:"tier1,omitempty"`
}
