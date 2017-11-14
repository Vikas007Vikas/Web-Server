import socket
import os
import datetime
import threading
import time

port = int(raw_input())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""

s.bind((host, port))
s.listen(5)
users={}
count={}
blacklist={}
authentication={}
recent_time={}
# authentication=False

class myThread(threading.Thread):
    def __init__(self,conn,addr):
        threading.Thread.__init__(self)
        self.conn=conn
        self.addr=addr
    def run(self):
        print "taking data"
        data = conn.recv(4096)
        print "data received"
        # if not data:
        #     break
        print "data: ",data
        if data[0]=='G' and data[1]=='E' and data[2]=='T':
            try:
                if not authentication[addr[0]]:
                    conn.send("HTTP/1.1 200 OK\r\n\r\n")
                    conn.send('<!DOCTYPE html><html><form action="" method="post" enctype="multipart/form-data"> ...<h2>Username </h2><input type="text" name="Username"><br><h2>Password</h2><input type="password" name="Password"><br><input type="submit" value="submit">\r\n')
                    # conn.close()
                else:
                    data=data.split()
                    data=data[1]
                    filename=data[1:]
                    f = open(filename,'rb')
                    data=f.read()
                    header_ok = "HTTP/1.1 200 OK"
                    header_info={
                		"Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                		"Content-Length": len(data),
                		"Keep-Alive": "timeout=%d,max=%d" %(10,100),
                		"Connection": "Keep-Alive",
                		"Content-Type": "text/html"
                    }
                    st=""
                    for i in header_info:
                        st=st+i+':'+str(header_info[i])+'\r\n'

                    print st
                    conn.send("%s\r\n%s\r\n\r\n" %(header_ok,st))
                    f.close()
                    f1 = open(filename,'rb')
                    l=f1.read(1024)
                    while l:
                        conn.send(l)
                        l=f1.read(1024)
                    f1.close()
                conn.close()
            # conn.close()
            except IOError:
                conn.send("HTTP/1.1 404 Not Found\r\n\r\n")
                conn.send("<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>")
                conn.close()

        elif data[0]=='P' and data[1]=='O' and data[2]=='S' and data[3]=='T':
            try:
                if not authentication[addr[0]]:
                    data=data.split('\r\n\r\n')
                    username=data[2].split('\r\n')[0]
                    password=data[3].split('\r\n')[0]
                    print username,password

                    if username not in users.keys():
                        users[username]=hash(password)
                        authentication[addr[0]]=True
                    else:
                        if users[username]==hash(password):
                            authentication[addr[0]]=True
                    conn.send("HTTP/1.1 200 OK\r\n\r\n")
                    print users
                    if not authentication[addr[0]]:
                        # conn.send("HTTP/1.1 200 OK\r\n\r\n")
                        conn.send('<!DOCTYPE html><html><h2>Authentication unsuccessful</h2></html>')
                        conn.send('<!DOCTYPE html><html><form action="" method="post" enctype="multipart/form-data"> ...<h2>Username </h2><input type="text" name="Username"><br><h2>Password</h2><input type="password" name="Password"><br><input type="submit" value="submit">\r\n')
                    else:
                        data=data[0].split()
                        data=data[1]
                        f=open(data[1:],"rb")
                        l=f.read(1024)
                        while l:
                            conn.send(l)
                            l=f.read(1024)
                        f.close()

                #POST request
                else:
                    data=data.split('\n\r\n')
                    print data[2]
                    fi=data[1].split(';')
                    fi=fi[2].split('\r\n')
                    fi=fi[0]
                    leng=len(fi)
                    filename=fi[11:len(fi)-1]
                    f=open(filename,'wb')
                    f.write(data[2])
                    f.close()

                    conn.send("HTTP/1.1 200 OK\r\n\r\n")
                    conn.send('<!DOCTYPE html><html><h2>File Uploaded</h2></html>')
                conn.close()
            except IOError:
                print count[addr[0]]
                if count[addr[0]]>2:
                    conn.send('HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n')
                conn.send("<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>")
                conn.close()

                # print "yes"
                # conn.send("HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>")
                # flag=1
                # conn.close()
            # conn.close()

while True:
    conn, addr = s.accept()
    present_time=time.time()
    if addr[0] in blacklist.keys() and present_time - blacklist[addr[0]] < 60:
        conn.close()
    else:
        if addr[0] in blacklist.keys():
            del blacklist[addr[0]]
        if addr[0] not in authentication:
            authentication[addr[0]]=False
        if addr[0] not in count:
            count[addr[0]]=1
            recent_time[addr[0]]=present_time
        else:
            if  present_time - recent_time[addr[0]] <= 5:
                count[addr[0]]+=1
            else:
                count[addr[0]]=1
            recent_time[addr[0]]=present_time
        if count[addr[0]]>10:
            data = conn.recv(4096)
            conn.send("HTTP/1.1 200 OK\r\n\r\n")
            conn.send('<!DOCTYPE html><html><h2>You are Blacklisted</h2><br><h2>Further Requests to server from this client are not accepted</h2></html>')
            blacklist[addr[0]]=present_time
            conn.close()
        else:
            thread=myThread(conn,addr)
            thread.start()


s.close()
