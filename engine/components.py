# Game Objects Components
import pygame
import math


pygame.init()

class GameObj:
    """Game Object"""
    def __init__(self):
        # Components
        self.transform = None
        self.sprite = None
        self.collider = None
        self.audio = []

class Component:
    """Component Base"""
    def __init__(self, game_obj: GameObj):
        self.game_obj = game_obj

class TransformComponent(Component):
    """Coordinates and Size"""
    def __init__(self, game_obj: GameObj, x=0, y=0, width=100, height=100):
        super().__init__(game_obj)
        self.game_obj.transform = self # Add TransformComponent to GameObj

        self.x = x
        self.y = y
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._re_size(value, self._height)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._re_size(self._width, value)

    def get_coords(self):
        return (self.x, self.y)

    def re_size(self, width: int, height: int):
        self._width = width
        self._height = height

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._resize(self._width, self._height)

class SpriteComponent(Component):
    """Sprite"""
    def __init__(self, game_obj: GameObj, path: str):
        super().__init__(game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.sprite = self # Add SpriteComponent to GameObj Components

        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (self.game_obj.transform.width, self.game_obj.transform.height))

    def _re_size(self, width: int, height: int):
        self.img = pygame.transform.scale(self.img, (width, height))

    def render(self, screen):
        screen.blit(self.img, (self.game_obj.transform.x, self.game_obj.transform.y))

    def render_to(self, screen, coords: tuple):
        screen.blit(self.img, coords)

class AnimationComponent(SpriteComponent):
    """Animation"""
    def __init__(self, game_obj: GameObj, frame_path_list: list, frame_indx=0, speed=1):
        Component.__init__(self, game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.sprite = self # Add AnimationComponent to GameObj
        self._frame_indx = frame_indx # Animation Frame Index
        self.speed = speed

        # Sprites load
        self.img_list = []
        for path in frame_path_list:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (self.game_obj.transform.width, self.game_obj.transform.height))
            self.img_list.append(img)

    @property
    def frame_indx(self):
        return math.floor(self._frame_indx)

    @frame_indx.setter
    def frame_indx(self, value):
        self._frame_indx = value

    @property
    def img(self):
        return self.img_list[self.frame_indx]

    @img.setter
    def img(self, value):
        self.img_list[self.frame_indx] = value

    def _re_size(self, width: int, height: int):
        for img in self.img_list:
            img = pygame.transform.scale(img, (width, height))

    def anim_play(self):
        self._frame_indx = (self._frame_indx + self.speed) % len(self.img_list)

class AudioComponent(Component):
    """Sounds"""
    def __init__(self, game_obj: GameObj, path: str):
        super().__init__(game_obj)

        self.game_obj.audio.append(self)

        self.audio = pygame.mixer.Sound(path)

    def play(self):
        self.audio.play()

class ColliderComponent(Component):
    """Game Objects Interaction"""
    def __init__(self, game_obj: GameObj):
        super().__init__(game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.collider = self

    def is_intersection(self, game_obj: GameObj):
        # game_obj Transform Component exsiting check
        if game_obj.transform is None:
            raise BaseException('You forget add TransformComponent to game_obj')

        return (abs(game_obj.transform.x - self.game_obj.transform.x) <= self.game_obj.transform.width) \
        and (abs(game_obj.transform.y - self.game_obj.transform.y) <= self.game_obj.transform.height)