package models

// This file is auto-generated.
// Please contact avi-sdk@avinetworks.com for any change requests.

// AttackDNSAmplification attack Dns amplification
// swagger:model AttackDnsAmplification
type AttackDNSAmplification struct {

	// The record type in the DNS query. Enum options - DNS_RECORD_OTHER, DNS_RECORD_A, DNS_RECORD_NS, DNS_RECORD_CNAME, DNS_RECORD_SOA, DNS_RECORD_PTR, DNS_RECORD_HINFO, DNS_RECORD_MX, DNS_RECORD_TXT, DNS_RECORD_RP, DNS_RECORD_DNSKEY, DNS_RECORD_AAAA, DNS_RECORD_SRV, DNS_RECORD_OPT, DNS_RECORD_RRSIG, DNS_RECORD_AXFR, DNS_RECORD_ANY. Field introduced in 21.1.1.
	RecordType *string `json:"record_type,omitempty"`

	// The source port for the DNS query. Field introduced in 21.1.1.
	SrcPort *int32 `json:"src_port,omitempty"`
}
