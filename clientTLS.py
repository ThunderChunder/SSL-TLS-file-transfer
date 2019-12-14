#Client side file transfer using TLS to Server
#Create a socket for TCP packets to IPV4 addresses and wrap in TLS context.
#Load Root certificate to verify server Certificate is authentic
#Once connection is establised send file data until entirely sent then close connection.
import socket, ssl, pprint
import os, time

host = 'localhost'
portNumb = 555
flag = 1
fileName = 'Forest_Lizard.jpg'
fileToSend = open(fileName, 'rb');
data = fileToSend.read(1024)
try: 
	#create socket to handle TCP packets from IPV4 addresses
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#custom security settings:
	#context is TLS protocol
	context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	#certificate is required
	context.verify_mode = ssl.CERT_REQUIRED
	#Do not check host name matches since cert does not match domain name
	context.check_hostname = False
	#load CArsa.crt to verify server.crt is authentic
	context.load_verify_locations("CACertificate/CArsa.crt")

	#SSL version 2, 3 are insecure so they have been blocked
	context.options |= ssl.OP_NO_SSLv2
	context.options |= ssl.OP_NO_SSLv3

	#wrap soc in tls to ensure certificate is verified and used
	sslConn = context.wrap_socket(soc, server_hostname=host) 
	#connect to server via TCP on portNumb

	sslConn.connect((host, portNumb))

	#ssl.match_hostname(sslConn.getpeercert(), host)

except Exception as e:
	print(e)
	flag = 0
while data and flag == 1:
	try:
		#send data to bound host
		sslConn.send(data)
		#read remaining bytes until EOF
		data = fileToSend.read(1024)
	except Exception as e:
		print(e)
		break
#close connection to server
fileToSend.close()
print('File '+fileName + ' sending complete')