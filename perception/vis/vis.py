import argparse
import os

from perception import ALGOS
from perception.vis.FrameWrapper import FrameWrapper
import cv2 as cv
from perception.vis.window_builder import Visualizer
import cProfile as cp
import pstats
import imageio
from matplotlib.pyplot import Figure
import numpy as np

# Parse arguments
parser = argparse.ArgumentParser(description='Visualizes perception algorithms.')
parser.add_argument('--data', default='webcam', type=str)
parser.add_argument('--algorithm', type=str, required=True)
parser.add_argument('--cProfiler', default='disabled_cprof', type=str)
parser.add_argument('--save_video', action='store_true')
args = parser.parse_args()

# Get algorithm module
Algorithm = ALGOS[args.algorithm]

# Initialize image source
# detects args.data, get a list of all file directory when given a directory
# change data_source to a list of all files in the directory
if os.path.isdir(args.data):
    data_sources = os.listdir(args.data)
else:
    data_sources = [args.data]
data = FrameWrapper(data_sources, 0.25)

algorithm = Algorithm()
window_builder = Visualizer(algorithm.var_info())
video_frames = []


# Main Loop
def main():
    for frame in data:

        state, debug_frames = algorithm.analyze(
            frame, debug=True, slider_vals=window_builder.update_vars()
        )

        for i, dframe in enumerate(debug_frames):
            if isinstance(dframe, Figure):
                img = np.fromstring(dframe.canvas.tostring_rgb(), dtype=np.uint8,
                                    sep='')
                img = img.reshape(dframe.canvas.get_width_height()[::-1] + (3,))
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                debug_frames[i] = img

        to_show = window_builder.display(debug_frames)
        cv.imshow('Debug Frames', to_show)
        if args.save_video:
            video_frames.append(to_show)

        key_pressed = cv.waitKey(60) & 0xFF
        if key_pressed == 112:
            cv.waitKey(0)  # pause
        if key_pressed == 113:
            break  # quit

if args.cProfiler == 'disabled_cprof':
    main()
else:
    cp.run('main()', 'algo_stats')
    p = pstats.Stats('algo_stats')
    if args.cProfiler != 'all_methods':
        p.print_stats(args.cProfiler)
    else:
        p.print_stats()

cv.destroyAllWindows()

if args.save_video:
    height, width, _ = video_frames[0].shape
    w = imageio.get_writer('deb_cap.mp4')
    for img in video_frames:
        height2, width2, _ = img.shape
        if (height2, width2) == (height, width):
            imag = cv.resize(img, (width - (width % 16), height - (height % 16)))
            imag = cv.cvtColor(imag, cv.COLOR_BGR2RGB)
            w.append_data(imag)
    w.close()
