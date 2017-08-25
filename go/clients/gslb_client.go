package clients

// This file is auto-generated.
// Please contact avi-sdk@avinetworks.com for any change requests.

import (
	"github.com/avinetworks/sdk/go/models"
	"github.com/avinetworks/sdk/go/session"
)

// GslbClient is a client for avi Gslb resource
type GslbClient struct {
	aviSession *session.AviSession
}

// NewGslbClient creates a new client for Gslb resource
func NewGslbClient(aviSession *session.AviSession) *GslbClient {
	return &GslbClient{aviSession: aviSession}
}

func (client *GslbClient) getAPIPath(uuid string) string {
	path := "api/gslb"
	if uuid != "" {
		path += "/" + uuid
	}
	return path
}

// GetAll is a collection API to get a list of Gslb objects
func (client *GslbClient) GetAll() ([]*models.Gslb, error) {
	var plist []*models.Gslb
	err := client.aviSession.GetCollection(client.getAPIPath(""), &plist)
	return plist, err
}

// Get an existing Gslb by uuid
func (client *GslbClient) Get(uuid string) (*models.Gslb, error) {
	var obj *models.Gslb
	err := client.aviSession.Get(client.getAPIPath(uuid), &obj)
	return obj, err
}

// GetByName - Get an existing Gslb by name
func (client *GslbClient) GetByName(name string) (*models.Gslb, error) {
	var obj *models.Gslb
	err := client.aviSession.GetObjectByName("gslb", name, &obj)
	return obj, err
}

// Create a new Gslb object
func (client *GslbClient) Create(obj *models.Gslb) (*models.Gslb, error) {
	var robj *models.Gslb
	err := client.aviSession.Post(client.getAPIPath(""), obj, &robj)
	return robj, err
}

// Update an existing Gslb object
func (client *GslbClient) Update(obj *models.Gslb) (*models.Gslb, error) {
	var robj *models.Gslb
	path := client.getAPIPath(obj.UUID)
	err := client.aviSession.Put(path, obj, &robj)
	return robj, err
}

// Delete an existing Gslb object with a given UUID
func (client *GslbClient) Delete(uuid string) error {
	return client.aviSession.Delete(client.getAPIPath(uuid))
}

// DeleteByName - Delete an existing Gslb object with a given name
func (client *GslbClient) DeleteByName(name string) error {
	res, err := client.GetByName(name)
	if err != nil {
		return err
	}
	return client.Delete(res.UUID)
}
