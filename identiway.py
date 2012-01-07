#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time

import sleekxmpp
from statusnet import StatusNet

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

class IdentiWay(sleekxmpp.ClientXMPP):
    """
    An XMPP client which acts as a simple gateway for Identica/StatusNet.
    """

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.api_conns = {}
        self.api_conns["reality@jabber.rootbash.com"] = StatusNet("http://identi.ca/api", "reality", "")

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        from_root = str(msg['from']).split('/')[0]
        if str(msg['body'])[0] == '/':
            tokens = msg['body'][1:].split()
            if tokens[0] == 'identify':
                print 'eh'
            elif tokens[0] == 'version': 
                msg.reply("You're currently talking to reality's super sexy xmpp bridge <3")
        else:
            try:
                self.api_conns[from_root].statuses_update(msg['body'], "reality's super sexy xmpp bridge <3")
                msg.reply("Message Sent.").send()
            except:
                msg.reply("You haven't registered your Identi.ca account. Type '/identify <api path> <username> <password>'.")

if __name__ == '__main__':
    xmpp = IdentiWay("realibridge@jabber.rootbash.com", "")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the pydns library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(threaded=False)
        print("Done")
    else:
        print("Unable to connect.")
