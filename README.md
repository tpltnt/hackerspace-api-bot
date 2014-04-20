hackerspace-api-bot
===================

Bridge your hackerspace to XMPP. The bot will be online when 
your hackerspace is open, and offline if the space is closed.

bot installation (Debian)
-------------------------
* create directory: ```$ mkdir /etc/hackerspace-api-bot```
* install Python: ```# apt-get install virtualenv python3```
* create bot environment: ```$ virtualenv --python=/usr/bin/python3 bot-env```
* activate it: ```$ source bot-env/bin/activate```
* install dependencies: ```$ pip-3.2 install requests && pip-3.2 install sleekxmpp```
* install daemontools: ```# apt-get install daemontools```
  * create config /etc/init/svscan.conf:
```
start on runlevel [12345]
stop on runlevel [^12345]
respawn
exec /command/svscanboot
```

references
----------
* [daemontools](http://cr.yp.to/daemontools.html)
* [hackerspace API](http://spaceapi.net/)
* [SleekXMPP](http://sleekxmpp.com/)
* [requests](http://docs.python-requests.org/)
* [virtualenv](http://www.virtualenv.org)
