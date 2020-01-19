# Cancelled Classes Core
APP Project: "Cancelled Classes" Server Core

## How to use
### Using already built Docker container
Download an existing container from 
https://github.com/up201605618/cancelled_classes_core/packages
or
https://hub.docker.com/r/upa201605618/cancelled_classes_core/tags
and run:
```shell script
docker run
-p %MACHINENAME%:8080:%PORT%
-v %DBLOCATION%:/core/db
--name cancelled_classes_core
cancelled_classes_core
```
Where:
 - %MACHINENAME% can be: 
   - 'localhost', for local usage **ONLY**;
   - '0.0.0.0', to bind to all interfaces;
   - interface address, to bind to that particular interface
 - %DBLOCATION% is a directory in the HOST where to store the
 database file

### Building the Docker container
From the root directory of the project, run:
```shell script
docker build -t cancelled_classes_core .
```
Follow the instruction on [how to run](#using-already-built-docker-container) the container.

# License
This project is licensed under the [MIT](./LICENSE.md) license.