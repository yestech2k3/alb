// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// NsxtSIServiceDetails nsxt s i service details
// swagger:model NsxtSIServiceDetails
type NsxtSIServiceDetails struct {

	// Error message. Field introduced in 20.1.8.
	ErrorString *string `json:"error_string,omitempty"`

	// NSX-T ServiceInsertion service name. Field introduced in 20.1.8.
	Service *string `json:"service,omitempty"`
}
