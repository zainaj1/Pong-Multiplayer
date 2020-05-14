import sys
from typing import List
import socket
import pygame
import errno
import pickle

from object import Object
""" Main client for playing the game

Attributes
==========
HEADERSIZE: int
    Max amount of characters for the header to be added to the msg
PORT: int
    The port number to connect too
MAX_PLAYERS: int
    The maximum number of clients that can be connect to the server
IP: int
    The ip of the server to connect to
    
Methods
=======
render(List[Objects]) -> None
    renders the objects onto pygame screen as rectangles 
"""

HEADERSIZE = 10
PORT = 2444
MAX_PLAYERS = 2
IP = "127.0.0.1"

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# Initialize pygame
pygame.init()
(width, height) = (620, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
clock = pygame.time.Clock()


def render(objects: List[Object]) -> None:
    """ Render the objects onto the pygame screen"""
    for object in objects:
        object.render(screen)


while True:
    clock.tick(420)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys_pressed = pygame.key.get_pressed()
    # Detect key input and send to server
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        msg = "up"
        msg = bytes(f'{len(msg):<{HEADERSIZE}}' + msg, "utf-8")
        client_socket.send(msg)
    elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        msg = "down"
        msg = bytes(f'{len(msg):<{HEADERSIZE}}' + msg, "utf-8")
        client_socket.send(msg)
    else:
        msg = " "
        msg = bytes(f'{len(msg):<{HEADERSIZE}}' + msg, "utf-8")
        client_socket.send(msg)

    try:
        while True:
            # Get data from server
            msg_header = client_socket.recv(HEADERSIZE)
            if not len(msg_header):
                print("Connection failed")
                sys.exit()
            msg_len = int(msg_header.decode("utf-8"))
            msg = client_socket.recv(msg_len)

            objects = pickle.loads(msg)
            render(objects)
            pygame.display.flip()
            screen.fill((0, 0, 0))

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Read error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print(' General Error', str(e))
        sys.exit()




