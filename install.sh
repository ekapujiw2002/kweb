#!/bin/sh
sudo install -g dialout kweb /usr/bin
sudo cp ./kweb.desktop /usr/share/applications
sudo cp ./minimalkioskbrowser.png /usr/share/pixmaps
sudo cp ./kweb.1.gz /usr/share/man/man1
sudo cp ./kwebhelper.py /usr/local/bin
sudo chmod +x /usr/local/bin/kwebhelper.py
sudo cp ./kwebhelper_settings.py /usr/local/bin
sudo chmod +x /usr/local/bin/kwebhelper_settings.py

