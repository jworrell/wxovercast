import socket
import time

START_MESSAGE = chr(1)
END_MESSAGE = chr(3)

sock = socket.create_connection(("oi.weatherwire.net",15000))

logged_in = False
log_in_string = open("connect.txt").read() + "\n"

sock.recv(4096)
sock.sendall(log_in_string)

in_message = False
buff = ""
bytes_read = 0
start_time = time.time()

while True:
    # If we're in the middle of a message or have no data, get more data
    if buff == "" or in_message:
        data_in = sock.recv(4096)
        bytes_read += len(data_in)
    
        if not data_in:
            break
    
        buff += data_in
    
    # If we're not in the middle of a message, look for one. 
    if not in_message:
        start_pos = buff.find(START_MESSAGE)
        
        if start_pos == -1:
            continue
        
        in_message = True
        buff = buff[start_pos+1:]
    
    # If we are in the middle of a message, look for the end  
    if in_message:
        end_pos = buff.find(END_MESSAGE)
        
        if end_pos == -1:
            continue
        
        in_message = False
        message = buff[:end_pos]
        buff = buff[end_pos+1:]
        
        start = 5
        trimmed = (message.replace("\n"," ").replace("\r",""))[start:start+200]
        if trimmed.startswith("SA") or trimmed.startswith("FT"):
            print trimmed
