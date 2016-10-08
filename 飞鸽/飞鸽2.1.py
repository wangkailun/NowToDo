from tkinter import *
import socket
import _thread
import time
from tkinter.filedialog import *
import os , struct

class Win:
	def __init__(self):
		self.window = Tk()
		self.window.title("飞鸽客户端")
		self.frame1 = Frame(self.window)
		self.frame1.pack()
		self.text = Text(self.frame1)
		self.text.pack()
		self.text.config(bd = 4 , relief = RIDGE)
		self.MSG = StringVar()
		self.entry = Entry(self.frame1 , textvariable = self.MSG)
		self.entry.pack(side = LEFT , expand = True , fill = BOTH)
		self.entry.config(bd = 4 , relief = RIDGE)
		self.button = Button(self.frame1 , text = "发送消息" , command = self.SendMessage)
		self.button.pack(side = RIGHT)
		self.button.config(bd = 4 , relief = RAISED)
		self.button.config(bg = "white" , fg = "black")
		self.button2 = Button(self.frame1 , text = "发送文件" , command = self.SendFile)
		self.button2.config(bd =4 , relief = RAISED)
		self.button2.pack(fill = BOTH )
		
	def ReceviveMessage(self):
		ServerIP = 'localhost'
		ServerPort = 50001
		self.s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.s.connect((ServerIP,ServerPort))
		while True:
			self.message = self.s.recv(1024).decode("utf8")
			if self.message !='':
				a = time.strftime("%H:%M:%S" , time.localtime())
				self.text.tag_config('a',foreground = "green")
				self.text.insert(INSERT , "服务器 * * * * "+a+" * * * * *\n","a")
				self.text.insert(INSERT , "   "+self.message+"\n")
		
		
	def SendMessage(self):
		if self.MSG.get() !='':
			a = time.strftime("%H:%M:%S",time.localtime())
			self.text.tag_config('a',foreground = "green")
			self.text.insert(INSERT , "客户端 * * * * "+a+" * * * * *\n",'a')
			self.text.insert(INSERT,"    "+self.MSG.get()+ "\n")
			self.s.send(self.MSG.get().encode("utf8"))
			self.entry.delete(0 , END)
	
	
	def StartNewThread(self):
		_thread.start_new_thread(self.ReceviveMessage,())
		
	def SendFile(self):
		ServerIP = "localhost"
		ServerPort = 50002
		self.s1 = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.s1.connect((ServerIP , ServerPort))
		a = time.strftime("%H:%M:%S" , time.localtime())
		filename = askopenfilename(filetypes = (("word ,excel" , "*.doc;*.slx") , ("text", "*.txt") ,("All File" , "*.*")))
		print(filename)
		if os.path.isfile(filename):
			#fileinfo_size = struct.calcsize("128sl")
			#定义文件头信息，包含文件名和文件大小
			file = open(filename , "r")
			#headmessage = [os.path.basename(filename) , os.path.getsize(filename)]
			filename = os.path.basename(filename).encode("utf8")
			#filesize = os.path.getsize(filename).st_size.encode("ut
			print(filename)
			#print(filedata.encode("utf8") , headmessage.encode("utf8"))
			self.text.tag_config('a',foreground = "green")
			self.text.insert(INSERT ,"客户端 * * * * "+a+" * * * * *\n" , "a")
			self.text.insert(INSERT , "   开始传输文件")
			self.s1.send(filename)
			filedata = file.readline()
			while filedata:
				self.s1.send(filedata.encode("utf8"))
				filedata = file.readline()
				
			file.close()
			self.s1.close()
			self.text.insert(INSERT ,"客户端 * * * * "+a+" * * * * *\n" , "a")
			self.text.insert(INSERT , "   文件传输完成")
			'''
		else:
			self.text.insert(INSERT ,"客户端 * * * * "+a+" * * * * *\n" , "a")
			self.text.insert(INSERT , "   您选择的不是一个文件，请重新选择！")
			fo = open(filename , "rb")
			while True:
				filedata = fo.read(1024)
				if not filedata:
					break
				s1.send(filedata)
			fo.close()
			self.text.insert(INSERT ,"客户端 * * * * "+a+" * * * * *\n" , "a")
			self.text.insert(INSERT , "   文件下载上传成功！")
			s1.close()
			'''
		else:
			self.text.insert(INSERT , "客户端 * * * * "+a+" * * * * *\n" ,"a")
			self.text.insert(INSERT ,"   文件传输失败")
			self.s1.close()
			
		
def main():
	app = Win()
	app.StartNewThread()
	app.window.mainloop()
			
if __name__ == "__main__":
	main()