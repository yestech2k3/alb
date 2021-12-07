// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// ControllerInterface controller interface
// swagger:model ControllerInterface
type ControllerInterface struct {

	// Default gateway of the mgmt interface. Field introduced in 20.1.8.
	Gateway *IPAddr `json:"gateway,omitempty"`

	// Interface name. Field introduced in 20.1.8.
	IfName *string `json:"if_name,omitempty"`

	// IP address of the interface. Field introduced in 20.1.8.
	IP *IPAddrPrefix `json:"ip,omitempty"`

	// Interface label like mgmt, secure channel or HSM. Enum options - MGMT, SE_SECURE_CHANNEL, HSM. Field introduced in 20.1.8.
	Labels []string `json:"labels,omitempty"`

	// Mac address of interface. Field introduced in 20.1.8.
	MacAddress *string `json:"mac_address,omitempty"`

	// IP address mode DHCP/STATIC. Enum options - DHCP, STATIC, VIP, DOCKER_HOST. Field introduced in 20.1.8.
	Mode *string `json:"mode,omitempty"`

	// Public IP of interface. Field introduced in 20.1.8.
	PublicIPOrName *IPAddr `json:"public_ip_or_name,omitempty"`
}
