// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// OAuthResourceServer o auth resource server
// swagger:model OAuthResourceServer
type OAuthResourceServer struct {

	// Access token type. Enum options - ACCESS_TOKEN_TYPE_JWT, ACCESS_TOKEN_TYPE_OPAQUE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.
	// Required: true
	AccessType *string `json:"access_type"`

	// Validation parameters to be used when access token type is JWT. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.
	JwtParams *JWTValidationParams `json:"jwt_params,omitempty"`

	// Validation parameters to be used when access token type is opaque. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.
	OpaqueTokenParams *OpaqueTokenValidationParams `json:"opaque_token_params,omitempty"`
}
