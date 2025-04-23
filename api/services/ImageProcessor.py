import cv2
import numpy as np
import os
from django.conf import settings
from .JsonFormatter import JSONFormatter
from .ContourAnalyzer import ContourAnalyzer

class ImageProcessor:
    """To process RGB Values"""
    def __init__(self):
        self.contour_analyzer = ContourAnalyzer()
        self.json_formatter = JSONFormatter()
        
    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Error: Could not load an Image")
        
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Convert to RGB Image
        imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #Convert to HSV Image
        lowerYellow = np.array([23, 100, 100])
        upperYellow = np.array([100, 255, 255])
        mask = cv2.inRange(imageHSV, lowerYellow, upperYellow)
        yellow_only = cv2.bitwise_and(image, image, mask=mask)#Yellow areas in the regions only display
        finalImage = cv2.GaussianBlur(yellow_only, (5, 5), 0)
        gray_image = cv2.cvtColor(finalImage, cv2.COLOR_BGR2GRAY)
        _,binaryImage = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binaryImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tubeContours = []
        areas = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:
                x, y, w, h = cv2.boundingRect(contour)
                aspectRatio = w/h if h!=0 else 0
                if aspectRatio > 0.5 and aspectRatio < 2.0:
                    tubeContours.append(contour)
                    areas.append(area)
        centroids = []
        for contour in tubeContours:
            centroid = ContourAnalyzer.calculate_centroid(contour)
            if centroid:
                centroids.append(centroid)
        
        filtered_centroids = []
        for i in range(len(centroids)):
            include_centroid = True
            for j in range(i + 1, len(centroids)):
                distance = np.sqrt((centroids[i][0] - centroids[j][0])**2 + (centroids[i][1] - centroids[j][1])**2)
                if distance < 100:
                    include_centroid = False  # Mark for removal
                    break  # No need to compare further with this centroid
            if include_centroid:
                filtered_centroids.append(centroids[i])
        rows = ContourAnalyzer.group_into_rows(filtered_centroids)
        for row in rows:
            row.sort(key=lambda c: c[0])
        row_contours = ContourAnalyzer.map_contours_to_rows(filtered_centroids, tubeContours, rows)
        average_RGB_values = ContourAnalyzer.calculate_average_rgb(imageRGB, row_contours)
        result_json = JSONFormatter.generate_json(average_RGB_values)
        contoured_image = cv2.drawContours(image, [np.array(contour) for row in row_contours for contour in row], -1, (0, 255, 0), 2)
        return result_json
        
    



            
            



            
