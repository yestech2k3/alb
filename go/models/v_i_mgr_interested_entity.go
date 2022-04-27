// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// VIMgrInterestedEntity v i mgr interested entity
// swagger:model VIMgrInterestedEntity
type VIMgrInterestedEntity struct {

	//  Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	InterestedUUID *string `json:"interested_uuid"`
}
