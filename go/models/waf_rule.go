// Copyright 2021 VMware, Inc.
// SPDX-License-Identifier: Apache License 2.0
package models

// This file is auto-generated.

// WafRule waf rule
// swagger:model WafRule
type WafRule struct {

	// Enable or disable WAF Rule Group. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	Enable *bool `json:"enable"`

	// Exclude list for the WAF rule. The fields in the exclude list entry are logically and'ed to deduce the exclusion criteria. If there are multiple excludelist entries, it will be 'logical or' of them. Field introduced in 17.2.3. Maximum of 64 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	ExcludeList []*WafExcludeListEntry `json:"exclude_list,omitempty"`

	//  Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	Index *int32 `json:"index"`

	// The rule field is sensitive and will not be displayed. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	IsSensitive *bool `json:"is_sensitive,omitempty"`

	// WAF Rule mode. This can be detection or enforcement. If this is not set, the Policy mode is used. This only takes effect if the policy allows delegation. Enum options - WAF_MODE_DETECTION_ONLY, WAF_MODE_ENFORCEMENT. Field introduced in 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Mode *string `json:"mode,omitempty"`

	// User-friendly optional name for a rule. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Name *string `json:"name,omitempty"`

	// The execution phase where this rule will be executed. Enum options - WAF_PHASE_CONNECTION, WAF_PHASE_REQUEST_HEADER, WAF_PHASE_REQUEST_BODY, WAF_PHASE_RESPONSE_HEADER, WAF_PHASE_RESPONSE_BODY, WAF_PHASE_LOGGING. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.
	// Read Only: true
	Phase *string `json:"phase,omitempty"`

	// Rule as per Modsec language. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	// Required: true
	Rule *string `json:"rule"`

	// Identifier (id) for a rule per Modsec language. All SecRule and SecAction directives require an id. It is extracted from the id action in a Modsec rule. Rules within a single WAF Policy are required to have unique rule_ids. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	RuleID *string `json:"rule_id,omitempty"`

	// Tags for WAF rule as per Modsec language. They are extracted from the tag action in a ModSec rule. Field introduced in 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.
	Tags []string `json:"tags,omitempty"`
}
