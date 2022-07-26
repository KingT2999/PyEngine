# Game Objects Components
from abc import ABC, abstractmethod
import copy
import pygame


pygame.init()

class IGameObj(ABC):
    @abstractmethod
    def spawn(self): pass

class GameObj(IGameObj):
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

#<=======================Components=======================>
class IComponent(ABC):
    game_obj: GameObj

class Component(IComponent):
    """Component Base"""
    def __init__(self, game_obj: GameObj) -> None:
        self.game_obj = game_obj

# Transform Component
class ITransformComponent(IComponent):
    """Coordinates and Size"""
    x: int
    y: int
    width: int
    height: int

    @abstractmethod
    def get_coords(self): pass

    @abstractmethod
    def re_size(self): pass

class TransformComponent(Component, ITransformComponent):
    """Coordinates and Size"""
    def __init__(self, game_obj: GameObj, x=0, y=0, width=100, height=100) -> None:
        Component.__init__(self, game_obj)
        self.game_obj.transform = self # Add TransformComponent to GameObj

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_coords(self) -> tuple:
        return (self.x, self.y)

    def re_size(self, size: tuple) -> None:
        self.width, self.height = size

# Sprite Component
class ISpriteComponent(IComponent):
    """Sprite"""
    img: pygame.Surface

    @abstractmethod
    def _get_resized_img(self): pass

    @abstractmethod
    def render(self): pass

    @abstractmethod
    def render_to(self): pass

class SpriteComponent(ISpriteComponent, Component):
    """Sprite"""
    def __init__(self, game_obj: GameObj, path: str) -> None:
        Component.__init__(self, game_obj)

        # Transform Component exsiting check
        if self.game_obj.transform is None:
            raise BaseException('You forget add TransformComponent')

        self.game_obj.sprite = self # Add SpriteComponent to GameObj Components

        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (self.game_obj.transform.width, self.game_obj.transform.height))

    # Img Resizing
    def _get_resized_img(self, size: tuple) -> pygame.Surface:
        img = copy.copy(self.img)
        img = pygame.transform.scale(img, size)

        return img

    # Rendering
    def render(self, screen: pygame.SurfaceType, size=None) -> None:
        if size is None:
            img = self._get_resized_img((self.game_obj.transform.width, self.game_obj.transform.height))
            screen.blit(img, (self.game_obj.transform.x, self.game_obj.transform.y))
        else:
            screen.blit(self._get_resized_img(size), (self.game_obj.transform.x, self.game_obj.transform.y))

    def render_to(self, screen, coords: tuple, size=None) -> None:
        if size is None:
            screen.blit(self.img, coords)
        else:
            screen.blit(self._get_resized_img(size), coords)

# Animation Component
class IAnimationComponent(ISpriteComponent):
    """Animation"""
    _frame_indx: float
    speed: int
    img_list: list
    
    @property
    @abstractmethod
    def frame_indx(self): pass

    @frame_indx.setter
    @abstractmethod
    def frame_indx(self): pass

    @property
    @abstractmethod
    def img(self): pass

    @img.setter
    @abstractmethod
    def img(self): pass

    @abstractmethod
    def anim_play(self): pass


class AnimationComponent(IAnimationComponent, SpriteComponent):
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
        return int(self._frame_indx)

    @frame_indx.setter
    def frame_indx(self, value) -> None:
        self._frame_indx = value

    @property
    def img(self) -> pygame.SurfaceType:
        return self.img_list[self.frame_indx]

    @img.setter
    def img(self, value) -> None:
        self.img_list[self.frame_indx] = value

    def anim_play(self) -> None:
        self._frame_indx = (self._frame_indx + self.speed) % len(self.img_list)

# Audio Component
class IAudioComponent(IComponent):
    """Sounds"""
    audio: pygame.mixer.Sound

    @abstractmethod
    def play(self): pass

class AudioComponent(IAudioComponent, Component):
    """Sounds"""
    def __init__(self, game_obj: GameObj, path: str) -> None:
        Component.__init__(self, game_obj)

        if self.game_obj.audio is None:
            self.game_obj.audio = []

        self.game_obj.audio.append(self)

        self.audio = pygame.mixer.Sound(path)

    def play(self) -> None:
        self.audio.play()

# Collider Component
class IColliderComponent(IComponent):
    """Game Objects Interaction"""

    @abstractmethod
    def is_intersection(self): pass

class ColliderComponent(IColliderComponent, Component):
    """Game Objects Interaction"""
    def __init__(self, game_obj: GameObj) -> None:
        Component.__init__(self, game_obj)

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