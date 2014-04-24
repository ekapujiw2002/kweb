prefix=/usr

kweb: kweb.c
	gcc -O kweb.c -o kweb `pkg-config --cflags gtk+-3.0 --libs webkitgtk-3.0`

install: kweb
	sudo install -g dialout kweb $(prefix)/bin
	sudo cp ./kweb.desktop $(prefix)/share/applications
	sudo cp ./minimalkioskbrowser.png $(prefix)/share/pixmaps
	sudo cp ./kweb.1.gz $(prefix)/share/man/man1
	sudo cp ./kwebhelper.py $(prefix)/local/bin
	sudo chmod +x $(prefix)/local/bin/kwebhelper.py
	sudo cp ./kwebhelper_settings.py $(prefix)/local/bin
	sudo chmod +x $(prefix)/local/bin/kwebhelper_settings.py

remove: 
	sudo rm $(prefix)/bin/kweb
	sudo rm $(prefix)/share/applications/kweb.desktop
	sudo rm $(prefix)/share/pixmaps/minimalkioskbrowser.png
	sudo rm $(prefix)/share/man/man1/kweb.1.gz
	sudo rm $(prefix)/local/bin/kwebhelper.py
	sudo rm $(prefix)/local/bin/kwebhelper_settings.py

clean:
	rm ./kweb

tar: kweb.c Makefile
	cd .. && tar -czvf kweb_1.4.tar.gz ./kweb-1.4/Makefile ./kweb-1.4/kweb.c ./kweb-1.4/INSTALL ./kweb-1.4/COPYING ./kweb-1.4/minimalkioskbrowser.png ./kweb-1.4/kweb.desktop ./kweb-1.4/kweb.1.gz ./kweb-1.4/kwebhelper.py ./kweb-1.4/kwebhelper_settings.py ./kweb-1.4/kweb ./kweb-1.4/kweb_manual.pdf ./kweb-1.4/Examples/default_homepage.html ./kweb-1.4/Examples/kiosk ./kweb-1.4/Examples/kioskm ./kweb-1.4/install.sh ./kweb-1.4/remove.sh ./kweb-1.4/tools.tar.gz ./kweb-1.4/check.py ./kweb-1.4/changelog-1-4.txt

deb: kweb
	debuild -us -uc	

install-deb: kweb_1.4-*_armhf.deb
	sudo dpkg -i ../kweb_1.4-*_armhf.deb
