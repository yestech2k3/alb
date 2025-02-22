/*
 * Copyright 2021 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */
package com.vmware.avi.sdk;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.logging.Logger;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpRequest;
import org.springframework.http.MediaType;
import org.springframework.http.client.ClientHttpRequestExecution;
import org.springframework.http.client.ClientHttpRequestInterceptor;
import org.springframework.http.client.ClientHttpResponse;

public class AviAuthorizationInterceptor implements ClientHttpRequestInterceptor {

	static final Logger LOGGER = Logger.getLogger(AviAuthorizationInterceptor.class.getName());

	private AviCredentials aviCredentials;

	public AviAuthorizationInterceptor(AviCredentials aviCredentials) {
		this.aviCredentials = aviCredentials;
	}

	public Boolean addIfAbsent(String key, HttpHeaders headers) {
		Boolean flag = false;
		if ((headers.getContentType() != null)
				&& ((headers.getContentType().toString().contains(MediaType.MULTIPART_FORM_DATA_VALUE.toString())))) {
			return flag;
		}        
		if (headers.containsKey(key)) {
			flag = true;
		}
		return flag;
	}

	@Override
	public ClientHttpResponse intercept(HttpRequest request, byte[] body, ClientHttpRequestExecution execution) throws IOException{
		LOGGER.info("__INIT__ Inside Interceptor..");
		int numApiExecCount = 0;
		if (!aviCredentials.getLazyAuthentication()
				&& (null == this.aviCredentials.getSessionID() || this.aviCredentials.getSessionID().isEmpty())
				&& !aviCredentials.getIsUnAuthenticatedApi()) {
			AviRestUtils.authenticateSession(this.aviCredentials);
		}
		ClientHttpResponse response = null;
		try {
			numApiExecCount = 0;
			HttpHeaders headers = request.getHeaders();
			if (addIfAbsent("Content-Type", headers)) {
				headers.setContentType(MediaType.APPLICATION_JSON);
			}            
			if (!addIfAbsent("X-Avi-Version", headers)) {
				headers.add("X-Avi-Version", this.aviCredentials.getVersion());
			}
			if (!addIfAbsent("X-Avi-Tenant", headers)) {
				headers.add("X-Avi-Tenant", this.aviCredentials.getTenant());
			}
			if (!aviCredentials.getIsUnAuthenticatedApi()){
				headers.add("X-CSRFToken", this.aviCredentials.getCsrftoken());
				headers.add(HttpHeaders.COOKIE, "csrftoken=" + this.aviCredentials.getCsrftoken() + "; " + "avi-sessionid="
						+ this.aviCredentials.getSessionID());
			}
			headers.add("Referer", AviRestUtils.getControllerURL(this.aviCredentials));

			response = execution.execute(request, body);

			int responseCode = response.getRawStatusCode();
			String requestUri = request.getURI().getPath();
			if(responseCode == 200 && requestUri.contains("useraccount")){
				LOGGER.info("Inside clearing the user session...");
				AviRestUtils.clearSession(this.aviCredentials);
				LOGGER.info("Clear session execution completed");
			}

			if (Arrays.asList(419, 401).contains(responseCode)) {
				numApiExecCount++;
				while (numApiExecCount < this.aviCredentials.getNumApiRetries()) {
					LOGGER.info("Inside Interceptor authentication retries:: " + numApiExecCount);
					response.close();
					headers.remove("X-CSRFToken");
					headers.remove("Cookie");
					AviRestUtils.authenticateSession(this.aviCredentials);
					headers.add("X-CSRFToken", this.aviCredentials.getCsrftoken());
					headers.add(HttpHeaders.COOKIE, "csrftoken=" + this.aviCredentials.getCsrftoken() + "; "
							+ "avi-sessionid=" + this.aviCredentials.getSessionID());

					Thread.sleep(this.aviCredentials.getRetryWaitTime() * 1000);
					response = execution.execute(request, body);
					LOGGER.info("Interceptor execution completed for retries");
					if (Arrays.asList(419, 401).contains(response.getRawStatusCode())) {
						numApiExecCount++;
						continue;
					} else {
						numApiExecCount = 0;
						break;
					}
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
			throw e;
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		LOGGER.info("__DONE__ Interceptor");
		return response;
	}

}
