#!/usr/bin/env python
# -*- coding: utf-8 -*-

# helper file for kweb Minimal Kiosk Browser
# Copyright 2013-2014 by Guenter Kreidl
# free software without any warranty
# you can do with it what you like
# version 1.4

import os,urllib,sys,subprocess,threading,time
import Tkinter as tk

# GLOBAL OPTIONS
# use external settings file, if not empty
#settings = ''
settings = '/usr/local/bin/kwebhelper_settings.py'

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

# take settings from separate file:
if settings and os.path.exists(settings):
    try:
        execfile(settings)
    except:
        pass

if not homedir:
    homedir = os.path.expanduser('~')
dldir = homedir +'/Downloads'
if not os.path.exists(dldir):
    os.mkdir(dldir)

# helper functions

def get_opt(options):
    if '--win' in options:
        pos = options.index('--win')
        if pos < (len(options) -2):
            options[pos+1] = '"' + options[pos+1] + '"'
    return ' '.join(options)

def get_playlist(url, audio_as_stream):
    playlist = []
    fn = ''
    audioonly = True
    go = False
    if url.startswith('http://'):
        try:
            fn,h = urllib.urlretrieve(url)
            go = True
        except:
            pass
    elif url.startswith('file://'):
        fn = url.replace('file://','').replace('%20',' ')
        fn = urllib.unquote(fn)
        if os.path.exists(fn):
            go = True
    elif os.path.exists(url):
        fn = url
        go = True
    if go:
        f = file(fn,'rb')
        pl = f.read()
        f.close()
        if url.startswith('http://'):
            os.remove(fn)
        pll = pl.split('\n')
        if url.lower().endswith('.m3u') or url.lower().endswith('.m3u8'):
            for s in pll:
                if s != '' and not s.startswith('#'):
                    if s.split('.')[-1].lower() in audioextensions:
                        pass
                    elif audio_as_stream and s.split('.')[-1].lower() not in videoextensions:
                        pass
                    else:
                        audioonly = False
                    playlist.append(s)
        elif url.lower().endswith('.pls'):
            for s in pll:
                if s.startswith('File'):
                    aurl = s.split('=')[1].strip()
                    playlist.append(aurl)
    return (audioonly, playlist)
    

def video_tag_extractor(url):
    result = []
    if url.startswith('file://'):
        fpath = url.replace('file://','').replace('%20',' ')
    else:
        try:
            fpath,h = urllib.urlretrieve(url)
        except:
            return result
    f = file(fpath,'rb')
    html = f.read()
    f.close()
    if '<video ' in html:
        htl = html.split('<video')
        for ind in range(1,len(htl)):
            if not 'src="' in htl[ind]:
                continue
            vtl = htl[ind].split('src="')
            if len(vtl) > 2:
                links = []
                for l in vtl[1:]:
                    pos = l.find('"')
                    links.append(l[0:pos])
                link = links[0]
                for li in links:
                    if preferred_html5_video_format and li.lower().endswith(preferred_html5_video_format):
                        link = li
            else:
                vt = vtl[1]
                pos = vt.find('"')
                link = vt[0:pos]
            if link.startswith('http://')  or link.startswith('https://') or link.startswith('rtsp://') or link.startswith('rtmp://'):
                result.append(link)
            elif link.startswith('file://'):
                newlink = '"'+link.replace('file://','').replace('%20',' ')+'"'
                result.append(newlink)
            else:
                urll = url.split('/')
                if link.startswith('/'):
                    newlink = '/'.join(urll[0:3]+[link[1:]])
                else:
                    relcount = len(urll) - 1 - link.count('../')
                    newlink = '/'.join(urll[0:relcount]+[link.replace('../','')])
                if newlink.startswith('file://'):
                    newlink = '"'+newlink.replace('file://','').replace('%20',' ')+'"'
                result.append(newlink)
    return result

def play_ytdl(res):
    vlist = res.split('\n')
    if (len(vlist) == 1) or (len(vlist) == 2 and vlist[1] == ''):
        vurl = vlist[0]
        if kill_omxplayer:
            dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
        pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+youtube_omxoptions+[vurl]+['>', '/dev/null', '2>&1']
        os.execv("/usr/bin/xterm",pargs)
    else:
        if kill_omxplayer:
            script = '#!/bin/bash\nkillall omxplayer.bin > /dev/null 2>&1\n'
        else:
            script = '#!/bin/bash\n'
        for vurl in vlist:
            if vurl != '':
                script += 'omxplayer ' + get_opt(youtube_omxoptions) + ' "' + vurl + '" > /dev/null 2>&1\n'
        f = file(dldir+os.sep+'playall.sh','wb')
        f.write(script)
        f.close()
        os.chmod(dldir+os.sep+'playall.sh',511)
        os.execl("/usr/bin/xterm","xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",dldir+os.sep+'playall.sh')

def play_html5(tags):
    if len(tags) == 1:
        if kill_omxplayer:
            dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
        pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+youtube_omxoptions+[tags[0]]+['>', '/dev/null', '2>&1']
        os.execv("/usr/bin/xterm",pargs)
    else:
        if kill_omxplayer:
            script = '#!/bin/bash\nkillall omxplayer.bin > /dev/null 2>&1\n'
        else:
            script = '#!/bin/bash\n'
        for t in tags:
            script += 'omxplayer ' + get_opt(youtube_omxoptions) + ' ' + t + ' > /dev/null 2>&1\n'

        f = file(dldir+os.sep+'playall.sh','wb')
        f.write(script)
        f.close()
        os.chmod(dldir+os.sep+'playall.sh',511)
        os.execl("/usr/bin/xterm","xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",dldir+os.sep+'playall.sh')
    

# omxaudioplayer GUI

class omxaudioplayer(tk.Frame):

    def __init__(self, master=None, playlist=[],mode='simple',autofinish=True,volume=0,omxoptions=[],
                 fontheight=14,fontname='SansSerif',maxlines=8,width=40,autoplay=True):
        tk.Frame.__init__(self, master)
        self.set_defaults()
        self.fontheight = min([max([fontheight,10]),22])
        self.fontname = fontname
        try:
            self.font = (self.fontname,str(self.fontheight),'bold')
        except:
            self.font = ('SansSerif',str(self.fontheight),'bold')
        self.maxlines = min([max([maxlines,5]),25])
        self.defaultwidth = min([max([width,40]),80])
        self.root = master
        self.root.bind("<<finished>>",self.on_finished)
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.title("omxaudioplayer")
        self.root.resizable(False,False)
        for keysym in self.keybindings:
            self.root.bind(keysym,self.keyp_handler)
        self.grid()
        self.omxoptions = omxoptions
        self.autofinish = autofinish
        self.playlist = playlist
        self.autoplay = autoplay
        self.mode = mode
        self.status = 'stopped'
        self.omxprocess = None
        self.omxwatcher = None
        self.songpointer = 0
        self.listpointer = 0
        self.currentvolume = min([max([volume,-20]),4])
        self.changedvolume = tk.IntVar()
        self.changedvolume.set(volume)
        self.playcontent = tk.StringVar()
        self.playcontent.set(self.playstring)
        self.createwidgets()
        if self.playlist and self.autoplay:
            self.playsong(0)

    def set_defaults(self):
        self.playstring = '>'
        self.pausestring = '||'
        self.stopstring = '[]'
        self.rewstring = '←'
        self.fwdstring = '→'
        self.prevstring = '↑'
        self.nextstring = '↓'
        self.vchdelay = 0.05
        self.keybindings = ['<KeyPress-Down>','<KeyPress-Up>','<KeyPress-space>','<KeyPress-q>','<KeyPress-Escape>',
                            '<KeyPress-plus>','<KeyPress-minus>','<KeyPress-Left>','<KeyPress-Right>','<KeyPress-Return>',
                            '<KeyPress-KP_Enter>','<KeyPress-KP_Add>','<KeyPress-KP_Subtract>']

    def keyp_handler(self, event):
        if event.keysym in ['space','Return','KP_Enter']:
            self.playpause()
        elif event.keysym in ['q','Escape']:
            self.stop()
        elif event.keysym == 'Down':
            while self.nextbutton['state'] == tk.DISABLED:
                time.sleep(0.1)
            self.nextsong()
        elif event.keysym == 'Up':
            while self.prevbutton['state'] == tk.DISABLED:
                time.sleep(0.1)
            self.prevsong()
        elif event.keysym == 'Left':
            self.sendcommand('\x1b\x5b\x44')
        elif event.keysym == 'Right':
            self.sendcommand('\x1b\x5b\x43')
        else:
            av = 0
            if event.keysym in ['plus','KP_Add']:
                av = 1
            elif event.keysym in ['minus','KP_Subtract']:
                av = -1
            if av != 0:
                nv = self.changedvolume.get() + av
                if nv in range(-20,5):
                    self.changedvolume.set(nv)
                    self.vol_changed(nv) 


    def playsong(self, index):
        if not self.omxprocess:
            self.prevbutton['state'] = tk.DISABLED
            self.nextbutton['state'] = tk.DISABLED
            self.songpointer = index
            pargs = ['omxplayer', '--vol', str(self.currentvolume*300)] + self.omxoptions + [self.playlist[index]]
            self.omxprocess = subprocess.Popen(pargs,stdin=subprocess.PIPE,stdout=file('/dev/null','wa'))
            self.omxwatcher = threading.Timer(0,self.watch)
            self.omxwatcher.start()
            self.status = 'playing'
            self.playcontent.set(self.pausestring)
            selection = self.playlistwindow.curselection()
            if not selection or index != int(selection[0]):
                self.listpointer = index
                self.playlistwindow.selection_clear(0, len(self.playlist)-1)
                self.playlistwindow.selection_set(index)
            self.playlistwindow.see(index)
            time.sleep(0.3)
            self.prevbutton['state'] = tk.NORMAL
            self.nextbutton['state'] = tk.NORMAL

    def on_close(self):
        if self.omxprocess:
            self.status='closing'
            self.sendcommand('q')
            time.sleep(0.1)
            if self.omxprocess:
                try:
                    self.omxprocess.terminate()
                    time.sleep(0.1)
                except:
                    pass
                if self.omxprocess:
                    try:
                        self.omxprocess.kill()
                        time.sleep(0.1)
                    except:
                        pass
        self.root.destroy()

    def on_finished(self, *args):
        stat = self.status
        self.status = 'stopped'
        self.playcontent.set(self.playstring)
        if stat != 'finished':
            if self.songpointer == self.listpointer:
                self.nextsong()
            else:
                self.songpointer = self.listpointer
                self.playsong(self.songpointer)

    def watch(self):
        if self.omxprocess:
            try:
                dummy = self.omxprocess.wait()
            except:
                pass
        self.omxprocess = None
        if self.status != 'closing':
            self.root.event_generate("<<finished>>")

    def sendcommand(self, cmd):
        if self.omxprocess:
            try:
                self.omxprocess.stdin.write(cmd)
            except:
                pass

    def playpause(self):
        if self.status in ['stopped','finished']:
            self.songpointer = self.listpointer
            self.playsong(self.songpointer)

        elif self.status == 'paused':
            self.sendcommand('p')
            self.status = 'playing'
            self.playcontent.set(self.pausestring)

        elif self.status == 'playing':
            self.sendcommand('p')
            self.status = 'paused'
            self.playcontent.set(self.playstring)

    def stop(self,stat='finished'):
        if self.omxprocess:
            self.status = stat
            self.sendcommand('q')
        else:
            self.playcontent.set(self.playstring)
            self.status = 'stopped'

    def rewind(self):
        self.sendcommand('\x1b\x5b\x44')

    def forward(self):
        self.sendcommand('\x1b\x5b\x43')

    def prevsong(self):
        if self.listpointer != self.songpointer and self.status != 'stopped':
            self.stop('stopped')
        elif self.listpointer > 0:
            self.listpointer = self.listpointer - 1
            self.playlistwindow.selection_clear(0, len(self.playlist)-1)
            self.playlistwindow.selection_set(self.listpointer)
            if self.status == 'stopped':
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')

    def nextsong(self):
        if self.listpointer != self.songpointer and self.status != 'stopped':
            self.stop('stopped')
        elif self.listpointer < len(self.playlist)-1:
            self.listpointer = self.listpointer + 1
            self.playlistwindow.selection_clear(0, len(self.playlist)-1)
            self.playlistwindow.selection_set(self.listpointer)
            if self.status == 'stopped':
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')
        elif self.autofinish:
            self.on_close()

    def vol_changed(self, volume):
        vol = int(volume)
        if self.status != 'stopped':
            if vol > self.currentvolume:
                diff = vol - self.currentvolume
                self.currentvolume = vol
                for k in range(0,diff):
                    self.sendcommand('+')
                    time.sleep(self.vchdelay)

            elif vol < self.currentvolume:
                diff = self.currentvolume - vol
                self.currentvolume = vol
                for k in range(0,diff):
                    self.sendcommand('-')
                    time.sleep(self.vchdelay)
        else:
            self.currentvolume = vol
 
    def on_listbox_select(self,event):
        sel = self.playlistwindow.curselection()
        if sel:
            self.listpointer = int(sel[0])

    def on_listbox_double(self,event):
        self.on_listbox_select(event)
        if self.status != 'stopped':
            if self.songpointer == self.listpointer:
                self.stop()
                self.playsong(self.listpointer)
            else:
                self.stop('stopped')
        else:
            self.playsong(self.listpointer)

    def focus_out(self, event):
        self.root.focus_set()

    def createwidgets(self):
        if len(self.playlist) > self.maxlines:
            self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
            self.yScroll['width'] = int(self.yScroll['width']) + (self.fontheight-10)
            hg = self.maxlines
        else:
            hg = len(self.playlist)
        self.playlistwindow = tk.Listbox(self, takefocus=0, selectmode = 'single', width = self.defaultwidth, height = hg, font=self.font,activestyle='none',bg='#000', fg = '#ddd', selectbackground='#60c', selectforeground='#ffffd0')
        for url in self.playlist:
            song = url.split('/')[-1]
            self.playlistwindow.insert(tk.END, urllib.unquote(song).replace('%20',' '))
        self.playlistwindow.selection_set(self.songpointer)
        self.playlistwindow.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.playlistwindow.bind("<Double-Button-1>",self.on_listbox_double)
        self.playlistwindow.bind("<FocusIn>",self.focus_out)
        self.playlistwindow.grid(row=0,column=0,columnspan=7, sticky=tk.N+tk.S+tk.E+tk.W)
        if len(self.playlist) > self.maxlines:
            self.playlistwindow.configure(yscrollcommand=self.yScroll.set)
            self.yScroll['command'] = self.playlistwindow.yview
            self.yScroll.grid(row=0,column=7, sticky=tk.N+tk.S)
        self.playbutton = tk.Button(self, command=self.playpause, font=self.font, textvariable = self.playcontent, width = 3, justify = tk.CENTER)
        self.playbutton.grid(row=1,column=0)
        self.stopbutton = tk.Button(self, command=self.stop, font=self.font, text = self.stopstring, width = 3, justify = tk.CENTER)
        self.stopbutton.grid(row=1,column=1)

        self.prevbutton = tk.Button(self, command=self.rewind, font=self.font, text = self.rewstring, width = 3, justify = tk.CENTER)
        self.prevbutton.grid(row=1,column=2)
        self.nextbutton = tk.Button(self, command=self.forward, font=self.font, text = self.fwdstring, width = 3, justify = tk.CENTER)
        self.nextbutton.grid(row=1,column=3)

        self.prevbutton = tk.Button(self, command=self.prevsong, font=self.font, text = self.prevstring, width = 3, justify = tk.CENTER)
        self.prevbutton.grid(row=1,column=4)
        self.nextbutton = tk.Button(self, command=self.nextsong, font=self.font, text = self.nextstring, width = 3, justify = tk.CENTER)
        self.nextbutton.grid(row=1,column=5)
        self.volume = tk.Scale(self, command=self.vol_changed, font=self.font, length=str((self.fontheight-2)*(self.defaultwidth-30))+'p', from_ = -20, to=4, variable=self.changedvolume ,orient=tk.HORIZONTAL, resolution=1, showvalue=0)
        self.volume.grid(row=1,column=6)

# main script function

args = sys.argv
if len(args) > 2:
    mode = args[1]
    url = args[2]
    mimetype = ''

# media section: play audio, video, m3u playlists and streams

    if mode == 'av':
        mtflag = True
        if len(args) > 3:
            mimetype = args[3]
            if mimetypes and mimetype not in mimetypes:
                mtflag = False
        url_extension = url.lower().split('.')[-1]
        if url_extension in ['m3u','m3u8','pls'] and mtflag:
            audioonly, playlist = get_playlist(url,try_stream_as_audio)
            if playlist:
                if audioonly and useVLC:
                    os.execl("/usr/bin/vlc","vlc",url)
                elif audioonly and useAudioplayer:
                    if kill_omxplayer:
                        dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
                    root = tk.Tk()
                    player = omxaudioplayer(master=root, playlist=playlist,volume=defaultaudiovolume,omxoptions=omxaudiooptions,
                                            autofinish=autofinish,fontheight=fontheight,fontname=fontname,maxlines=maxlines,
                                            autoplay=autoplay,width=lwidth)
                    player.mainloop()
                else:
                    if audioonly:
                        options = omxaudiooptions
                    else:
                        options = omxoptions
                    if kill_omxplayer:
                        script = '#!/bin/bash\nkillall omxplayer.bin > /dev/null 2>&1\n'
                    else:
                        script = '#!/bin/bash\n'
                    for s in playlist:
                        if audioonly and omxplayer_in_terminal_for_audio:
                            script += 'echo "now playing: '+ urllib.unquote(s.split('/')[-1]) +'"\n'
                        script += 'omxplayer ' + get_opt(options) + ' "' + s + '" > /dev/null 2>&1\n'
                        
                    f = file(dldir+os.sep+'playall.sh','wb')
                    f.write(script)
                    f.close()
                    os.chmod(dldir+os.sep+'playall.sh',511)
                    if omxplayer_in_terminal_for_audio and audioonly:
                        os.execlp(preferred_terminal,preferred_terminal,"-e",dldir+os.sep+'playall.sh')
                    elif omxplayer_in_terminal_for_video and not audioonly:
                        os.execl("/usr/bin/xterm","xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",dldir+os.sep+'playall.sh')               
                    else:
                        os.execl(dldir+os.sep+'playall.sh','playall.sh')
            
        elif mtflag:
            url_valid = True
            if url.startswith('file://'):
                url = url.replace('file://','').replace('%20',' ')
                url = urllib.unquote(url)
                if not os.path.exists(url):
                    url_valid = False
            elif not url.startswith('http'):
                if not os.path.exists(url):
                    url_valid = False
            if url_valid:
                if url_extension in audioextensions or (try_stream_as_audio and not url_extension in videoextensions):
                    if useVLC:
                        os.execl("/usr/bin/vlc","vlc",url)
                    elif useAudioplayer:
                        if kill_omxplayer:
                            dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
                        root = tk.Tk()
                        player = omxaudioplayer(master=root, playlist=[url],volume=defaultaudiovolume,omxoptions=omxaudiooptions,
                                                autofinish=autofinish,fontheight=fontheight,fontname=fontname,maxlines=maxlines,
                                                autoplay=autoplay,width=lwidth)
                        player.mainloop()
                    else:
                        if kill_omxplayer:
                            dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
                        if omxplayer_in_terminal_for_audio:
                            pargs = [preferred_terminal,'-e','omxplayer'] + omxaudiooptions + [url]
                            os.execvp(preferred_terminal,pargs)
                        else:
                            pargs = ['omxplayer'] + omxaudiooptions + [url]
                            os.execvp('omxplayer',pargs)         
                            
                else:
                    if kill_omxplayer:
                        dummy = os.system('killall omxplayer.bin > /dev/null 2>&1')
                    options = omxoptions
                    if live_tv:
                        for lt in live_tv:
                            if url.startswith(lt):
                                options = omx_livetv_options
                                break
                    if omxplayer_in_terminal_for_video:
                        pargs = ["xterm","-fn","fixed","-fullscreen", "-maximized", "-bg", "black", "-fg", "black", "-e",'omxplayer']+options+[url]+['>', '/dev/null', '2>&1']
                        os.execv("/usr/bin/xterm",pargs)
                    else:
                        pargs = ['omxplayer'] + omxoptions + [url]
                        os.execvp('omxplayer',pargs)         
                        
# end of media section

# pdf section (download - if needed - and open pdf file)
    elif mode == 'pdf':
        if not (pdfprogpath and pdfprog):
            if os.path.exists('/usr/bin/xpdf'):
                pdfprogpath = '/usr/bin/xpdf'
                pdfprog = 'xpdf'
            else:
                pdfprogpath = '/usr/bin/mupdf'
                pdfprog = 'mupdf'
        go = False
        # option to open pdf as files from http://localhost instead of downloading them first
        if pdfpathreplacements and url.startswith('http://localhost'):
            for k,v in pdfpathreplacements.iteritems():
                if url.startswith(k):
                    nurl = url.replace(k,v)
                    if os.path.exists(urllib.unquote(nurl.replace('file://','').replace('%20',' ').split('#')[0])):
                        url = nurl
                    break
        if url.startswith('file://'):
            url = url.replace('file://','').replace('%20',' ')
            url = urllib.unquote(url)
            urll = url.split('#page=')
            f = urll[0]
            if os.path.exists(f):
                if len(urll) > 1:
                    page = urll[1].split('&')[0]
                    os.execv(pdfprogpath,[pdfprog]+pdfoptions+[f,page])
                else:
                    os.execv(pdfprogpath,[pdfprog]+pdfoptions+[f])
        else:
            if url.endswith('.pdf') or url.endswith('.PDF') or '.pdf#page' in url.lower():
                urll = url.split('#page=')
                fname = urllib.unquote(urll[0].split('/')[-1].replace('%20',' '))
                f = dldir+os.sep+urllib.unquote(urll[0].split('/')[-1].replace('%20',' '))
                if os.path.exists(f):
                    go = True
                else:
                    try:
                        fn,h = urllib.urlretrieve(urll[0],f)
                        go = True
                    except:
                        pass
            if go:
                if len(urll) > 1:
                    page = urll[1].split('&')[0]
                    os.execv(pdfprogpath,[pdfprog]+pdfoptions+[f,page])
                else:
                    os.execv(pdfprogpath,[pdfprog]+pdfoptions+[f])

# end of pdf section

# download section
    elif mode == 'dl':
        # download file using wget
        if show_download_in_terminal:
            os.execlp(preferred_terminal,preferred_terminal,'-e', "wget", "-P", dldir,"--no-clobber","--adjust-extension","--content-disposition",url,"--load-cookies",homedir + "/.web_cookie_jar","--no-check-certificate")
        else:
            os.execl("/usr/bin/wget", "wget", "-P", dldir,"--no-clobber","--adjust-extension","--content-disposition",url,"--load-cookies",homedir + "/.web_cookie_jar","--no-check-certificate")

#end of download section

# command execution section
    elif mode == 'cmd':
        cmd = ''
        formdata = False
        cpage = 'file:///homepage.html?cmd='
        url = url.decode('utf-8')
        if url.startswith('#'):
            cmd = url[1:]
        elif url.startswith(cpage):
            cmd = url.replace(cpage,'')
            if not cmd.startswith('formdata'):
                cmd = urllib.unquote_plus(cmd).replace('%20',' ')
        elif url.startswith('http://localhost') and ('/homepage.html?cmd=' in url):
            cmd = url.split('/homepage.html?cmd=')[1]
            if not cmd.startswith('formdata'):
                cmd = urllib.unquote_plus(cmd).replace('%20',' ')
        if cmd:
            if cmd.startswith('formdata'):
                formdata = True
                cmd = cmd.split('formdata')[1].strip()
                if '&' in cmd:
                    cmdargs = cmd.split('&')
                    for ind in range(0,len(cmdargs)):
                        if '=' in cmdargs[ind]:
                            cargl = cmdargs[ind].split('=')
                            if cargl[0].startswith('quoted') and cargl[1] != '':
                                cmdargs[ind] = " '" + urllib.unquote_plus(cargl[1]) + "'"
                            elif cargl[0].startswith('dquoted') and cargl[1] != '':
                                cmdargs[ind] = ' "' + urllib.unquote_plus(cargl[1]) + '"'
                            elif cargl[1] != '':
                                cmdargs[ind] = ' ' + urllib.unquote_plus(cargl[1])
                            else:
                                cmdargs[ind] = ''
                        else:
                            cmdargs[ind] = ' ' + urllib.unquote_plus(cmdargs[ind]).strip()
                    cmd = ''.join(cmdargs).strip()
                else:
                    cmd = urllib.unquote_plus(cmd).strip()
            cmdl = cmd.split(' ')
            if len(cmdl)>1 and cmdl[0] == 'sudo':
                realname = cmdl[1]
            else:
                realname = cmdl[0]
            desktop_app = False
            if check_desktop and '/' not in realname:
                if os.path.exists('/usr/share/applications/'+realname+'.desktop'):
                    desktop_app = True
            if desktop_app or (realname in direct_commands) or (formdata and not formdata_in_terminal):
                cmdline = cmd.encode('utf-8')
            else:
                cmdline = preferred_terminal + ' -e '+cmd.encode('utf-8')
            if run_as_script:
                dmcount = 0
                scpath = dldir+os.sep+'temp'+str(dmcount)+'.sh'
                while os.path.exists(scpath):
                    dmcount += 1
                    scpath = dldir+os.sep+'temp'+str(dmcount)+'.sh'
                f = file(scpath,'wb')
                f.write('#!/bin/bash\n'+cmdline+'\nrm '+scpath+'\n')
                f.close()
                os.chmod(scpath,511)
                os.execl(scpath,scpath)
            else:
                try:
                    dummy = os.system(cmdline)
                except:
                    pass
# end of command execution section

# web video section (HTML5 and all websites supported by youtube-dl)
    elif mode == 'ytdl' and os.path.exists('/usr/bin/youtube-dl'): #youtube and HTML5 videos
        if html5_first:
            tags = video_tag_extractor(url)
            if tags: #extract embedded html5 video
                play_html5(tags)
            else:
                yta = ['youtube-dl', '-g']+youtube_dl_options+[url]
                yt = subprocess.Popen(yta,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (res,err) = yt.communicate()
                if res and not err:
                    play_ytdl(res)
        else:
            yta = ['youtube-dl', '-g']+youtube_dl_options+[url]
            yt = subprocess.Popen(yta,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (res,err) = yt.communicate()
            if res and not err:
                play_ytdl(res)
            else:
                tags = video_tag_extractor(url)
                if tags: #extract embedded html5 video
                    play_html5(tags)

# end of web video section
