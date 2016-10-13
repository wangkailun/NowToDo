from tkinter import *
import select
import socket

import multiprocessing

input_list = []
output_list = []
import socket  , socketserver ,os , struct
from tkinter import *
import _thread
import time

class Servers:
	def __init__(self , conn):
		self.connection = conn
		self.window = Tk()
		self.window.title("飞鸽服务器端")
		self.frame1 = Frame(self.window)
		self.frame1.pack()
		self.text = Text(self.frame1)
		self.text.pack()
		self.text.config(bd = 4 , relief =RIDGE)
		self.MSG = StringVar()
		self.entry = Entry(self.frame1 , textvariable = self.MSG)
		self.entry.pack(side = LEFT , expand = True , fill = BOTH)
		self.entry.config(bd = 4 , relief = GROOVE)
		self.button = Button(self.frame1 , text = "发送" , command = self.SendMessage)
		self.button.pack(side = RIGHT)
		self.button.config(bd = 4 , relief = RAISED)
			
			

	def ReceiveMessage(self):
		while True:
			self.data = self.connection.recv(1024).decode("utf8")
			if self.data == '':
				continue
			else:
				a =time.strftime("%H:%M:%S" , time.localtime())
				self.text.tag_config('a',foreground = "green")
				self.text.insert(INSERT , "客户端 * * * * "+a+" * * * * *\n",'a')
				self.text.insert(INSERT , "   "+self.data+"\n")

	def SendMessage(self):
		self.message = self.MSG.get()
		if self.message != '':
			a = time.strftime("%H:%M:%S" , time.localtime())
			self.text.tag_config('a',foreground = "green")
			self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n",'a')
			self.text.insert(INSERT,"   "+self.message+"\n")
			self.connection.send(self.message.encode("utf8"))
			self.entry.delete(0,END)
			
	def StartNewThread(self):
		_thread.start_new_thread(self.ReceiveMessage,())

	
def Work(conn):
	server = Servers(conn)
	server.StartNewThread()
	server.window.mainloop()

		
		
class Server:
	def __init__(self):
		Port = 50000
		Host = ""
		Addr = (Host , Port)
		server = socket.socket()
		server.bind(Addr)
		server.listen(10)
		
		server.setblocking(False)
		input_list.append(server)
		while True:
			stdinput , stdoutput , stderr = select.select(input_list , output_list , input_list)
			for obj in stdinput:
				if obj == server:
					print("hello")
					conn , addr = server.accept()
					multiprocessing.Process(target = Work , args =(conn ,)).start()
					
if __name__ == "__main__":
	App = Server()