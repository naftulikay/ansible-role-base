#!/usr/bin/make -f

.DEFAULT_GOAL := apply
.PHONY: apply

DEFAULT_IMAGE:=centos7
IMAGE:=$(shell echo "$${IMAGE:-$(DEFAULT_IMAGE)}")

clean:
	@docker-compose rm -fs $(IMAGE)

start:
	@docker-compose up -d $(IMAGE)

shell: start
	@docker exec -it $(IMAGE) bash

test: start
	@docker exec $(IMAGE) ansible --version
	@docker exec $(IMAGE) wait-for-boot
	@docker exec $(IMAGE) env ANSIBLE_FORCE_COLOR=yes \
		ansible-playbook /etc/ansible/roles/default/tests/playbook.yml

apply:
	@mkdir -p target/ .ansible/galaxy-roles
	@rsync --exclude=.ansible/galaxy-roles -a ./ .ansible/galaxy-roles/vim-personal/
	@ansible-playbook -i localhost, --ask-become-pass local.yml
