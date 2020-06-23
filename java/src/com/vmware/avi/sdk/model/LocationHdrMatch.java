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
import java.util.ArrayList;
import java.util.List;
/**
 * LocationHdrMatch
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class LocationHdrMatch {
  @JsonProperty("match_case")
  private String matchCase = "INSENSITIVE";

  @JsonProperty("match_criteria")
  private String matchCriteria = null;

  @JsonProperty("value")
  private List<String> value = null;

  public LocationHdrMatch matchCase(String matchCase) {
    this.matchCase = matchCase;
    return this;
  }

   /**
   * Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE.
   * @return matchCase
  **/
  @Schema(description = "Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE.")
  public String getMatchCase() {
    return matchCase;
  }

  public void setMatchCase(String matchCase) {
    this.matchCase = matchCase;
  }

  public LocationHdrMatch matchCriteria(String matchCriteria) {
    this.matchCriteria = matchCriteria;
    return this;
  }

   /**
   * Criterion to use for matching location header value in the HTTP response. Enum options - HDR_EXISTS, HDR_DOES_NOT_EXIST, HDR_BEGINS_WITH, HDR_DOES_NOT_BEGIN_WITH, HDR_CONTAINS, HDR_DOES_NOT_CONTAIN, HDR_ENDS_WITH, HDR_DOES_NOT_END_WITH, HDR_EQUALS, HDR_DOES_NOT_EQUAL.
   * @return matchCriteria
  **/
  @Schema(required = true, description = "Criterion to use for matching location header value in the HTTP response. Enum options - HDR_EXISTS, HDR_DOES_NOT_EXIST, HDR_BEGINS_WITH, HDR_DOES_NOT_BEGIN_WITH, HDR_CONTAINS, HDR_DOES_NOT_CONTAIN, HDR_ENDS_WITH, HDR_DOES_NOT_END_WITH, HDR_EQUALS, HDR_DOES_NOT_EQUAL.")
  public String getMatchCriteria() {
    return matchCriteria;
  }

  public void setMatchCriteria(String matchCriteria) {
    this.matchCriteria = matchCriteria;
  }

  public LocationHdrMatch value(List<String> value) {
    this.value = value;
    return this;
  }

  public LocationHdrMatch addValueItem(String valueItem) {
    if (this.value == null) {
      this.value = new ArrayList<String>();
    }
    this.value.add(valueItem);
    return this;
  }

   /**
   * String value(s) in the location header.
   * @return value
  **/
  @Schema(description = "String value(s) in the location header.")
  public List<String> getValue() {
    return value;
  }

  public void setValue(List<String> value) {
    this.value = value;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    LocationHdrMatch locationHdrMatch = (LocationHdrMatch) o;
    return Objects.equals(this.matchCase, locationHdrMatch.matchCase) &&
        Objects.equals(this.matchCriteria, locationHdrMatch.matchCriteria) &&
        Objects.equals(this.value, locationHdrMatch.value);
  }

  @Override
  public int hashCode() {
    return Objects.hash(matchCase, matchCriteria, value);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class LocationHdrMatch {\n");
    
    sb.append("    matchCase: ").append(toIndentedString(matchCase)).append("\n");
    sb.append("    matchCriteria: ").append(toIndentedString(matchCriteria)).append("\n");
    sb.append("    value: ").append(toIndentedString(value)).append("\n");
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
