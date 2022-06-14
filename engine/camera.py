import sys
sys.path.append('../')

from PyEngine.config import WINDOW_WIDTH, WINDOW_HEIGHT
from .components import GameObj


class Camera:
	def __init__(self, x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT) -> None:
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def get_local_x(self, x: int) -> int:
		return x - self.x

	def get_local_y(self, y: int) -> int:
		return y - self.y

	def get_local_coords(self, coords: tuple) -> tuple:
		return (coords[0] - self.x, coords[1] - self.y)
	
	@property
	def width_coeff(self) -> float:
		return WINDOW_WIDTH / self.width

	@width_coeff.setter
	def width_coeff(self, value) -> None:
		self.width = int(WINDOW_WIDTH / self.width)

	@property
	def height_coeff(self) -> None:
		return WINDOW_HEIGHT / self.height
	
	@height_coeff.setter
	def height_coeff(self, value) -> float:
		self.height = int(WINDOW_HEIGHT / value)

	def follow(self, coords: tuple) -> None:
		self.x = coords[0] - self.width // 2
		self.y = coords[1] - self.height // 2