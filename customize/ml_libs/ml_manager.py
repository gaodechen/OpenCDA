# -*- coding: utf-8 -*-

"""
Since multiple CAV normally use the same ML/DL model, here we have this class to enable different
CAVs share the same model to avoid duplicate memory consumption.
"""

# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: MIT

import cv2
import torch
import sklearn


class MLManager(object):
    """
    A class that should contain all the ML models you want to initialize.
    """
    def __init__(self):
        """
        Construction class.
        """
        self.object_detector = torch.hub.load('ultralytics/yolov5', 'yolov5m')

    def draw_2d_box(self, result, rgb_image):
        """
        Draw 2d bounding box based on the yolo detection.
        Args:
            result (yolo.Result):Detection result from yolo 5.
            rgb_image (np.ndarray): Camera rgb image.

        Returns:
            (np.ndarray): camera image with bbx drawn.
        """
        # torch.Tensor
        bounding_box = result.xyxy[0]
        if bounding_box.is_cuda:
            bounding_box = bounding_box.cpu().detach().numpy()
        else:
            bounding_box = bounding_box.detach().numpy()

        for i in range(bounding_box.shape[0]):
            detection = bounding_box[i]

            # the label has 80 classes, which is the same as coco dataset
            label = int(detection[5])
            label_name = result.names[label]

            # todo: temporary, we need a filter to filter out labels.
            if label_name == 'airplane':
                continue
            x1, y1, x2, y2 = int(detection[0]), int(detection[1]), int(detection[2]), int(detection[3])
            cv2.rectangle(rgb_image, (x1,  y1), (x2, y2), (0, 255, 0), 2)
            # draw text on it
            cv2.putText(rgb_image, label_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 1)

        return rgb_image

