import socket
import re
import os

TCP_IP='192.168.1.230'
TCP_PORT= 8080
BUFFER_SIZE=1024

def main(inputQ,outputQ):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Uncomment this line when actually running
	s.bind((TCP_IP, TCP_PORT))

	s.listen(1)

	conn, addr = s.accept()

	tempRe = re.compile('temp')
	
	cpuRe = re.compile('cpu')
	
	#diskRe = re.compile('disk')

	print('Connection address:', addr)
	while True:
		#Attempts to get data from connection, if successful adds to input queue	
		data=conn.recv(BUFFER_SIZE).decode()
		data=data.lower()
		if len(data) > 0:
			inputQ.put(data)
		if not inputQ.empty():
			recieved = inputQ.get()
			if tempRe.search(recieved):
				output = os.popen('vcgencmd measure_temp').readline()
				outputQ.put(output)
			elif cpuRe.search(recieved):
				out = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
				outputQ.put(out+"%")
			else:
				outputQ.put("error")
			print("Recieved data: ", recieved)
		#if not data: break
		
		# If output is not empty
		if (outputQ.empty() == False):
		# Gets first item from output queue and sends to lower Pi	
			message = outputQ.get()
			conn.send(message.encode())
#	if not data: break
#	print('recieved data:', data)
			#conn.send(data.encode())
	conn.close()
	return 0
