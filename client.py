import socket
import threading
import time

def send_data(s):
    while True:
        message=input("")
        try:
            s.send(message.encode('ascii'))
            time.sleep(0.5)
            if message=="@close":
                print("[-] CONNECTION CLOSED")
                s.close()
        except:
            print("[-] SERVER IS CLOSED!!")
            break

def display_data(s):
    while True:
        try:
            data = s.recv(1024)
            print(str(data.decode('ascii')))
        except:
            print("[-] SERVER IS CLOSED!!")
            s.close()
            break
        time.sleep(0.5)
    
def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 8000
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    try:
        s.connect((host,port))
        threading.Thread(target=send_data,args=(s,)).start()
        threading.Thread(target=display_data,args=(s,)).start()
    except:
        print("server is offline!")


    # message you send to server
    # close the connection
 
if __name__ == '__main__':
    Main()


