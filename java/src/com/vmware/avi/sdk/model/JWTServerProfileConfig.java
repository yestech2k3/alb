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
 * The JWTServerProfileConfig is a POJO class extends AviRestResource that used for creating
 * JWTServerProfileConfig.
 *
 * @version 1.0
 * @since 
 *
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class JWTServerProfileConfig  {
    @JsonProperty("controller_internal_auth")
    private ControllerInternalAuth controllerInternalAuth = null;



    /**
     * This is the getter method this will return the attribute value.
     * Jwt auth configuration for profile_type controller_internal_auth.
     * Field introduced in 20.1.6.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @return controllerInternalAuth
     */
    public ControllerInternalAuth getControllerInternalAuth() {
        return controllerInternalAuth;
    }

    /**
     * This is the setter method to the attribute.
     * Jwt auth configuration for profile_type controller_internal_auth.
     * Field introduced in 20.1.6.
     * Default value when not specified in API or module is interpreted by Avi Controller as null.
     * @param controllerInternalAuth set the controllerInternalAuth.
     */
    public void setControllerInternalAuth(ControllerInternalAuth controllerInternalAuth) {
        this.controllerInternalAuth = controllerInternalAuth;
    }


    @Override
    public boolean equals(java.lang.Object o) {
      if (this == o) {
          return true;
      }
      if (o == null || getClass() != o.getClass()) {
          return false;
      }
      JWTServerProfileConfig objJWTServerProfileConfig = (JWTServerProfileConfig) o;
      return   Objects.equals(this.controllerInternalAuth, objJWTServerProfileConfig.controllerInternalAuth);
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      sb.append("class JWTServerProfileConfig {\n");
                  sb.append("    controllerInternalAuth: ").append(toIndentedString(controllerInternalAuth)).append("\n");
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
