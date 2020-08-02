#!/bin/bash

docker run --rm influxdb:meta influxd-meta config > influxdb-meta.conf
docker run -v $PWD/influxdb-meta.conf:/etc/influxdb/influxdb-meta.conf:ro \
	            influxdb -config /etc/influxdb/influxdb-meta.conf
