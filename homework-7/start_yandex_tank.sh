#!/usr/bin/env bash
yandex-tank() {
	docker run --rm -it \
		-v "$(pwd)"/yandex_tank:/var/loadtest \
		-v "$(pwd)"/ssh/ssh_key:/root/.ssh/id_rsa \
		--net=container:google_app \
		direvius/yandex-tank:latest \
		--config="$1"
}

yandex-tank load1.yaml
yandex-tank load2.yaml
yandex-tank load3.yaml