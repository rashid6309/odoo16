#!/bin/bash


sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo apt --fix-broken install -y
