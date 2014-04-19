#!/usr/bin/env python3

"""
Make your hackerspace a XMPP buddy.
"""
from configparser import ConfigParser
from optparse import OptionParser
import logging
import requests
import sleekxmpp
import sys
import time
import urllib.request
import json

class HackerspaceApiBot(sleekxmpp.ClientXMPP):
    """
    A SleekXMPP based bot that will mimic the on-/offline 
    status of a given hackerspace. It also authorizes other
    automatically to allow status tracking.
    """
    def __init__(self, jid, password):
        super(HackerspaceApiBot, self).__init__(jid, password, plugin_whitelist=['xep_0199'])
        self.auto_authorize = True
        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence("hello world")
        self.get_roster()

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()
    # JID and password as arguments
    optp.add_option("-c", "--config", dest="config",
                    help="configuration file (ini-format) to use")
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="XMPP account password to use")
    optp.add_option("-u", "--url", dest="jsonurl",
                    help="URL to load hackerspace API json file from")

    opts, args = optp.parse_args()

    
    if None == opts.config:
        if None == opts.jid:
            print("no JID given ...")
            sys.exit(1)
        if None == opts.jsonurl:
            print("no URL given ...")
            sys.exit(1)
        if None == opts.password:
            print("no XMPP account password given ...")
            sys.exit(1)
    else:
        configfile = ConfigParser()
        configfile.read(opts.config)
        if 1 != len(configfile.sections()):
            print("can not process more than on section/hackerspace currently ...")
            sys.exit(2)
        # iterate over all sections (hackerspace configs)
        for section in configfile:
            # skip default
            if "DEFAULT" == section:
                continue
            print("using \"" + section + "\" configuration")
            opts.jid = configfile[section]['jid']
            opts.jsonurl = configfile[section]['url']
            opts.password = configfile[section]['password']

    # set up logging (for debugging)
    #logging.basicConfig(level=logging.INFO,
    #                    format='%(levelname)-8s %(message)s')

    # just run in an endless loop and check from time to time
    while(True):
        try:
            jsondata = requests.get(opts.jsonurl)
        except AttributeError:
            print("reading from URL failed")
            continue
        if 200 != jsondata.status_code:
            print("reading from URL failed")
            continue
        spacestate = json.loads(jsondata.text)
        print("spacestate: " + str(spacestate['open']))
        if spacestate['open']:
            # validate TLS Certificates
            #xmpp.ca_certs = "path/to/ca/cert"
            # set up the bot
            xmpp = HackerspaceApiBot(opts.jid, opts.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data Forms
            xmpp.register_plugin('xep_0060') # PubSub
            xmpp.register_plugin('xep_0199') # XMPP Ping
            # connect to server and set status
            if xmpp.connect(use_tls=True, use_ssl=False):
                xmpp.process(block=True)
                print("going online ...")
            else:
                print("unable to connect to server")
        # wait 5 minutes before checking again
        time.sleep(5*60)
