#!/usr/bin/env python3

"""
Make your hackerspace a XMPP buddy.
"""
from optparse import OptionParser
import sleekxmpp


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

    opts, args = optp.parse_args()
