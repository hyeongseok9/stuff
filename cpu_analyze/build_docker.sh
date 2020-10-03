#!/bin/bash

docker build -t simple-influxviewer -f Dockerfile.viewer .
docker build -t simple-influxvapi -f Dockerfile.api .
