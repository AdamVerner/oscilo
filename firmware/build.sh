#!/usr/bin/env bash

set -e # stop on first failed command

./sine_gen.py

quartus_map --read_settings_files=on --write_settings_files=off main -c main
quartus_fit --read_settings_files=off --write_settings_files=off main -c main
quartus_asm --read_settings_files=off --write_settings_files=off main -c main
quartus_sta main -c main
quartus_eda --read_settings_files=off --write_settings_files=off main -c main

echo "#############################"
echo "  finished successfully"
md5sum output_files/main.sof
date
