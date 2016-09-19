#!/usr/bin/env python
# coding=utf-8
import socket
import threading
import main
import time
import sys
import math
import json

def xstr(s):
    if s is None:
        return ''
    return str(s)

def listenToServer():
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
                    components = l.split()
                    sender = components[0][1:].split("!")[0]
                    msg = " ".join(components[3:])
                    msg = msg[1:]
                    callback(sender, msg)

def callback(sender, msg):
    msg = str(msg)
    print (msg)

    sendmsg("aoeu", sender)

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
NICK = "Ruokabot"
CHAN = "#ro-bot"
REALNAME = "Revolin ruokabot"

sock.connect(("irc.inet.fi", 6667))
sendRaw("NICK %s" % NICK)
sendRaw("USER %s 8 * : %s" % (NICK, REALNAME))
time.sleep(1)

listenToServer()
