#Server side of file transfer using TLS
#Load Server Certificate to be shared via TLS handshake to client
#Create server side socket to receive file transfer and write to  file
#Allow up to 5 concurrent connections to server using threads
#Receive data and write to file then close file.
import socket, ssl
import threading

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="serverCertificate/server.crt", keyfile="serverCertificate/serverPriv.key")
#SSL version 2, 3 are insecure so they have been blocked
context.options |= ssl.OP_NO_SSLv2
context.options |= ssl.OP_NO_SSLv3

#create socket object
bSocket = socket.socket()
#bind host name to socket on pot number
bSocket.bind(('localhost', 555))
#socket listening for up to 5 connections
bSocket.listen(5)

def deal_with_client(stream, f):
	print('-----------------------------------------\n')
	while True:
		#read from stream and store
		data = stream.recv(1024)
		if not data:
			break
		else:
			#write data from stream.recv(..) to file
			f.write(data)
	print('End Of File received, closing connection...')
	print('-----------------------------------------\n')
	f.close()
index = 1

while True:
	#accept connection, newSocket sends/receives data. fromaddr is client address
	newSocket, fromaddr = bSocket.accept()
	#wrap accepted port with ssl protocol
	stream = context.wrap_socket(newSocket, server_side=True)
	#open file to write data to
	f = open('decrypted#' + str(index), 'wb')
	index +=1
	#Prints IP address of Client
	print("'Connection established from " + str(fromaddr))
	try:
		#initalise thread to run deal_with_client(..) function
		p1 = threading.Thread(target=deal_with_client, args=(stream, f))
		#start thread
		p1.start()
	except KeyboardInterrupt:
        		break
	except Exception:
			print('\n Error in handling client\n')
			break
print('\n-----------------------------------------')
print('Server shutting down...\n')
