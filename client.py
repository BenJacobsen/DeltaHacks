import socket
import select
import errno
import sys
import tkinter as tk

class client_ui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def submit(self):
        if  self.username == "":
            self.username = self.entry_text.get()
        self.submit_done = True


    def setStateLoading(self, stateText):
        self.text["text"] = stateText
        self.hide_interaction()

    def setStatePrompt(self, prompt):
        self.entry_text.set("")
        self.text["text"] = prompt
        self.show_interaction()
        self.submit_done = False


    def create_widgets(self):
        self.text = tk.Label(self, text = "Please input your username", width = '50')
        self.text.pack()
        self.entry_text = tk.StringVar(self)
        self.entry = tk.Entry(self, bd = 5, textvariable = self.entry_text, width = 200)
        self.entry.pack()
        self.submit = tk.Button(self, text="Submit", fg="black", command = self.submit, width = "100")
        self.submit.pack(side="bottom")
        self.submit_done = False
        self.username = ""

    def update_text(self, text):
        self.text["text"] = text
        self.text.pack()

    def hide_interaction(self):
        self.submit.pack_forget()
        self.entry.pack_forget()

    def show_interaction(self):
        self.entry.pack()
        self.submit.pack()






root = tk.Tk()
ui = client_ui(master=root)
while True:
    ui.update()
    ui.update_idletasks()
    if ui.submit_done:
        ui.setStateLoading("Waiting for other players...")
        ui.update()
        ui.update_idletasks()
        break


HEADER_LENGTH = 10



IP = "127.0.0.1"
PORT = 1234
my_username = ui.username
print("done")
#my_username = "ben"
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
#send username
#if user_message:

    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
    #user_message = message.encode('utf-8')
    #user_message_header = f"{len(user_message):<{HEADER_LENGTH}}".encode('utf-8')
    #client_socket.send(user_message_header + user_message)

while True:

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            prompt_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(prompt_header):
                print('Connection closed by the server')
                sys.exit()

            prompt_length = int(prompt_header.decode('utf-8').strip())
            prompt = client_socket.recv(prompt_length).decode('utf-8')

            # Print message    TURN INTO GENERAL FUNCTION
            ui.setStatePrompt(f'{prompt}')

            while True:
                ui.update()
                ui.update_idletasks()
                if ui.submit_done:
                    ui.setStateLoading("Waiting for other players to respond...")
                    ui.update()
                    ui.update_idletasks()
                    break


                # Wait for user to input a message
            message = ui.entry_text.get()
            #message = input(f'{res_pretext} > ')
    # If message is not empty - send it
            if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()