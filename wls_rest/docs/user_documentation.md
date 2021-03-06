# User documentation

###### [Back](README.md)

Here is an overview of the features.

## API Documentation

* [1. Modus operandi](#1-modus-operandi)
* [2. Authentication](#2-authentication)
* [3. Main functionality](#3-main-functionality)
  * [3.1. Servers management](#31-servers-management)
  * [3.2. Clusters management](#32-clusters-management)
  * [3.3. Domain management](#33-domain-management)
  * [3.4. Applications management](#34-applications-management)
  * [3.5. Deployment](#35-deployment)
  * [3.6. WebLogic Server administration](#36-weblogic-server-management)
  * [3.7. Monitoring](#37-monitoring)
* [4. Optional arguments](#4-optional-arguments)
* [5. Configuration](#5-configuration)

## 1. Modus operandi

![Request processing image](wls_rest/docs/img/request.png?raw=true "Request processing in CERN CLI Tool.")

A user is making a request using command line to the CERN CLI System for performing operation on server resources. CLI Tool is gathering credentials from the user and sends it to the WebLogic server. Server checks if the user is authenticated and authorized and accomplishes user request or denies due to lack of permission. 

![Dataflow image](wls_rest/docs/img/dataflow.png?raw=true "Overview of CERN infrastructure.")

Request is parsed and validated against incorrect elements. According to the requested operation, proper strategy objects are created and injected with API data from the dictionary (URL, Curl options). Additional data about the domain (clusters, servers) is collected from the server as REST request. Here it needs to be emphasized that the administration server URL needs to be passed to the CLI as a parameter. 

When strategy objects are ready, they are executed and the result is returned to the View module. Result is expected in a JSON format. Built- in parser converts this result to more convenient form and parsed output is displayed to the user. 

## 2. Authentication

There are following policies of using CERN CLI Tool: 

#### 2.1 Interactive mode 

`wls-cli --url ADMIN_SERVER_URL {SOME_REQUEST}`  

It is a default option and it doesn't requires any additional parameters. CLI Tool asks user for credentials with every request. 

#### 2.2 Netrc file 

`wls-cli --url ADMIN_SERVER_URL {SOME_REQUEST} --netrc`  

It is possible to use .netrc file stored in user's home directory. Example .netrc file: 

```
machine wls-admin.cern.ch
        login weblogic
        password XXXXX
```

#### 2.3 HTTP cookie 

`wls-cli --url ADMIN_SERVER_URL {SOME_REQUEST} --usession`  

Oracle Weblogic Server maintains Java session and generates unique HTTP cookie for further communication. User can use this token for further communication with the server instead of typing his credentials with every request.

Note: User will be asked for a credentials only for the first time and when previous cookie file expires. 

#### 2.4 Custom script 

`wls-cli --url ADMIN_SERVER_URL {SOME_REQUEST} --username USERNAME --passwd_script SCRIPT_TO_EXECUTE`  

 User can use his/her own script for passing a password.

Example:

`--passwd_script "echo XXXX" `

#### 2.5 Credentials given explicitly in parameter 

`wls-cli --url ADMIN_SERVER_URL {SOME_REQUEST} --username USERNAME --passwd PASSWD`  

User can pass a username and a password explicitly in parameters. 

#### 2.6 CERN specific implementation 

`wls-cli --i CERN_ENTITY_NAME {SOME_REQUEST} `  

This solution is based on CERN's wlstab script and it is not possible to execute it outside CERN. 


## 3. Main functionality 

#### 3.1 Servers Management

###### a. Start a server

> wls-cli --url ADMIN_SERVER_URL --start server --target SERVER_NAME

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --start server --target server__A_2`

###### b. Stop a server

> wls-cli --url ADMIN_SERVER_URL --stop server --target SERVER_NAME

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --stop server --target server__A_2`

###### c. Check the status of a server

> wls-cli --url ADMIN_SERVER_URL --status server --target SERVER_NAME

Note: here you can add optional parameter *-l* or *--long* that enables output with full status parameters. 

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --status server --target server__A_2`

###### d. Restart a server

> wls-cli --url ADMIN_SERVER_URL --restart server --target SERVER_NAME

Note: cannot perform for Admin Server.

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --restart server --target server__A_2`

###### e. Suspend a server

> wls-cli --url ADMIN_SERVER_URL --susped server --target SERVER_NAME

This operation makes server go into *admin* state. 

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --suspend server --target server__A_2`

###### g. Resume a server

> wls-cli --url ADMIN_SERVER_URL --resume server --target SERVER_NAME

After suspending the server (server is in *admin* state) we can make it return to the *running* state. 

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --resume server --target server__A_2`

#### 3.2 Clusters Management

###### a. Start a cluster

> wls-cli --url ADMIN_SERVER_URL --start cluster --target CLUSTER_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --start cluster --target server__B_Cluster`

###### b. Stop a cluster

> wls-cli --url ADMIN_SERVER_URL --stop cluster --target CLUSTER_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --stop cluster --target server__B_Cluster`

###### c. Check the status of a cluster

> wls-cli --url ADMIN_SERVER_URL --status cluster --target CLUSTER_NAME

Note: here you can add optional parameter *-l* or *--long* that enables output with full status parameters. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --status cluster --target server__B_Cluster`

###### d. Restart a cluster

> wls-cli --url ADMIN_SERVER_URL --restart cluster --target CLUSTER_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --restart cluster --target server__B_Cluster`

###### e. Suspend a cluster

> wls-cli --url ADMIN_SERVER_URL --suspend cluster --target CLUSTER_NAME

This operation makes cluster (every server in the cluster) go into *admin* state. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --suspend cluster --target server__B_Cluster`

###### g. Resume a cluster

> wls-cli --url ADMIN_SERVER_URL --resume cluster --target CLUSTER_NAME

After suspending a cluster (every server in the cluster is in *admin* state) we can make it return to the *running* state. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --resume cluster --target server__B_Cluster`

#### 3.3 Domain Management

###### a. Start a domain

> wls-cli --url ADMIN_SERVER_URL --start domain

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --start domain`

###### b. Stop a domain

> wls-cli --url ADMIN_SERVER_URL --stop domain

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --stop domain`

###### c. Check the status of a domain

> wls-cli --url ADMIN_SERVER_URL --status domain

Note: here you can add optional parameter *-l* or *--long* that enables output with full status parameters. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --status domain`

#### 3.4 Applications Management

###### a. Start an application

> wls-cli --url ADMIN_SERVER_URL --start app --appname APP_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --start app --appname myapp`

###### b. Stop an application

> wls-cli --url ADMIN_SERVER_URL --stop app --appname APP_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --stop app --appname myapp`

###### c. Check the status of an application

> wls-cli --url ADMIN_SERVER_URL --status app --appname APP_NAME

Note: here you can add optional parameter *--long* or *-l* that shows additional parameters. 

Note2: here you can add optional parameter *--servlets* that shows servlets and its parameters. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --status app --appname myapp`

###### d. Update an application

> wls-cli --url ADMIN_SERVER_URL --update app --appname APP_NAME

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --update app --appname myapp`

#### 3.5 Deployment

###### a. Redeploy uploaded application

> wls-cli --url ADMIN_SERVER_URL --redeploy --appname APP_NAME --adminfs

Note: Use this method when the file to redeploy is already on the Administration Server file system.

Note2: *--file* argument is accepted by the parser, but will be ignored in execution.

Note3: *--target* argument is accepted by the parser, but will be ignored in execution. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --redeploy --appname myapp --adminfs `

###### b. Redeploy an application from a local file

> wls-cli --url ADMIN_SERVER_URL --redeploy --appname APP_NAME --file APP_PATH

Note: *--target* argument is accepted by the parser, but will be ignored in execution. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --redeploy --appname myapp --file /ORA/dbs01/syscontrol/projects/wls/scripts/rest/j2eeapplication-2.0.1-SNAPSHOT.war`

###### c. Redeploy uploaded library

> wls-cli --url ADMIN_SERVER_URL --redeploy --libname LIB_NAME --adminfs 

Note: Use this method when the file to redeploy is already on the Administration Server file system.

Note2: file argument is accepted by the parser, but will be ignored in execution.

Note3: target argument is accepted by the parser, but will be ignored in execution. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --redeploy --libname ssoFilters_v20 --adminfs`

###### d. Redeploy a library from a local file

> wls-cli --url ADMIN_SERVER_URL --redeploy --libname LIB_NAME --file APP_PATH

Note: *--target* argument is accepted by the parser, but will be ignored in execution. 

Example:

` wls-cli --url https://wls-admin.cern.ch:7002 --redeploy --libname ssoFilters_v20 --file /ORA/dbs01/wls/home/ssoFilters-v2.0.10.jar`

###### e. Deploy an application from a local file

> wls-cli --url ADMIN_SERVER_URL --deploy --targets TARGET_NAME --appname APP_NAME --file LOCAL_PATH 

> wls-cli --url ADMIN_SERVER_URL --deploy --targets TARGET1_NAME TARGET2_NAME (...) --appname APP_NAME --file LOCAL_PATH 

Note: this kind of deployment is default. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --deploy --appname myapp --file /ORA/dbs01/syscontrol/projects/wls/scripts/rest/j2eeapplication-2.0.1-SNAPSHOT.war --targets server__A_1 server__A_2`

###### f. Deploy uploaded application

> wls-cli --url ADMIN_SERVER_URL --deploy --adminfs --targets TARGET_NAME --appname APP_NAME -- file UPLOADED_APP_PATH 

> wls-cli --url ADMIN_SERVER_URL --deploy --adminfs --targets TARGET1_NAME  TARGET2_NAME (...) --appname APP_NAME -- file UPLOADED_APP_PATH 

Note: To perform this kind of deployment you need to add *--adminfs* parameter to the request. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --deploy --appname myapp --file /ORA/dbs01/syscontrol/projects/wls/scripts/rest/j2eeapplication-2.0.1-SNAPSHOT.war --targets server__A_1 server__A_2 --adminfs `

###### g. Deploy a library from local file

> wls-cli --url ADMIN_SERVER_URL --deploy --targets TARGET_NAME --libname LIB_NAME -- file APP_PATH 

> wls-cli --url ADMIN_SERVER_URL --deploy --targets TARGET1_NAME  TARGET2_NAME (...) --libname LIB_NAME -- file APP_PATH 

Note: this kind of deployment is default. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --deploy --libname ssoFilters_v20#1.0@2.0.10 --file /ORA/dbs01/wls/home/ssoFilters-v2.0.10.jar --targets server__A_1 server__A_2`

###### h. Deploy uploaded library

> wls-cli --url ADMIN_SERVER_URL --deploy --adminfs --targets TARGET_NAME --libname LIB_NAME -- file UPLOADED_APP_PATH 

> wls-cli --url ADMIN_SERVER_URL --deploy --adminfs --targets TARGET1_NAME  TARGET2_NAME (...) --libname LIB_NAME -- file UPLOADED_APP_PATH 

Note: To perform this kind of deployment you need to add *--adminfs* parameter to the request. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --deploy --libname ssoFilters_v20 --file /ORA/dbs01/wls/home/ssoFilters-v2.0.10.jar --targets server__A_1 server__A_2 --adminfs`

###### i. Undeploy an application

> wls-cli --url ADMIN_SERVER_URL --undeploy --appname APP_NAME 

Note: *--target* and *--file* arguments are accepted by the parser, but will be ignored in execution.  

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --undeploy --appname myapp `

###### j. Undeploy a library

> wls-cli --url ADMIN_SERVER_URL --undeploy --libname APP_NAME 

Note: *--target* and *--file* arguments are accepted by the parser, but will be ignored in execution.  

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --undeploy --libname ssoFilters_v20`


#### 3.6 WebLogic Server Management

###### a. Lock & Edit administration configuration

> wls-cli --url ADMIN_SERVER_URL --admin_change start

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --admin_change start`

###### b. Activate and release administration configuration

> wls-cli --url ADMIN_SERVER_URL --admin_change activate

Example:
###### e. Suspend a server
`wls-cli --url https://wls-admin.cern.ch:7002 --admin_change activate`

###### c. Cancel administration configuration

> wls-cli --url ADMIN_SERVER_URL --admin_change cancel

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --admin_change cancel`

#### 3.7 Monitoring

###### a. List all deployed applications

>  wls-cli --url ADMIN_SERVER_URL --show apps

Note: here you can add optional parameter *--long* or *-l* that shows additional parameters. 

Note2: here you can add optional parameter *--servlets* that shows servlets and its parameters. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --show apps --long`

###### b. List all deployed libraries

>  wls-cli --url ADMIN_SERVER_URL --show libs

Note: here you can add optional parameter *--long* or *-l* that shows additional parameters.

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --show libs -l`

###### c. List all WebLogic targets

>  wls-cli --url ADMIN_SERVER_URL --show targets 

Targets: all servers and clusters in the domain.

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --show targets`

###### d. List all WebLogic jobs

>  wls-cli --url ADMIN_SERVER_URL --show jobs

Note: here you can add optional parameter *-l* or *--long* that enables output with all parameters. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --show jobs --long`

###### e. Show HTTP access logs of a server

> wls-cli --url ADMIN_SERVER_URL --logs httpaccess --target SERVER_NAME

Note: Here you can use optional option *--maxResults X* for showing last X logs. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --logs httpaccess --target server__B_1 --maxResults 3`

###### f. Show datasource logs of a server

>  wls-cli --url ADMIN_SERVER_URL --logs datasource --target SERVER_NAME 

Note: Here you can use optional option *--maxResults X* for showing last X logs. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --logs datasource --target server__B_1`

###### g. Show server logs

>  wls-cli --url ADMIN_SERVER_URL --logs server --target SERVER_NAME 

Note: Here you can use optional option *--maxResults X* for showing last X logs. 

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --logs server --target server__B_2 --maxResults 3`

###### h. Show domain logs

>  wls-cli --url ADMIN_SERVER_URL --logs domain

Note: Here you can use optional option *--maxResults X* for showing last X logs.  

Example:

`wls-cli --url https://wls-admin.cern.ch:7002 --logs domain --maxResults 50`

## 4. Optional arguments

###### a. help

> wls-cli -h
 
> wls-cli -help

Use *-h* or *--help* for showing help screen. 

###### b. async

>  wls-cli {REQUEST} --async 

Use *--async* for making asynchronous operations. 

###### c. noforce

> wls-cli --noforce

All operations are forced from default. Use *--noforce* for resigning from forcing operation. 

###### d. raw

> wls-cli --raw

Use *--raw* for printing default json as an output. 

###### e. v / verbose

> wls-cli -v

> wls-cli --verbose

Use *-v* or *--verbose* for printing debug communicates of a Tool. 

###### f. v2 / verbose2

> wls-cli -v2

> wls-cli --verbose2

Second level of verbose mode. Use *-v2* or *--verbose2* for printing curl communicates in a verbose mode and debug communicates of a Tool.

###### g. maxResults

> wls-cli {LOGS REQUEST} --maxResults X 

Use *--maxResults X* for showing last X logs. 

###### h. version

> wls-cli --version 

Use *--version* for checking CLI Tool version. 

###### i. operationTimeout

> wls-cli {REQUEST} --operationTimeout X 

Use *--operationTimeout X* for setting X seconds for Curl request timeout. Default time is 10 minutes. 

###### j. l / long

> wls-cli {SERVER STATUS/APPS/JOBS REQUEST} -l 

> wls-cli {SERVER STATUS/APPS/JOBS REQUEST} --long 

Use *-l* or *--long* for printing full status parameters for server / apps / libs / jobs. 

## 5. Configuration

There are some predefined parameters which can be redefined by the user. The location is: 
*cerndb-infra-wls_rest/wls_rest/src/wlscli/common/constans.py*


- constans.py/Constans/ADMINSERVER_NAME
- constans.py/Constans/TOOL_VERSION

- constans.py/Constans/TIMEOUT

  Max time in HTTP connection. Default 2 seconds.
- constans.py/Constans/CONNECT_TIMEOUT

  Max time for operation. Default 10 minutes. 
- constans.py/Constans/FORCE_OPERATION
- constans.py/Constans/MAX_RESULTS


