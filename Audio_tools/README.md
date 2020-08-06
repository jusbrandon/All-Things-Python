# Summary 
Simple Generic class which utilizes youtube-dl as its core, 
link can be found [here](https://github.com/ytdl-org/youtube-dl) for its original source
# Installation
```
cd Audio_tools
pipenv install  # To install any packages used in the program
```
####Windows Requirement

Download the [youtube-dl file](https://yt-dl.org/latest/youtube-dl.exe) (This file can be placed anywhere of your choosing
except for **C:\Windows\System32**! and download [ libav-11.3-win64.7z](http://builds.libav.org/windows/release-gpl/). 
and take note of its location as it needed for the program to work. 

Both file location should be included
in you **PATH**. Including just the directory that contains your "youtube-dl.exe" file and everything under "/win64/usr/bin"
which you can get by extracted the libav-11.3 zipped file

For another exaplanation please refer to this [Guide](https://stackoverflow.com/questions/30770155/ffprobe-or-avprobe-not-found-please-install-one/38878753) 
by **Federico Alvarez**

If libav-11.3 does not work try and download the [FFMPEG](https://ffmpeg.zeranoe.com/builds/) and  include this in 
your **PATH**