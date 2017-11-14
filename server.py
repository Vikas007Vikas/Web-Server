import socket
import datetime

port = input("PORT: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
try:
    s.bind((host, port))
except:
    print "Socket creation Error"
    exit(0)
s.listen(15)

print 'Server is up and listening....'

while True:
	try:
		conn,addr = s.accept()
	except:
		s.close()
	print 'Got connection from', addr

	while True:
		try:
			data = conn.recv(1024)
		except:
			conn.close()
			print 'connection closed to the client'
			break
		if not data:
			continue
		div = data.split()
		#print div
		if div[0] == 'GET':
			fname = div[1]
			if fname == '/':
				fname += 'index.html'
			fname = fname[1:]
			#print fname
			try:
				f = open(fname,'rb')
				content = f.read()
				#print content
				#conn.send('\nHTTP/1.1 200 OK\n\n')
				nowtime = datetime.datetime.now()
				frst_header = 'HTTP/1.1 200 OK'
				header_info = {
					"Date": nowtime.strftime("%Y-%m-%d %H:%M"),
					"Content-Length": len(content),
					"Keep-Alive": "timeout=%d,max=%d" %(10,100),
					"Connection": "Keep-Alive",
					"Content-Type": "text/html;text/css"
				} 
				following_header = "\r\n".join("%s:%s" % (item, header_info[item]) for item in header_info)
				print "following_header:", following_header
				conn.send("%s\r\n%s\r\n\r\n" %(frst_header, following_header))
				conn.send(content)
				conn.close()
			except IOError:
				conn.send('\nHTTP/1.1 200 OK\n\n')
				content = '<!DOCTYPE html>\n<html>\n\t<head>404 Page Not Found</head>\n\t<body>OK!</body>\n</html>\n\n'
				#print content
				conn.send(content)
				conn.close()

