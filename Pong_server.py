import socket
import pickle
import select

from object import Object

""" Main server for running the game
Attributes
==========
HEADERSIZE: int
    Max amount of characters for the header to be added to the msg
PORT: int
    The port number to connect too
MAX_PLAYERS: int
    The maximum number of clients that can be connect to the server
PLAYERS: list
    List of player sockets to be used by select
CLIENTS: dict
    Information about all connected sockets
BALL_MOMENTUM: int
    Speed at which ball moves
PADDLE_SPEED: int
    Speed at which player moves
SCORE: int
    Score of the game 
"""

# Global constants
HEADERSIZE = 10
PORT = 2444
MAX_PLAYERS = 2
IP = "127.0.0.1"
PLAYERS = []
CLIENTS = {}
BALL_MOMENTUM = [-0.3, 0.3]
PADDLE_SPEED = 0.3
SCORE = 0

# Initialize socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if not s:
    exit(1)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(5)
PLAYERS.append(s)

# Initialize game objects
objects = [Object((5, 5), (620/2, 480/2), (255, 255, 255)),
           Object((5, 45), (10, 480/2), (255, 255, 255)),
           Object((5, 45), (600, 480/2), (255, 255, 255))]


def receive_input(player_socket):
    """
    Get input from PLAYERS
    :param player_socket:
    :return:
    """
    try:
        command_header = player_socket.recv(HEADERSIZE)

        if not len(command_header):
            return False

        input_length = int(command_header.decode("utf-8"))
        return {"command": command_header,
                "input": player_socket.recv(input_length)}
    except:
        return False


def send_msg(player_socket, msg):
    """
    Allows the PLAYERS to send text based messages to each other
    :param player_socket:
    :param msg:
    :return:
    """
    try:
        message = f'{CLIENTS[player_socket]} ' + msg
        message = bytes(f'{len(message):<{HEADERSIZE}}' + message, "utf-8")
        player_socket.send(message)
    except:
        return False


def send_objects(player_socket):
    """
    Allows server to send game objects to players
    :param player_socket: socket
    :return:
    """
    try:
        message = pickle.dumps(objects)
        message = bytes(f'{len(message):<{HEADERSIZE}}', "utf-8") + message
        player_socket.send(message)
    except:
        return False


while True:
    # Process client requests
    read_sockets, write_sockets, exception_sockets = \
        select.select(PLAYERS, [], PLAYERS)


    # Handle when client is sending data
    for notified_socket in read_sockets:

        # Connect new client
        if notified_socket == s:
            player_socket, player_address = s.accept()

            if len(PLAYERS) <= 2:
                PLAYERS.append(player_socket)
                CLIENTS[player_socket] = (f'player{len(PLAYERS) - 1}',
                                          objects[len(PLAYERS) - 1])
                print(f"Accepted connection from {player_address}")
            else:
                # TODO make it so that extra players can spectate
                msg = "Sorry game has already started"
                msg = bytes(f'{len(msg):<{HEADERSIZE}}' + msg, "utf-8")
                player_socket.send(msg)
                player_socket.close()

        # Get input from old client
        else:
            message = receive_input(notified_socket)

            if message is False:
                print(f"Closed connection from {CLIENTS[notified_socket][0]}")
                PLAYERS.remove(notified_socket)
                CLIENTS.pop(notified_socket)
                continue

            print(f"Recieved input from {CLIENTS[notified_socket][0]}: "
                  f"{message['input'].decode('utf-8')}")

            input = message['input'].decode('utf-8')
            print(input)
            paddle = CLIENTS[notified_socket][1]
            # handle paddle logic
            if input == "up":
                if paddle.y >= 5:
                    paddle.add_force((0, -1 * PADDLE_SPEED))

            elif input == "down":
                if paddle.y <= 430:
                    paddle.add_force((0, PADDLE_SPEED))

            # Send data to other CLIENTS
            for player_socket in CLIENTS:
                # if player_socket != notified_socket:
                # Todo error trap the message that was received
                send_objects(player_socket)
                print(f"sending data to {CLIENTS[notified_socket][0]}")

    # Todo: make it so that ball interacts with the paddles
    # Todo: put the game on a seperate process from the sever
    # Todo: make it so that SCORE up dates when paddles hit end

    # Handle ball logic
    if len(PLAYERS) == 3:
        ball = objects[0]
        if 435 <= ball.y or ball.y <= 5:
            BALL_MOMENTUM[1] = BALL_MOMENTUM[1] * -1
        elif 610 <= ball.x or ball.x <= 5:
            SCORE += 1
            if BALL_MOMENTUM[1] < 0:
                BALL_MOMENTUM[0] = -0.3
            else:
                BALL_MOMENTUM[0] = 0.3
            PADDLE_SPEED = 0.3
            ball.x, ball.y = (620/2, 480/2)
            print(SCORE)

        if ball.in_bound(objects[1].rect) or ball.in_bound(objects[2].rect):
            s[0] = (BALL_MOMENTUM[0] + 0.005) * -1
            PADDLE_SPEED += 0.005
        ball.add_force(BALL_MOMENTUM)

    # Remove bad connections
    for notified_socket in exception_sockets:
        PLAYERS.remove(notified_socket)
        CLIENTS.pop(notified_socket)




