#!/usr/bin/env python
# coding=utf-8
import socket
import threading
import main
import time
import sys
import math
import json
from menufile import *

def xstr(s):
    if s is None:
        return ''
    return unicode(s)

def listenToServer(menu):
    data = []
    while True:
        chunk = sock.recv(1024)
        if chunk == '':
            raise RuntimeError("connection lost")
        data.append(chunk)
        lines = b''.join(data).decode("UTF-8").split("\r\n")
        if data[-2:-1] != "\r\n":
            data = [lines[-1].encode("UTF-8")]
            lines = lines[:-1]
        else:
            data = []
        for l in lines:
            if l.startswith("PING"):
                sendRaw("PONG :" + l[6:])
            else:
                if l.split()[1] == "001":
                    sendRaw("MODE %s :+B" % NICK)
                else:
                    callback(l, menu)

def callback(l, menu):
    components = l.split()
    print (components)
    user = components[0][1:].split("!")[0]
    src = components[2]
    msg = " ".join(components[3:])
    msg = msg[1:]
    print (msg)

    # From here on is the custom part
    if len(msg) < 2:
        return
    if msg[0] == "!":
        delay = 1.2  # seconds between messages
        cmd = msg[1:].split()
        # always
        if cmd[0] == "help":
            if src == NICK:
                src = user
            sendmsg("Commands (q=query only):", src)
            sendmsg("q" + " "*2 + "!menu", src)
            sendmsg(" "*5 + "Responds with a list of restaurants used to fetch menus", src)
            sendmsg("q" + " "*2 + "!menu <restaurant>", src)
            sendmsg(" "*5 + "Responds with todays menu of restaurant. Restaurant name is a caps insensitive substring of actual name (!menu * = all menus)", src)

        # only in private querys
        if src == NICK:
            if cmd[0] == "menu":
                rest = menu.hae_menu_json()["restaurants"]
                if len(cmd) == 1:
                    sendmsg(unicode("Select a restaurant from the list: " + ", ".join(i["name"] for i in rest)) , user)
                elif len(cmd) >= 2:
                    if cmd[1] == "*":
                        for i in rest:
                            sendmsg(unicode(i["name"]), user)
                            time.sleep(delay)

                            options = {}
                            for j in i["menus"][0]["meals"]:
                                name = j["name"]
                                options[name] = []
                                for x in j["contents"]:
                                    options[name].append(x["name"])
                            for o in options:
                                sendmsg(unicode(o + ": " + ", ".join(options[o])), user)
                                time.sleep(delay)
                    else:
                        found = False
                        for i in rest:
                            if " ".join(cmd[1:]).lower() in i["name"].lower():
                                found = True
                                options = {};
                                for j in i["menus"][0]["meals"]:
                                    name = j["name"]
                                    options[name] = []
                                    for x in j["contents"]:
                                        options[name].append(x["name"])
                                for o in options:
                                    sendmsg(unicode(o + ": " + ", ".join(options[o])), user)
                                    time.sleep(delay)
                                break
                        if not found:
                            sendmsg("Restaurant could not be found", user)
        # only in channels
        else:
            pass

def sendmsg(msg, to):
    msgl = xstr(msg).split("\n")
    for m in msgl:
        for i in [m[j*400:(j+1)*400] if (len(m) > (j+1)*400) else m[j*400:] for j in range(0, math.floor(len(m)/400.0) + 1)]:
            sendRaw("%s %s :%s" % ("PRIVMSG", to, i))

def sendRaw(msg):
    totalsent = 0
    ba = (msg+"\r\n").encode('UTF-8')
    while totalsent < len(ba):
        sent = sock.send(ba[totalsent:])
        if sent == 0:
            raise RuntimeError("connection lost")
        totalsent += sent

receiver = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
NICK = "Murkinapurkki"
CHANS = ["#ro-bot", "#tut-ruoka"]
REALNAME = "Revol-Bot"
menu = Menu()

sock.connect(("irc.cc.tut.fi", 6667))
sendRaw("NICK %s" % NICK)
sendRaw("USER %s 0 * : %s" % (NICK, REALNAME))
for i in CHANS:
    sendRaw("JOIN %s" % i)

listenToServer(menu)
