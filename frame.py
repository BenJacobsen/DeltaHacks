import socket
import select
HEADER_LENGTH = 10
PORT = 1234

class player:
    def __init__(self, name):
        self.name = name
        self.prompts = []
        self.responses = []

class game:
    def __init__(self, url, prompts, prompt_assign_func, round_start_func, round_end_func, end_func, max_players, max_rounds): #front_end
        self.players = {}
        self.player_keys = []
        self.num_players = 0
        self.round_num = 0
        self.num_answers = 0

        self.IP = url
        self.prompts = prompts
        self.prompt_assign_func = prompt_assign_func
        self.round_start_func = round_start_func
        self.round_end_func = round_end_func
        self.end_func = end_func
        
        self.max_players = max_players
        self.max_rounds = max_rounds

        
    
    def setup_after_login(self):
        sorted_prompts = self.prompt_assign_func(self)
        for i in range(0, len(self.player_keys)):
            self.players[self.player_keys[i]].prompts = sorted_prompts[i]
        if self.max_rounds == 0:
            for prompt in sorted_prompts:
                if len(prompt) > self.max_rounds:
                    self.max_rounds = len(prompt)

    def start(self):
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
        server_socket.bind((self.IP, PORT))

        # This makes server listen to new connections
        server_socket.listen()

        # List of sockets for select.select()
        #sockets_list = [server_socket]
        sockets_list = []
        server_list = [server_socket]
        # List of connected clients - socket as a key, user header and name as data

        print(f'Listening for connections on {self.IP}:{PORT}...')


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
                return player(name[2:-1])
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
                return str(client_socket.recv(message_length))[2:-1]

            except:

                # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
                # or just lost his connection
                # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
                # and that's also a cause when we receive an empty message
                return False

        def perform_round():
            for player_socket in self.player_keys:
                prompt = self.players[player_socket].prompts[self.round_num]
                prompt_header = f"{len(prompt):<{HEADER_LENGTH}}".encode('utf-8')
                player_socket.send(prompt_header + prompt.encode('utf-8'))
            self.round_num += 1
                



        #Loop for accepting users
        while self.num_players < self.max_players or (self.round_num <= self.max_rounds and self.num_answers < self.num_players):

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
                if notified_socket == server_socket and self.num_players < self.max_players:

                    # Accept new connection
                    # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                    # The other returned object is ip/port set
                    client_socket, client_address = server_socket.accept()
                    if self.num_players >= self.max_players:
                        #print()
                        print("bad_login")
                        continue
                    # Client should send his name right away, receive it
                    #print(player.name)
                    #print(player.id)
                    # If False - client disconnected before he sent his name
                    #print(self.num_players)
                    #print(self.max_players)


                    self.num_players += 1
                    
                    # Add accepted socket to select.select() list
                    sockets_list.append(client_socket)
                    # Also save username and username header
                    self.players[client_socket] = receive_login(client_socket)
                    print('Accepted new connection from {}:{}, username: {}.'.format(*client_address, self.players[client_socket].name))
                    if (self.num_players == self.max_players):
                        self.player_keys = sockets_list
                        self.setup_after_login()
                        perform_round()
                        self.round_start_func(self)

                # Else existing socket is sending a message
                else:
                    #check if already answered
                    if len(self.players[notified_socket].responses) == self.round_num - 1:
                        self.num_answers += 1
                        self.players[notified_socket].responses.append(receive_response(notified_socket))
                        #everyone answered
                        if self.num_answers == self.num_players and self.round_num < self.max_rounds:
                            self.round_end_func(self)
                            perform_round()
                            self.round_start_func(self)
                            self.num_answers = 0



            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)
        #for key,value in self.players.items():
        #    print(key)
        #print(sockets_list[0])
        #print(self.players[self.player_keys].responses[0])
        self.end_func(self)
                # Remove from our list of users



