#!/usr/bin/env python3

"""
Make your hackerspace a XMPP buddy.
"""

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
