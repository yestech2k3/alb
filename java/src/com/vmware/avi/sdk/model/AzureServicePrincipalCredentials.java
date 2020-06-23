/*
 * Avi avi_global_spec Object API
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 20.1.1
 * Contact: support@avinetworks.com
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */

package com.vmware.avi.sdk.model;

import java.util.Objects;
import java.util.Arrays;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * AzureServicePrincipalCredentials
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class AzureServicePrincipalCredentials {
  @JsonProperty("application_id")
  private String applicationId = null;

  @JsonProperty("authentication_token")
  private String authenticationToken = null;

  @JsonProperty("tenant_id")
  private String tenantId = null;

  public AzureServicePrincipalCredentials applicationId(String applicationId) {
    this.applicationId = applicationId;
    return this;
  }

   /**
   * Application Id created for Avi Controller. Required for application id based authentication only. Field introduced in 17.2.1.
   * @return applicationId
  **/
  @Schema(description = "Application Id created for Avi Controller. Required for application id based authentication only. Field introduced in 17.2.1.")
  public String getApplicationId() {
    return applicationId;
  }

  public void setApplicationId(String applicationId) {
    this.applicationId = applicationId;
  }

  public AzureServicePrincipalCredentials authenticationToken(String authenticationToken) {
    this.authenticationToken = authenticationToken;
    return this;
  }

   /**
   * Authentication token created for the Avi Controller application. Required for application id based authentication only. Field introduced in 17.2.1.
   * @return authenticationToken
  **/
  @Schema(description = "Authentication token created for the Avi Controller application. Required for application id based authentication only. Field introduced in 17.2.1.")
  public String getAuthenticationToken() {
    return authenticationToken;
  }

  public void setAuthenticationToken(String authenticationToken) {
    this.authenticationToken = authenticationToken;
  }

  public AzureServicePrincipalCredentials tenantId(String tenantId) {
    this.tenantId = tenantId;
    return this;
  }

   /**
   * Tenant ID for the subscription. Required for application id based authentication only. Field introduced in 17.2.1.
   * @return tenantId
  **/
  @Schema(description = "Tenant ID for the subscription. Required for application id based authentication only. Field introduced in 17.2.1.")
  public String getTenantId() {
    return tenantId;
  }

  public void setTenantId(String tenantId) {
    this.tenantId = tenantId;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    AzureServicePrincipalCredentials azureServicePrincipalCredentials = (AzureServicePrincipalCredentials) o;
    return Objects.equals(this.applicationId, azureServicePrincipalCredentials.applicationId) &&
        Objects.equals(this.authenticationToken, azureServicePrincipalCredentials.authenticationToken) &&
        Objects.equals(this.tenantId, azureServicePrincipalCredentials.tenantId);
  }

  @Override
  public int hashCode() {
    return Objects.hash(applicationId, authenticationToken, tenantId);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class AzureServicePrincipalCredentials {\n");
    
    sb.append("    applicationId: ").append(toIndentedString(applicationId)).append("\n");
    sb.append("    authenticationToken: ").append(toIndentedString(authenticationToken)).append("\n");
    sb.append("    tenantId: ").append(toIndentedString(tenantId)).append("\n");
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
