#!/usr/bin/env python
import socket
import curl
import os
import argparse
import time

def showBanner():
                                  
    print "__   __    _     ____   _____ "
    print "\ \ / /   / \   |  _ \ |  ___|"
    print " \ V /   / _ \  | |_) || |_   "
    print "  | |   / ___ \ |  __/ |  _|  "
    print "  |_|  /_/   \_\|_|    |_|    "
    print "                              "





def checkPort(target,portnum, pName):
    """ Return true if the port is open, false otherwise """
    #Todo/Extra: Run silently and just return True/False
    #            Too many false results displayed
    sock = socket.socket()
    try:
        sock.connect((target, portnum))
        print "\n\033[92mPort: %d OPEN --> %s \033[0m" % (portnum, pName) #prints in green colour
        return True
    except socket.error, e:
        return False
    return False

def checkURL(url):
    """ Return the status code returned from the web server, False if no success at all """
    #Todo/Extra: only show successes, or better still, return the list
    #and let the caller decide what to do
    c=curl.Curl()
    response=c.get(url)
    code=c.info()["http-code"] #returns the code 200 or 404 I think
    if code!=404:				#200 meaning it works (I think)
        print "!!!",
    	print "Request for %s gives a code of %d"%(url,code)

    return 


def urlDirForce(root):
    """ Tries a standard list of common web directories to see if any exost on the target fromt he given root URL """


#dirb <url_base> <url_base> [<wordlist_file(s)>] [options]
    #List of dirs to try
    dirs=["admin", "administrator", "backup", "config",
          "cpanel", "data", "images", "panel", "proxy", "staff",
          "uploads", "upload", "user", "users", "webmaster", "webhp"]

    #Take off any white space from the root given
    root=root.strip()

    #Check the root starts with http://
    if not root.lower().startswith("http://"):
        root="http://"+root
    
    #Make sure it ends with /
    if root[-1]!="/":
        root=root+"/"


    #Now run the check for every dir
    for i in dirs:
        checkURL(root+i)
       
    return 


def portScan(target):
    """ Returns a list of open ports from the range 1-100 on the target """
    #TODO/Extra: Update port list to cover most common rather than
    #first 100
    fname = open("commonPorts.txt")
    p = []
    n = []
    for line in fname.readlines():
    	portNum = line.split('\t')
    	p.append(portNum[0])
    	n.append(portNum[1])
    print "Scanning now..."
    time.sleep(1)
    counter = 0
    for ports in p:
    	checkPort(target, int(ports), n[counter])
    	counter+=1

def checkAnonFTP(target,port=21):
    """ Returns True if the target appears to be running an anonymous FTP service. False otherwise. Defaults to checking on port 21 """
    s=socket.socket()
    s.connect((target,port))
    data=s.recv(100)

    s.send("USER anonymous\n")
    data=s.recv(100)

    s.send("PASS anonymous\n")
    data=s.recv(100)

    s.close()
    if data.startswith("230"):
        print "Anonymous FTP enabled"
        return True
    return False

def enumLocalUsers():
    sers=[]
    f=open("/etc/passwd")
    for l in f:
        print l.split(":")[0]
        #split each element by the colon, as appears in te passwd file

def findSetUID():
    #TODO/URGENT: Fix this
    #Hmmm, this just shows the executables, but we need the ones with
    #setUID
    os.system("find / -perm -4000 -user root -type f -print")
    #  find 
    #  / root
    # -perm (permission) -4000 (set to 4000 [root code])
    # -type f (says the type we're looking for are files)
    # -print (print out the results) 
        
def setTarget():
    return raw_input("Enter target IP/URL: ")

if __name__=="__main__":
    option=" "
    target=None
    showBanner()
    while not option[0] in ["q","Q"]:
        print "\nTarget: %s"%str(target)
        print "\n1. Set target"
        if target!=None:
            print "2. Port scan target (most common ports)"
            print "3. URL directory brute-force"
            print "4. Test for anonymous FTP"
        print "5. Enumerate local users"
        print "6. Find local setuid files"
        print "Q. Quit"
        option=raw_input("\nChoose an option: ")
        if option[0] == "1":
            target=setTarget()
        elif option[0] == "2":
            portScan(target)
        elif option[0] == "3":
            urlDirForce(target)
        elif option[0] == "4":
            checkAnonFTP(target)
        elif option[0] == "5":
            enumLocalUsers()
        elif option[0] == "6":
            findSetUID()
        elif option[0] in ["Q","q"]:
            break
        else:
            print "Unknown option\n\n"
            
    
