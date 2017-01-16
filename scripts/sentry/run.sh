#!/usr/bin/env bash

sudo ansible-playbook ./playbook.yml -i ./inventories/dev -e hostname=devmeter --connection=local
