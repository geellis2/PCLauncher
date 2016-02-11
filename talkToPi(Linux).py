import platform
import socket
from subprocess import call
#create a server node everytime a client node stops talking to it.
HOST = ''
PORT = 55543
cont = 1
while cont == 1 :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected to by:', addr
    while 1:
        data = conn.recv(1024)
        if not data: break
        print data
        #this will reboot to windows when asked
        #this probably creates security issues
        if data == 'start windows' :
            grubfile = open('/boot/grub/grub.cfg') 
            bootstr = ""
            for line in grubfile:
                if 'Windows' in line:
                    first = line.index("\'") + 1
                    second = line.index("\'", first, len(line)) 
                    bootstr = line[first:second]
        #searched through grubfile to find location of windows
            call(["sudo", "grub-reboot", bootstr])
            call(["sudo", "reboot"])
        if data == 'get status':
            data = platform.system()    #will retun Linux or Windows or OSX depending
        #shuts down host program
        if data == 'quit' :
            cont = 0

        conn.sendall(data)
    s.close()
    conn.close()


