# Deploy a Kafka broker

The file [docker-compose.yml](docker-compose.yml) uses the Docker images [wurstmeister/zookeeper](https://hub.docker.com/r/wurstmeister/zookeeper) and [wurstmeister/kafka](https://hub.docker.com/r/wurstmeister/kafka) 

Install Docker and Docker-compose  

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

# 

docker run --rm --name telegraf -d -v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro telegraf


# Kafkacat 

Kafkacat is a command line tool to produce and consume messages  

## Installation 

On Ubuntu, run this command to install kafkacat
```
$ apt-get install kafkacat
```

Alternatively, install Docker and use the Docker image [edenhill/kafkacat](https://hub.docker.com/r/edenhill/kafkacat/)  

## List metadata from topics from a broker

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

#

