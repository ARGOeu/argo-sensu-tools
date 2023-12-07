# argo-sensu-tools

## Description

The package argo-sensu-tools contains tools needed for handling results of passive metrics on Sensu agents. It contains a tool `passive2sensud` running as a service, that passes the results from FIFO file `/var/nagios/rw/nagios.cmd` to Sensu backend. The log is written in `/var/log/argo-sensu-tools/argo-sensu-tools.log`.

## Installation

The tool is packaged as a `.rpm` package. It is available in the ARGO repositories, and the installation comes down to simple call:

```shell
yum install -y argo-sensu-tools
```

## Configuration

The tool configuration is stored in file `/etc/argo-sensu-tools/argo-sensu-tools.conf`. There are three mandatory sections needed for the correct functioning of the tool.

### GENERAL section

The GENERAL section must contain two entries: one defining the path of fifo file, and one defining voname.

```text
[GENERAL]
fifo = /var/nagios/rw/nagios.cmd
voname = ops
```

### SENSU section

SENSU section must contain three entries with defined information on Sensu backend: url, access token for Sensu API, and name of the namespace the agent is assigned to.

```text
[SENSU]
url = https://sensu-devel.cro-ngi.hr:8080/
token = t0k3n
namespace = TENANT
```

### WEB-API section

Here you define information on ARGO Web-API: url, access token, and metric profiles used for configuration of the agent.

```text
[WEB-API]
url = https://api.devel.argo.grnet.gr
token = w3b-4p1-t0k3n
metricprofiles = ARGO_MON, ARGO_MON2
```

## Running

The configuration needs to be set up properly before the service `passive2sensu.service` can be started. It is simply started with command:

```shell
systemctl start passive2sensu.service
```

If everything is correctly configured, the service should be up and running.
