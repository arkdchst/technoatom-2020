#!/usr/bin/env bash
mkdir ssh
ssh-keygen -t rsa -f ssh/ssh_key -N ''
cp ssh/ssh_key.pub google_app/

docker build -t google_app google_app/
