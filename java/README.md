# Avi SDK

Avi SDK is a java API which creates a session with controller and perform CRUD operations.

## Prerequisites
jdk 1.8

Maven
## Installation



Download the latest jar from https://search.maven.org/artifact/com.vmware.avi.sdk/avisdk

add the jar into the classpath of your project. or depending on the project type,
you can add Avi SDK as a dependancy


## Usage Examples

We can Use Avi API in 2 ways:

1. AviApi Using Rest Template.

- **Create Avi API Session :**
```
AviCredentials aviCredentials = new AviCredentials("controller_ip", "username", "password");
aviCredentials.setTenant("tenant");
aviCredentials.setVersion("version");
AviApi restTemplate = AviApi.getSession(aviCredentials);
```

- **Creating health monitor :**
```
HealthMonitor healthMonitor = new HealthMonitor();
healthMonitor.setName("demo_HM");
healthMonitor.setType("HEALTH_MONITOR_PING");
restTemplate.post(healthMonitorObject);
```

- **Fetching health monitor info :**
```
HealthMonitor healthMonitor = restTemplate.getForObject(HealthMonitor.class, "healthmonitor-637a5af9-1b64-4040-bc5e-e94c9b524819");
```

- **Updating health monitor :**
```
HealthMonitor healthMonitorObject = restTemplate.getForObject(HealthMonitor.class, "healthmonitor-637a5af9-1b64-4040-bc5e-e94c9b524819");
healthMonitorObject.setName("updated_Hm");
restTemplate.put(healthMonitorObject, "healthmonitor-637a5af9-1b64-4040-bc5e-e94c9b524819");
```

- **Deleting health monitor :**
```
restTemplate.delete(HealthMonitor.class, "healthmonitor-637a5af9-1b64-4040-bc5e-e94c9b524819");
```

2. AviApi using JSON Object.

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

- **Fetching health monitor info :**
```
Map<String, String> val = new HashMap<String, String>();
val.put("name", "test_hm1");
JSONObject healthmonitor = apiInstance.get("healthmonitor", val);
```

- **Deleting health monitor :**
```
Map<String, String> val = new HashMap<String, String>();
val.put("name", "test_hm1");
JSONObject healthmonitor = serv.get("healthmonitor", val);
JSONArray resp = (JSONArray) healthmonitor.get("results");
JSONObject result = (JSONObject) resp.get(0);
String uuid = (String) result.get("uuid");
apiInstance.delete("healthmonitor",uuid);
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
