// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// VIControllerVnicInfo v i controller vnic info
// swagger:model VIControllerVnicInfo
type VIControllerVnicInfo struct {

	//  Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	Portgroup *string `json:"portgroup"`

	//  Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	VnicIP []*VIGuestvNicIPAddr `json:"vnic_ip,omitempty"`
}
