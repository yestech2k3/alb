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
 * The SeDupipEventDetails is a POJO class extends AviRestResource that used for creating
 * SeDupipEventDetails.
 *
 * @version 1.0
 * @since 
 *
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SeDupipEventDetails  {
    @JsonProperty("local_mac")
    private String localMac = null;

    @JsonProperty("remote_mac")
    private String remoteMac = null;

    @JsonProperty("vnic_ip")
    private String vnicIp = null;

    @JsonProperty("vnic_name")
    private String vnicName = null;



    /**
     * This is the getter method this will return the attribute value.
     * Mac address.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return localMac
     */
    public String getLocalMac() {
        return localMac;
    }

    /**
     * This is the setter method to the attribute.
     * Mac address.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param localMac set the localMac.
     */
    public void setLocalMac(String  localMac) {
        this.localMac = localMac;
    }

    /**
     * This is the getter method this will return the attribute value.
     * Mac address.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return remoteMac
     */
    public String getRemoteMac() {
        return remoteMac;
    }

    /**
     * This is the setter method to the attribute.
     * Mac address.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param remoteMac set the remoteMac.
     */
    public void setRemoteMac(String  remoteMac) {
        this.remoteMac = remoteMac;
    }

    /**
     * This is the getter method this will return the attribute value.
     * Vnic ip.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return vnicIp
     */
    public String getVnicIp() {
        return vnicIp;
    }

    /**
     * This is the setter method to the attribute.
     * Vnic ip.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param vnicIp set the vnicIp.
     */
    public void setVnicIp(String  vnicIp) {
        this.vnicIp = vnicIp;
    }

    /**
     * This is the getter method this will return the attribute value.
     * Vnic name.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return vnicName
     */
    public String getVnicName() {
        return vnicName;
    }

    /**
     * This is the setter method to the attribute.
     * Vnic name.
     * Allowed in enterprise edition with any value, essentials, basic, enterprise with cloud services edition.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param vnicName set the vnicName.
     */
    public void setVnicName(String  vnicName) {
        this.vnicName = vnicName;
    }


    @Override
    public boolean equals(java.lang.Object o) {
      if (this == o) {
          return true;
      }
      if (o == null || getClass() != o.getClass()) {
          return false;
      }
      SeDupipEventDetails objSeDupipEventDetails = (SeDupipEventDetails) o;
      return   Objects.equals(this.vnicName, objSeDupipEventDetails.vnicName)&&
  Objects.equals(this.vnicIp, objSeDupipEventDetails.vnicIp)&&
  Objects.equals(this.remoteMac, objSeDupipEventDetails.remoteMac)&&
  Objects.equals(this.localMac, objSeDupipEventDetails.localMac);
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("class SeDupipEventDetails {\n");
                  sb.append("    localMac: ").append(toIndentedString(localMac)).append("\n");
                        sb.append("    remoteMac: ").append(toIndentedString(remoteMac)).append("\n");
                        sb.append("    vnicIp: ").append(toIndentedString(vnicIp)).append("\n");
                        sb.append("    vnicName: ").append(toIndentedString(vnicName)).append("\n");
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
