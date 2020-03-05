#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from  threading import Thread
class client(Thread):
    def __init__(self,s,list,st):
        self.s,self.list,self.string=s,list,st
        Thread.__init__(self)
    def run(self):
        if(self.list[0]=="exit"):
                self.s.send(self.list[0].encode('utf-8'))
        if(self.list[0]=="list"):
            self.s.send(self.list[0].encode('utf-8'))
            data=pickle.loads(self.s.recv(1024))
            print(data)
        if(self.list[0]=="download"):
            f=open(self.list[1],"wb")
            self.s.send(self.string.encode('utf-8'))
            size=int(self.s.recv(1024))
            x=self.s.recv(1024)
            f.write(x)
            for i in tqdm(range(0,size,1024)):
                x=self.s.recv(1024)
                f.write(x)
            f.close()
            print("file downloaded sucess")
        if(self.list[0]=="upload"):
            f=open(self.list[1],"rb")
            self.s.send(self.string.encode('utf-8'))
            self.s.send(str(os.stat("./"+self.list[1]).st_size).encode('utf-8'))
        # size=s.recv(1024).decode('utf-8')
            l=f.read(1024)
            self.s.send(l)
            for i in tqdm(range(0,os.stat("./"+self.list[1]).st_size,1024)):
                self.s.send(l)
                l=f.read(1024)
            f.close()
            self.s.close()
            print("file uploaded sucess")


# In[ ]:


from tqdm import tqdm
import os
import pickle
from  threading import Thread
import socket                
def main():
    while True:
        # string="upload taha.mp3"
        s = socket.socket()
        s.connect(('127.0.0.1', 5555))
        string=input()
        clie=client(s,string.split(" "),string)
        clie.start()


# In[ ]:


if __name__ == "__main__":
    main()

