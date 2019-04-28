import cv2
import numpy as np

import sys
sys.path.insert(0, '../background_removal')
from featureGray2_higher_order_fns import init_aggregate_rescaling
from peak_removal_adaptive_thresholding import filter_out_highest_peak_multidim

if __name__ == "__main__":
    cap = cv2.VideoCapture('../data/course_footage/GOPR1142.mp4')

def init_combined_filter():
    aggregate_rescaling = init_aggregate_rescaling()

    def combined_filter(frame, display_figs=False):
        pca_frame = aggregate_rescaling(frame) # this resizes the frame within its body

        __, other_frame = filter_out_highest_peak_multidim(
                                    np.dstack([pca_frame]), percentile=20)
        other_frame = other_frame[:,:,:3]

        if display_figs:
            cv2.imshow('original', frame)
            cv2.imshow('pca thing', pca_frame)
            cv2.imshow('other filter thing', other_frame)
        return other_frame
    return combined_filter

if __name__ == "__main__":
    ret = True
    ret_tries = 0
    while 1 and ret_tries < 50:
        combined_filter = init_combined_filter()
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            filtered_frame = combined_filter(frame, True)

            ret_tries = 0
            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break
        else:
            ret_tries += 1