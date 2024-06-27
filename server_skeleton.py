##############################################################################
# server.py
##############################################################################

import socket
import select
import chatlib_skeleton

# GLOBALS
users = {"test": {"password": "testing", "score": 0, "questions_asked": []}}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

MAX_MSG_LENGTH = 1024
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	msg = chatlib_skeleton.build_message(code, data)
	conn.send(msg.encode())
	print("[SERVER] ", msg)	  # Debug print

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode()
	cmd, data = chatlib_skeleton.parse_message(full_msg)
	print("[CLIENT] ", full_msg)	  # Debug print
	return cmd, data


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	print("Setting up server...")
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()
	print("Listening for client...")
	return server_socket
	


		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(conn, "ERROR", error_msg)
	


	
##### MESSAGE HANDLING


def handle_highscore_message(conn):
	sorted_users = sorted(dict.items(), key = lambda x: x["Password"], reverse = True)
	top_users = []
	for user in sorted_users:
		player = user+": "+users[user]["password"]+"\n"
		top_users.append(player)
	build_and_send_message(conn, "ALL_SCORE", top_users)


def handle_logged_message(conn):
	logged = ", ".join(list(logged_users.values()))
	build_and_send_message(conn, "LOGGED_ANSWER", logged)


def handle_getscore_message(conn, username):
	global users
	if(username not in users.keys()):
		send_error(conn, "User Not Found")
		return
	build_and_send_message(conn, "YOUR_SCORE", users[username]["score"])


def handle_logout_message(conn):
	"""
	Closes the given socket (in later chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	logged_users.pop(conn.getpeername())
	conn.close()


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	user = data.split("#")
	if user[0] not in users.keys():
		send_error(conn, "User Not Found")
		return
	if(user[1] != users[user[0]]["password"]):
		send_error(conn, "Wrong Password")
		return
	build_and_send_message(conn, "LOGIN_OK", "")
	logged_users[conn.getpeername()] = user[0]


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	if cmd == "LOGIN" and conn.getpeername() not in logged_users:
		handle_login_message(conn, data)
		return
	if conn.getpeername() not in logged_users:
		send_error(conn, "User not logged in")
		return
	if cmd == "LOGIN" and conn.getpeername() in logged_users:
		send_error(conn, "User already logged in")
		return
	if cmd == "LOGOUT" or cmd == "":
		handle_logout_message(conn)
		return
	if cmd == "MY_SCORE":
		handle_getscore_message(conn, logged_users[conn.getpeername()])
		return
	if cmd == "HIGH_SCORE":
		handle_highscore_message(conn)
		return
	if cmd == "LOGGED":
		handle_logged_message(conn)
		return



def main():
	# Initializes global users and questions dictionaries using load functions, will be used later
	global users
	global questions
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	client_socket, client_address = server_socket.accept()
	print("Client connected")
	while True:
		try:
			cmd, data = recv_message_and_parse(client_socket)
		except:
			client_socket.close()
			print("Socket closed")
		if(data is None and cmd is None):
			send_error(client_socket, "An error occurred")
		else:
			handle_client_message(client_socket, cmd, data)



if __name__ == '__main__':
	main()

