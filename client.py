import socket
import chatlib_skeleton  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
	Builds a new message using chatlib, wanted code and message.
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
    msg = chatlib_skeleton.build_message(code, data)
    conn.send(msg.encode())
    print("Message sent:", msg)


def recv_message_and_parse(conn):
    """Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message.
	If error occured, will return None, None
	"""
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib_skeleton.parse_message(full_msg)
    return cmd, data


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    code_msg, dat = recv_message_and_parse(conn)
    return code_msg, dat


def get_score(conn):
    cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
    if(cmd!="YOUR_SCORE"):
        print("An error occurred")
        return
    print("Your score is", data)


def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, "HIGHSCORE", "")
    if(cmd!="ALL_SCORE"):
        print("An error occurred")
        return
    print("High Scores Table:")
    print(data)


def play_question(conn):
    cmd, data = build_send_recv_parse(conn, "GET_QUESTION", "")
    if(cmd=="NO_QUESTION"):
        print("GAME OVER")
        return
    if(cmd=="YOUR_QUESTION"):
        print(data.split("#")[1])
        print(data.split("#")[2])
        print(data.split("#")[3])
        print(data.split("#")[4])
        print(data.split("#")[5])
        ans = input("Enter your answer: ")
        while(ans.isdigit()==False or int(ans)<1 or int(ans)>4):
            ans = input("Enter a digit between 1-4: ")
        msg = data.split("#")[0]+chatlib_skeleton.DATA_DELIMITER+ans
        cmd, data = build_send_recv_parse(conn, "SEND_ANSWER", msg)
        if(cmd=="CORRECT_ANSWER"):
            print("Correct!")
            return
        if(cmd=="WRONG_ANSWER"):
            print("Wrong! The answer is", data)
            return
    print("An ERROR occurred")
    return


def get_logged_users(conn):
    cmd, data = build_send_recv_parse(conn, "LOGGED", "")
    if(cmd=="LOGGED_ANSWER"):
        print("The logged users:", data)
        return
    print("An ERROR occurred")
    return


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = username+chatlib_skeleton.DATA_DELIMITER+password
        build_and_send_message(conn, chatlib_skeleton.PROTOCOL_CLIENT["login_msg"], data)
        cmd, data = recv_message_and_parse(conn)
        if(cmd == chatlib_skeleton.PROTOCOL_SERVER["login_ok_msg"]):
            print("Login is successful")
            return
        print("Login failed. Try again")


def logout(conn):
    while True:
        build_and_send_message(conn, chatlib_skeleton.PROTOCOL_CLIENT["logout_msg"], "")
        cmd, data = recv_message_and_parse(conn)
        if(cmd == None):
            conn.close()
            print("Logout is successful")
            return
        print("Logout failed. Try again")

def main():
    my_socket = connect()
    login(my_socket)
    while True:
        print("p        Play a trivia question")
        print("s        Get my score")
        print("h        Get high score")
        print("l        Get logged users")
        print("q        Quit")
        action=input("Please enter your choice:")
        if(action=="p"):
            play_question(my_socket)
        elif(action=="s"):
            get_score(my_socket)
        elif(action=="h"):
            get_highscore(my_socket)
        elif(action=="l"):
            get_logged_users(my_socket)
        elif(action=="q"):
            logout(my_socket)
            break

if __name__ == '__main__':
    main()
