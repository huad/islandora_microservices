#!/bin/bash
nohup python2.6 islandora_listener.py -C islandora_listener.cfg -P plugins/smithsonian_plugin.cfg > ./islandora_listener.log 2>&1 &
