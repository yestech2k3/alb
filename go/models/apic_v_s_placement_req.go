// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// ApicVSPlacementReq apic v s placement req
// swagger:model ApicVSPlacementReq
type ApicVSPlacementReq struct {

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Graph *string `json:"graph,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Lifs []*Lif `json:"lifs,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	NetworkRel []*APICNetworkRel `json:"network_rel,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	TenantName *string `json:"tenant_name,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Vdev *string `json:"vdev,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Vgrp *string `json:"vgrp,omitempty"`
}
