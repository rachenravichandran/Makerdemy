#MQTT Primer
#By Rachen Ravichandran, Makerdemy

import paho.mqtt.client as paho                 #This is a library module which consists of all MQTT related functions. paho.mqtt.client is given an alias name of paho
from tkinter import *		                #This is a GUI library module for creating buttons and form entries

QoS = 0 			                #set your own QoS value here and check how fast your message service works for various QoS values
 
#(2)------------READ (1) BEFORE READING THE FOLLOWING-------------
#In python, a function definition starts with "def function_name()"

def add_name():			                #This function is called when the button add is pressed
    master.title(addName.get())		
    #Changes the title of window from "Enter name" to entered name in the addName entry field using the inbuilt addName.get() function
    addName.configure(state = "disabled")
    add.configure(state = "disabled")
    #.configure() function is used here to disable the button from being pressed. i.e. if state is set as disabled, then the button freezes.

def on_message(client, userdata, msg):    	#This function is called automatically whenever a message is received to the subscribed topic
    message = str(msg.payload.decode("utf-8"))  #Converts the byte array of input subscribed message to string
    output.configure(text = message)		#Changes the 'output' label's value to the subscribed message
    
def send_click():				#This function is called when the button send is pressed
    output.configure(text = "You said : " + masterSays.get())
    #Changes the 'output' label's value to the string assigned to "text"
    client.publish(topic = "chatRoom/" + addName.get(), payload = masterSays.get(), qos = QoS) 
    #publishes the message entered in masterSays field to the topic "chatRoom/<entered-name>". Uses specified QoS value.
    masterSays.delete(0,"end")                  #deletes the entered text in masterSays entry field

def exit_click():				#This function is called when the button close is pressed
    client.publish(topic = "chatRoom/" + addName.get(), payload = addName.get() + " disconnected...", qos = QoS)
    client.loop_stop()				#The MQTT client is disconnected from the MQTT broker
    exit(0)					#Close the execution

#(1)------------READ THIS BEFORE READING (2)--------------
#This is where your program execution begins
master = Tk()					#Creates a GUI window called 'master'
master.title("Enter name")			#Title of the window is set as "Enter name"
master.geometry("340x300")			#Size of the window is set

addName = Entry(master, width = 40)	
#This creates an entry field in the window "master" named "addName" and the field size is 40 (40 characters will be displayed)
addName.grid(column = 0, row = 0, pady = 10, padx = 5)
#This adds the entry field addName to your grid at column 0 and row 0. The spacing between adjacent widgets is set by padx = 5 
#(horizontal spacing) and the spacing between rows above and below is set by pady = 10 (vertical spacing.) pad represents padding

add = Button(master, text = "Enter name", command = add_name)
#Adds a button "add" to your "master" window with text as "Enter Name" and when the button is pressed, the function add_name() is called
add.grid(column = 1, row = 0, pady =10, padx = 5)
#This adds the button add to your grid at column 1 and row 0 with padding space for x and y as 5 and 10 respectively

masterSays = Entry(master, width = 40)
#This creates an entry field in the window "master" named "masterSays" and the field size is 40
masterSays.grid(column = 0, row = 1, pady = 10)
#This adds the entry field masterSays to your grid at column 0 and row 1 with padding y spacing as 10. 

send = Button(master, text = "Send message", command = send_click)
#Adds a button "send" to your "master" window with text as "Send message" and when the button is pressed, the function send_click() is called
send.grid(column = 1, row = 1, pady = 10)
#This adds the button send to your grid at column 1 and row 1 with padding space for y as 10 respectively

output = Label(master, text = "Your message will be seen here.", justify = LEFT)
#This adds a label to your "master" window. A label simply displays a text given in "text" parameter and the texts are aligned to left
output.grid(column = 0, columnspan = 2, row = 2, pady = 10)
#columnspan indicates that this widget spans or covers two columns (from column 0 to column 1). This label is added to your grid at row = 2 and column = 0

close = Button(master, text = "Exit", command = exit_click)
#Adds a button "close" to your "master" window with text as "Exit" and when the button is pressed, the function exit_click() is called
close.grid(column = 0, columnspan = 2, row = 3, pady = 10)
#This adds the button close to your grid at column 0 and row 3 with pady = 10 and spanning across two columns (0 and 1)

client = paho.Client()			        #Creates a Paho MQTT client object
client.on_message = on_message		        #the inbuilt .on_message function is assigned with our own function definition on_message
client.connect("iot.eclipse.org", 1883)#Indicates the IoT Eclipse broker at the port 1883 to which the connection is to be established
client.subscribe(topic = "chatRoom", qos = QoS) #The Paho MQTT client subscribes to the topic "chatRoom"

client.loop_start()			        #A network connection is established with the broker and the connection is maintained
master.mainloop() 			        #This allows the "master" window from closing automatically

