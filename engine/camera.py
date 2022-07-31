from abc import ABC, abstractmethod
import sys
sys.path.append('../')

from PyEngine.config import WINDOW_WIDTH, WINDOW_HEIGHT
from .components import GameObj


class ICamera:
	x: int
	y: int
	width: int
	height: int
	CURRENT_CAMERA: 'Camera'

	@property
	@abstractmethod
	def width_coeff(self): pass

	@width_coeff.setter
	@abstractmethod
	def width_coeff(self, value): pass

	@property
	@abstractmethod
	def height_coeff(self): pass

	@height_coeff.setter
	@abstractmethod
	def height_coeff(self, value): pass

	@abstractmethod
	def get_local_x(self): pass

	@abstractmethod
	def get_local_y(self): pass

	@abstractmethod
	def get_local_coords(self): pass

	@abstractmethod
	def follow(self): pass

class Camera(ICamera):
	CURRENT_CAMERA: 'Camera'

	def __init__(self, x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT) -> None:
		self.x = x
		self.y = x
		self.width = width
		self.height = height
	
	# Scale Coefficient
	@property
	def width_coeff(self) -> float:
		return WINDOW_WIDTH / self.width

	@width_coeff.setter
	def width_coeff(self, value) -> None:
		self.width = int(WINDOW_WIDTH / value)

	@property
	def height_coeff(self) -> None:
		return WINDOW_HEIGHT / self.height

	@height_coeff.setter
	def height_coeff(self, value) -> float:
		self.height = int(WINDOW_HEIGHT / value)

	# Local Coords
	def get_local_x(self, x: int) -> int:
		return (x - self.x) * self.width_coeff

	def get_local_y(self, y: int) -> int:
		return (y - self.y) * self.height_coeff

	def get_local_coords(self, coords: tuple) -> tuple:
		return ((coords[0] - self.x) * self.width_coeff, (coords[1] - self.y) * self.height_coeff)

	def follow(self, coords: tuple) -> None:
		self.x = coords[0] - (self.width) // 2
		self.y = coords[1] - (self.height) // 2

# camera = Camera(0, 0, 500, 500)
Camera.CURRENT_CAMERA = Camera(0, 0, 500, 500)