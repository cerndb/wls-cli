# Technical documentation

###### [Back](README.md)

## Table of contents

* [1. Architecture](#1-architecture)
  * [1.1. Controller](#11-controller)
  * [1.2. Model](#12-model)
  * [1.3. View](#13-view)
  * [1.4. Services](#14-services)
* [2. UML Diagrams](#2-uml-diagrams)
  * [2.1. Use case diagrams](#21-use-case-diagrams)
  * [2.2. Class diagrams](#22-class-diagrams)
  * [2.3. Machine state diagram](#23-machine-state-diagram)
  * [2.4. Sequence diagram](#24-sequence-diagram)
* [3. Tests](#3-tests)

## 1. Architecture

A tool has been realised with Model View Controller architecture pattern. The user is making a request which is received and interpreted by a controller. If the request is valid, controller creates a proper service object from services layer. The service object is executing requested operation (this layer is communicating with the WebLogic Server) and it updates the model. In line with the observer design pattern, model informs controller about the update and the controller passes updated mockup to the view. The view parses the data and displays final output to the user.

#### 1.1 Controller

Controller is a primary module. It steers the process of executing user request. At the beginning, controller receives user request and parses it. If the request is valid, controller interprets user's intention and performs user authentication and authorisation process. If credentials and priviledges are correct, controller passes the data to the service object in order to execute user request. Thereafter, model informs controller about it's update and controller sends JSON data to the view module.

Authorisation and authentication possible procedures:
- User's credentials explicitly in request's parameters
  
  Very convenient way of passing credentials in the case where user wants to make few requests in succession.
- User put username in request's parameters and indicated a password script
  
  More secure solution, because user's password is not passed in the plain text.
- CERN infrastructure scripts
  
  This option works only on the basis of *wlstab* and *webtab* scripts which are in the CERN infrastructure.
- Netrc file
  
  Netrc file should exist in user's home directory. Data inside the file are read by Curl library.
- HTTP cookie
  
  Oracle WebLogic 12.1.3 stores session data and tool user can utilize the potential of that fact. User will be asked for credentials only during first time and every after cookie will be expired.
- User interactively requested for credentials
  
  Easiest and default mode of work. User will be asked for the credentials with every request to the tool.


#### 1.2 Model

Model stores business logic and application logic data. In the business logic there is API provided by Oracle in the URL form. Application logic handles all the data that are required during tool work.

#### 1.3 View

It receives user request and passes it to the controller (via event queue). At the end it receives JSON data to be parsed and displays parsed output to the end user.

![Curl / WL CLI tool comparison image](wls_rest/docs/img/comparison.png?raw=true "Comparison of the Curl and the CLI Tool.")

#### 1.4 Services

It carries the implementation of a business logic services. It provides an access to concrete operations on WebLogic resources.

## 2. UML Diagrams

#### 2.1 Use case diagrams

![Use case diagram: servers / clusters / domain management](wls_rest/docs/img/diagrams/use_case/diagram_servers.png?raw=true "Use case diagram: servers / clusters / domain management")

![Use case diagram: applications / deployments management](wls_rest/docs/img/diagrams/use_case/diagram_apps.png?raw=true "Use case diagram: applications / deployments management")

![Use case diagram: monitoring](wls_rest/docs/img/diagrams/use_case/diagram_monit.png?raw=true "Use case diagram: monitoring")

#### 2.2 Class diagrams

###### 2.2.1 Main

![Class diagram: main components](wls_rest/docs/img/diagrams/class/class_diagram_main.png?raw=true "Class diagram: main components")

###### 2.2.2 Controller

![Class diagram: controller module](wls_rest/docs/img/diagrams/class/controller/class_diagram_controller.png?raw=true "Class diagram: controller module")

###### 2.2.3 View

![Class diagram: view module](wls_rest/docs/img/diagrams/class/view/class_diagram_view.png?raw=true "Class diagram: view module")

###### 2.2.4 Model

![Class diagram: model module, main components](wls_rest/docs/img/diagrams/class/model/class_diagram_model_main.png?raw=true "Class diagram: model module, main components")

![Class diagram: model module, business logic](wls_rest/docs/img/diagrams/class/model/class_diagram_model_bl.png?raw=true "Class diagram: model module, business logic")

![Class diagram: model module, application logic](wls_rest/docs/img/diagrams/class/model/class_diagram_model_al.png?raw=true "Class diagram: model module, application logic")

###### 2.2.5 Services

![Class diagram: services module, main components](wls_rest/docs/img/diagrams/class/service/class_diagram_service_main.png?raw=true "Class diagram: services module, main components")

![Class diagram: services module, security components 1](wls_rest/docs/img/diagrams/class/service/class_diagram_service_sec1.png?raw=true "Class diagram: services module, security components 1")

![Class diagram: services module, security components 2](wls_rest/docs/img/diagrams/class/service/class_diagram_service_sec2.png?raw=true "Class diagram: services module, security components 2")

![Class diagram: service module, NM and Curl layer](wls_rest/docs/img/diagrams/class/service/class_diagram_service_nm_curl.png?raw=true "Class diagram: service module, NM and Curl layer")

![Class diagram: services module, WebLogic layer](wls_rest/docs/img/diagrams/class/service/class_diagram_service_wl.png?raw=true "Class diagram: services module, WebLogic layer")

###### 2.2.6 Common

![Class diagram: common module, main components](wls_rest/docs/img/diagrams/class/common/class_diagram_common_main.png?raw=true "Class diagram: common module, main components")

![Class diagram: common module, events](wls_rest/docs/img/diagrams/class/common/class_diagram_common_ev.png?raw=true "Class diagram: common module, events")

![Class diagram: common module, utils](wls_rest/docs/img/diagrams/class/common/class_diagram_common_ut.png?raw=true "Class diagram: common module, utils")

#### 2.3 State machine diagram

![State machine diagram](wls_rest/docs/img/diagrams/state/diagram.png?raw=true "State machine diagram")

#### 2.4 Sequence diagram

![Sequence diagram](wls_rest/docs/img/diagrams/sequence/diagram.png?raw=true "Sequence diagram")

## 3. Tests

The aim of testing is to verify and validate software. There are 64 automatic unit tests provided with the tool. 

- Functional tests
  
  There is a mock HTTP server created which simulates Oracle WebLogic Server. The tool is processing full operation and communicates with the server. The aim of those tests is to check if REST request created by the tool are correct.

- View module tests
  
  There is independent view module instance created. The instance is injected with ready JSON outputs from a file. The aim of those tests is to check if view module parses JSON responses properly and without any errors.
