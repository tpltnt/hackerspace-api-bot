#!/usr/bin/env python3

"""
Make your hackerspace a XMPP buddy.
"""
from optparse import OptionParser
import sleekxmpp
import time
import urllib
import json

class HackerspaceApiBot(sleekxmpp.ClientXMPP):
    """
    A SleekXMPP based bot that will mimic the on-/offline 
    status of a given hackerspace.
    """
    def __init__(self, jid, password):
        super(HackerspaceApiBot, self).__init__(jid, password)
        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence("hello world")
        self.get_roster()

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()
    # JID and password as arguments
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-u", "--url", dest="jsonurl",
                    help="URL to load hackerspace API json file from")

    opts, args = optp.parse_args()

    # just run in an endless loop
    while(True):
        spacestate = json.load(urllib.urlopen(opts.jsonurl))
        if spacestate['open']:
            # set up the bot
            xmpp = HackerspaceApiBot(opts.jid, opts.password)
            xmpp.register_plugin('xep_0199') # XMPP Ping
            # connect to server and set status
            if xmpp.connect():
                xmpp.process(block=True)
                print("going online ...")
            else:
                print("unable to connect to server")
        time.sleep(60)
