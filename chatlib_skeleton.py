# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"logout_ok_msg" : "LOGOUT_OK",
"logout_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	if(isinstance(cmd, str)==False or isinstance(data, str)==False or len(data)>MAX_DATA_LENGTH or len(cmd)>CMD_FIELD_LENGTH):
		return ERROR_RETURN
	full_msg = ''
	full_msg += cmd
	full_msg += ' '*(CMD_FIELD_LENGTH-(len(cmd)))
	full_msg += DELIMITER
	full_msg += '0'*(LENGTH_FIELD_LENGTH-len(str(len(data))))
	full_msg += str(len(data))
	full_msg += DELIMITER
	full_msg += data
	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	if(isinstance(data, str)==False):
		return ERROR_RETURN, ERROR_RETURN
	data = data.strip()
	splitted=data.split(DELIMITER)
	if(len(splitted)!=3):
		return ERROR_RETURN, ERROR_RETURN
	cmd = splitted[0]
	length = splitted[1]
	msg = splitted[2]
	if(len(msg)>MAX_DATA_LENGTH or len(splitted[0])!=CMD_FIELD_LENGTH or len(length)!=LENGTH_FIELD_LENGTH or length.isdigit()==False):
		return ERROR_RETURN, ERROR_RETURN
	cmd = cmd.replace(" ", "")
	if(cmd=="ALL_SCORE"):
		if(len(msg)+1!=int(length)):
			return ERROR_RETURN, ERROR_RETURN
	elif(len(msg)!=int(length)):
		return ERROR_RETURN, ERROR_RETURN
	if(cmd==PROTOCOL_CLIENT["login_msg"]):
		if(split_data(msg, 2)==[ERROR_RETURN]):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=='LOGOUT' or cmd=='LOGGED' or cmd=='GET_QUESTION' or cmd=='MY_SCORE' or cmd=='HIGHSCORE' or cmd==PROTOCOL_SERVER["login_ok_msg"] or cmd=="NO_QUESTIONS" or cmd=="CORRECT_ANSWER"):
		if(msg!=''):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=='SEND_ANSWER'):
		if(split_data(msg, 2)==[ERROR_RETURN]):
			return ERROR_RETURN, ERROR_RETURN
		id=msg.split(DATA_DELIMITER)[0]
		choice=msg.split(DATA_DELIMITER)[1]
		if(id.isdigit()==False or choice.isdigit()==False or int(choice)>4 or int(choice)<=0):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=="LOGGED_ANSWER"):
		return cmd, msg
	elif(cmd=="YOUR_SCORE"):
		if(msg.isdigit()==False):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=="ALL_SCORE"):
		if(msg!=""):
			msg2 = msg.replace(" ", "").splitlines()
			msg_list=[]
			for i in msg2:
				msg_list.append(i.split(":"))
			for i in msg_list:
				if(len(i)!=2):
					return ERROR_RETURN, ERROR_RETURN
				if(i[1].isdigit()==False):
					return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=="YOUR_QUESTION"):
		msg_list=msg.split("#")
		if(len(msg_list)!=6):
			return ERROR_RETURN, ERROR_RETURN
		if(msg_list[0].isdigit()==False):
			return ERROR_RETURN, ERROR_RETURN
		if(int(msg_list[0])<1):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	elif(cmd=="WRONG_ANSWER"):
		if(msg.isdigit()==False):
			return ERROR_RETURN, ERROR_RETURN
		if(int(msg)<1 or int(msg)>4):
			return ERROR_RETURN, ERROR_RETURN
		return cmd, msg
	return ERROR_RETURN, ERROR_RETURN


def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	splitted=msg.split(DATA_DELIMITER)
	if(len(splitted)==expected_fields):
		return splitted
	return [ERROR_RETURN]


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	joined=DATA_DELIMITER.join(msg_fields)
	return joined
