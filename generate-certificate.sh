#!/bin/bash
# REMEMBER: CN needs to be set correctly or the tunnel will fail
echo "Generating keypair..."
openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 3650 -nodes -out cert/server.crt -keyout cert/server.key
echo "DONE"