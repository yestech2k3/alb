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
import com.vmware.avi.sdk.model.EventMap;
import com.vmware.avi.sdk.model.PatchData;
import com.vmware.avi.sdk.model.SeGroupStatus;
import com.vmware.avi.sdk.model.SeUpgradeEvents;
import com.vmware.avi.sdk.model.UpgradeOpsParam;
import com.vmware.avi.sdk.model.UpgradeOpsState;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.ArrayList;
import java.util.List;
/**
 * UpgradeStatusInfo
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class UpgradeStatusInfo {
  @JsonProperty("_last_modified")
  private String _lastModified = null;

  @JsonProperty("duration")
  private Integer duration = null;

  @JsonProperty("enable_patch_rollback")
  private Boolean enablePatchRollback = null;

  @JsonProperty("enable_rollback")
  private Boolean enableRollback = null;

  @JsonProperty("end_time")
  private String endTime = null;

  @JsonProperty("enqueue_time")
  private String enqueueTime = null;

  @JsonProperty("image_ref")
  private String imageRef = null;

  @JsonProperty("name")
  private String name = null;

  @JsonProperty("node_type")
  private String nodeType = null;

  @JsonProperty("obj_cloud_ref")
  private String objCloudRef = null;

  @JsonProperty("params")
  private UpgradeOpsParam params = null;

  @JsonProperty("patch_image_ref")
  private String patchImageRef = null;

  @JsonProperty("patch_list")
  private List<PatchData> patchList = null;

  @JsonProperty("patch_version")
  private String patchVersion = null;

  @JsonProperty("previous_image_ref")
  private String previousImageRef = null;

  @JsonProperty("previous_patch_image_ref")
  private String previousPatchImageRef = null;

  @JsonProperty("previous_patch_list")
  private List<PatchData> previousPatchList = null;

  @JsonProperty("previous_patch_version")
  private String previousPatchVersion = null;

  @JsonProperty("previous_version")
  private String previousVersion = null;

  @JsonProperty("progress")
  private Integer progress = null;

  @JsonProperty("se_upgrade_events")
  private List<SeUpgradeEvents> seUpgradeEvents = null;

  @JsonProperty("seg_status")
  private SeGroupStatus segStatus = null;

  @JsonProperty("start_time")
  private String startTime = null;

  @JsonProperty("state")
  private UpgradeOpsState state = null;

  @JsonProperty("system")
  private Boolean system = null;

  @JsonProperty("tasks_completed")
  private Integer tasksCompleted = null;

  @JsonProperty("tenant_ref")
  private String tenantRef = null;

  @JsonProperty("total_tasks")
  private Integer totalTasks = null;

  @JsonProperty("upgrade_events")
  private List<EventMap> upgradeEvents = null;

  @JsonProperty("upgrade_ops")
  private String upgradeOps = null;

  @JsonProperty("url")
  private String url = null;

  @JsonProperty("uuid")
  private String uuid = null;

  @JsonProperty("version")
  private String version = null;

   /**
   * UNIX time since epoch in microseconds. Units(MICROSECONDS).
   * @return _lastModified
  **/
  @Schema(description = "UNIX time since epoch in microseconds. Units(MICROSECONDS).")
  public String getLastModified() {
    return _lastModified;
  }

  public UpgradeStatusInfo duration(Integer duration) {
    this.duration = duration;
    return this;
  }

   /**
   * Duration of Upgrade operation in seconds. Field introduced in 18.2.6.
   * @return duration
  **/
  @Schema(description = "Duration of Upgrade operation in seconds. Field introduced in 18.2.6.")
  public Integer getDuration() {
    return duration;
  }

  public void setDuration(Integer duration) {
    this.duration = duration;
  }

  public UpgradeStatusInfo enablePatchRollback(Boolean enablePatchRollback) {
    this.enablePatchRollback = enablePatchRollback;
    return this;
  }

   /**
   * Check if the patch rollback is possible on this node. Field introduced in 18.2.6.
   * @return enablePatchRollback
  **/
  @Schema(description = "Check if the patch rollback is possible on this node. Field introduced in 18.2.6.")
  public Boolean isEnablePatchRollback() {
    return enablePatchRollback;
  }

  public void setEnablePatchRollback(Boolean enablePatchRollback) {
    this.enablePatchRollback = enablePatchRollback;
  }

  public UpgradeStatusInfo enableRollback(Boolean enableRollback) {
    this.enableRollback = enableRollback;
    return this;
  }

   /**
   * Check if the rollback is possible on this node. Field introduced in 18.2.6.
   * @return enableRollback
  **/
  @Schema(description = "Check if the rollback is possible on this node. Field introduced in 18.2.6.")
  public Boolean isEnableRollback() {
    return enableRollback;
  }

  public void setEnableRollback(Boolean enableRollback) {
    this.enableRollback = enableRollback;
  }

  public UpgradeStatusInfo endTime(String endTime) {
    this.endTime = endTime;
    return this;
  }

   /**
   * End time of Upgrade operation. Field introduced in 18.2.6.
   * @return endTime
  **/
  @Schema(description = "End time of Upgrade operation. Field introduced in 18.2.6.")
  public String getEndTime() {
    return endTime;
  }

  public void setEndTime(String endTime) {
    this.endTime = endTime;
  }

  public UpgradeStatusInfo enqueueTime(String enqueueTime) {
    this.enqueueTime = enqueueTime;
    return this;
  }

   /**
   * Enqueue time of Upgrade operation. Field introduced in 18.2.6.
   * @return enqueueTime
  **/
  @Schema(description = "Enqueue time of Upgrade operation. Field introduced in 18.2.6.")
  public String getEnqueueTime() {
    return enqueueTime;
  }

  public void setEnqueueTime(String enqueueTime) {
    this.enqueueTime = enqueueTime;
  }

  public UpgradeStatusInfo imageRef(String imageRef) {
    this.imageRef = imageRef;
    return this;
  }

   /**
   * Image uuid for identifying the current base image. It is a reference to an object of type Image. Field introduced in 18.2.6.
   * @return imageRef
  **/
  @Schema(description = "Image uuid for identifying the current base image. It is a reference to an object of type Image. Field introduced in 18.2.6.")
  public String getImageRef() {
    return imageRef;
  }

  public void setImageRef(String imageRef) {
    this.imageRef = imageRef;
  }

  public UpgradeStatusInfo name(String name) {
    this.name = name;
    return this;
  }

   /**
   * Name of the system such as cluster name, se group name and se name. Field introduced in 18.2.6.
   * @return name
  **/
  @Schema(description = "Name of the system such as cluster name, se group name and se name. Field introduced in 18.2.6.")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public UpgradeStatusInfo nodeType(String nodeType) {
    this.nodeType = nodeType;
    return this;
  }

   /**
   * Type of the system such as controller_cluster, se_group or se. Enum options - NODE_CONTROLLER_CLUSTER, NODE_SE_GROUP, NODE_SE_TYPE. Field introduced in 18.2.6.
   * @return nodeType
  **/
  @Schema(description = "Type of the system such as controller_cluster, se_group or se. Enum options - NODE_CONTROLLER_CLUSTER, NODE_SE_GROUP, NODE_SE_TYPE. Field introduced in 18.2.6.")
  public String getNodeType() {
    return nodeType;
  }

  public void setNodeType(String nodeType) {
    this.nodeType = nodeType;
  }

  public UpgradeStatusInfo objCloudRef(String objCloudRef) {
    this.objCloudRef = objCloudRef;
    return this;
  }

   /**
   * Cloud that this object belongs to. It is a reference to an object of type Cloud. Field introduced in 18.2.6.
   * @return objCloudRef
  **/
  @Schema(description = "Cloud that this object belongs to. It is a reference to an object of type Cloud. Field introduced in 18.2.6.")
  public String getObjCloudRef() {
    return objCloudRef;
  }

  public void setObjCloudRef(String objCloudRef) {
    this.objCloudRef = objCloudRef;
  }

  public UpgradeStatusInfo params(UpgradeOpsParam params) {
    this.params = params;
    return this;
  }

   /**
   * Get params
   * @return params
  **/
  @Schema(description = "")
  public UpgradeOpsParam getParams() {
    return params;
  }

  public void setParams(UpgradeOpsParam params) {
    this.params = params;
  }

  public UpgradeStatusInfo patchImageRef(String patchImageRef) {
    this.patchImageRef = patchImageRef;
    return this;
  }

   /**
   * Image uuid for identifying the current patch.Example  Base-image is 18.2.6 and a patch 6p1 is applied, then this field will indicate the 6p1 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.
   * @return patchImageRef
  **/
  @Schema(description = "Image uuid for identifying the current patch.Example  Base-image is 18.2.6 and a patch 6p1 is applied, then this field will indicate the 6p1 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.")
  public String getPatchImageRef() {
    return patchImageRef;
  }

  public void setPatchImageRef(String patchImageRef) {
    this.patchImageRef = patchImageRef;
  }

  public UpgradeStatusInfo patchList(List<PatchData> patchList) {
    this.patchList = patchList;
    return this;
  }

  public UpgradeStatusInfo addPatchListItem(PatchData patchListItem) {
    if (this.patchList == null) {
      this.patchList = new ArrayList<PatchData>();
    }
    this.patchList.add(patchListItem);
    return this;
  }

   /**
   * List of patches applied to this node. Example  Base-image is 18.2.6 and a patch 6p1 is applied, then a patch 6p5 applied, this field will indicate the [{&#x27;6p1&#x27;, &#x27;6p1_image_uuid&#x27;}, {&#x27;6p5&#x27;, &#x27;6p5_image_uuid&#x27;}] value. Field introduced in 18.2.8, 20.1.1.
   * @return patchList
  **/
  @Schema(description = "List of patches applied to this node. Example  Base-image is 18.2.6 and a patch 6p1 is applied, then a patch 6p5 applied, this field will indicate the [{'6p1', '6p1_image_uuid'}, {'6p5', '6p5_image_uuid'}] value. Field introduced in 18.2.8, 20.1.1.")
  public List<PatchData> getPatchList() {
    return patchList;
  }

  public void setPatchList(List<PatchData> patchList) {
    this.patchList = patchList;
  }

  public UpgradeStatusInfo patchVersion(String patchVersion) {
    this.patchVersion = patchVersion;
    return this;
  }

   /**
   * Current patch version applied to this node. Example  Base-image is 18.2.6 and a patch 6p1 is applied, then this field will indicate the 6p1 value. . Field introduced in 18.2.6.
   * @return patchVersion
  **/
  @Schema(description = "Current patch version applied to this node. Example  Base-image is 18.2.6 and a patch 6p1 is applied, then this field will indicate the 6p1 value. . Field introduced in 18.2.6.")
  public String getPatchVersion() {
    return patchVersion;
  }

  public void setPatchVersion(String patchVersion) {
    this.patchVersion = patchVersion;
  }

  public UpgradeStatusInfo previousImageRef(String previousImageRef) {
    this.previousImageRef = previousImageRef;
    return this;
  }

   /**
   * Image uuid for identifying previous base image.Example  Base-image was 18.2.5 and an upgrade was done to 18.2.6, then this field will indicate the 18.2.5 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.
   * @return previousImageRef
  **/
  @Schema(description = "Image uuid for identifying previous base image.Example  Base-image was 18.2.5 and an upgrade was done to 18.2.6, then this field will indicate the 18.2.5 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.")
  public String getPreviousImageRef() {
    return previousImageRef;
  }

  public void setPreviousImageRef(String previousImageRef) {
    this.previousImageRef = previousImageRef;
  }

  public UpgradeStatusInfo previousPatchImageRef(String previousPatchImageRef) {
    this.previousPatchImageRef = previousPatchImageRef;
    return this;
  }

   /**
   * Image uuid for identifying previous patch.Example  Base-image was 18.2.6 with a patch 6p1. Upgrade was initiated to 18.2.8 with patch 8p1. The previous_image field will contain 18.2.6 and this field will indicate the 6p1 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.
   * @return previousPatchImageRef
  **/
  @Schema(description = "Image uuid for identifying previous patch.Example  Base-image was 18.2.6 with a patch 6p1. Upgrade was initiated to 18.2.8 with patch 8p1. The previous_image field will contain 18.2.6 and this field will indicate the 6p1 value. . It is a reference to an object of type Image. Field introduced in 18.2.6.")
  public String getPreviousPatchImageRef() {
    return previousPatchImageRef;
  }

  public void setPreviousPatchImageRef(String previousPatchImageRef) {
    this.previousPatchImageRef = previousPatchImageRef;
  }

  public UpgradeStatusInfo previousPatchList(List<PatchData> previousPatchList) {
    this.previousPatchList = previousPatchList;
    return this;
  }

  public UpgradeStatusInfo addPreviousPatchListItem(PatchData previousPatchListItem) {
    if (this.previousPatchList == null) {
      this.previousPatchList = new ArrayList<PatchData>();
    }
    this.previousPatchList.add(previousPatchListItem);
    return this;
  }

   /**
   * List of patches applied to this node on previous major version. Field introduced in 18.2.8, 20.1.1.
   * @return previousPatchList
  **/
  @Schema(description = "List of patches applied to this node on previous major version. Field introduced in 18.2.8, 20.1.1.")
  public List<PatchData> getPreviousPatchList() {
    return previousPatchList;
  }

  public void setPreviousPatchList(List<PatchData> previousPatchList) {
    this.previousPatchList = previousPatchList;
  }

  public UpgradeStatusInfo previousPatchVersion(String previousPatchVersion) {
    this.previousPatchVersion = previousPatchVersion;
    return this;
  }

   /**
   * Previous patch version applied to this node.Example  Base-image was 18.2.6 with a patch 6p1. Upgrade was initiated to 18.2.8 with patch 8p1. The previous_image field will contain 18.2.6 and this field will indicate the 6p1 value. . Field introduced in 18.2.6.
   * @return previousPatchVersion
  **/
  @Schema(description = "Previous patch version applied to this node.Example  Base-image was 18.2.6 with a patch 6p1. Upgrade was initiated to 18.2.8 with patch 8p1. The previous_image field will contain 18.2.6 and this field will indicate the 6p1 value. . Field introduced in 18.2.6.")
  public String getPreviousPatchVersion() {
    return previousPatchVersion;
  }

  public void setPreviousPatchVersion(String previousPatchVersion) {
    this.previousPatchVersion = previousPatchVersion;
  }

  public UpgradeStatusInfo previousVersion(String previousVersion) {
    this.previousVersion = previousVersion;
    return this;
  }

   /**
   * Previous version prior to upgrade.Example  Base-image was 18.2.5 and an upgrade was done to 18.2.6, then this field will indicate the 18.2.5 value. . Field introduced in 18.2.6.
   * @return previousVersion
  **/
  @Schema(description = "Previous version prior to upgrade.Example  Base-image was 18.2.5 and an upgrade was done to 18.2.6, then this field will indicate the 18.2.5 value. . Field introduced in 18.2.6.")
  public String getPreviousVersion() {
    return previousVersion;
  }

  public void setPreviousVersion(String previousVersion) {
    this.previousVersion = previousVersion;
  }

  public UpgradeStatusInfo progress(Integer progress) {
    this.progress = progress;
    return this;
  }

   /**
   * Upgrade operations progress which holds value between 0-100. Allowed values are 0-100. Field introduced in 18.2.8, 20.1.1.
   * @return progress
  **/
  @Schema(description = "Upgrade operations progress which holds value between 0-100. Allowed values are 0-100. Field introduced in 18.2.8, 20.1.1.")
  public Integer getProgress() {
    return progress;
  }

  public void setProgress(Integer progress) {
    this.progress = progress;
  }

  public UpgradeStatusInfo seUpgradeEvents(List<SeUpgradeEvents> seUpgradeEvents) {
    this.seUpgradeEvents = seUpgradeEvents;
    return this;
  }

  public UpgradeStatusInfo addSeUpgradeEventsItem(SeUpgradeEvents seUpgradeEventsItem) {
    if (this.seUpgradeEvents == null) {
      this.seUpgradeEvents = new ArrayList<SeUpgradeEvents>();
    }
    this.seUpgradeEvents.add(seUpgradeEventsItem);
    return this;
  }

   /**
   * ServiceEngineGroup upgrade errors. Field introduced in 18.2.6.
   * @return seUpgradeEvents
  **/
  @Schema(description = "ServiceEngineGroup upgrade errors. Field introduced in 18.2.6.")
  public List<SeUpgradeEvents> getSeUpgradeEvents() {
    return seUpgradeEvents;
  }

  public void setSeUpgradeEvents(List<SeUpgradeEvents> seUpgradeEvents) {
    this.seUpgradeEvents = seUpgradeEvents;
  }

  public UpgradeStatusInfo segStatus(SeGroupStatus segStatus) {
    this.segStatus = segStatus;
    return this;
  }

   /**
   * Get segStatus
   * @return segStatus
  **/
  @Schema(description = "")
  public SeGroupStatus getSegStatus() {
    return segStatus;
  }

  public void setSegStatus(SeGroupStatus segStatus) {
    this.segStatus = segStatus;
  }

  public UpgradeStatusInfo startTime(String startTime) {
    this.startTime = startTime;
    return this;
  }

   /**
   * Start time of Upgrade operation. Field introduced in 18.2.6.
   * @return startTime
  **/
  @Schema(description = "Start time of Upgrade operation. Field introduced in 18.2.6.")
  public String getStartTime() {
    return startTime;
  }

  public void setStartTime(String startTime) {
    this.startTime = startTime;
  }

  public UpgradeStatusInfo state(UpgradeOpsState state) {
    this.state = state;
    return this;
  }

   /**
   * Get state
   * @return state
  **/
  @Schema(description = "")
  public UpgradeOpsState getState() {
    return state;
  }

  public void setState(UpgradeOpsState state) {
    this.state = state;
  }

  public UpgradeStatusInfo system(Boolean system) {
    this.system = system;
    return this;
  }

   /**
   * Flag is set only in the cluster if the upgrade is initiated as a system-upgrade. . Field introduced in 18.2.6.
   * @return system
  **/
  @Schema(description = "Flag is set only in the cluster if the upgrade is initiated as a system-upgrade. . Field introduced in 18.2.6.")
  public Boolean isSystem() {
    return system;
  }

  public void setSystem(Boolean system) {
    this.system = system;
  }

  public UpgradeStatusInfo tasksCompleted(Integer tasksCompleted) {
    this.tasksCompleted = tasksCompleted;
    return this;
  }

   /**
   * Completed set of tasks in the Upgrade operation. Field introduced in 18.2.6.
   * @return tasksCompleted
  **/
  @Schema(description = "Completed set of tasks in the Upgrade operation. Field introduced in 18.2.6.")
  public Integer getTasksCompleted() {
    return tasksCompleted;
  }

  public void setTasksCompleted(Integer tasksCompleted) {
    this.tasksCompleted = tasksCompleted;
  }

  public UpgradeStatusInfo tenantRef(String tenantRef) {
    this.tenantRef = tenantRef;
    return this;
  }

   /**
   * Tenant that this object belongs to. It is a reference to an object of type Tenant. Field introduced in 18.2.6.
   * @return tenantRef
  **/
  @Schema(description = "Tenant that this object belongs to. It is a reference to an object of type Tenant. Field introduced in 18.2.6.")
  public String getTenantRef() {
    return tenantRef;
  }

  public void setTenantRef(String tenantRef) {
    this.tenantRef = tenantRef;
  }

  public UpgradeStatusInfo totalTasks(Integer totalTasks) {
    this.totalTasks = totalTasks;
    return this;
  }

   /**
   * Total number of tasks in the Upgrade operation. Field introduced in 18.2.6.
   * @return totalTasks
  **/
  @Schema(description = "Total number of tasks in the Upgrade operation. Field introduced in 18.2.6.")
  public Integer getTotalTasks() {
    return totalTasks;
  }

  public void setTotalTasks(Integer totalTasks) {
    this.totalTasks = totalTasks;
  }

  public UpgradeStatusInfo upgradeEvents(List<EventMap> upgradeEvents) {
    this.upgradeEvents = upgradeEvents;
    return this;
  }

  public UpgradeStatusInfo addUpgradeEventsItem(EventMap upgradeEventsItem) {
    if (this.upgradeEvents == null) {
      this.upgradeEvents = new ArrayList<EventMap>();
    }
    this.upgradeEvents.add(upgradeEventsItem);
    return this;
  }

   /**
   * Events performed for Upgrade operation. Field introduced in 18.2.6.
   * @return upgradeEvents
  **/
  @Schema(description = "Events performed for Upgrade operation. Field introduced in 18.2.6.")
  public List<EventMap> getUpgradeEvents() {
    return upgradeEvents;
  }

  public void setUpgradeEvents(List<EventMap> upgradeEvents) {
    this.upgradeEvents = upgradeEvents;
  }

  public UpgradeStatusInfo upgradeOps(String upgradeOps) {
    this.upgradeOps = upgradeOps;
    return this;
  }

   /**
   * Upgrade operations requested. Enum options - UPGRADE, PATCH, ROLLBACK, ROLLBACKPATCH, SEGROUP_RESUME. Field introduced in 18.2.6.
   * @return upgradeOps
  **/
  @Schema(description = "Upgrade operations requested. Enum options - UPGRADE, PATCH, ROLLBACK, ROLLBACKPATCH, SEGROUP_RESUME. Field introduced in 18.2.6.")
  public String getUpgradeOps() {
    return upgradeOps;
  }

  public void setUpgradeOps(String upgradeOps) {
    this.upgradeOps = upgradeOps;
  }

   /**
   * url
   * @return url
  **/
  @Schema(description = "url")
  public String getUrl() {
    return url;
  }

  public UpgradeStatusInfo uuid(String uuid) {
    this.uuid = uuid;
    return this;
  }

   /**
   * UUID Identifier for the system such as cluster, se group and se. Field introduced in 18.2.6.
   * @return uuid
  **/
  @Schema(description = "UUID Identifier for the system such as cluster, se group and se. Field introduced in 18.2.6.")
  public String getUuid() {
    return uuid;
  }

  public void setUuid(String uuid) {
    this.uuid = uuid;
  }

  public UpgradeStatusInfo version(String version) {
    this.version = version;
    return this;
  }

   /**
   * Current base image applied to this node. Field introduced in 18.2.6.
   * @return version
  **/
  @Schema(description = "Current base image applied to this node. Field introduced in 18.2.6.")
  public String getVersion() {
    return version;
  }

  public void setVersion(String version) {
    this.version = version;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    UpgradeStatusInfo upgradeStatusInfo = (UpgradeStatusInfo) o;
    return Objects.equals(this._lastModified, upgradeStatusInfo._lastModified) &&
        Objects.equals(this.duration, upgradeStatusInfo.duration) &&
        Objects.equals(this.enablePatchRollback, upgradeStatusInfo.enablePatchRollback) &&
        Objects.equals(this.enableRollback, upgradeStatusInfo.enableRollback) &&
        Objects.equals(this.endTime, upgradeStatusInfo.endTime) &&
        Objects.equals(this.enqueueTime, upgradeStatusInfo.enqueueTime) &&
        Objects.equals(this.imageRef, upgradeStatusInfo.imageRef) &&
        Objects.equals(this.name, upgradeStatusInfo.name) &&
        Objects.equals(this.nodeType, upgradeStatusInfo.nodeType) &&
        Objects.equals(this.objCloudRef, upgradeStatusInfo.objCloudRef) &&
        Objects.equals(this.params, upgradeStatusInfo.params) &&
        Objects.equals(this.patchImageRef, upgradeStatusInfo.patchImageRef) &&
        Objects.equals(this.patchList, upgradeStatusInfo.patchList) &&
        Objects.equals(this.patchVersion, upgradeStatusInfo.patchVersion) &&
        Objects.equals(this.previousImageRef, upgradeStatusInfo.previousImageRef) &&
        Objects.equals(this.previousPatchImageRef, upgradeStatusInfo.previousPatchImageRef) &&
        Objects.equals(this.previousPatchList, upgradeStatusInfo.previousPatchList) &&
        Objects.equals(this.previousPatchVersion, upgradeStatusInfo.previousPatchVersion) &&
        Objects.equals(this.previousVersion, upgradeStatusInfo.previousVersion) &&
        Objects.equals(this.progress, upgradeStatusInfo.progress) &&
        Objects.equals(this.seUpgradeEvents, upgradeStatusInfo.seUpgradeEvents) &&
        Objects.equals(this.segStatus, upgradeStatusInfo.segStatus) &&
        Objects.equals(this.startTime, upgradeStatusInfo.startTime) &&
        Objects.equals(this.state, upgradeStatusInfo.state) &&
        Objects.equals(this.system, upgradeStatusInfo.system) &&
        Objects.equals(this.tasksCompleted, upgradeStatusInfo.tasksCompleted) &&
        Objects.equals(this.tenantRef, upgradeStatusInfo.tenantRef) &&
        Objects.equals(this.totalTasks, upgradeStatusInfo.totalTasks) &&
        Objects.equals(this.upgradeEvents, upgradeStatusInfo.upgradeEvents) &&
        Objects.equals(this.upgradeOps, upgradeStatusInfo.upgradeOps) &&
        Objects.equals(this.url, upgradeStatusInfo.url) &&
        Objects.equals(this.uuid, upgradeStatusInfo.uuid) &&
        Objects.equals(this.version, upgradeStatusInfo.version);
  }

  @Override
  public int hashCode() {
    return Objects.hash(_lastModified, duration, enablePatchRollback, enableRollback, endTime, enqueueTime, imageRef, name, nodeType, objCloudRef, params, patchImageRef, patchList, patchVersion, previousImageRef, previousPatchImageRef, previousPatchList, previousPatchVersion, previousVersion, progress, seUpgradeEvents, segStatus, startTime, state, system, tasksCompleted, tenantRef, totalTasks, upgradeEvents, upgradeOps, url, uuid, version);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class UpgradeStatusInfo {\n");
    
    sb.append("    _lastModified: ").append(toIndentedString(_lastModified)).append("\n");
    sb.append("    duration: ").append(toIndentedString(duration)).append("\n");
    sb.append("    enablePatchRollback: ").append(toIndentedString(enablePatchRollback)).append("\n");
    sb.append("    enableRollback: ").append(toIndentedString(enableRollback)).append("\n");
    sb.append("    endTime: ").append(toIndentedString(endTime)).append("\n");
    sb.append("    enqueueTime: ").append(toIndentedString(enqueueTime)).append("\n");
    sb.append("    imageRef: ").append(toIndentedString(imageRef)).append("\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
    sb.append("    nodeType: ").append(toIndentedString(nodeType)).append("\n");
    sb.append("    objCloudRef: ").append(toIndentedString(objCloudRef)).append("\n");
    sb.append("    params: ").append(toIndentedString(params)).append("\n");
    sb.append("    patchImageRef: ").append(toIndentedString(patchImageRef)).append("\n");
    sb.append("    patchList: ").append(toIndentedString(patchList)).append("\n");
    sb.append("    patchVersion: ").append(toIndentedString(patchVersion)).append("\n");
    sb.append("    previousImageRef: ").append(toIndentedString(previousImageRef)).append("\n");
    sb.append("    previousPatchImageRef: ").append(toIndentedString(previousPatchImageRef)).append("\n");
    sb.append("    previousPatchList: ").append(toIndentedString(previousPatchList)).append("\n");
    sb.append("    previousPatchVersion: ").append(toIndentedString(previousPatchVersion)).append("\n");
    sb.append("    previousVersion: ").append(toIndentedString(previousVersion)).append("\n");
    sb.append("    progress: ").append(toIndentedString(progress)).append("\n");
    sb.append("    seUpgradeEvents: ").append(toIndentedString(seUpgradeEvents)).append("\n");
    sb.append("    segStatus: ").append(toIndentedString(segStatus)).append("\n");
    sb.append("    startTime: ").append(toIndentedString(startTime)).append("\n");
    sb.append("    state: ").append(toIndentedString(state)).append("\n");
    sb.append("    system: ").append(toIndentedString(system)).append("\n");
    sb.append("    tasksCompleted: ").append(toIndentedString(tasksCompleted)).append("\n");
    sb.append("    tenantRef: ").append(toIndentedString(tenantRef)).append("\n");
    sb.append("    totalTasks: ").append(toIndentedString(totalTasks)).append("\n");
    sb.append("    upgradeEvents: ").append(toIndentedString(upgradeEvents)).append("\n");
    sb.append("    upgradeOps: ").append(toIndentedString(upgradeOps)).append("\n");
    sb.append("    url: ").append(toIndentedString(url)).append("\n");
    sb.append("    uuid: ").append(toIndentedString(uuid)).append("\n");
    sb.append("    version: ").append(toIndentedString(version)).append("\n");
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
