#!/bin/bash

docker run --rm influxdb influxd config > influxdb.conf
docker run -e INFLUX_USERNAME:root -e INFLUX_PASSWORD:root -v $PWD/influxdb-meta.conf:/etc/influxdb/influxdb-meta.conf:ro \
	            influxdb -config /etc/influxdb/influxdb-meta.conf

docker run -d -e INFLUX_USERNAME:root -e INFLUX_PASSWORD:root \
	-p 8086:8086 \
    -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
    influxdb -config /etc/influxdb/influxdb.conf
