#import statements for socket and RSA
import socket
import RSA
#importing datetime for sending timestamps
import datetime
# import gmpy2
# 9060 for communication with Public Key Distribution Authority
# 10030 for communication with client B
# 7090 for exchanging replies with B

IP = '127.0.0.1'
#credentials for the client A (updated) 
PU_key = 182106040449176377254583258871575511
PR_key= 710464149512386391
mod = 471884124816129030187874111122712531
id_A = 1

#credentials for PKDA
PU_key_pkda = 182106040449176377254583258871575613

#credentials of client B not known

if __name__ == "__main__":
    soc = socket.socket()
    t1 = datetime.datetime.now()
    soc.connect((IP,9060))
    msg = "Key request for client B" +  "||" + str(t1)
    print("Message from client A to PKDA: " + msg)
    soc.send(str.encode(msg))
    reply = soc.recv(1024).decode()
    reply = (RSA.decrypt(reply, mod, PU_key_pkda)).split("||") #formatting the decrypted reply into a list
    # reply = (decrypted_reply)
    print(reply)
    PU_key_B = int(reply[0]) #0th index contains the public key of device B
    diff = datetime.datetime.strptime(reply[2], '%Y-%m-%d %H:%M:%S.%f') - t1 #difference of time 

    if((diff.total_seconds()) <= 1): #if the reply came later than 1 second,
        print("message reception was within the time limits")
    else:
        print("message has timed out.. Reply came late")

    if(reply[1] == (msg).split("||")[0]):
        print("Message is OK")
    else:
        print("Message is Corrupted.")
        
    print ('public key of B received: ', PU_key_B) 
    soc.close()


    # Now, send message to B
    soc = socket.socket()
    soc.connect((IP, 10030))
    print('Sending message to B... \n\n')

    import random
    nonce = random.randint(10**10, 10**15) 
    
    soc.send(str.encode(RSA.encrypt(str(id_A) + '||' + str(nonce), mod, PU_key_B)))
    soc.close()

    # Checking for a response from B

    soc = socket.socket()
    soc.bind(('', 7090))         
    print ("Socket is now binded to " + str(7090)) 
    soc.listen()      
    print ("Socket is now listening")            
    con, address = soc.accept()      
    print ('Successful connection with B') 
    print ('Reply from B received')
    # c.send(b'Sending confirmation to B')
    reply_from_B = (RSA.decrypt(con.recv(1024).decode(), mod, PR_key)).split("||")

    nonce2 = reply_from_B[1]
    if(int(nonce2) == nonce): #if the nonce value is different
        print("Nonce 1 is the same")
        print("original: " + str(nonce) + " received: " + str(nonce2))
    else:
        print("Nonce 1 not equal")
        print("original: " + str(nonce) + " received: " + str(nonce2))
    
    print ('Nonce 2 (sent by B): ', nonce2)

    con.send(str.encode(RSA.encrypt(nonce2, mod, PU_key_B)))

    #Exchange messages with client B
    i=0
    while i < 3: 
        con.send(str.encode(RSA.encrypt('Hi ' + str(i + 1), mod, PU_key_B)))
        print("Reply from B: " + RSA.decrypt(con.recv(1024).decode(), mod, PR_key))
        i+=1
    con.close()
    soc.close()