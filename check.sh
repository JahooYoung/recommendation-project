#!/bin/bash

for ((i=1; i<=4; i++)); do
    echo -e "\nnode$i jps:"
    docker exec -it node$i jps
done
