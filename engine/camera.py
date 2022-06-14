from .components import GameObj


class Camera:
	def __init__(self, x=0, y=0) -> None:
		self.x = x
		self.y = y

	def get_local_x(self, x: int) -> int:
		return x - self.x

	def get_local_y(self, y: int) -> int:
		return y - self.y

	def get_local_coords(self, coords: tuple) -> tuple:
		return (coords[0] - self.x, coords[1] - self.y)

	def follow(self, coords: tuple, w_width: int, w_height: int) -> None:
		self.x = coords[0] - w_width // 2
		self.y = coords[1] - w_height // 2