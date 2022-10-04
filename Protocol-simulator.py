import time
import os
import cursor
import blessings
import random

term = blessings.Terminal() 
cls  = lambda: os.system('clear')
randint = random.randint

#zero_frame=[0,0,0,0,0,0,0,0,0]
#responce_frame=[255,1,2,3,4,5,6,7,8]
#startframecounter = 0
#last_idn = 0
#temp_idn = 0
delay    = 1
lines    = 0

def prints(num,value):
    with term.location(0,1):
        print("----------------Sent array---------------")
    with term.location(0,num+1):
        print("                                                                                        ")
    with term.location(0,num+1):
        print(value)

def logs(num,value,type):
    with term.location(0,14):
        print("--------------Received array-------------")
    with term.location(type*50,num+15):
        print("                                                  ")
    with term.location(type*50,num+15):
        print("("+str(type)+")"+str(num)+">"+str(value))


class device:

    startframecounter = 0
    temp_idn = 0
    zero_frame=[0,0,0,0,0,0,0,0,0]
    responce_frame=[255,1,2,3,4,5,6,7,8]

    def __init__(self,number):
        self.number = number
        self.update()
        self.show()

    def show(self):
        print("")
        print("("+str(self.number)+")")
        print("SFC : "+str(device.startframecounter))
        print("tid : "+str(device.temp_idn))
        print("Zef : "+str(device.zero_frame))
        print("Res : "+str(device.responce_frame))

    def update(self):
        device.responce_frame[0]=255
        device.responce_frame[1]=self.number
        device.responce_frame[2]=randint(0,255)
        device.responce_frame[3]=randint(0,255)
        device.responce_frame[4]=randint(0,255)
        device.responce_frame[5]=randint(0,255)
        device.responce_frame[6]=randint(0,255)
        device.responce_frame[7]=randint(0,255)
        device.responce_frame[8]=randint(0,255)

    def protocol(self,received):
	self.rec = received
        logs(self.number,self.rec,0)
        self.update()
        logs(self.number,self.rec,1)
        if self.rec == None:
            device.startframecounter +=1
            if device.startframecounter > 10:
                device.startframecounter = 1
                prints(self.number,"Device "+str(self.number)+" Reset Cycle")

            if device.startframecounter == 1:
                prints(self.number,"Device "+str(self.number)+" Send own DATA"+str(device.responce_frame))
                time.sleep(delay)
                return self.responce_frame
            elif device.startframecounter == 2:
                prints(self.number,"Device "+str(self.number)+" Send Zero")
                time.sleep(delay)
                return self.zero_frame
            else:
                prints(self.number,"Device "+str(self.number)+" Waiting... "+str(device.startframecounter))
                time.sleep(delay)
        else:
	    #get id of received data
            device.temp_idn = self.rec[0]
	    #is not a zero frame
            if device.temp_idn != 0:
                device.temp_idn -=1
                self.rec[0]=device.temp_idn
                logs(self.number,self.rec,2)
                prints(self.number,"Device "+str(self.number)+" Forward frame "+str(self.rec))
                time.sleep(delay)
                return received
            else:
                prints(self.number,"Device "+str(self.number)+" Send own DATA")
                device.startframenumber = 1
                time.sleep(delay)
                return device.responce_frame

#--------------------------------------------------------------------------#
cursor.hide()
cls()

#testbench procedure
print("--------------Create Objects-------------")
D1 = device(1)
D2 = device(2)
D3 = device(3)
D4 = device(4)
D5 = device(5)
time.sleep(5)

cls()

print("|---                          TESTBENCH                          ---|")

while True:
    #arr = D1.protocol(D2.protocol(D3.protocol(D4.protocol(D5.protocol(None)))))
    #arr = D1.protocol(D2.protocol(None))
    with term.location(0,26):
        print("--------------Objects Variables-------------")
    res1 = D1.protocol(None)
    with term.location(0,27):
        D1.show()
    time.sleep(3)
    res2 = D2.protocol(res1)
    with term.location(0,27):
        D2.show()
    time.sleep(3)
    arr  = D3.protocol(res2)
    with term.location(0,27):
        D3.show()
    time.sleep(3)

    if arr != None:
        if arr[0]>0:
            lines +=1
            with term.location(0,34):
                print("--------------Final Result-------------")
            with term.location(0,(255-arr[0])+35):
                print("                                                                ")
            with term.location(0,(255-arr[0])+35):
                print(str(lines)+" | "+str(arr))
            with term.location(40,0):
                print(" ")
        else:
            with term.location(40,0):
                print("●")

