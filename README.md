# [CERN WebLogic CLI Tool](http://db-blog.web.cern.ch/blog/konrad-aleksander-kaczkowski/2015-11-cern-it-db-group-develops-new-weblogic-command-line)

CERN WebLogic CLI tool is written in Python. A project is being realized in an object oriented way to contribute towards flexibility, modularity and legibility of a solution and the modules of the system are designed to maximize end-user productivity. It is a comprehensive solution using WebLogic RESTful management services and providing a simple way of interacting with a user and possibility of integration with third party systems. The goal of the system is to provide a set of standardized functionality for managing resources shared in a distributed environment composed of hundreds WebLogic servers. Among them there are significant and business-critical applications. The product hides administration mechanisms by removing the complexity of the REST interface and shares user friendly abstraction layer. The system together with Oracle WebLogic Server follows the client- server architectural style. 

## Benefits

- **Speed:** REST CLI Tool has majority integration of Oracle WebLogic RESTful management API. This has tremendous effect of increasing speed of individual actions in comparison to the WebLogic Scripting Tool. 
- **Openness:** Tool is characterized by an emphasis on ease of integration. Due to simple interface it can be integrated with third- party systems and therefore it allows applying a PaaS approach. 
- **Ease of installation and maintenance:** REST CLI Tool requires only Python installed on a client machine and started Administration Server and can be executed from everywhere, also remotely outside the domain machine. It doesn't require any JVM or WebLogic installation. 
- **Ease of domain management:** Useful debugging facility in case of an error. WebLogic REST response includes a well- formed information with details of operation failure. CERN CLI Tool tests server response against any unsuccessful states and returns status code. 
- **Security** Tool may guarantee (on user request) secure connection and data transfer to/from Oracle WebLogic Server.


## [User documentation](wls_rest/docs/user_documentation.md)

## [Technical documentation](wls_rest/docs/technical_documentation.md)
