#!/bin/sh

set -e

# replace environment variables in the default.conf.tpl file with their values
# this will swap $(LISTEN_PORT) with the value of the LISTEN_PORT environment variable
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# start nginx and keep it running in the foreground
nginx -g 'daemon off;'
