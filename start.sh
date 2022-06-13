#!/bin/bash
app="maestro-1.0"
docker build -t ${app} .

#mount current local directory to /maestro & run
docker run -d -p 15001:15001 \
  --name=${app} \
  -v %cd%:/maestro \
  python3 maestro/maestro.py