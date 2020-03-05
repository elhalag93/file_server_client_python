#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import pickle
import os
from tqdm import tqdm
from  threading import Thread


# In[ ]:


#send_receive_files
class send_recive(Thread):
    def __init__(self,c,up_down,file_name,storage_path,file_size):
        self.c=c
        self.up_down, self.file_name,self.storage_path,self.file_size = up_down, file_name,storage_path,file_size
        Thread.__init__(self)
    def run(self):
        if(self.up_down == "download"):
            f= open(self.storage_path+self.file_name,"rb")
            l=f.read(1024)
            self.c.send(l)
            for i in tqdm(range(0,self.file_size,1024)):
                self.c.send(l)
                l=f.read(1024)
            f.close()
            print("file downloaded sucess")
        elif(self.up_down == "upload"):
            print("upload")
            f= open(self.storage_path+self.file_name,"wb")
            x=self.c.recv(1024)
            f.write(x)
            for i in tqdm(range(0,self.file_size,1024)):
                x=self.c.recv(1024)
                f.write(x)
            f.close()
            print("file uploaded sucess")


# In[ ]:


#send file
def main():
    port = 5555
    s = socket.socket()
    host = socket.gethostname()
    s.bind(('127.0.0.1', port))
    s.listen(50)
    while True:
        c, addr = s.accept()
        if(c!=None):
            string=c.recv(1024).decode('utf-8')
            list=string.split(" ")
            if(list[0]=="exit"):
                break
            if(list[0]=="list"):
                data=pickle.dumps(os.listdir("./"))
                c.send(data)
            if(list[0]=="download"):
                c.send(str(os.stat("./"+list[1]).st_size).encode('utf-8'))
                size=os.stat("./"+list[1]).st_size
                f=send_recive(c,list[0],list[1],"./",size)
                f.start()
            if(list[0]=="upload"):
                size=int(c.recv(1024))
                f=send_recive(c,list[0],list[1],"./",size)
                f.start()


# In[ ]:


if __name__ == "__main__":
    main()


# In[ ]:




