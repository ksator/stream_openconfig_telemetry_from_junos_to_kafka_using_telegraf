# About this repo  

- How to stream openconfig telemetry from junos devices to kafka using telegraf   
- How to consume the kafka messages using Kafkacat or Python

## Building blocks 
- Junos devices with Openconfig telemetry support (Junos devices are grpc servers)  
- a Kafka broker 
- Telegraf 
  - to collect openconfig data from Junos devices (`jti_openconfig_telemetry` input plugin, Telegraf is a grpc client)   
  - to produce Kafta messages (with the data collected from Junos devices) to the Kafka broker (`kafka` output plugin).
- Consumers: 
  - a command line tool (kafkacat) to consume Kafka messages
  - python scripts to consume Kafka messages 

# Requirements 

## Host requirements 

Install Docker and Docker-compose  

## Junos requirements  

### Junos packages 

In order to collect data from Junos using openconfig telemetry, the devices require the Junos packages ```openconfig``` and ```network agent```

Starting with Junos OS Release 18.3R1: 
- the Junos OS image includes the ```OpenConfig``` package; therefore, you do not need anymore to install ```OpenConfig``` separately on your device.  
- the Junos OS image includes the ```Network Agent```, therefore, you do not need anymore to install the ```network agent``` separately on your device.  

This setup is using an older Junos release, so I installed these two packages:  
```
jcluser@vMX1> show version | match "Junos:|openconfig|na telemetry"
Junos: 18.2R1.9
JUNOS na telemetry [18.2R1-S3.2-C1]
JUNOS Openconfig [0.0.0.10-1]
```
### YANG files on Junos devices  

This section is FYI only. 

To show YANG packages installed on Junos, run this command 
```
jcluser@vMX-1> show system yang package
Package ID            :junos-openconfig
YANG Module(s)        :iana-if-type.yang ietf-inet-types.yang ietf-interfaces.yang ietf-yang-types.yang jnx-aug-openconfig-bgp.yang jnx-aug-openconfig-if-ip.yang jnx-aug-openconfig-interfaces.yang jnx-aug-openconfig-isis.yang jnx-aug-openconfig-lacp.yang jnx-aug-openconfig-lldp.yang jnx-aug-openconfig-local-routing.yang jnx-aug-openconfig-mpls.yang jnx-aug-openconfig-ni.yang jnx-aug-openconfig-routing-policy.yang jnx-openconfig-dev.yang junos-extension.yang openconfig-bgp-common-multiprotocol.yang openconfig-bgp-common-structure.yang openconfig-bgp-common.yang openconfig-bgp-global.yang openconfig-bgp-neighbor.yang openconfig-bgp-peer-group.yang openconfig-bgp-policy.yang openconfig-bgp-types.yang openconfig-bgp.yang openconfig-extensions.yang openconfig-if-aggregate.yang openconfig-if-ethernet.yang openconfig-if-ip-ext.yang openconfig-if-ip.yang openconfig-inet-types.yang openconfig-interfaces.yang openconfig-isis-lsdb-types.yang openconfig-isis-lsp.yang openconfig-isis-policy.yang openconfig-isis-routing.yang openconfig-isis-types.yang openconfig-isis.yang openconfig-lacp.yang openconfig-lldp-types.yang openconfig-lldp.yang openconfig-local-routing.yang openconfig-mpls-igp.yang openconfig-mpls-ldp.yang openconfig-mpls-rsvp.yang openconfig-mpls-sr.yang openconfig-mpls-static.yang openconfig-mpls-te.yang openconfig-mpls-types.yang openconfig-mpls.yang openconfig-network-instance-l2.yang openconfig-network-instance-l3.yang openconfig-network-instance-types.yang openconfig-network-instance.yang openconfig-platform-transceiver.yang openconfig-platform-types.yang openconfig-platform.yang openconfig-policy-types.yang openconfig-rib-bgp-ext.yang openconfig-rib-bgp-types.yang openconfig-rib-bgp.yang openconfig-routing-policy.yang openconfig-segment-routing.yang openconfig-terminal-device.yang openconfig-transport-types.yang openconfig-types.yang openconfig-vlan-types.yang openconfig-vlan.yang openconfig-yang-types.yang
Translation Script(s) :openconfig-bgp.slax openconfig-interface.slax openconfig-lldp.slax openconfig-local-routing.slax openconfig-mpls.slax openconfig-network-instance.slax openconfig-ni-bgp.slax openconfig-ni-mpls.slax openconfig-policy.slax openconfig-vlan.slax
Translation script status is enabled
```
To list YANG modules available on Junos, run this command: 
```
jcluser@vMX-1> file list /opt/yang-pkg/junos-openconfig/yang/

/opt/yang-pkg/junos-openconfig/yang/:
deviation/
iana-if-type.yang
ietf-inet-types.yang
ietf-interfaces.yang
ietf-yang-types.yang
jnx-aug-openconfig-bgp.yang
jnx-aug-openconfig-if-ip.yang
jnx-aug-openconfig-interfaces.yang
jnx-aug-openconfig-isis.yang
jnx-aug-openconfig-lacp.yang
jnx-aug-openconfig-lldp.yang
jnx-aug-openconfig-local-routing.yang
jnx-aug-openconfig-mpls.yang
jnx-aug-openconfig-ni.yang
jnx-aug-openconfig-routing-policy.yang
jnx-openconfig-dev.yang@ -> /opt/yang-pkg/junos-openconfig/yang/deviation/jnx-openconfig-dev.yang
junos-extension.yang
openconfig-bgp-common-multiprotocol.yang
openconfig-bgp-common-structure.yang
openconfig-bgp-common.yang
openconfig-bgp-global.yang
openconfig-bgp-neighbor.yang
openconfig-bgp-peer-group.yang
openconfig-bgp-policy.yang
openconfig-bgp-types.yang
openconfig-bgp.yang
openconfig-extensions.yang
openconfig-if-aggregate.yang
openconfig-if-ethernet.yang
openconfig-if-ip-ext.yang
openconfig-if-ip.yang
openconfig-inet-types.yang
openconfig-interfaces.yang
openconfig-isis-lsdb-types.yang
openconfig-isis-lsp.yang
openconfig-isis-policy.yang
openconfig-isis-routing.yang
openconfig-isis-types.yang
openconfig-isis.yang
openconfig-lacp.yang
openconfig-lldp-types.yang
openconfig-lldp.yang
openconfig-local-routing.yang
openconfig-mpls-igp.yang
openconfig-mpls-ldp.yang
openconfig-mpls-rsvp.yang
openconfig-mpls-sr.yang
openconfig-mpls-static.yang
openconfig-mpls-te.yang
openconfig-mpls-types.yang
openconfig-mpls.yang
openconfig-network-instance-l2.yang
openconfig-network-instance-l3.yang
openconfig-network-instance-types.yang
openconfig-network-instance.yang
openconfig-platform-transceiver.yang
openconfig-platform-types.yang
openconfig-platform.yang
openconfig-policy-types.yang
openconfig-rib-bgp-ext.yang
openconfig-rib-bgp-types.yang
openconfig-rib-bgp.yang
openconfig-routing-policy.yang
openconfig-segment-routing.yang
openconfig-terminal-device.yang
openconfig-transport-types.yang
openconfig-types.yang
openconfig-vlan-types.yang
openconfig-vlan.yang
openconfig-yang-types.yang
```
To know which `reference` of a YANG module is used on a Junos device, run the below command.  
Example with openconfig-interfaces.yang YANG module
```
jcluser@vMX-1> file more /opt/yang-pkg/junos-openconfig/yang/openconfig-interfaces.yang
```
To understand which YANG deviations are used on a Junos device, run this command:  
```
jcluser@vMX-1> file more /opt/yang-pkg/junos-openconfig/yang/jnx-openconfig-dev.yang
```

### Junos configuration

```
jcluser@vMX-1> show configuration system services netconf | display set
set system services netconf ssh
```
```
jcluser@vMX-1> show configuration system services extension-service | display set
set system services extension-service request-response grpc clear-text port 32768
set system services extension-service request-response grpc skip-authentication
set system services extension-service notification allow-clients address 0.0.0.0/0
```

# Kafka broker

The file [docker-compose.yml](docker-compose.yml) uses the Docker images [wurstmeister/zookeeper](https://hub.docker.com/r/wurstmeister/zookeeper) and [wurstmeister/kafka](https://hub.docker.com/r/wurstmeister/kafka) 

Edit the file [docker-compose.yml](docker-compose.yml) and update `KAFKA_ADVERTISED_HOST_NAME` with your host IP

Run this command to create and start the containers
```
$ docker-compose -f docker-compose.yml up -d
```

Run these commands to verify
```
$ docker images | grep wurstmeister
wurstmeister/kafka       latest              988f4a6ca13c        4 months ago        421MB
wurstmeister/zookeeper   latest              3f43f72cb283        10 months ago       510MB
```
```
$ docker ps
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                                NAMES
45b13d484728        wurstmeister/kafka       "start-kafka.sh"         9 hours ago         Up 9 hours          0.0.0.0:9092->9092/tcp                               kafka
0957d9af0d62        wurstmeister/zookeeper   "/bin/sh -c '/usr/sb…"   9 hours ago         Up 9 hours          22/tcp, 2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp   zookeeper
```
```
$ nc -vz 100.123.35.0 9092
Connection to 100.123.35.0 9092 port [tcp/*] succeeded!
```

# Telegraf 

Telegraf is an open source collector written in GO.  
It is plugin-driven (it has input plugins, output plugins, ...)  

## Telegraf configuration  

We will use `jti_openconfig_telemetry` input plugin (grpc client to collect telemetry on junos devices) and `kafka` output plugin.   
So, Telegraf will collect openconfig data from Junos devices and produce Kafta messages (with the data collected) .

Update the file [telegraf.conf](telegraf.conf) with your host IP.  

## Start Telegraf 

Run this command to start Telegraf  
```
$ docker run --rm --name telegraf -d -v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro telegraf
```
```
$ docker images | grep telegraf
telegraf                 latest              c7fc0c75c4ff        2 days ago          254MB
```
```
$ docker ps | grep telegraf
6b885a329f40        telegraf                 "/entrypoint.sh tele…"   42 seconds ago      Up 41 seconds       8092/udp, 8125/udp, 8094/tcp                         telegraf
```
## Telegraf troubleshooting 

### Telegraf logs

For troubleshooting purposes you can run this command
```
$ docker logs telegraf
```

### Telegraf configuration  

start a shell session in the telegraf container
```
$ docker exec -it telegraf bash
```
verify the telegraf configuration file
```
# more /etc/telegraf/telegraf.conf
```
exit the telegraf container
```
# exit
```

## Verify on Junos devices

To Display information about sensors, run this command on a Junos device:

```
jcluser@vMX1> show agent sensors
```

To verify if there is an established connection between Telegraf (grpc client) and a Junos device (grpc server), run this command on a Junos device:
```
jcluser@vMX1> show system connections | grep 32768
```

# Kafkacat 

Kafkacat is a command line tool to produce and consume messages  

## Installation 

On Ubuntu, run this command to install kafkacat
```
$ apt-get install kafkacat
```

Alternatively, use the Docker image [edenhill/kafkacat](https://hub.docker.com/r/edenhill/kafkacat/)  

## List metadata

Using kafkacat
```
$ kafkacat -L -b 100.123.35.0:9092
Metadata for all topics (from broker -1: 100.123.35.0:9092/bootstrap):
 1 brokers:
  broker 1001 at 100.123.35.0:9092
 1 topics:
  topic "juniper" with 1 partitions:
    partition 0, leader 1001, replicas: 1001, isrs: 1001
$
```
Using Docker 
```
$ docker run --rm -it edenhill/kafkacat:1.5.0 -L -b 100.123.35.0:9092
```
## Consume messages

In consumer mode, Kafkacat gets messages from the broker and writes messages to stdout.  

To use Kafkacat in consumer mode with the broker `100.123.35.0:9092` and the topic `juniper`, run this  kafkacat command: 
```
$ kafkacat -C -b 100.123.35.0:9092 -t juniper
```
or run the equivalent Docker command: 
```
$ docker run --rm -it edenhill/kafkacat:1.5.0 -C -b 100.123.35.0:9092 -t juniper
```
To consumes only 2 messages and automatically exit, run this kafkacat command (or the equivalent Docker command): 
```
$ kafkacat -C -b 100.123.35.0 -t juniper -c 2 -e
{"fields":{"/interfaces/interface/subinterfaces/subinterface/state/counters/in-octets":59373539,"/interfaces/interface/subinterfaces/subinterface/state/counters/in-pkts":736358,"/interfaces/interface/subinterfaces/subinterface/state/counters/out-octets":1560241033,"/interfaces/interface/subinterfaces/subinterface/state/counters/out-pkts":1308821,"_component_id":65535,"_sequence":4,"_subcomponent_id":0,"_timestamp":1574749462088},"name":"/interfaces/","tags":{"/interfaces/interface/@name":"fxp0","/interfaces/interface/subinterfaces/subinterface/@index":"0","device":"100.123.1.0","host":"0ecd5d0a86e0","path":"sensor_1000_6_1:/interfaces/:/interfaces/:xmlproxyd","system_id":"vMX-addr-0"},"timestamp":1574749461}

{"fields":{"/interfaces/interface/subinterfaces/subinterface/state/counters/in-octets":860905509,"/interfaces/interface/subinterfaces/subinterface/state/counters/in-pkts":7719660,"/interfaces/interface/subinterfaces/subinterface/state/counters/out-octets":475378658,"/interfaces/interface/subinterfaces/subinterface/state/counters/out-pkts":7743830,"_component_id":65535,"_sequence":4,"_subcomponent_id":0,"_timestamp":1574749462088},"name":"/interfaces/","tags":{"/interfaces/interface/@name":"em1","/interfaces/interface/subinterfaces/subinterface/@index":"0","device":"100.123.1.0","host":"0ecd5d0a86e0","path":"sensor_1000_6_1:/interfaces/:/interfaces/:xmlproxyd","system_id":"vMX-addr-0"},"timestamp":1574749461}

$ 
```

To consume the last 2 messages and automatically exit, run this  kafkacat command (or the equivalent Docker command):  
```
$ kafkacat -C -b 100.123.35.0:9092 -t juniper -o -2 -e
```

# Python

We will consume Kafka messages using Python  

## Requirements 

On Ubuntu, run this command

```
$ pip install kafka-python  
```

## Use Python to consume messages

Update the variable `kafka` in the python scripts [consumer1.py](consumer1.py) and [consumer2.py](consumer2.py) with your broker IP. 

They consume and print the messages from your broker (topic juniper).  

```
$ python consumer1.py
------------<output omitted for brevity>--------------
topic=juniper offset=716900 value={"fields":{"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/export-policy":"bgp-out","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/import-policy":"bgp-in","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/allow-own-as":1,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/replace-peer-as":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/enabled":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/multihop-ttl":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/erroneous-update-messages":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/treat-as-withdraw":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/enabled":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/helper-only":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/local-restarting":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/mode":"HELPER_ONLY","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restart-time":120,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restarting":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/restart-time":120,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/logging-options/state/log-neighbor-state-changes":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-client":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-cluster-id":"zero-len","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/snmp-peer-index":1,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/auth-password":"(null)","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/description":"(null)","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/enabled":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/established-transitions":1,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval-pending":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/interface-error":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/last-established":271870,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/local-as":104,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/NOTIFICATION":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/UPDATE":5,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/NOTIFICATION":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/UPDATE":5,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/neighbor-address":"192.168.2.0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-as":102,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-group":"underlay","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-type":"EXTERNAL","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/input":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/output":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/remove-private-as":"0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/route-flap-damping":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-admin-status":"START","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-state":"ESTABLISHED","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-status":"RUNNING","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/supported-capabilities":"MPBGP","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-address":"192.168.2.1","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-port":54928,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/mtu-discovery":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/passive-mode":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-address":"192.168.2.0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-port":179,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/tcp-mss":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/allow-multiple-as":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/maximum-paths":16,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ibgp/state/maximum-paths":16,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/state/enabled":true,"_component_id":65535,"_sequence":2955,"_subcomponent_id":0,"_timestamp":1574756676802},"name":"/network-instances/network-instance/protocols/protocol/bgp/","tags":{"/network-instances/network-instance/@instance-name":"master","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/@neighbor-address":"192.168.2.0","device":"100.123.1.3","host":"6b885a329f40","path":"sensor_1001:/network-instances/network-instance/protocols/protocol/bgp/:/network-instances/network-instance/protocols/protocol/bgp/:rpd","system_id":"vMX-addr-3"},"timestamp":1574756675}

topic=juniper offset=716901 value={"fields":{"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/export-policy":"bgp-out","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/import-policy":"bgp-in","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/allow-own-as":1,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/replace-peer-as":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/enabled":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/multihop-ttl":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/erroneous-update-messages":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/treat-as-withdraw":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/enabled":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/helper-only":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/local-restarting":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/mode":"HELPER_ONLY","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restart-time":120,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restarting":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/restart-time":120,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/logging-options/state/log-neighbor-state-changes":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-client":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-cluster-id":"zero-len","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/snmp-peer-index":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/auth-password":"(null)","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/description":"(null)","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/enabled":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/established-transitions":1,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval-pending":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/interface-error":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/last-established":271866,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/local-as":104,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/NOTIFICATION":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/UPDATE":5,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/NOTIFICATION":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/UPDATE":3,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/neighbor-address":"192.168.1.0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-as":101,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-group":"underlay","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-type":"EXTERNAL","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/input":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/output":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/remove-private-as":"0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/route-flap-damping":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-admin-status":"START","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-state":"ESTABLISHED","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-status":"RUNNING","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/supported-capabilities":"MPBGP","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-address":"192.168.1.1","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-port":57814,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/mtu-discovery":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/passive-mode":false,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-address":"192.168.1.0","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-port":179,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/tcp-mss":0,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/allow-multiple-as":true,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/maximum-paths":16,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ibgp/state/maximum-paths":16,"/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/state/enabled":true,"_component_id":65535,"_sequence":2955,"_subcomponent_id":0,"_timestamp":1574756676802},"name":"/network-instances/network-instance/protocols/protocol/bgp/","tags":{"/network-instances/network-instance/@instance-name":"master","/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/@neighbor-address":"192.168.1.0","device":"100.123.1.3","host":"6b885a329f40","path":"sensor_1001:/network-instances/network-instance/protocols/protocol/bgp/:/network-instances/network-instance/protocols/protocol/bgp/:rpd","system_id":"vMX-addr-3"},"timestamp":1574756675}
------------<output omitted for brevity>--------------
```
```
$ python consumer2.py
------------<output omitted for brevity>--------------
######## new message #########
topic=juniper offset=1363231 device=100.123.1.3 timestamp=1574762713
openconfig_data={u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-client': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/remove-private-as': u'0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/supported-capabilities': u'MPBGP', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/allow-own-as': 1, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-type': u'EXTERNAL', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-admin-status': u'START', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/passive-mode': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/interface-error': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/state/enabled': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/description': u'(null)', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/last-established': 271870, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/restart-time': 120, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/NOTIFICATION': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restart-time': 120, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-status': u'RUNNING', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-as': 102, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-port': 179, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/established-transitions': 1, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-group': u'underlay', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/treat-as-withdraw': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/UPDATE': 5, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-address': u'192.168.2.1', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/local-as': 104, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-address': u'192.168.2.0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/enabled': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/output': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-state': u'ESTABLISHED', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/local-restarting': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/export-policy': u'bgp-out', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/mtu-discovery': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/allow-multiple-as': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/import-policy': u'bgp-in', u'_timestamp': 1574762714806, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/enabled': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restarting': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/tcp-mss': 0, u'_sequence': 5974, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/maximum-paths': 16, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ibgp/state/maximum-paths': 16, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/UPDATE': 5, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/snmp-peer-index': 1, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/helper-only': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-port': 54928, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/enabled': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/route-flap-damping': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/multihop-ttl': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/NOTIFICATION': 0, u'_component_id': 65535, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/input': 0, u'_subcomponent_id': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-cluster-id': u'zero-len', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/neighbor-address': u'192.168.2.0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval-pending': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/replace-peer-as': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/mode': u'HELPER_ONLY', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/erroneous-update-messages': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/auth-password': u'(null)', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/logging-options/state/log-neighbor-state-changes': False}
######## new message #########
topic=juniper offset=1363232 device=100.123.1.3 timestamp=1574762713
openconfig_data={u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-client': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/remove-private-as': u'0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/supported-capabilities': u'MPBGP', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/allow-own-as': 1, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-type': u'EXTERNAL', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-admin-status': u'START', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/passive-mode': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/interface-error': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/state/enabled': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/description': u'(null)', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/last-established': 271866, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/restart-time': 120, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/NOTIFICATION': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restart-time': 120, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-status': u'RUNNING', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-as': 101, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-port': 179, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/established-transitions': 1, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/peer-group': u'underlay', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/treat-as-withdraw': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/UPDATE': 5, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-address': u'192.168.1.1', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/local-as': 104, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/remote-address': u'192.168.1.0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/enabled': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/output': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/session-state': u'ESTABLISHED', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/local-restarting': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/export-policy': u'bgp-out', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/mtu-discovery': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/allow-multiple-as': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/apply-policy/state/import-policy': u'bgp-in', u'_timestamp': 1574762714806, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/enabled': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/peer-restarting': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/tcp-mss': 0, u'_sequence': 5974, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ebgp/state/maximum-paths': 16, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/use-multiple-paths/ibgp/state/maximum-paths': 16, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/sent/UPDATE': 3, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/snmp-peer-index': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/helper-only': True, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/transport/state/local-port': 57814, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/enabled': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/route-flap-damping': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/ebgp-multihop/state/multihop-ttl': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/messages/received/NOTIFICATION': 0, u'_component_id': 65535, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/queues/input': 0, u'_subcomponent_id': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/route-reflector/state/route-reflector-cluster-id': u'zero-len', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/neighbor-address': u'192.168.1.0', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/import-eval-pending': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/as-path-options/state/replace-peer-as': False, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/graceful-restart/state/mode': u'HELPER_ONLY', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/error-handling/state/erroneous-update-messages': 0, u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/state/auth-password': u'(null)', u'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/logging-options/state/log-neighbor-state-changes': False}
------------<output omitted for brevity>--------------
```
# Stop the setup 

## Telegraf 
```
$ docker stop telegraf
telegraf
```
```
$ docker ps | grep telegraf
$ docker ps -a | grep telegraf
```
## Kafka

### Stop Kafka without removing containers

```
$ docker-compose stop
Stopping kafka     ... done
Stopping zookeeper ... done
```
```
$ docker ps | grep wurstmeister
$ docker ps -a | grep wurstmeister
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                        PORTS               NAMES
45b13d484728        wurstmeister/kafka        "start-kafka.sh"         9 hours ago         Exited (143) 36 seconds ago                       kafka
0957d9af0d62        wurstmeister/zookeeper    "/bin/sh -c '/usr/sb…"   9 hours ago         Exited (137) 29 seconds ago                       zookeeper
```

### Stop Kafka and remove containers
```
$ docker-compose down
Stopping kafka     ... done
Stopping zookeeper ... done
Removing kafka     ... done
Removing zookeeper ... done
```
```
$ docker ps  | grep wurstmeister
$ docker ps -a | grep wurstmeister
```

# Credits 

Thank you to Jag Channa for writing this blog: https://openeye.blog/2018/03/05/streaming-junos-telemetry-to-apache-kafka-via-telegraf/   
It provided the basis for this repository.
