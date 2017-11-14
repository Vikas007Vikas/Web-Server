import socket
import sys

server_host=sys.argv[1]
server_port=int(sys.argv[2])
filename=sys.argv[3]
method=sys.argv[4]

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_host,server_port))
    if method=='GET':
        str1="GET /"+filename+" HTTP/1.1"+"\r\n"
        str2="Host: "+server_host+":"+str(server_port)+"\r\n"
        str3="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
        str4="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        str5="Accept-Language: en-US,en;q=0.5\r\n"
        str6="Accept-Encoding: gzip, deflate\r\n"
        str7="Connection: keep-alive\r\n"
        str8="Upgrade-Insecure-Requests: 1\r\n\r\n"

        data=str1+str2+str3+str4+str5+str6+str7+str8
        print data
        s.send(data)
    elif method=='POST':
        str1="POST /"+filename+" HTTP/1.1\r\n"
        str2="Host: "+server_host+":"+str(server_port)+"\r\n"
        str3="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
        str4="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        str5="Accept-Language: en-US,en;q=0.5\r\n"
        str6="Accept-Encoding: gzip, deflate\r\n"
        str8="Connection: keep-alive\r\n"
        str9="Upgrade-Insecure-Requests: 1\r\n\r\n"
        str7="Referer: http://"+server_host+":"+str(server_port)+"/"+filename+"\r\n"
        f=open(filename,'rb')
        str10='Content-Disposition: form-data; name="fileToUpload"; filename="'+filename+'"'+"\r\n"
        str11="Content-Type: text/plain\r\n\r\n"
        str12=f.read(4096)+"\r\n\r\n"
        data=str1+str2+str3+str4+str5+str6+str7+str8+str9+str10+str11+str12
        print data
        s.send(data)

except IOError:
    sys.exit(1)
ans=""
l=s.recv(1024)
while l:
    ans+=l
    l=s.recv(1024)
print ans
