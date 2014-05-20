import telnetlib
import time
from config import config


def getClients():
    print "Getting a list of clients."
    telnet.write("clientlist -times\n")
    clients = telnet.read_until("msg=ok")
    clients = clients.replace(" ", "\n")
    clients = clients.replace("\r", "")
    clients = clients.split("|")
    for i in range(0, len(clients)):
        try:
            if config["botname"] in clients[i]:
                clients.remove(clients[i])
            else:
                clients[i] = clients[i].split("\n")
                clients[i] = filter(None,clients[i])
        except IndexError:
           print "We've escaped the bounds of the loop. :O Skip it and we should be fine."
    return clients

def moveIdlers(clients):
    print "Checking for idlers."
    for i in range(0, len(clients)):
        if float(clients[i][5].strip("client_idle_time=")) > float(config["idle"])*60000:
            print "Moving user " + clients[i][3].replace("client_nickname=", "") + " to idle channel."
            telnet.write("clientmove clid="+clients[i][0].strip("clid=")+ " cid=13\n")
            telnet.read_until("msg=ok")
    print "Done checking for idlers."

print "TS3IdleBot"
print "http://www.github.com/rmgr\n"
print "Exit TS3IdleBot with CTRL + C."
print "Connecting to server " + config["host"]+ ":" + config["port"]
telnet = telnetlib.Telnet(config["host"],config["port"])
telnet.open(telnet.host, telnet.port)
telnet.write("login "+config["user"]+" "+config["pass"]+"\n")
telnet.read_until("msg=ok")
print "Connected successfully."

print "Using virtual server "+config["serverid"]
telnet.write("use sid="+config["serverid"] + "\n")
telnet.read_until("msg=ok")
print "Server selection successful."

print "Setting bot nickname as " + config["botname"] + "."
telnet.write("clientupdate client_nickname="+config["botname"]+"\n")
telnet.read_until("msg=ok")
print "Set successfully."

while True:
    try:
        clients = getClients()
        moveIdlers(clients)
        print "Sleeping for 5 minutes."
        time.sleep(300)
    except KeyboardInterrupt:
        print "Exiting TS3IdleBot"
        exit()
telnet.write("logout\n")
telnet.read_until("msg=ok")
telnet.close()
