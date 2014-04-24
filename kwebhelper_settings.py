#!/usr/bin/env python

# helper settings file for kweb Minimal Kiosk Browser
# Copyright 2013-2014 by Guenter Kreidl
# free software without any warranty
# you can do with it what you like
# version 1.4

# GLOBAL OPTIONS
# where the downloads, PDF files etc. go, make sure a "Downloads" folder exists there
#homedir = '/media/volume'
homedir = ''
# if empty, the user's home dir will be taken

# OMXPLAYER AUDIO VIDEO OPTIONS
omxoptions = []
# for selecting the sound output, uncomment one of these:
#omxoptions = ['-o','hdmi']
#omxoptions = ['-o','local']
# more options are also possible of course
# special options for watching live tv streams (omxplayer > 0.32)
omx_livetv_options = ['--live']
# add the start of your live tv stream links to this list to enable live tv options
live_tv = []
# like this:
#live_tv = ['http://192.168.0.5:9082']
# set this to false, if you want to allow more than one omxplayer instance
kill_omxplayer = True
#kill_omxplayer = False

# mimetypes: if given, this will restrict what omxplayer will be given to play:
mimetypes = []
# normally omxplayer is started from a terminal (xterm), to clear the screen and get full keyboard control
# Set the following to "False" to use omxplayer without starting a terminal first
omxplayer_in_terminal_for_video = True
#omxplayer_in_terminal_for_video = False
omxplayer_in_terminal_for_audio = True
#omxplayer_in_terminal_for_audio = False

# options for m3u playlists, to check that they contain only audio files or streams
audioextensions = ['mp3','aac','flac','wav','wma','cda','ogg','ogm','ac3','ape']
try_stream_as_audio = False
# if set to "True", the following list will be used for checking for video files
videoextensions = ['asf','avi','mpg','mp4','mpeg','m2v','m1v','vob','divx','xvid','mov','m4v','m2p','mkv','m2ts','ts','mts','wmv','webm']

# Play audio files or playlists that contain only audio files in omxaudioplayer GUI: 
useAudioplayer = True
# options for omxplayer to be used when playing audio
omxaudiooptions = []
# volume setting when starting omxaudioplayer ranging from -20 to 4 ( -60 to +12 db)
defaultaudiovolume = 0
# start playing and close after playing last song automatically (if "True", set to "False" to disable)
autoplay = True
autofinish = True
# Interface settings for omxaudioplayer:
# The font to be used for playlist and buttons
fontname = 'SansSerif'
# value between 10 and 22, will also determine the size of the GUI window:
fontheight = 14
# number of entries displayed in playlist window, between 5 and 25:
maxlines = 8
# width of the window, value between 40 and 80, defines the minimum number of characters of the song name
# displayed in the songlist (usually much more are shown!)
lwidth = 40

# if the following is set to "True", vlc will be used to play audio files and playlists (audio only)
useVLC = False
#useVLC = True

#COMMAND EXECUTION OPTIONS
# if this is set to "True", all Desktop (GUI) programs will be executed without starting a terminal first
check_desktop = True
#check_desktop = False
# direct commands will be executed without starting a terminal first
# use it for background commands or programs with a GUI that are not desktop programs or if check_desktop is set to "False"
direct_commands = ['kwebhelper.py','omxplayer']
# preferred terminal to run commands in, must be set
preferred_terminal = 'lxterminal'
#preferred_terminal = 'xterm'
formdata_in_terminal = False
#formdata_in_terminal = True
# set the following to "True", if you want to spare memory overhead (but you'll get more disk write accesses)
run_as_script = False
#run_as_script = True

# PDF OPTIONS
# preferred pdf reader; both must be set or emtpy
pdfprogpath = ''
pdfprog = ''
#pdfprogpath = '/usr/bin/mupdf'
#pdfprog = 'mupdf'
# additional options for pdf program (must match the selected program!):
pdfoptions = []
#pdfoptions = ['-fullscreen']
# this will allow to open pdf files on a local server as files instead of downloading them first;
# will only work with "http://localhost" links
pdfpathreplacements = {}
#pdfpathreplacements = {'http://localhost:8073/Ebooks1':'file:///var/www/Ebooks1'}

# DOWNLOAD OPTIONS
#download options for external download mode, enable one of these options:
show_download_in_terminal = True
#show_download_in_terminal = False

# ONLINE VIDEO OPTIONS
# options for pages containing video, either HTML5 video tags or all websites supported by youtube-dl
# if html5 video tags include more than one source format, select the preferred one here
preferred_html5_video_format = '.mp4'
# Choose, if HTML5 URL extraction is tried first and youtube-dl extraction afterwards or vice versa
html5_first = True
#html5_first = False
#additional youtube-dl options, e. g. selecting a resolution or file format
youtube_dl_options = []
#youtube_dl_options = ['-f','37/22/18']
# special omxplayer options for web video
youtube_omxoptions = []
# to use the same options as for other video, set
#youtube_omxoptions = omxoptions

### end of global settings
