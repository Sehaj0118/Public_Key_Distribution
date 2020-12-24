import socket
# 9060 is used for communicating with clients

#Credentials of Clients
PU_keyA = 182106040449176377254583258871575511
PU_keyB = 154234236513598500833278601624812369

#Credentials of PKDA
PR_key = 154234236513598500833278601624812277
PU_key = 182106040449176377254583258871575613
mod = 471884124816129030187874111122712531 

if __name__ == "__main__":
	soc = socket.socket()          
	print ("Socket has been created")

	soc.bind(('', 9060))         
	print ("Socket is now binded to",str(9060)) 
	
	soc.listen()      
	print ("socket is now listening")            
	
	# Establish connection with A. 
	import RSA
	import datetime

	con, address = soc.accept()

	print ('Client A is now connected.... ')  	
	req = (con.recv(1024).decode()).split("||")
	request_list = req[0]

	time = datetime.datetime.strptime(req[1], '%Y-%m-%d %H:%M:%S.%f')
	receive_time = time
	time= datetime.datetime.now()
	diff= time - receive_time 
	if(diff.total_seconds() <= 1):
		print("Message is received within time")
	else:
		print("Message didn't reach in time")

	print ('Sending public key of B')
	time = datetime.datetime.now()
	
	print('Message being sent: ', str(PU_keyB) + '||' + req[0] + '||' + str(time))
	con.send(str.encode(RSA.encrypt(str(PU_keyB) + '||' + req[0] + '||' + str(time), mod, PR_key)))
	# Close the connection with the A
	con.close()
	#--------------------------------------
	# Establish connection with B. 
	con, address = soc.accept()      
	print ('Successfully connected to client B')  	
	req = con.recv(1024).decode()
	request_list = (req).split("||")[0]
	print ('Public key of client A is being sent')
	con.send(str.encode(RSA.encrypt(str(PU_keyA) + '||' + req, mod, PR_key)))
	# Close the connection with the A
	con.close()

	soc.close()