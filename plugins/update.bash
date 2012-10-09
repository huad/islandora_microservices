#!/bin/bash
# Gets the latest data from github, not sure if the tokens will last indefinitely though.
wget 'https://raw.github.com/discoverygarden/sidora/6.x/data/microservices/smithsonian_plugin.cfg?login=nigelgbanks&token=2a79afc0e1be88033e3ec59afcf6d26e' -O smithsonian_plugin.cfg
wget 'https://raw.github.com/discoverygarden/sidora/6.x/data/microservices/smithsonian_plugin.py?login=nigelgbanks&token=bfd22c80e9e8ccc5fb5e7b6cb4a1d1ed' -O smithsonian_plugin.py
