# -*- coding: utf-8 -*-
"""
// By the Grace of Almighty-Succeed
Stepper Motor Driver Connection
// pul + to +5Volt
// dir + to +5 VOlt
// Enable - to ground

// pul - controls rotation- pin8
// dir - controls direction- pin9
//Enable +  inverted Enable- pin10
// Learn how to and set the Dip switches of Stepper Motor driver according to the table on the device
// I supplied 12 Volt DC to the stepper motor driver

"""

#%% PWM Outputs on D6
#!/usr/bin/env python3
from pyfirmata import Arduino#, util
from time import sleep
from tkinter import *
global board, pin1, pin2, pin3, pin4,  pin5, pin6, ard_ini
# in Arduino Firmata.begin(57600);
port='COM4'
h=650
w=950
ard_ini=0
def disconnect():
    ard_ini=0
    try:
        pin6.write(0)
        pin5.write(0)
        board.exit()
        sleep(2)
        print('Arduino Disconnected')
    except:
        print('Arduino not connected')
        pass
disconnect()
print('Start Your Work......')

def arduino_initialize():
    global board, pin1, pin2, pin3, pin4, pin5, pin6, ard_ini
    try:        
        print('Arduino initializing......')
        port=port_.get()
        board = Arduino(port) # Change to your port
        pin1 = board.get_pin('d:8:o') # digital: pin 8: pul 
        pin2 = board.get_pin('d:9:o') # digital: pin 9: direction
        pin3 = board.get_pin('d:10:o') # digital: pin 10: Inverted Enable
        pin4 = board.get_pin('d:11:o') # digital: pin 11: LED
        pin5 = board.get_pin('d:2:o') # digital: pin 2: LED Enable On
        pin6 = board.get_pin('d:3:o') # digital: pin 3: LED Arduino On
        
        ard_ini=1
        pin6.write(1)
        pin5.write(0)
        print('Arduino Initialized')
    except:
        print('Arduino Initialization Failed')

def Motor(fun=0):
    global board, pin1, pin2, pin3, pin4, pin5, pin6, ard_ini
    
    if ard_ini==0:
        pin5.write(0)
        print('Arduino not Initialized')
        return 0
    
    
    not_enable=horz_enable.get()
    if not_enable==0:
        pin3.write(1)
        print('Stepper Driver Enable Pin is Turned off')
        return 0
    
    pin3.write(0) # Stepper Driver Enable Pin Turn On
    if fun==0:
        turnn=int(turn_.get())
        loops=int(loop_.get())
    elif fun==1:
        turnn=int(motor_radio.get())
        loops=int(motor_loop.get())
    else:
        turnn=int(horz_v.get())
        loops=int(vert_v.get())
        
    direction=int(horz_direction.get())
    pin2.write(direction) # Set Direction
    timeon=horz_timeOn.get()/100000
    timeoff=horz_timeOff.get()/100000
    print('timeon', timeon)
    
    #timeon=horz_timeOn.get()/10
    #timeoff=horz_timeOff.get()/10
    pin4.write(1)
    print('Motor is rotating.........')
    pin5.write(1)
    for i in range(loops):
        for j in range(turnn):
            pin1.write(1)
            sleep(timeon)
            pin1.write(0)
            sleep(timeoff)
        print('Completed {} loops'.format(i+1))
    pin4.write(0)
    print("Task Completed")
    
#%%    
#%% tkinter initialize
root=Tk()
root.title("Casper-Stepper_Motor_Control")
root.iconbitmap("icons\\hat.ico")
root.geometry(str(w)+'x'+str(h))
#%% Input
row=0
port_=Entry(root, width=10,bg='lemon chiffon', borderwidth=10)
turn_=Entry(root, width=10,bg='lime green', borderwidth=10)
loop_=Entry(root, width=10,bg='sandy brown', borderwidth=10)

turn_.insert(0,'100')
loop_.insert(0,'3')
port_.insert(0, port)

port_.grid(row=0,column=0,columnspan=1, padx=1,pady=2)


# Create Button/items
row+=1
mylabel1=Label(root,text="Motor Rotation Functions",bg='white',fg='green').grid(row=row,column=0)
row+=1
mylabel2=Label(root,text="Turns",bg='white',fg='green').grid(row=row,column=0)
turn_.grid(row=row,column=0,columnspan=4, padx=1,pady=2)
row+=1
mylabel3=Label(root,text="Loops",bg='white',fg='green').grid(row=row,column=0)
loop_.grid(row=row,column=0,columnspan=4, padx=1,pady=2)



button00=Button(root,text="Arduino Initialize",padx=30, pady=30, command=(lambda:arduino_initialize())).grid(row=0,column=3)
button0=Button(root,text="Disconnect Arduino",padx=30, pady=30, command=(lambda:disconnect())).grid(row=0,column=4)
row+=1
button1=Button(root,text="Motor Rotate",padx=20, pady=10, command=(lambda:Motor())).grid(row=row,column=0,columnspan=4, padx=1,pady=2)

horz_enable=DoubleVar()
Label(root,text="Stepper Driver Enable Pin is on/off",bg='white',fg='green').grid(row=0,column=5)
enable=Scale(root, from_=0, to=1, resolution=1, variable=horz_enable, orient=HORIZONTAL).grid(row=1,column=5)

horz_direction=DoubleVar()
Label(root,text="Rotation Direction",bg='white',fg='green').grid(row=2,column=5)
enable=Scale(root, from_=0, to=1, resolution=1, variable=horz_direction, orient=HORIZONTAL).grid(row=3,column=5)

horz_timeOn=DoubleVar()
horz_timeOff=DoubleVar()
Label(root,text="TIme for Each Step in micro-sec*100- pulse on/off",bg='white',fg='green').grid(row=4,column=5)
enable=Scale(root, from_=0, to=100, resolution=1.0, length=200, label='Pulse on time',variable=horz_timeOn, orient=HORIZONTAL).grid(row=5,column=5)
enable=Scale(root, from_=0, to=100, resolution=1.0, length=200, label='Pulse off time', variable=horz_timeOff, orient=HORIZONTAL).grid(row=6,column=5)
horz_timeOn.set(5)
horz_timeOff.set(2)

#%% Radio Button
 
turn_modes=[("A","10"),
            ("B","20"),
            ("C","30"),
            ("D","40"),
            ("E","50")]
loop_modes=[("A","10"),
            ("B","20"),
            ("C","30"),
            ("D","40"),
            ("E","50")]


motor_radio=StringVar()
motor_radio.set("30") # Default Choice
motor_loop=StringVar()
motor_loop.set("30") # Default Choice

mylabel4=Label(root,text="Functional Mode-Time>>loop (Default-C,C)",bg='white',fg='green')
mylabel4.grid(row=5,column=0)

row=6
for i in range(len(turn_modes)):
    Radiobutton(root, text=turn_modes[i][0],variable=motor_radio, value=turn_modes[i][1]).grid(row=row,column=0)
    Radiobutton(root, text=loop_modes[i][0],variable=motor_loop, value=loop_modes[i][1]).grid(row=row,column=1)
    row+=1

row+=1
button2=Button(root,text="Click for Radio Function Execution",padx=20, pady=20,command=lambda:Motor(fun=1)).grid(row=row,column=0)
row-=1
#%% slider
horz_v=DoubleVar()
vert_v=DoubleVar()

horz=Scale(root, from_=0, to=200,length=200, resolution=1, label='Turns (degree=Turns*1.8)', variable=horz_v, orient=HORIZONTAL).grid(row=row,column=4)
vert=Scale(root, from_=0, to=100, label='Loops', variable=vert_v).grid(row=row,column=5)
horz_v.set(20)
vert_v.set(5)
row+=1

button3=Button(root,text="Click for Slider Function Execution",padx=20, pady=20,command=lambda:Motor(fun=2)).grid(row=row,column=4)
row+=1
#%%
button_exit=Button(root,text="Exit",padx=20, pady=10, command= root.quit) 
#button_exit.grid(row=row,column=0)
root.mainloop()
print('End of Progam')