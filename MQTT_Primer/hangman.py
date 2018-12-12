#MQTT Primer
#By Rachen Ravichandran, Makerdemy

import paho.mqtt.client as paho     #This is a library module which consists of all MQTT related functions. paho.mqtt.client is given an alias name of paho
from tkinter import *		    #This is a GUI library module for creating buttons and form entries

QoS = 0 			    #set your own QoS value here and check how fast your message service works for various QoS values
 
#(2)------------READ (1) BEFORE READING THE FOLLOWING-------------
#In python, a function definition starts with "def function_name()"
 
def on_message(client, userdata, msg):              #This function is called automatically whenever a message is received to the subscribed topic
    if(game_flag == 1):				    #if game mode is enabled, this variable is set '1'
        hang(str(msg.payload.decode("utf-8")))
	#.decode("utf-8") converts the byte array of input subscribed message in msg.payload to string using str()and passes it to the function hang()
    else:
        frndName = msg.topic.replace("chatRoom/","")                    #extracts the name of your friend from the topic name
        message = frndName + " says : " + str(msg.payload.decode("utf-8"))
        output.configure(text = message)                                #Changes the 'output' label's value to the subscribed message
        client.publish(topic = "chatRoom", payload = message, qos = QoS)#publishes the received message to the topic "chatRoom". Uses specified QoS value.

def add_click():                                            #This function is called when the button add is pressed
    frndTopic = "chatRoom/"+addFrnd.get()
    #stores the topic name as "chatRoom/<your-friend-name> entered in the addFrnd entry field using the inbuilt addFrnd.get() function
    output.configure(text = "You added : " + addFrnd.get()) #Changes the 'output' label's value to the subscribed message
    addFrnd.delete(0,"end")                                 #deletes the entered text in addFrnd entry field
    client.subscribe(topic = frndTopic, qos = QoS)          #The Paho MQTT client subscribes to the topic "chatRoom/<your-friend-name>"

def send_click():                                           #This function is called when the button send is pressed
    msg_pub(masterSays.get())                               #function msg_pub() is passed with the value entered in masterSays entry field
    masterSays.delete(0,"end")                              #deletes the entered text in masterSays entry field

def msg_pub(msg):
    output.configure(text = "You said : \"" + msg+"\"")                                 #Changes the 'output' label's value to the msg value
    client.publish(topic = "chatRoom", payload = "Chat Room says : " + msg, qos = QoS)  #publishes the message to the topic "chatRoom". Uses specified QoS value.

def exit_click():                                                                           #This function is called when the button close is pressed
    client.publish(topic = "chatRoom", payload = "Chat Room is disconnected...", qos = QoS) #publishes the message to the topic "chatRoom". Uses specified QoS value.
    client.loop_stop()				                                            #The MQTT client is disconnected from the MQTT broker
    exit(0)					                                            #Close the execution

def game_click():#This function is called when the button game is pressed
    global master_word, dup_word, game_flag#accesses the global variables so that any changes in the function is reflected outside the function too
    #master_word holds the word entered by the master Chat Room
    #dup_word is the guessed word by the player. For e.g. if master_word = "pizza" and the player has guessed the letters "p" and "z" so far, then dup_word = "p-zz-"
    #game_flag is set as 1 when game button is clicked indicating that game is started and as 0 when game is completed
    game_flag = 1
    master_word = word.get()            #stores the entered text for Hangman input into master_word
    word.configure(state = "disabled")
    game.configure(state = "disabled")
    #.configure() function is used here to disable the button from being pressed. i.e. if state is set as disabled, then the button freezes.
    dup_word = "-" * len(word.get())    #Converts each character of entered string to '-'	
    message = "Let's play a game.\nGuess the word : \"" + dup_word + "\"( " + str(len(word.get())) + " )\nEnter each letter one by one."
    msg_pub(message)                    #Passes the message to the function msg_pub() to publish the message to the subscribers

def hang(letter):                                   #letter indicates the character guessed by the subscriber
    global master_word, dup_word, count,game_flag   #accesses the global variables so that any changes in the function is reflected outside the function too
    #count indicates the number of wrong guesses made so far
    guess = 0                                       #this is a flag variable indicating whether the guess is right(1) or wrong(0)
    for i in range (len(master_word)):              #value of i is iterated from 0 to (length of master_word)-1
        if(master_word[i]== letter):                #if the guessed character matches any character in the master string, then execute below statements
            dup_word = dup_word[:i]+letter+dup_word[(i+1):]
	    #This statement replaces the '-' character(s) with the guessed letter at the position(s) where the letter matches master_word[i]
	    #for e.g. if master_word = "google", dup_word = "------", and letter = "g", at the end of iteration dup_word = "g--g--"
            guess = 1                               #indicates a right guess
    if (dup_word == master_word):                   #if the player guesses the whole word, then execute below statements
        message = "You've found the word : " + dup_word + ".\nTen points to Gryffindor" 
        word.configure(state = "normal")
        game.configure(state = "normal")
	#.configure() function is used here to enable the button which is previously freezed at the start of the game
        msg_pub(message)                            #Passes the message to the function msg_pub() to publish the message to the subscribers
        game_flag = 0                               #indicates that game is over and any message
        return                                      #returns to the called function
    if (guess == 1):                                #If the guess is right, then the guessed string is published
        message = "You got one right : " + dup_word
        msg_pub(message)                            #Passes the message to the function msg_pub() to publish the message to the subscribers
        return                                      #returns to the called function
    count = count + 1                               #if the guess is wrong, count is incremented
    if(count == 1):                                 #if this is the first wrong guess
        message = "________\n|      |\n|\n|\n|\n|\n|_______"    #type this statement in your Python shell to find out what it prints.
    elif (count == 2):                                          #if this is the second wrong guess and so on
        message = "________\n|      |\n|      0\n|\n|\n|\n|_______"
    elif (count == 3):
        message = "________\n|      |\n|      0\n|     /\n|\n|\n|_______"
    elif (count == 4):
        message = "________\n|      |\n|      0\n|     /|\n|\n|\n|_______"
    elif (count == 5):
        message = "________\n|      |\n|      0\n|     /|\\\n|\n|\n|_______"
    elif (count == 6):
        message = "________\n|      |\n|      0\n|     /|\\\n|     /\n|\n|_______"
    else :
        message = "________\n|      |\n|      0\n|     /|\\\n|     / \\\n|\n|_______\nIt seems game is over"
        word.configure(state = "normal")
        game.configure(state = "normal")
	#.configure() function is used here to enable the button which is previously freezed at the start of the game
        count = 0
        dup_word=""
        master_word=""
        game_flag = 0
	#the above variables are reset to its initial value so that they can be used next time in the game
    message = "You guessed wrong\n" + message
    msg_pub(message)                                #Passes the message to the function msg_pub() to publish the message to the subscribers
    
#(1)------------READ THIS BEFORE READING (2)--------------
#This is where your program execution begins
master = Tk()#Creates a GUI window called 'master'
master.title("Chat Room")                           #Title of the window is set as "Enter name"
master.geometry("350x350")                          #Size of the window is set
count = 0
#count indicates the number of wrong guesses made so far. Here it is initialized to 0
game_flag = 0
#game_flag is set as 1 when game button is clicked indicating that game is started and as 0 when game is completed. Here it is initialized to 0

addFrnd = Entry(master, width = 40)
#This creates an entry field in the window "master" named "addFrnd" and the field size is 40 (40 characters will be displayed)
addFrnd.grid(column = 0, row = 0, pady = 10, padx = 5)
#This adds the entry field addFrnd to your grid at column 0 and row 0. The spacing between adjacent widgets is set by padx = 5 
#(horizontal spacing) and the spacing between rows above and below is set by pady = 10 (vertical spacing.) pad represents padding

add = Button(master, text = "Add a friend", command = add_click)
#Adds a button "add" to your "master" window with text as "Add a friend" and when the button is pressed, the function add_click() is called
add.grid(column = 1, row = 0, pady =10, padx = 5)
#This adds the button add to your grid at column 1 and row 0 with padding space for x and y as 5 and 10 respectively

masterSays = Entry(master, width = 40)
#This creates an entry field in the window "master" named "masterSays" and the field size is 40
masterSays.grid(column = 0, row = 1, pady = 10)
#This adds the entry field masterSays to your grid at column 0 and row 1 with padding y spacing as 10.

send = Button(master, text = "Send message", command = send_click)
#Adds a button "send" to your "master" window with text as "Send message" and when the button is pressed, the function send_click() is called
send.grid(column = 1, row = 1, pady = 10)
#This adds the button send to your grid at column 1 and row 1 with padding space for y as 10 

word = Entry(master, width = 40)
#This creates an entry field in the window "master" named "word" and the field size is 40. This is where the master enters his Hangman word
word.grid(column = 0, row = 2, pady = 10, padx = 5)
#This adds the entry field masterSays to your grid at column 0 and row 2 with padding y spacing as 10 and paddingx spacing as 5

game = Button(master, text = "Start the game", command = game_click)
#Adds a button "send" to your "master" window with text as "Start the game" and when the button is pressed, the function game_click() is called
game.grid(column = 1, row = 2, pady =10, padx = 5)
#This adds the button game to your grid at column 1 and row 2 with padding space for y and x as 10 and 5 respectively

label_text = "1. Add your friends one by one.\n2. Send your message by clicking 'Send message' button\n3. To start the Hangman game, enter the word to guess.\n\
Then, press \'Start the game\'"
output = Label(master, text = label_text, justify = LEFT)
#This adds a label to your "master" window. A label simply displays a text given in "text" parameter and the texts are aligned to left
output.grid(column = 0, columnspan =2, row = 3, pady = 10)
#columnspan indicates that this widget spans or covers two columns (from column 0 to column 1). This label is added to your grid at row = 3 and column = 0

close = Button(master, text = "Exit", command = exit_click)
#Adds a button "close" to your "master" window with text as "Exit" and when the button is pressed, the function exit_click() is called
close.grid(column = 0, columnspan = 2, row = 4, pady = 10)
#This adds the button close to your grid at column 0 and row 4 with pady = 10 and spanning across two columns (0 and 1)

client = paho.Client()                                  #Creates a Paho MQTT client object
client.on_message = on_message                          #the inbuilt .on_message function is assigned with our own function definition on_message
client.connect("iot.eclipse.org", 1883)                 #Indicates the IoT Eclipse broker at the port 1883 to which the connection is to be established

client.loop_start()                                     #A network connection is established with the broker and the connection is maintained
master.mainloop()                                       #This allows the "master" window from closing automatically

