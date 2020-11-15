import numpy as np
import cv2 as cv
import math
from typing import Dict, Tuple, List

def nothing(x):
	pass

class Visualizer:
	def __init__(self, vars: Dict[str, Tuple[Tuple[int, int], int]]):
		self.variables = vars.keys()
		cv.namedWindow('Debug Frames')
		for name, info in vars.items():
			range, default_val = info
			low_range, high_range = range
			cv.createTrackbar(name, 'Debug Frames', low_range, high_range, nothing)
			cv.setTrackbarPos(name, 'Debug Frames', default_val)

	def three_stack(self, frames: List[np.ndarray]) -> List[np.ndarray]:
		newLst = []
		for frame in frames:
			if len(frame.shape) == 2 or frame.shape[2] == 1:
				frame = np.stack((frame, frame, frame), axis=2)
			newLst.append((frame))
		return newLst

	def display(self, frames: List[np.ndarray]) -> np.ndarray:
		num_frames = len(frames)
		assert (num_frames > 0 and num_frames <= 9), 'Invalid number of frames!'
		frames = self.three_stack(frames)

		columns = math.ceil(num_frames/math.sqrt(num_frames))
		rows = math.ceil(num_frames/columns)
		frame_num = 0
		to_show = 0
		for j in range(rows):
			this_row = frames[frame_num]
			for i in range(columns * j + 1, columns * (j + 1)):
				frame_num += 1
				if frame_num < num_frames:
					to_add = frames[frame_num]
					this_row = np.hstack((this_row, to_add))
				else:
					this_row = np.hstack((this_row, np.zeros(frames[0].shape, dtype=np.uint8)))
			if type(to_show) != int:
				to_show = np.vstack((to_show, this_row))
			else:
				to_show = this_row
			frame_num += 1
		return to_show

	def update_vars(self) -> Dict[str, int]:
		variable_values = {}
		for var in self.variables:
			variable_values[var] = cv.getTrackbarPos(var, 'Debug Frames')
		return variable_values