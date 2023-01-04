# import socket programming library
import socket
import time
# import thread module
from _thread import *
import threading
#private m send krne m dikkat aa rahi h jb user left krta h
def chatwithtwo(c,numusr,data):
			check_none=0
			c.send("[+] WELCOME TO PRIVATE CHAT".encode())
			c.send("[+]choose to which one you wanna chat".encode())
			for i in range(len(usernames)):
				if numusr != usernames[i]: 
					if None!=usernames[i]:
						select=f"\n{i}. {usernames[i]}\n"
						c.send(select.encode())
					else:
						check_none+=1
						if check_none>=((len(usernames))-1):
							c.send("\nSORRY !!!!!!\n[-] NO USER FOUND !!".encode())
							return
			select_username=c.recv(1024)
			select_username=select_username.decode()
			print("select:",select_username)
			try:
				if usernames[int(select_username)] in usernames:
						chat_two_display(numusr,c,clients[int(select_username)])
				else:
						c.send("[-] wrong selection".encode())
			except:
				c.send("[-] wrong input".encode())
			try:
				c.send("[-] NOW YOU ARE IN BROADCAST SERVER\n".encode())
			except:
				pass
def chat_two_display(numusr,c,recver):
	message=f"[!]If you also want to chat with {numusr}\nuse @private and select {numusr} (or to whom you want to chat)\nthis message will not been shown to all"
	recver.send(message.encode())
	sendcheck={}
	while True:
			try:
				data = c.recv(1024)
				data=data.decode()
				sendcheck[numusr]=c
				if data=="@broadcast":
					display_data(c,numusr)
				elif data=="@private":
					chatwithtwo(c,numusr,data)
				else:
					for i in range(len(clients)):
						if clients[i]==recver:
							send_to=usernames[i]
					print(f"[+] {numusr} --> {send_to}:- {data}")
					chat_two_send(numusr,data,recver,c)
			except:
				break
				#data="@broadcast"
			'''if data=="@broadcast":
				display_data(c,numusr)
			elif data=="@private":
				chatwithtwo(c,numusr,data)
			else:
				for i in range(len(clients)):
					if clients[i]==recver:
						send_to=usernames[i]
				print(f"[+] {numusr} --> {send_to}:- {data}")
				chat_two_send(numusr,data,recver,c)'''
def chat_two_send(numusr,data,recver,c):
	try:
		sendingtoall=f"[+] {numusr} (private):- {data}"
		recver.send(sendingtoall.encode())
	except:
		message=f"[-] {numusr} has left so we are redirecting you to BROADCAST server"
		c.send(message.encode())
		display_data(c,numusr)
def user_left(numusr):
	print(f"[$] {numusr} disconnected ")
	for i in range(len(clients)):
		if usernames[i]==numusr:
			usernames[i]=None
			clients[i]=None
	for i in range(len(clients)):
		sendingtoall=f"[-] {numusr}: has left the chat"
		try:
			clients[i].sendall(sendingtoall.encode())
		except:
			pass

def send_data(numusr,senddata,clients,sendcheck):
	#lock.release()
	for i in range(len(clients)):
		if not clients[i]==sendcheck[numusr]:
			sendingtoall=f"[+] {numusr}:- {senddata}"
			try:
				clients[i].sendall(sendingtoall.encode())
			except:
				pass
def display_data(c,numusr):
		c.send("[+] WELCOME TO BROADCAST SERVER".encode())
		sendcheck={}
		while True:
			time.sleep(0.5)
			try:
				data = c.recv(1024)
				sendcheck[numusr]=c
				print(f"[+] {numusr}:- {data.decode()}")
			except:
				user_left(numusr)
				break

			if data.decode()=="@private":
				chatwithtwo(c,numusr,data)
			else:
				send_data(numusr,data.decode(),clients,sendcheck)
# thread function
def threaded(c,username):
		threading.Thread(target=display_data,args=(c,username)).start()#3
def username_check(c):
	while True:
		try:
				c.send("\n[+]enter your username".encode())
				uname=c.recv(1024)
				if uname.decode() not in usernames:
					datatosend=f"---> your username is {uname.decode()}"
					if None in usernames:
						for i in range(len(usernames)):
							if usernames[i]==None:
								usernames[i]=uname.decode()
					else:
						usernames.append(uname.decode())
					if None in clients:
						for i in range(len(clients)):
							if clients[i]==None:
								clients[i]=c
					else:
						clients.append(c)
					c.sendall(datatosend.encode())
					break
				else:
					c.send("[-] This username is alredy in use!!!".encode())
		except:
			print("[+] USER LEFT!!")
			uname=None
			c.close()
			break
	return uname.decode()


def Main():
	host = "127.0.0.1"

	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 8000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")
	global clients
	global usernames
	global threads
	clients=[]
	usernames=[]
	threads=[]
	connectio(s)

def connectio(s):
	while True:
		# establish connection with client
		c, addr = s.accept()

		# lock acquired by client
		print('Connected to :', addr[0], ':', addr[1])
		username=username_check(c)
		# Start a new thread and return its identifier
		threaded(c,username)#


if __name__ == '__main__':
	Main()