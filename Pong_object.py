import pygame
class Object:
    """Represents how all the items in the game should look. This class includes
    attributes and methods all items must have.
    Attributes:
    ===========
    width: int
        the with of the object
    height:
        the height of the object
    x: int
        the x coordinate
    y: int
        the y coordinate
    color: tuple
        the color of the item in rgb
    rect: pygame.rect.RectType
        pygame representation of the object

    Methods:
    ========
    render(Surface) -> None
        draw the item onto the surface
    update(x, y) -> None
        change the position of the item
    in_bounds(item) -> bool
        checks if the passed in item touches the current item
    position() -> tuple
        returns the current (x,y) coordinate of the item
    Representation Invariants
    =========================
    0 <= x <= board width
    0 <= y <= board height
    width is a multiple of the game array length and the board size
    height is a multiple of the game array width and the board size
    colour's elements are in the range 0 - 255 as a tuple(int, int, int)
    """
    width = int
    height = int
    x: int
    y: int
    color: tuple
    rect: pygame.rect.RectType

    def __init__(self, size: tuple, position: tuple, color: tuple):
        self.width, self.height = size
        self.x, self.y = position
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, scene: pygame.Surface) -> None:
        """Defines how the function should be drawn on the screen
        :param scene: Main scene the game is showing.
        """
        dimensions = (self.x, self.y, self.width, self.height)
        rect = pygame.draw.rect(scene, self.color, dimensions)

    def update(self, position: tuple) -> None:
        """Updates the x y coordinate of the game.
        :param position: a tuple in the form (x: int, y: int)
        """
        self.x, self.y = position

    def add_force(self, position: tuple) -> None:
        """Updates the x y coordinate of the game.
        :param position: a tuple in the form (x: int, y: int)
        """
        self.x += position[0]
        self.y += position[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def in_bound(self, item2: pygame.rect.RectType) -> bool:
        """Checks to see if two objects are touching.
        :param item2: an item object
        :return: True if touching, False if not
        """
        print(type(item2))
        return self.rect.colliderect(item2)

    def __str__(self) -> None:
        self.render()
