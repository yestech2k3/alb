// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// NsxtSIRuleDetails nsxt s i rule details
// swagger:model NsxtSIRuleDetails
type NsxtSIRuleDetails struct {

	// Rule Action. Field introduced in 20.1.8.
	Action *string `json:"action,omitempty"`

	// Destinatios excluded or not. Field introduced in 20.1.8.
	Destexclude *bool `json:"destexclude,omitempty"`

	// Destination of redirection rule. Field introduced in 20.1.8.
	Dests []string `json:"dests,omitempty"`

	// Rule Direction. Field introduced in 20.1.8.
	Direction *string `json:"direction,omitempty"`

	// Error message. Field introduced in 20.1.8.
	ErrorString *string `json:"error_string,omitempty"`

	// Pool name. Field introduced in 20.1.8.
	Pool *string `json:"pool,omitempty"`

	// ServiceEngineGroup name. Field introduced in 20.1.8.
	Segroup *string `json:"segroup,omitempty"`

	// Services of redirection rule. Field introduced in 20.1.8.
	Services []string `json:"services,omitempty"`

	// Sources of redirection rule. Field introduced in 20.1.8.
	Sources []string `json:"sources,omitempty"`
}
