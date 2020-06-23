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
import com.vmware.avi.sdk.model.DsrProfile;
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * UDPFastPathProfile
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class UDPFastPathProfile {
  @JsonProperty("dsr_profile")
  private DsrProfile dsrProfile = null;

  @JsonProperty("per_pkt_loadbalance")
  private Boolean perPktLoadbalance = null;

  @JsonProperty("session_idle_timeout")
  private Integer sessionIdleTimeout = 10;

  @JsonProperty("snat")
  private Boolean snat = true;

  public UDPFastPathProfile dsrProfile(DsrProfile dsrProfile) {
    this.dsrProfile = dsrProfile;
    return this;
  }

   /**
   * Get dsrProfile
   * @return dsrProfile
  **/
  @Schema(description = "")
  public DsrProfile getDsrProfile() {
    return dsrProfile;
  }

  public void setDsrProfile(DsrProfile dsrProfile) {
    this.dsrProfile = dsrProfile;
  }

  public UDPFastPathProfile perPktLoadbalance(Boolean perPktLoadbalance) {
    this.perPktLoadbalance = perPktLoadbalance;
    return this;
  }

   /**
   * When enabled, every UDP packet is considered a new transaction and may be load balanced to a different server.  When disabled, packets from the same client source IP and port are sent to the same server.
   * @return perPktLoadbalance
  **/
  @Schema(description = "When enabled, every UDP packet is considered a new transaction and may be load balanced to a different server.  When disabled, packets from the same client source IP and port are sent to the same server.")
  public Boolean isPerPktLoadbalance() {
    return perPktLoadbalance;
  }

  public void setPerPktLoadbalance(Boolean perPktLoadbalance) {
    this.perPktLoadbalance = perPktLoadbalance;
  }

  public UDPFastPathProfile sessionIdleTimeout(Integer sessionIdleTimeout) {
    this.sessionIdleTimeout = sessionIdleTimeout;
    return this;
  }

   /**
   * The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600.
   * @return sessionIdleTimeout
  **/
  @Schema(description = "The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600.")
  public Integer getSessionIdleTimeout() {
    return sessionIdleTimeout;
  }

  public void setSessionIdleTimeout(Integer sessionIdleTimeout) {
    this.sessionIdleTimeout = sessionIdleTimeout;
  }

  public UDPFastPathProfile snat(Boolean snat) {
    this.snat = snat;
    return this;
  }

   /**
   * When disabled, Source NAT will not be performed for all client UDP packets.
   * @return snat
  **/
  @Schema(description = "When disabled, Source NAT will not be performed for all client UDP packets.")
  public Boolean isSnat() {
    return snat;
  }

  public void setSnat(Boolean snat) {
    this.snat = snat;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    UDPFastPathProfile udPFastPathProfile = (UDPFastPathProfile) o;
    return Objects.equals(this.dsrProfile, udPFastPathProfile.dsrProfile) &&
        Objects.equals(this.perPktLoadbalance, udPFastPathProfile.perPktLoadbalance) &&
        Objects.equals(this.sessionIdleTimeout, udPFastPathProfile.sessionIdleTimeout) &&
        Objects.equals(this.snat, udPFastPathProfile.snat);
  }

  @Override
  public int hashCode() {
    return Objects.hash(dsrProfile, perPktLoadbalance, sessionIdleTimeout, snat);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class UDPFastPathProfile {\n");
    
    sb.append("    dsrProfile: ").append(toIndentedString(dsrProfile)).append("\n");
    sb.append("    perPktLoadbalance: ").append(toIndentedString(perPktLoadbalance)).append("\n");
    sb.append("    sessionIdleTimeout: ").append(toIndentedString(sessionIdleTimeout)).append("\n");
    sb.append("    snat: ").append(toIndentedString(snat)).append("\n");
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
