#!/usr/bin/env bash

ok=false
for i in {1..10}; do
	ping -c1 myapp && curl "http://myapp:8083/" && ok=true && break
	sleep 2
done >/dev/null 2>&1

if [ "$ok" = "true" ]; then
	"$@"
else
	echo 'myapp wait timeout' >&2
	exit 1
fi
