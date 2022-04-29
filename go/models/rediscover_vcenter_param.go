// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// RediscoverVcenterParam rediscover vcenter param
// swagger:model RediscoverVcenterParam
type RediscoverVcenterParam struct {

	//  Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	Cloud *string `json:"cloud"`
}
