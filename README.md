# How to install

Install virtualenvwrapper and python3

Then create a virtualenv:
   
    git clone https://github.com/uwekamper/pysdltest
    cd pysdltest 
    mkvirtualenv -a . -p /path/to/your/python3 pysdltest

When you want to start working on it

    workon pysdltest

You might need to install FFMpeg and the SDL2 libs for your operating system. See SDL2 docs on how to install.

# Resources not include

The files that are loaded from the resources folder are not include. You need to find your own images that work for you.

# How to download videos for testvid.py

youtube-dl https://vimeo.com/channels/beeple/54969949 -F

Then select something that suit yout, e.g.

youtube-dl https://vimeo.com/channels/beeple/54969949 -f http-720p
