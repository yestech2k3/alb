// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// Lif lif
// swagger:model Lif
type Lif struct {

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Cifs []*Cif `json:"cifs,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Lif *string `json:"lif,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	LifLabel *string `json:"lif_label,omitempty"`

	//  Field deprecated in 21.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Subnet *string `json:"subnet,omitempty"`
}
