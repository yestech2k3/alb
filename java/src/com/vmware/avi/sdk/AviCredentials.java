/*
 * Copyright 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */
package com.vmware.avi.sdk;

/**
 * This is a POJO class contains all parameters for AVI controller credentials.
 * 
 * @author: Chaitanya Deshpande
 *
 */
public class AviCredentials
{

    public AviCredentials()
    {
    }

    /**
     * Constructor to instantiate class with basic mandatory parameters
     * 
     * @param controller
     *            The controller IP(With HTTP or without HTTP).
     * @param username
     *            The Username of controller's credentials.
     * @param password
     *            password of controller.
     */
    public AviCredentials(String controller, String username, String password)
    {
        this.controller = controller;
        this.username = username;
        this.password = password;
    }
    
    public AviCredentials(String controller, String username)
    {
        this.controller = controller;
        this.username = username;
    }

    /**
     * Constructor to instantiate class with all parameters
     * 
     * @param controller
     *            Controller IP.
     * @param username
     *            Username of controller.
     * @param password
     *            Password of controller.
     * @param tenant
     *            Tenant name from controller.
     * @param version
     *            Version of AVI controller.
     * @param tenantUuid
     *            Tenant ID.
     * @param port
     *            Port for creating new object.
     * @param timeout
     *            Timeout for AVI Session.
     * @param sessionID
     *            The session ID.
     * @param csrftoken
     *            Csrftoken.
     * @param token
     *            Token for REST call if have.
     * @param verify
     *            For check SSL is want.
     * @param retryConxnErrors
     *            Retry connection timeout.
     * @param connectionTimeout
     *            Connection timeout for socket
     */
    public AviCredentials(String controller, String username, String password, String tenant, String version,
            String tenantUuid, Integer port, Integer timeout, String sessionID, String csrftoken,
            String token, Boolean verify, Boolean retryConxnErrors, Integer connectionTimeout)
    {
        this.controller = controller;
        this.username = username;
        this.password = password;
        this.tenant = tenant;
        this.version = version;
        this.tenantUuid = tenantUuid;
        this.port = port;
        this.timeout = timeout;
        this.sessionID = sessionID;
        this.csrftoken = csrftoken;
        this.token = token;
        this.verify = verify;
        this.retryConxnErrors = retryConxnErrors;
        this.connectionTimeout = connectionTimeout;
    }

    /**
     * Constructor to instantiate class with all parameters
     * include unauthenticated APIs parameters
     *
     * @param controller
     *            Controller IP.
     * @param username
     *            Username of controller.
     * @param password
     *            Password of controller.
     * @param tenant
     *            Tenant name from controller.
     * @param version
     *            Version of AVI controller.
     * @param tenantUuid
     *            Tenant ID.
     * @param port
     *            Port for creating new object.
     * @param timeout
     *            Timeout for AVI Session.
     * @param sessionID
     *            The session ID.
     * @param csrftoken
     *            Csrftoken.
     * @param token
     *            Token for REST call if have.
     * @param verify
     *            For check SSL is want.
     * @param retryConxnErrors
     *            Retry connection timeout.
     * @param connectionTimeout
     *            Connection timeout for socket
     * @param isUnauthenticatedApi
     *            For check unauthenticated API is want.
     */
    public AviCredentials(String controller, String username, String password, String tenant, String version,
            String tenantUuid, Integer port, Integer timeout, String sessionID, String csrftoken,
            String token, Boolean verify, Boolean retryConxnErrors, Integer connectionTimeout, Boolean isUnAuthenticatedApi)
    {
        this(controller, username, password, tenant, version, tenantUuid, port, timeout, sessionID, csrftoken, token,
				verify, retryConxnErrors, connectionTimeout);
		this.isUnAuthenticatedApi = isUnAuthenticatedApi;
    }

    private String controller;
    private String username;
    private String password;
    private String tenant = "admin";
    private String version;
    private String tenantUuid;
    private Integer port = 443;
    private Integer timeout = 60; // 1 min default
    private String sessionID;
    private String csrftoken;
    private String token;
    private Boolean verify = false;// for SSL and HTTPS
    private Boolean retryConxnErrors;
    private Integer numApiRetries = 3;
    private Integer retryWaitTime = 5;
    private Boolean lazyAuthentication = false;
    private Integer connectionTimeout = 60; // 1 min default
    private Boolean isUnAuthenticatedApi = false;// for unauthenticated apis

    /**
     * Gets the controller's IP.
     * 
     * @return A String representing the controller's IP.
     */
    public String getController()
    {
        return controller;
    }

    /**
     * Sets the controller IP.
     * 
     * @param controller
     *            A String containing the controller's IP.
     */
    public void setController(String controller)
    {
        this.controller = controller;
    }

    /**
     * Gets the username of controller.
     * 
     * @return A String representing the Username of controller.
     */
    public String getUsername()
    {
        return username;
    }

    /**
     * Sets the username of controller.
     * 
     * @param username
     *            A String containing the username of controller.
     */
    public void setUsername(String username)
    {
        this.username = username;
    }

    /**
     * Gets the password of controller.
     * 
     * @return A String representing the password of controller.
     */
    public String getPassword()
    {
        return password;
    }

    /**
     * Sets the password of controller.
     * 
     * @param password
     *            A String containing the password of the controller.
     */
    public void setPassword(String password)
    {
        this.password = password;
    }

    /**
     * Gets the Tenant.
     * 
     * @return A String representing Tenant name.
     */
    public String getTenant()
    {
        return tenant;
    }

    /**
     * Sets the Tenant name.
     * 
     * @param tenant
     *            A String containing the tenant name.
     */
    public void setTenant(String tenant)
    {
        this.tenant = tenant;
    }

    /**
     * Gets the version of controller.
     * 
     * @return A String representing version of the controller.
     */
    public String getVersion()
    {
        return version;
    }

    /**
     * Sets the version.
     * 
     * @param version
     *            A String containing version of the controller.
     */
    public void setVersion(String version)
    {
        this.version = version;
    }

    /**
     * Gets the tenant ID.
     * 
     * @return A String representing tenant ID.
     */
    public String getTenantUuid()
    {
        return tenantUuid;
    }

    /**
     * Sets the tenant ID.
     * 
     * @param tenantUuid
     *            A String containing tenant ID.
     */
    public void setTenantUuid(String tenantUuid)
    {
        this.tenantUuid = tenantUuid;
    }

    /**
     * Gets the port.
     * 
     * @return A Integer representing port.
     */
    public Integer getPort()
    {
        return port;
    }

    /**
     * Sets the port.
     * 
     * @param port
     *            A Integer containing port
     */
    public void setPort(Integer port)
    {
        this.port = port;
    }

    /**
     * Gets the timeout
     * 
     * @return A Integer representing timeout.
     */
    public Integer getTimeout()
    {
        return timeout;
    }

    /**
     * Sets the timeout.
     * 
     * @param timeout
     *            A Integer containing timeout for session.
     */
    public void setTimeout(Integer timeout)
    {
        this.timeout = timeout;
    }

    /**
     * Gets the session ID.
     * 
     * @return A String representing session ID.
     */
    public String getSessionID()
    {
        return sessionID;
    }

    /**
     * Sets the session ID.
     * 
     * @param sessionID
     *            A String containing session ID.
     */
    public void setSessionID(String sessionID)
    {
        this.sessionID = sessionID;
    }

    /**
     * Gets the csrftoken.
     * 
     * @return A String representing csrftoken.
     */
    public String getCsrftoken()
    {
        return csrftoken;
    }

    /**
     * Sets the csrftoken
     * 
     * @param csrftoken
     *            A String containing csrftoken.
     */
    public void setCsrftoken(String csrftoken)
    {
        this.csrftoken = csrftoken;
    }

    /**
     * Gets the token.
     * 
     * @return A String representing token for session.
     */
    public String getToken()
    {
        return token;
    }

    /**
     * Sets the token.
     * 
     * @param token
     *            A String containing token.
     */
    public void setToken(String token)
    {
        this.token = token;
    }

    /**
     * Gets the verify for SSL.
     * 
     * @return A Boolean representing verify for SSL check.
     */
    public Boolean getVerify()
    {
        return verify;
    }

    /**
     * Sets the verify.
     * 
     * @param verify
     *            A Boolean containing verify for SSL check.
     */
    public void setVerify(Boolean verify)
    {
        this.verify = verify;
    }

    /**
     * Gets the retry connection errors.
     * 
     * @return A Boolean representing retry connection.
     */
    public Boolean getRetryConxnErrors()
    {
        return retryConxnErrors;
    }

    /**
     * Sets the retry connection error.
     * 
     * @param retryConxnErrors
     *            A Boolean containing retry connection errors.
     */
    public void setRetryConxnErrors(Boolean retryConxnErrors)
    {
        this.retryConxnErrors = retryConxnErrors;
    }

    /**
     * Gets the number of API retries.
     * 
     * @return A Integer representing number of API retries.
     */
    public Integer getNumApiRetries()
    {
        return numApiRetries;
    }

    /**
     * Sets the number of API retries.
     * 
     * @param numApiRetries
     *            A Integer containing number of API retries.
     */
    public void setNumApiRetries(Integer numApiRetries)
    {
        this.numApiRetries = numApiRetries;
    }

    /**
     * Gets the retry wait time.
     * 
     * @return A Integer representing retry wait time.
     */
    public Integer getRetryWaitTime()
    {
        return retryWaitTime;
    }

    /**
     * Sets the retry wait time.
     * 
     * @param retryWaitTime
     *            A Integer containing retry wait time.
     */
    public void setRetryWaitTime(Integer retryWaitTime)
    {
        this.retryWaitTime = retryWaitTime;
    }

    /**
     * Gets lazy authentication.
     * 
     * @return A Boolean representing lazy authentication.
     */
    public Boolean getLazyAuthentication()
    {
        return lazyAuthentication;
    }

    /**
     * Sets the lazy authentication.
     * 
     * @param lazyAuthentication
     *            A Boolean containing lazy authentication or not.
     */
    public void setLazyAuthentication(Boolean lazyAuthentication)
    {
        this.lazyAuthentication = lazyAuthentication;
    }

    /**
     * Gets the connection timeout
     * @return A Integer representing connection timeout.
     */
    public Integer getConnectionTimeout() {
        return connectionTimeout;
    }

    /**
     * Sets the connection timeout.
     * @param connectionTimeout
     *          A Integer containing connection timeout for socket.
     */
    public void setConnectionTimeout(Integer connectionTimeout) {
        this.connectionTimeout = connectionTimeout;
    }

    /**
     * Gets unauthenticate api.
	 *
	 * @return A Boolean representing unauthenticate apis.
	 */
	public Boolean getIsUnAuthenticatedApi() {
		return isUnAuthenticatedApi;
	}

	/**
	 * Sets the unauthenticate apis
	 *
	 * @param isUnauthenticatedApi A Boolean containing unauthenticate api or not.
	 */
	public void setIsUnAuthenticatedApi(Boolean isUnAuthenticatedApi) {
		this.isUnAuthenticatedApi = isUnAuthenticatedApi;
	}

	@Override
	public String toString() {
		return "AviCredentials [controller=" + controller + ", username=" + username + ", password=" + password
				+ ", tenant=" + tenant + ", version=" + version + ", tenantUuid=" + tenantUuid + ", port=" + port
				+ ", timeout=" + timeout + ", connectionTimeout=" + connectionTimeout + ", sessionID=" + sessionID
                + ", csrftoken=" + csrftoken + ", token=" + token + ", verify=" + verify
                + ", retryConxnErrors=" + retryConxnErrors + ", numApiRetries=" + numApiRetries
				+ ", retryWaitTime=" + retryWaitTime + ", lazyAuthentication=" + lazyAuthentication
                + ", isUnauthenticatedApi=" + isUnAuthenticatedApi + "]";
	}
}
