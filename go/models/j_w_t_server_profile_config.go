// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// JWTServerProfileConfig j w t server profile config
// swagger:model JWTServerProfileConfig
type JWTServerProfileConfig struct {

	// JWT Auth configuration for profile_type CONTROLLER_INTERNAL_AUTH. Field introduced in 20.1.6.
	ControllerInternalAuth *ControllerInternalAuth `json:"controller_internal_auth,omitempty"`
}
