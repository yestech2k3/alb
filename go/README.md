# Avi Go SDK and Utilities

Avi GO SDK is a Go Package that provides APIs to communicate with Avi Controller’s REST APIs. It uses Avisession class and provides utilities to simplify integration with Avi controller.

It handles session authentication and keeps a cache of sessions to avoid multiple connection setups and teardowns across different API Session invocation. It automatically updates session cookies, 
CSRF Tokens from controller and provides helper APIs and templates for Avi Objects. Other important features are X-AVI-TENANT (tenant) header handling and sample source code for common load balancing examples.

Here are list of important SDK directories

- **Go**: Source for the Go SDK. No need to download packages. Go will take care of a packages installations.
Here are list of important SDK directories
    - **examples**: Go sample are in directory go/examples.
        - **create_vs.go**: Gives example to create session and generic client to Avi Controller, Create pool with one 
        server, Create SSL VS and Fetch object by name.
   
    - **clients**: It contains AviClients which are needed to establish connection between the Go SDK and Avi Controller
     using the Avi session class. Each resource has its own client to establish connection.
   
    - **sessions**: It contains all generic code of REST calls for Avi session and helper routines from REST API calls. 
    It creates and maintains session for a given resurce.
   
    - **models**: It contains all models required to capture the API response. Basically its nothing but the structures 
    to grab and store data of corresponding REST API calls.
# Prerequisites
Go Lang ([Click here](https://golang.org/doc/install) for more information)

# Installation
They can be installed simply as:
### Avi Go SDK Install
```sh
$ mkdir -p src/github.com/avinetworks/
$ cd src/github.com/avinetworks/
$ git clone https://github.com/vmware/alb-sdk.git
#GOPATH will be path till src dir.
$ export GOPATH=~/src
```

### Usage Examples
Please follow following steps to create session, pool and virtualservice.
1. Create create_vs.go file and write following code in the file.
2. Import AVI session, models and clients
```
package main

import (
	"github.com/vmware/alb-sdk/go/clients"
	"github.com/vmware/alb-sdk/go/models"
	"github.com/vmware/alb-sdk/go/session"
	)
```
3. Create AVI API session. Specify AVI controller IP, username, password, tenant and API version
for your NSX ALB controller
```
aviClient, err := clients.NewAviClient("10.10.25.25", "admin",
		session.SetPassword("something"),
		session.SetTenant("admin"),
		session.SetInsecure,
		session.SetControllerStatusCheckLimits(5, 10)
		session.SetVersion("22.1.1"))
```
- We can use following options while creating session.
    - **SetPassword(password string)** : Use this for NewAviSession option argument for setting password
    - **SetTenant(tenant string)** : Use this for NewAviSession option argument for setting tenant
    - **SetInsecure** : Use this for NewAviSession option argument for allowing insecure connection to AviController
    - **SetControllerStatusCheckLimits(numRetries, retryInterval int)** : 
        SetControllerStatusCheckLimits allows client to limit the number of tries the SDK should 
        attempt to reach the controller at the time gap of specified time intervals.
    - **SetTransport(transport \*http.Transport)** : Use this for NewAviSession option argument for
        configuring http transport to enable connection
    - **SetClient(client HttpClient)** : SetClient allows callers to inject their own HTTP client.
    - **SetVersion(version string)** : Use this for NewAviSession option argument for setting version
    - **SetAuthToken(authToken string)** : Use this for NewAviSession option argument for setting authToken
    - **SetRefreshAuthTokenCallback(f func() string)** : Use this for NewAviSession option argument 
        for setting authToken
    - **SetRefreshAuthTokenCallbackV2(f func() (string, error))** : Use this for NewAviSession 
        option argument for setting authToken with option to return error found
    - **DisableControllerStatusCheckOnFailure(controllerStatusCheck bool)** : Use this for 
        NewAviSession option argument to disable controller status check.
    - **SetTimeout(timeout time.Duration)** : Use this for NewAviSession option argument to set 
        API timeout
    - **SetLazyAuthentication(lazyAuthentication bool)** : Use this for NewAviSession option 
        argument to enable the lazy authentication.
    - **SetMaxApiRetries(max_api_retries int)** : Use this for NewAviSession option argument to 
        sel maximum allowed API retries
    - **SetApiRetryInterval(api_retry_interval int)** : Use this for NewAviSession option argument 
        to set API retry interval.

4. Create pool 'my-test-pool' with one server. Here we can use the models defined in go/models.
```go
pobj := models.Pool{}
pname := "my-test-pool"
pobj.Name = &pname
serverobj := models.Server{}
enabled := true
serverobj.Enabled = &enabled
ipType := "V4"
addr := "10.90.20.12"
serverobj.IP = &models.IPAddr{Type: &ipType, Addr: &addr}
pobj.Servers = append(pobj.Servers, &serverobj)

npobj, err := aviClient.Pool.Create(&pobj)
if err != nil {
  fmt.Println("Pool creation failed: ", err)
  return
}
```

5. Create vsvip 'test-vip' :

```go
vsVip := models.VsVip{}
vipAddr := "10.90.20.51"
vipip := models.IPAddr{Type: &ipType, Addr: &vipAddr}
vipId := "1"
vipObj := models.Vip{VipID: &vipId, IPAddress: &vipip}

vipName := "test-vip"
vsVip.Name = &vipName
vsVip.Vip = append(vsVip.Vip, &vipObj)

vsVipObj, err := aviClient.VsVip.Create(&vsVip)

if err != nil {
    fmt.Println("VIP creation failed: ", err)
}
```

6. Create virtualservice 'my-test-vs' using pool 'my-test-pool':

```go
vsobj := models.VirtualService{}
vname := "my-test-vs"
vsobj.Name = &vname
vsobj.VsvipRef = vsVipObj.UUID
vsobj.PoolRef = npobj.UUID
port := int32(80)
vsobj.Services = append(vsobj.Services, &models.Service{Port: &port})

nvsobj, err := aviClient.VirtualService.Create(&vsobj)
if err != nil {
    fmt.Println("VS creation failed: ", err)
    return
}
fmt.Printf("VS obj: %+v", *nvsobj)
```

7. Fetching object by name:

```go
var obj interface{}
err = aviClient.AviSession.GetObjectByName("virtualservice", "my-test-vs", &obj)
fmt.Printf("VS obj: %v\n", obj)

err = aviClient.AviSession.GetObject(
	"virtualservice", session.SetName("my-test-vs"), session.SetResult(&obj),
	session.SetCloudUUID("cloud-f39f950a-e6ca-442d-b546-fc31520991bb"))
fmt.Printf("VS with CLOUD_UUID obj: %v", obj)
```

8. Delete virtualservice

```go
aviClient.VirtualService.Delete(nvsobj.UUID)
```
9. Delete pool

```go
aviClient.Pool.Delete(npobj.UUID)
```
10. Now we can run create_vs.go to create/delete VS, pool.
```sh
$ go run create_vs.go
```

- Metric and Inventory API example:
```go
package main

import (
	//"flag"
	"fmt"
	"github.com/vmware/alb-sdk/go/clients"
	"github.com/vmware/alb-sdk/go/session"
)

type MetricRequest struct {
	Step           int    `json:"step"`
	Limit          int    `json:"limit"`
	EntityUUID     string `json:"entity_uuid"`
	MetricID       string `json:"metric_id"`
	IncludeName    string `json:"include_name"`
	IncludeRefs    string `json:"include_refs"`
	PadMissingData string `json:"pad_missing_data"`
}

type Metrics struct {
	MetricRequests []MetricRequest `json:"metric_requests"`
}

func main() {
	// Create a session and a generic client to Avi Controller
	aviClient, err := clients.NewAviClient("10.10.25.42", "admin",
		session.SetPassword(""),
		session.SetTenant("admin"),
		session.SetInsecure)
	if err != nil {
		fmt.Println("Couldn't create session: ", err)
		return
	}
	mr := MetricRequest{Step: 1, Limit: 1, EntityUUID: "*", MetricID: "l7_server.max_concurrent_sessions", IncludeName: "True", IncludeRefs: "True", PadMissingData: "False"}
	sr := []MetricRequest{}
	sr = append(sr, mr)
	req := Metrics{MetricRequests: sr}
	path := "/api/analytics/metrics/collection"
	var rsp interface{}
	aviClient.AviSession.Post(path, req, &rsp)
	fmt.Printf("response %v\n", rsp)
}
```
- To compile:

```sh
$ go build -o /usr/bin/create_vs create_vs.go
```
- To include Go SDK in third party code:

Following is an example entry of vendor.json file in Terraform provider
```go
"package": [{
                "path": "github.com/vmware/alb-sdk/go/clients",
                "revision": "23def4e6c14b4da8ac2ed8007337bc5eb5007998",
                "revisionTime": "2016-01-25T20:49:56Z",
                "version": "18.1.3",
                "versionExact": "18.1.3"
            },
            {
                "path": "github.com/vmware/alb-sdk/go/session",
                "revision": "23def4e6c14b4da8ac2ed8007337bc5eb5007998",
                "revisionTime": "2016-01-25T20:49:56Z",
                "version": "18.1.3",
                "versionExact": "18.1.3"
            }]
```

Following is an example to import Go SDK packages in third party Go code
```go
import (
	"github.com/vmware/alb-sdk/go/clients"
	"github.com/vmware/alb-sdk/go/session"
)
```
