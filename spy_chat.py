#------------------------------------------------------------------------------------------------------------------
# importing section

from spy_details import spy, Spy, ChatMessage, friends                                                                  #importing from spy_details.py
from steganography.steganography import Steganography                                                                   #This is for hiding messages in an image
from datetime import datetime                                                                                           #Helps in determinig time and date
from termcolor import colored                                                                                           #For making our app more colorful
#end of impoting stuff
#------------------------------------------------------------------------------------------------------------------

STATUS_MESSAGES = ['I am bond, james bond', 'I am better than greatest.', 'Untouchable']
print "Hello! Let\'s get started"

question = "Do you want to continue as " + spy.salutation + " " + colored('spy.name','red') + " (Y/N)? "
existing =raw_input(question)

#--------------------------------------------------------------------------------------------------------------------
#from here on declaring functions for our app
def add_status():                                                                                                       #This method is for setting up spys status
    updated_status_message = None
    if spy.current_status_message != None:                                                                              #checking whether the status is empty or not
        print 'Your current status message is %s \n' % (spy.current_status_message)
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")                                          #asking the user for selecting default status or make a new one

    if default.upper() == "N":                                                                                          #if the user choses to make his own status
        new_status_message = raw_input("What status message do you want to set? ")                                      #taking input as status from user

        if len(new_status_message) > 0:                                                                                 #cheking that the new status is not empty
            STATUS_MESSAGES.append(new_status_message)                                                                  #adding the new status in the list of status
            updated_status_message = new_status_message

    elif default.upper() == 'Y':
        item_position = 1
        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))


        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:                                                                                                               #if user press other buttens than 'y/n'
        print 'The option you chose is not valid! Press either y or n.'

    if updated_status_message:
        print 'Your updated status message is: %s' % (updated_status_message)
    else:
        print 'You current don\'t have a status update'

    return updated_status_message


def add_friend():                                                                                                       #This function is to add new friends

    new_friend = Spy('','',0,0.0)                                                                                       #using the spy class from spy_details.py

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    new_friend.name = new_friend.salutation + " " + new_friend.name

    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:                            #checking whether the new friend is fit to be a spy
        friends.append(new_friend)                                                                                      #if yes then adding him in the friends list
        print 'Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'                                   #if he dosen't fit in the criteria
    return len(friends)


def select_a_friend():                                                                                                  #This funtion allows the user to select the friend he want to
                                                                                                                        # chat with
    item_number = 0
    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number +1,
                                                                friend.salutation,
                                                                friend.name,
                                                                friend.age,
                                                                friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")                                                               #Asking the user to choose his friends he wants to chat with

    friend_choice_position = int(friend_choice) - 1
    return friend_choice_position

def send_message():                                                                                                     #This function is to send the secret message

    friend_choice = select_a_friend()                                                                                   #Choosing the friend you want to send secret message

    original_image = raw_input("What is the name of the image?")                                                        #Asking the user the name of the image along with extension
    output_path = "output.jpg"                                                                                          #It will be the name of the name of the file that would contain
                                                                                                                        #secret message
    text = raw_input("What do you want to say? ")                                                                       #Asking the user for the message

    if len(text) == 0:                                                                                                  #checking whether the message is not empty
        print 'There was no secret message, so it was not sent'
    else:                                                                                                               #if the secret message is not empty then
        Steganography.encode(original_image, output_path, text)                                                         #hiding the secret messsage in the image
        new_chat = ChatMessage(text,True)
        friends[friend_choice].chats.append(new_chat)                                                                   #Saving all the conversating with your friend
        print "Your secret message image is ready!"

def read_message():                                                                                                     #Decoding the secret message

    sender = select_a_friend()
    output_path = raw_input("What is the name of the file?")                                                            #Asking for the file name that contain secret message
    secret_text = Steganography.decode(output_path)
    new_chat = ChatMessage(secret_text, False)
    friends[sender].chats.append(new_chat)

    print "Your secret message has been saved!"
    special_words = ['SOS','SAVE ME',"HELP","DANGER"]                                                                   #These are the distress signal
    if secret_text.upper() == 'SOS' or secret_text.upper() == 'SAVE ME' or secret_text.upper() == 'HELP':               #code words for the spy being in danger
        print 'Hand tight, help has been dispatched \n'

def read_chat_history():                                                                                                #Seeing the chat history

    read_for = select_a_friend()
    print '\n'

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print '[%s] %s: %s' % (chat.time.strftime(colored("%d %B %Y",'blue')), 'You said:', chat.message)
        else:
            print '[%s] %s: %s' % (chat.time.strftime(colored("%d %B %Y", 'blue')), 'You said:', chat.message0)

def remove_a_spy():                                                                                                     #To remove a spy from the app
    spammer = select_a_friend()
    for chat in friends[spammer].chats:
        words = chat.message.split()
        if len(words) >= 100:                                                                                           #if a spy says more than 100 words than it means he is spammign the chat
            print 'You are spamming the chat that\'s why you are being removed form this app '
            del(friends[spammer])                                                                                       #deleting his entire record from the app

def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name
    if spy.age > 12 and spy.age < 50:                                                                                   #cheking whether the spy is fit to a spy
        print "Authentication complete.\n Welcome " + spy.name + ", age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard \n"


#Giving some appreciation to the spy on the basis of their rating

        if 4.0 <= spy.rating<=5:
            print 'Wow its nice to see a legendary spy! \n'
        elif 3.0 <= spy.rating <=3.9:
            print "You are one of the elite spy! \n"
        else:
            print "Huh an ordinary spy \n"

        show_menu = True
        while show_menu:                                                                                                #App will show the menu for the user to choose
            menu_choices = "What do you want to do? \n " \
                           "1. Add a status update \n " \
                           "2. Add a friend \n " \
                           "3. Send a secret message \n " \
                           "4. Read a secret message \n " \
                           "5. Read Chats from a user \n " \
                           "6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % (number_of_friends)                                                   #Showing the number of friends you have
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                    remove_a_spy()
                elif menu_choice == 6:
                    print 'Thank you for using our app, please visit us again'
                    exit()
                else:
                    print 'Invalid choice!! '
                    show_menu = False
    else:
        print 'Sorry you are not of the correct age to be a spy'

#function declatratino ends here
#-----------------------------------------------------------------------------------------------------------------------

if existing.upper() == "Y":                                                                                             #if the user chooses default profile
    start_chat(spy)
elif existing.upper() == "N":                                                                                           #if user chooses to make his own profile

    spy = Spy('','',0,0.0)
    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:                                                                                               #checking whether the name is not empty
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        spy.rating = raw_input("What is your spy rating?")
        spy.rating = float(spy.rating)

        start_chat(spy)
    else:
        print 'Please add a valid spy name'

else:
    print 'Please press Y/N'

#finally our spy chat application is complete!!