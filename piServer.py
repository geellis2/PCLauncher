import sys
import socket
from subprocess import call
#declare self as host, an arbitrary port and a boolean value
HOST = ''
PORT = 56231
cont = 1

def connectToPC(data):
    count = 0
    if len(sys.argv) < 2:
        print "usage: ", sys.argv[0], " [IP or DNS address of PC]"
        print "need IP or DNS for booting to Windows or checking status"
        return "Connect Failed"
    #try 10 times because of boot time(this is probably still overkill)
    #there is probably a better way to do this.
    while count < 10:   
        PCHOST = sys.argv[1]
        PCPORT = 55543
        print count
        #create a socket
        try:
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #now we connect the socket to the ip we want to talk to.
            s1.connect((PCHOST, PCPORT))
            s1.sendall(data)
            #recieve data now?
            data = s1.recv(1024)
            s1.close()
            count = 50
            data = "Booted to Windows"
        except:
            #if the PC hasn't booted yet
            count = count + 1
    if count < 50 :
        data = "not connected"
    return data

def MagicPacket(packet):
    import socket
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sends a wake on lan packet to broadcast
    #small amount of error checking
    if len(packet) != 13:
        return;
    hexed = chr(int(packet[:2], 16)) + chr(int(packet[2:4], 16)) + chr(int(packet[4:6], 16)) + chr(int(packet[6:8], 16)) + chr(int(packet[8:10], 16)) + chr(int(packet[10:12], 16))
    #^^there has to be a better way... for now, this should work but there's no error checking...
    s.sendto('\xff'*6+ hexed*16, ('<broadcast>', 9))
    s.close()
    print "Attempted to wake host"


while cont == 1 :
    #set up socket to listen for commands
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    #print some useful info if run in terminal
    print 'Connected to by:', addr
    #start recieving data
    while 1:
        data = conn.recv(1024)
        if not data: break
        #conn.sendall(data)
        #this will send magic packet when asked
        if 'send magic packet to ' in data:
            data = data[20:]
            MagicPacket(data)
            data = 'packet sent'
        if 'start windows on ' in data:
            data = data[17:]
            MagicPacket('start widows') 
            #connect to PC, then ask it to
            data = connectToPC(data)
            #boot_to_windows
            print data
        if data == 'get status' :
            #connect to PC and ask it to identify self
            data = connectToPC(data)
            #data = 'running OS unknown'	
            print data
        #shuts down host program
        if data == 'quit' :
            cont = 0
        conn.sendall(data)
    s.close()
    conn.close()


