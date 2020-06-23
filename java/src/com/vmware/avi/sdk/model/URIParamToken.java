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
 * URIParamToken
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class URIParamToken {
  @JsonProperty("end_index")
  private Integer endIndex = null;

  @JsonProperty("start_index")
  private Integer startIndex = null;

  @JsonProperty("str_value")
  private String strValue = null;

  @JsonProperty("type")
  private String type = null;

  public URIParamToken endIndex(Integer endIndex) {
    this.endIndex = endIndex;
    return this;
  }

   /**
   * Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - &#x27;end of string&#x27;.
   * @return endIndex
  **/
  @Schema(description = "Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - 'end of string'.")
  public Integer getEndIndex() {
    return endIndex;
  }

  public void setEndIndex(Integer endIndex) {
    this.endIndex = endIndex;
  }

  public URIParamToken startIndex(Integer startIndex) {
    this.startIndex = startIndex;
    return this;
  }

   /**
   * Index of the starting token in the incoming URI.
   * @return startIndex
  **/
  @Schema(description = "Index of the starting token in the incoming URI.")
  public Integer getStartIndex() {
    return startIndex;
  }

  public void setStartIndex(Integer startIndex) {
    this.startIndex = startIndex;
  }

  public URIParamToken strValue(String strValue) {
    this.strValue = strValue;
    return this;
  }

   /**
   * Constant string to use as a token.
   * @return strValue
  **/
  @Schema(description = "Constant string to use as a token.")
  public String getStrValue() {
    return strValue;
  }

  public void setStrValue(String strValue) {
    this.strValue = strValue;
  }

  public URIParamToken type(String type) {
    this.type = type;
    return this;
  }

   /**
   * Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX.
   * @return type
  **/
  @Schema(required = true, description = "Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX.")
  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    URIParamToken urIParamToken = (URIParamToken) o;
    return Objects.equals(this.endIndex, urIParamToken.endIndex) &&
        Objects.equals(this.startIndex, urIParamToken.startIndex) &&
        Objects.equals(this.strValue, urIParamToken.strValue) &&
        Objects.equals(this.type, urIParamToken.type);
  }

  @Override
  public int hashCode() {
    return Objects.hash(endIndex, startIndex, strValue, type);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class URIParamToken {\n");
    
    sb.append("    endIndex: ").append(toIndentedString(endIndex)).append("\n");
    sb.append("    startIndex: ").append(toIndentedString(startIndex)).append("\n");
    sb.append("    strValue: ").append(toIndentedString(strValue)).append("\n");
    sb.append("    type: ").append(toIndentedString(type)).append("\n");
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
