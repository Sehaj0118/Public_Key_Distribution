# first of all import the socket library 
import socket, RSA, datetime 
# 9060 for communication with Public Key Distribution Authority
# 10030 for communication with client A
# 7090 for exchanging replies with A
IP = '127.0.0.1'
#credentials of A
PU_key_A = -1
ID_A = -1

#credentials of B
PR_key = 117477982670003491925783789957926129
PU_key = 154234236513598500833278601624812369
mod = 471884124816129030187874111122712531

#credentials of PKDA
PU_key_pkda = 182106040449176377254583258871575613

if __name__ == "__main__":
	soc = socket.socket()          
	soc.bind(('', 10030))         
	 
	soc.listen()      
	print ("Socket is now listening")            
	
	con, address = soc.accept()      
	print ('Successful connection with A')  	
	reply_from_A = (RSA.decrypt(con.recv(1024).decode(), mod, PR_key)).split("||") #split into list of parameters sent
	ID_A = reply_from_A[0]
	nonceA = int(reply_from_A[1])

	print('Request from A is received')
	print ("ID of A: " + str(ID_A) + "  Nonce received: " + str(nonceA) + "\n\n")
	# Close the connection with the A 
	con.close() 
	soc.close()

	soc = socket.socket()          
	
	send_time = datetime.datetime.now()
	message = 'Key request for client A' + '||' + str(send_time)
	# Connection request of A
	soc.connect((IP, 9060))
	soc.send(str.encode(message))
	print("Message from client B to PKDA: " + message)

	reply = RSA.decrypt(soc.recv(1024).decode(), mod, PU_key_pkda).split("||")
	print("\n\n" + str(reply) + '\n\n')
	receive_time = datetime.datetime.strptime(reply[2], '%Y-%m-%d %H:%M:%S.%f') #formatting the date

	diff = receive_time - send_time
	if(diff.total_seconds() <= 1):
		print("message is received within time")
	else:
		print("message is NOT received within time")

	print("Message received from PKDA: "+ str(reply))
	print ('Public key of A received from PKDA: ', int(reply[0]))
	soc.close()

	# Connecting with A again
	soc = socket.socket()
	soc.connect((IP, 7090))
	# Talking to A
	print('Sending confirmation/reply to A...')

	import random
	nonceB = random.randint(10**10, 10**15)

	soc.send(RSA.encrypt(str(nonceA) + '||' + str(nonceB), mod, int(reply[0])).encode())

	reply_from_A = (RSA.decrypt(soc.recv(1024).decode(), mod, PR_key)).split("||")
	
	print ('\n Received confirmation of A', reply_from_A)

	if(int(reply_from_A[0]) == nonceB):
		print("Nonce sent is equal to nonce received")
	else:
		print("Nonce sent is not equal to nonce received")
		

	i=0
	while i < 3:
		print("Message from A: " + RSA.decrypt(soc.recv(1024).decode(), mod, PR_key))
		soc.send(RSA.encrypt('Got it ' + str(i + 1), mod, int(reply[0])).encode())
		i+=1
	soc.close()