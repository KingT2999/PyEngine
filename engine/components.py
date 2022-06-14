# Game Objects Components
import copy
import pygame
import math


pygame.init()

class GameObj:
    """Game Object"""
    def __init__(self) -> None:
        # Components
        self.transform = None
        self.sprite = None
        self.collider = None
        self.audio = None

    def spawn(self):
        game_obj = copy.copy(self)

        if self.transform is not None:
            game_obj.transform = copy.copy(self.transform)
            game_obj.transform.game_obj = game_obj

        if self.sprite is not None:
            game_obj.sprite = copy.copy(self.sprite)
            game_obj.sprite.game_obj = game_obj

        if self.collider is not None:
            game_obj.collider = copy.copy(self.collider)
            game_obj.collider.game_obj = game_obj

        if self.audio is not None:
            game_obj.audio = copy.copy(self.audio)
            game_obj.audio.game_obj = game_obj


        return game_obj

class Component:
    """Component Base"""
    def __init__(self, game_obj: GameObj) -> None:
        self.game_obj = game_obj

class TransformComponent(Component):
    """Coordinates and Size"""
    def __init__(self, game_obj: GameObj, x=0, y=0, width=100, height=100) -> None:
        super().__init__(game_obj)
        self.game_obj.transform = self # Add TransformComponent to GameObj

        self.x = x
        self.y = y
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._re_size(value, self._height)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._re_size(self._width, value)

    def get_coords(self) -> tuple:
        return (self.x, self.y)

    def re_size(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

        if self.game_obj.sprite is not None:
            self.game_obj.sprite._resize(self._width, self._height)

class SpriteComponent(Component):
    """Sprite"""
    def __init__(self, game_obj: GameObj, path: str) -> None:
        super().__init__(game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.sprite = self # Add SpriteComponent to GameObj Components

        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (self.game_obj.transform.width, self.game_obj.transform.height))

    def _re_size(self, width: int, height: int) -> None:
        self.img = pygame.transform.scale(self.img, (width, height))
    
    def __get_resized_img(self, size: tuple) -> pygame.SurfaceType:
        img = copy.copy(self.img)
        img = pygame.transform.scale(img, size)

        return img

    def render(self, screen, size=None) -> None:
        if size is None:
            screen.blit(self.img, (self.game_obj.transform.x, self.game_obj.transform.y))
        else:
            screen.blit(self.__get_resized_img(size), (self.game_obj.transform.x, self.game_obj.transform.y))

    def render_to(self, screen, coords: tuple, size=None) -> None:
        if size is None:
            screen.blit(self.img, coords)
        else:
            screen.blit(self.__get_resized_img(size), coords)

class AnimationComponent(SpriteComponent):
    """Animation"""
    def __init__(self, game_obj: GameObj, frame_path_list: list, frame_indx=0, speed=1) -> None:
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
    def frame_indx(self) -> int:
        return math.floor(self._frame_indx)

    @frame_indx.setter
    def frame_indx(self, value) -> None:
        self._frame_indx = value

    @property
    def img(self) -> pygame.SurfaceType:
        return self.img_list[self.frame_indx]

    @img.setter
    def img(self, value) -> None:
        self.img_list[self.frame_indx] = value

    def _re_size(self, width: int, height: int) -> None:
        for img in self.img_list:
            img = pygame.transform.scale(img, (width, height))

    def anim_play(self) -> None:
        self._frame_indx = (self._frame_indx + self.speed) % len(self.img_list)

class AudioComponent(Component):
    """Sounds"""
    def __init__(self, game_obj: GameObj, path: str) -> None:
        super().__init__(game_obj)

        if self.game_obj.audio is None:
            self.game_obj.audio = []

        self.game_obj.audio.append(self)

        self.audio = pygame.mixer.Sound(path)

    def play(self) -> None:
        self.audio.play()

class ColliderComponent(Component):
    """Game Objects Interaction"""
    def __init__(self, game_obj: GameObj) -> None:
        super().__init__(game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.collider = self

    def is_intersection(self, game_obj: GameObj) -> bool:
        # game_obj Transform Component exsiting check
        if game_obj.transform is None:
            raise BaseException('You forget add TransformComponent to game_obj')

        return (abs(game_obj.transform.x - self.game_obj.transform.x) <= self.game_obj.transform.width) \
        and (abs(game_obj.transform.y - self.game_obj.transform.y) <= self.game_obj.transform.height)
