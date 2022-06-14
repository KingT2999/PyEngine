import sys
sys.path.append('../')

from PyEngine.config import WINDOW_WIDTH, WINDOW_HEIGHT
from .components import GameObj


class Camera:
	def __init__(self, x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT) -> None:
		self.x = x
		self.y = y
		self._width = width
		self._height = height
	
	# Scale Coefficient
	@property
	def width_coeff(self) -> float:
		return WINDOW_WIDTH / self._width

	@width_coeff.setter
	def width_coeff(self, value) -> None:
		self._width = int(WINDOW_WIDTH / self._width)

	@property
	def height_coeff(self) -> None:
		return WINDOW_HEIGHT / self._height

	@height_coeff.setter
	def height_coeff(self, value) -> float:
		self._height = int(WINDOW_HEIGHT / value)
	
	# Size Getters and Setters
	@property
	def width(self) -> int:
		return self._width
	
	@width.setter
	def width(self, value) -> None:
		self._width = value
	
	@property
	def height(self) -> int:
		return self._height
	
	@height.setter
	def height(self, value) -> None:
		self._height = value

	def get_local_x(self, x: int) -> int:
		return x - self.x

	def get_local_y(self, y: int) -> int:
		return y - self.y

	def get_local_coords(self, coords: tuple) -> tuple:
		return (coords[0] - self.x, coords[1] - self.y)
	


	def follow(self, coords: tuple) -> None:
		self.x = coords[0] - (self._width) // 2
		self.y = coords[1] - (self._height) // 2