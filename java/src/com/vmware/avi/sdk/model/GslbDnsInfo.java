/*
 * Copyright 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.avi.sdk.model;

import java.util.*;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * The GslbDnsInfo is a POJO class extends AviRestResource that used for creating
 * GslbDnsInfo.
 *
 * @version 1.0
 * @since 
 *
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class GslbDnsInfo  {
    @JsonProperty("dns_active")
    private Boolean dnsActive = null;

    @JsonProperty("dns_vs_states")
    private List<GslbPerDnsState> dnsVsStates = null;

    @JsonProperty("gs_status")
    private GslbDnsGsStatus gsStatus = null;

    @JsonProperty("retry_count")
    private Integer retryCount = null;



    /**
     * This is the getter method this will return the attribute value.
     * This field indicates that atleast one dns is active at the site.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return dnsActive
     */
    public Boolean getDnsActive() {
        return dnsActive;
    }

    /**
     * This is the setter method to the attribute.
     * This field indicates that atleast one dns is active at the site.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param dnsActive set the dnsActive.
     */
    public void setDnsActive(Boolean  dnsActive) {
        this.dnsActive = dnsActive;
    }
    /**
     * This is the getter method this will return the attribute value.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return dnsVsStates
     */
    public List<GslbPerDnsState> getDnsVsStates() {
        return dnsVsStates;
    }

    /**
     * This is the setter method. this will set the dnsVsStates
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return dnsVsStates
     */
    public void setDnsVsStates(List<GslbPerDnsState>  dnsVsStates) {
        this.dnsVsStates = dnsVsStates;
    }

    /**
     * This is the setter method this will set the dnsVsStates
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return dnsVsStates
     */
    public GslbDnsInfo addDnsVsStatesItem(GslbPerDnsState dnsVsStatesItem) {
      if (this.dnsVsStates == null) {
        this.dnsVsStates = new ArrayList<GslbPerDnsState>();
      }
      this.dnsVsStates.add(dnsVsStatesItem);
      return this;
    }

    /**
     * This is the getter method this will return the attribute value.
     * This field encapsulates the gs-status edge-triggered framework.
     * Field introduced in 17.1.1.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return gsStatus
     */
    public GslbDnsGsStatus getGsStatus() {
        return gsStatus;
    }

    /**
     * This is the setter method to the attribute.
     * This field encapsulates the gs-status edge-triggered framework.
     * Field introduced in 17.1.1.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param gsStatus set the gsStatus.
     */
    public void setGsStatus(GslbDnsGsStatus gsStatus) {
        this.gsStatus = gsStatus;
    }

    /**
     * This is the getter method this will return the attribute value.
     * This field is used to track the retry attempts for se download errors.
     * Field introduced in 17.1.1.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return retryCount
     */
    public Integer getRetryCount() {
        return retryCount;
    }

    /**
     * This is the setter method to the attribute.
     * This field is used to track the retry attempts for se download errors.
     * Field introduced in 17.1.1.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param retryCount set the retryCount.
     */
    public void setRetryCount(Integer  retryCount) {
        this.retryCount = retryCount;
    }


    @Override
    public boolean equals(java.lang.Object o) {
      if (this == o) {
          return true;
      }
      if (o == null || getClass() != o.getClass()) {
          return false;
      }
      GslbDnsInfo objGslbDnsInfo = (GslbDnsInfo) o;
      return   Objects.equals(this.dnsActive, objGslbDnsInfo.dnsActive)&&
  Objects.equals(this.dnsVsStates, objGslbDnsInfo.dnsVsStates)&&
  Objects.equals(this.gsStatus, objGslbDnsInfo.gsStatus)&&
  Objects.equals(this.retryCount, objGslbDnsInfo.retryCount);
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("class GslbDnsInfo {\n");
                  sb.append("    dnsActive: ").append(toIndentedString(dnsActive)).append("\n");
                        sb.append("    dnsVsStates: ").append(toIndentedString(dnsVsStates)).append("\n");
                        sb.append("    gsStatus: ").append(toIndentedString(gsStatus)).append("\n");
                        sb.append("    retryCount: ").append(toIndentedString(retryCount)).append("\n");
                  sb.append("}");
      return sb.toString();
    }

    /**
     * Convert the given object to string with each line indented by 4 spaces
     * (except the first line).
     */
    private String toIndentedString(java.lang.Object o) {
      if (o == null) {
          return "null";
      }
      return o.toString().replace("\n", "\n    ");
    }
}
