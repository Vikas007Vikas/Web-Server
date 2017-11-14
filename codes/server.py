import socket
import os
import datetime
import hashlib
import time

port = int(raw_input())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""
s.bind((host, port))
s.listen(5)

def sendingdata(filename):
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

    conn.send("%s\r\n%s\r\n\r\n" %(header_ok,st))
    f.seek(0,0)
    l=f.read(1024)
    while l:
        conn.send(l)
        l=f.read(1024)
    f.close()
while True:
    conn, addr = s.accept()
    try:
        data = conn.recv(4096)
        print "data is :",data
        if data[0]=='G' and data[1]=='E' and data[2]=='T':
            print "data: ",data
            data=data.split()
            data=data[1]
            sendingdata(data[1:])
            print data[1:]
            conn.close()
        elif data[0]=='P' and data[1]=='O' and data[2]=='S' and data[3]=='T':
            print data
            data=data.split('\r\n\r\n')
            fi=data[1].split(';')
            fi=fi[2].split('\r\n')
            fi=fi[0]
            leng=len(fi)
            filename=fi[11:len(fi)-1]
            f=open(filename,'wb')
            finaldata=data[2].split('\r\n')
            # print finaldata
            f.write(finaldata[0])
            f.close()

            conn.send("HTTP/1.1 200 OK\r\n\r\n")
            conn.send('<!DOCTYPE html><html><h2>File Uploaded</h2></html>')
            conn.close()
    except IOError:
        conn.send('HTTP/1.1 404 Not Found\r\nContent-Type:text/html\r\n\r\n')
        conn.send("<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>")
        conn.close()
s.close()
