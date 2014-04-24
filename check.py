#!/usr/bin/env python

# check for programs needed by Minimal Kiosk Browser
# and install default homepage.html, if none exists

import os

homedir = os.path.expanduser('~')
cwd = os.getcwd()
dependencies_fullfilled = True

print "... looking for programs needed by Minimal Kiosk Browser"

# checking for xterm
if os.path.exists('/usr/bin/xterm'):
    print "found: xterm"
else:
    dependencies_fullfilled = False
    print "xterm not found. It is needed by Minimal Kiosk Browser. Install it with:"
    print "sudo apt-get install xterm"
    print

# checking for PDF support
if not os.path.exists('/usr/bin/mupdf') and not os.path.exists('/usr/bin/xpdf'):
    dependencies_fullfilled = False
    print "No suitable PDF viewer found. Install xpdf with:"
    print "sudo apt-get install xpdf"

elif os.path.exists('/usr/bin/mupdf') and not os.path.exists('/usr/bin/xpdf'):
    print "minimal PDF support is found using mupdf."
    print "for better PDF support it is highly recommended to install xpdf:"
    print "sudo apt-get install xpdf"
    print
else:
    print "found: xpdf for best PDF support"

#checking for omxplayer
if os.path.exists('/usr/bin/omxplayer'):
    print "found: omxplayer"
else:
    dependencies_fullfilled = False
    print "omxplayer not found. It is needed for audio and video support. Install it with:"
    print "sudo apt-get install omxplayer"
    print

#checking for youtube-dl
if os.path.exists('/usr/bin/youtube-dl'):
    print "found: youtube-dl"
else:
    dependencies_fullfilled = False
    print "youtube-dl not found. It is needed for web video support. Install it with:"
    print "sudo apt-get install youtube-dl"
    print "Afterwards run TWICE:"
    print "sudo youtube-dl -U"
    print

#checking for lxterminal
if os.path.exists('/usr/bin/lxterminal'):
    print "found: lxterminal"
else:
    dependencies_fullfilled = False
    print "lxterminal not found. It is needed for command line support."
    print "You can disable it's use in kwebhelper_settings by setting: preferred_terminal = 'xterm'"
    print "otherwise you must install it with:"
    print "sudo apt-get install lxterminal"
    print

#checking for vlc
if os.path.exists('/usr/bin/vlc'):
    print "found: vlc (for optional audio playlist support)"
else:
    print "vlc not found. It can be optionally used for audio playlists (disabled by default)."
    print "If you want to make use of this option, you must install it with:"
    print "sudo apt-get install vlc"
    print

# creating default homepage:
if not os.path.exists(homedir + os.sep + 'homepage.html'):
    f = file('Examples/default_homepage.html','rb')
    t = f.read().decode('utf-8')
    f.close()
    t = t.replace('$manual$','<a href="file://'+cwd+'/kweb_manual.pdf">manual</a>')
    f = file(homedir + os.sep + 'homepage.html','wb')
    f.write(t.encode('utf-8'))
    f.close()
    print "created default homepage"
else:
    print "You already have a hompage.html file in your user directory"
print
if dependencies_fullfilled:
    print "All important programs needed by Minimal Kiosk Browser have been found."
    print "You can start to use it now with all possible options."
else:
    print "Some programs needed to use all features of Minimal Kiosk Browser are not installed."
    print "Follow the install recommendations above."
