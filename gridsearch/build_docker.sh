#!/bin/bash

docker build -t registry.whatap.io:5000/hsnam_dev:0921 -f Dockerfile .

#docker run -d registry.whatap.io:5000/hsnam_dev:0917

docker push registry.whatap.io:5000/hsnam_dev:0921 
