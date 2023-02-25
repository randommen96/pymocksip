#!/usr/bin python3
import socket
import sys
import re

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 5060)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

while True:
    print('\nwaiting to receive message', file=sys.stderr)
    data, address = sock.recvfrom(4096)

    print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
    print(data, file=sys.stderr)

    data = data.decode('UTF-8')

    if data:
        matches = re.findall("(.+?):(.+)",data);
        print("Matches: "),len(matches);
        rtnmsg = "SIP/2.0 200 OK\r\n";
        first = True;
        keep = ("call-id","cseq","via","from","content-length");
        for match in matches:
            if first == False:
                print("Match "),match[0];
                if match[0] == "To":
                    rtnmsg += match[0]+": "+match[1].replace("\r","")+";tag=faketag\r\n";

                else:
                    rtnmsg += match[0]+": "+match[1].replace("\r","")+"\r\n";
            else:
                first = False;
    print("==== Sending ====", file=sys.stderr)
    print(rtnmsg, file=sys.stderr)
    rtnmsg = rtnmsg.encode('UTF-8')
    sent = sock.sendto(rtnmsg, address)
    print('sent %s bytes back to %s' % (sent, address), file=sys.stderr)
