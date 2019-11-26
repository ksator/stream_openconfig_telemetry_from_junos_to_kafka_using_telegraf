# About this repo  

- How to stream openconfig telemetry from junos devices to kafka using telegraf   
- How to consume the kafka messages  

We will use: 
- Junos devices with Openconfig telemetry support (Junos devices are the grpc servers)  
- Telegraf to collect openconfig data from Junos devices (Telegraf is the grpc client)  
- a Kafka broker 
- Telegraf to produce Kafta messages (with the data collected from Junos devices) to the Kafka broker.
- a Kafka command line tool (kafkacat) to consume messages from the broker 
- python scripts to to consume messages from the broker  

# Requirements 

## Host requirements 

Install Docker and install Docker-compose  

## Junos requirements  

### Junos packages 

In order to collect data from Junos using openconfig telemetry, the devices require the Junos packages ```openconfig``` and ```network agent```

Starting with Junos OS Release 18.3R1: 
- the Junos OS image includes the ```OpenConfig``` package; therefore, you do not need anymore to install ```OpenConfig``` separately on your device.  
- the Junos OS image includes the ```Network Agent```, therefore, you do not need anymore to install the ```network agent``` separately on your device.  

This setup is using an older Junos release, so I installed these two packages. 

Here's the details:
```
jcluser@vMX1> show version | match "Junos:|openconfig|na telemetry"
Junos: 18.2R1.9
JUNOS na telemetry [18.2R1-S3.2-C1]
JUNOS Openconfig [0.0.0.10-1]
```
To show YANG packages installed on Junos, run this command 
```
jcluser@vMX-1> show system yang package
Package ID            :junos-openconfig
YANG Module(s)        :iana-if-type.yang ietf-inet-types.yang ietf-interfaces.yang ietf-yang-types.yang jnx-aug-openconfig-bgp.yang jnx-aug-openconfig-if-ip.yang jnx-aug-openconfig-interfaces.yang jnx-aug-openconfig-isis.yang jnx-aug-openconfig-lacp.yang jnx-aug-openconfig-lldp.yang jnx-aug-openconfig-local-routing.yang jnx-aug-openconfig-mpls.yang jnx-aug-openconfig-ni.yang jnx-aug-openconfig-routing-policy.yang jnx-openconfig-dev.yang junos-extension.yang openconfig-bgp-common-multiprotocol.yang openconfig-bgp-common-structure.yang openconfig-bgp-common.yang openconfig-bgp-global.yang openconfig-bgp-neighbor.yang openconfig-bgp-peer-group.yang openconfig-bgp-policy.yang openconfig-bgp-types.yang openconfig-bgp.yang openconfig-extensions.yang openconfig-if-aggregate.yang openconfig-if-ethernet.yang openconfig-if-ip-ext.yang openconfig-if-ip.yang openconfig-inet-types.yang openconfig-interfaces.yang openconfig-isis-lsdb-types.yang openconfig-isis-lsp.yang openconfig-isis-policy.yang openconfig-isis-routing.yang openconfig-isis-types.yang openconfig-isis.yang openconfig-lacp.yang openconfig-lldp-types.yang openconfig-lldp.yang openconfig-local-routing.yang openconfig-mpls-igp.yang openconfig-mpls-ldp.yang openconfig-mpls-rsvp.yang openconfig-mpls-sr.yang openconfig-mpls-static.yang openconfig-mpls-te.yang openconfig-mpls-types.yang openconfig-mpls.yang openconfig-network-instance-l2.yang openconfig-network-instance-l3.yang openconfig-network-instance-types.yang openconfig-network-instance.yang openconfig-platform-transceiver.yang openconfig-platform-types.yang openconfig-platform.yang openconfig-policy-types.yang openconfig-rib-bgp-ext.yang openconfig-rib-bgp-types.yang openconfig-rib-bgp.yang openconfig-routing-policy.yang openconfig-segment-routing.yang openconfig-terminal-device.yang openconfig-transport-types.yang openconfig-types.yang openconfig-vlan-types.yang openconfig-vlan.yang openconfig-yang-types.yang
Translation Script(s) :openconfig-bgp.slax openconfig-interface.slax openconfig-lldp.slax openconfig-local-routing.slax openconfig-mpls.slax openconfig-network-instance.slax openconfig-ni-bgp.slax openconfig-ni-mpls.slax openconfig-policy.slax openconfig-vlan.slax
Translation script status is enabled
```
To list YANG modules available on Junos, Run this command: 
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
We will use jti_openconfig_telemetry input plugin (grpc client to collect telemetry on junos devices) and kafka output plugin.   
So, Telegraf will collect openconfig data from Junos devices and produce Kafta messages (with the data collected) .

Update the file [telegraf.conf](telegraf.conf) with your host IP.  

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

In producer mode, Kafkacat reads messages from stdin, and sends them to the broker.  
In consumer mode, Kafkacat gets messages from the broker and writes messages to stdout.  

To use Kafkacat in consumer mode with the broker `100.123.35.0:9092` and the topic `juniper`: 
run this  kafkacat command: 
```
$ kafkacat -C -b 100.123.35.0:9092 -t juniper
```
or run this Docker command: 
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

# Consume Kafka messages using Python

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
