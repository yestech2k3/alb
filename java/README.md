# Avi SDK

Avi SDK is a Java API which creates a session with controller and perform CRUD operations.

## Prerequisites
jdk 1.8

Maven
## Installation



Download the jar from https://github.com/vmware/alb-sdk/blob/java_sdk/java/target/avisdk-18.2.7-SNAPSHOT.jar

add the jar into the classpath of your project.

for documentation please refer https://github.com/vmware/alb-sdk/blob/java_sdk/java/target/avisdk-18.2.7-SNAPSHOT-javadoc.jar.

## Usage Examples

AviApi is a pilot class of the API.

- **Create Avi API Session :**
```
AviCredentials creds= new AviCredentials("198.51.100.12", "admin", "something");
creds.setTenant("admin");
creds.setVersion("18.2.8");
AviApi apiInstance = AviApi.getSession(creds);
```

- **Creating health monitor :**
```
JSONObject hmData = new JSONObject();
hmData.put("type","HEALTH_MONITOR_PING");
hmData.put("name","test_hm1");
hmData.put("send_interval","20");
apiInstance.post("healthmonitor", hmData);
```

- **Creating pool with one server and health monitor reference :**
```
JSONObject poolData = new JSONObject();
poolData.put("name", "test-pool");
poolData.put("enabled", true);
JSONObject poolServerData = new JSONObject();
poolServerData.put("enabled", false);
JSONObject serverIp = new JSONObject();
serverIp.put("addr", "192.0.0.1");
serverIp.put("type", "V4");
poolServerData.put("ip", serverIp);
poolData.put("servers", Arrays.asList(poolServerData));
poolData.put("health_monitor_ref", "/api/healthmonitor?name=test_hm1");
apiInstance.post("pool", poolData);
```

- **Creating vsvip :**
```
JSONObject vsVipData = new JSONObject();
vsVipData.put("name", "test-vsvip");
JSONObject vipServerIp = new JSONObject();
vipServerIp.put("addr", "10.90.20.51");
vipServerIp.put("type", "V4");
JSONObject vipData = new JSONObject();
vipData.put("ip_address", vipServerIp);
vipData.put("vip_id", "1");
vsVipData.put("vip", Arrays.asList(vipData));
apiInstance.post("vsvip", vsVipData);
```

- **Creating virtual service using pool and vsvip reference :**
```
JSONObject vsData = new JSONObject();
vsData.put("name", "sample_vs");
JSONObject vsServiceData = new JSONObject();
vsServiceData.put("port", "90");
vsServiceData.put("enable_ssl", false);
vsData.put("services", Arrays.asList(vsServiceData));
vsData.put("vsvip_ref", "/api/vsvip?name=test-vsvip");
vsData.put("pool_ref", "/api/pool?name=test-pool");
api.post("virtualservice", vsData);
```

- **Fetching object by name :**
```
Map<String, String> val = new HashMap<String, String>();
val.put("name", "sample_vs");
JSONObject virtualService = apiInstance.get("virtualservice", val);
```

- **Deleting object by name :**
```
Map<String, String> val = new HashMap<String, String>();
val.put("name", "sample_vs");
JSONObject virtualService = serv.get("virtualservice", val);
JSONArray resp = (JSONArray) virtualService.get("results");
JSONObject result = (JSONObject) resp.get(0);
String uuid = (String) result.get("uuid");
apiInstance.delete("virtualservice",uuid);
```
- **Uploading file :**
```
apiInstance.fileUpload("fileservice/hsmpackages?hsmtype=safenet", "/mnt/files/hsmpackages/safenet.tar","controller://hsmpackages");
```

- **Downloading file :**
```
Map<String, String> param = new HashMap<String, String>();
param.put("full_system", "true");
param.put("passphrase", "abc1234");
apiInstance.fileDownload("/configuration/export", "filepath", param);
```



