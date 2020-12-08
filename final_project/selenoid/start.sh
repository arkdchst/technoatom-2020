#!/usr/bin/env bash
docker run -d --rm								\
--name selenoid									\
--network myapp									\
-v /var/run/docker.sock:/var/run/docker.sock	\
-v "$PWD"/config/:/etc/selenoid/:ro				\
aerokube/selenoid:latest-release -container-network=myapp