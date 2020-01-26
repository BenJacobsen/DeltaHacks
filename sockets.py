import socket
import select
from frame import game, player
HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
def prompt_assign(num_players, prompts):
    return [[prompts[0], prompts[1]] for i in range(num_players)]
gamer = game('localhost', ['Favorite Sport?', 'Favorite Food?'], prompt_assign, 2)

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
#sockets_list = [server_socket]
sockets_list = []
server_list = [server_socket]
# List of connected clients - socket as a key, user header and name as data

print(f'Listening for connections on {IP}:{PORT}...')


def receive_login(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        name = str(client_socket.recv(message_length))
        # Return an object of message header and message data
        return player(name)
        #return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False
# Handles message receiving
def receive_response(client_socket):

    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        # Return an object of message header and message data
        return str(client_socket.recv(message_length))

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

def perform_round():
    print("round")
    print(gamer.round_num)
    for player_socket in gamer.player_keys:
        prompt = gamer.players[player_socket].prompts[gamer.round_num]
        prompt_header = f"{len(prompt):<{HEADER_LENGTH}}".encode('utf-8')
        player_socket.send(prompt_header + prompt.encode('utf-8'))
    gamer.round_num += 1
        



#Loop for accepting users
while gamer.num_players < gamer.max_players or (gamer.round_num <= gamer.max_rounds and gamer.num_answers < gamer.num_players):

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(server_list + sockets_list, [], server_list + sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket and gamer.num_players < gamer.max_players:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()
            if gamer.num_players >= gamer.max_players:
                #print()
                print("bad_login")
                continue
            # Client should send his name right away, receive it
            #print(player.name)
            #print(player.id)
            # If False - client disconnected before he sent his name
            #print(gamer.num_players)
            #print(gamer.max_players)


            gamer.num_players += 1
            
            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            # Also save username and username header
            gamer.players[client_socket] = receive_login(client_socket)
            print('Accepted new connection from {}:{}, username: {}.'.format(*client_address, gamer.players[client_socket].name))
            if (gamer.num_players == gamer.max_players):
                gamer.player_keys = sockets_list
                gamer.setup_after_login()
                perform_round()
        # Else existing socket is sending a message
        else:
            #client_socket, client_address = server_socket.accept()
            #print(gamer.players[notified_socket].name)
            #print(len(gamer.players[notified_socket].responses))
            #print(gamer.round_num)
            if len(gamer.players[notified_socket].responses) == gamer.round_num - 1:
                gamer.num_answers += 1
                print("here")
                gamer.players[notified_socket].responses.append(receive_response(notified_socket))
                print(gamer.players[notified_socket].responses[0])
                if gamer.num_answers == gamer.num_players and gamer.round_num < gamer.max_rounds:
                    perform_round()
                    gamer.num_answers = 0



    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)
#for key,value in gamer.players.items():
#    print(key)
#print(sockets_list[0])
#print(gamer.players[gamer.player_keys].responses[0])
print("GAME OVER")
        # Remove from our list of users