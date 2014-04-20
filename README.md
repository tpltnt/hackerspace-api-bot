hackerspace-api-bot
===================

Bridge your hackerspace to [XMPP](https://en.wikipedia.org/wiki/XMPP). 
The bot will be online when your hackerspace is open, and offline if 
the space is closed.

bot installation (Debian)
-------------------------
* create directory: ```$ mkdir /etc/hsbot && chmod 755 /etc/hsbot```
* install Python: ```# apt-get install virtualenv python3```
* create bot environment: ```$ virtualenv --python=/usr/bin/python3 bot-env```
* activate it: ```$ source bot-env/bin/activate```
* install dependencies: ```$ pip-3.2 install requests && pip-3.2 install sleekxmpp```
* install daemontools: ```# apt-get install daemontools daemontools-run```
  * create config /etc/init/svscan.conf:
```
start on runlevel [12345]
stop on runlevel [^12345]
respawn
exec /usr/bin/svscanboot
```
  * *or* add this line to /etc/rc.local: ```bash -cf '/usr/bin/svscanboot &'```
* create file "/etc/hsbot/run"
```
#!/bin/sh
cd /etc/hsbot
exec setuidgid hsbot /bin/bash -c "source bot-env/bin/activate && ./bot.py -c CONFIG
```
* add a dedicated user: ```adduser --shell /bin/bash --disabled-password hsbot```
* adjust file permissions and ownership: ```# chmod 755 /etc/hsbot/run && chown -R hsbot:hsbot /etc/hsbot```
* create hsbot service in daemontools: ```# ln -s /etc/hsbot /etc/service/hsbot```

references
----------
* [daemontools](http://cr.yp.to/daemontools.html)
* [hackerspace API](http://spaceapi.net/)
* [SleekXMPP](http://sleekxmpp.com/)
* [requests](http://docs.python-requests.org/)
* [virtualenv](http://www.virtualenv.org)
