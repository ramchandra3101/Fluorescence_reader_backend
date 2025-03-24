import cv2
import numpy as np

class ContourAnalyzer:
    @staticmethod
    def calculate_centroid(contour):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY
        else:
            return None
       

    @staticmethod
    def group_into_rows(centroids, threshold=50):
        rows = []
        for centroid in centroids:
            added = False
            for row in rows:
                if abs(row[0][1] - centroid[1]) < threshold:
                    row.append(centroid)
                    added = True
                break
        if not added:
            rows.append([centroid])
        return rows

    @staticmethod
    def map_contours_to_rows(centroids, contours, rows):
        row_contours = [[] for _ in range(len(rows))]

        for i, row in enumerate(rows):
            for centroid in row:
            # Find the closest contour to the centroid
                closest_contour = min(contours, key=lambda c: np.linalg.norm(np.array(centroid) - np.array(ContourAnalyzer.calculate_centroid(c))))
                closest_contour=np.array(closest_contour)
                row_contours[i].append(closest_contour)

        return row_contours[::-1]

    @staticmethod
    def calculate_average_rgb(image, row_contours):
        average_rgb_values = []
        for row in row_contours:
            row_averages = []
            for contour in row:
                # Create a mask for the current contour
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
                
                # Extract the RGB values using the mask
                masked_image = cv2.bitwise_and(image, image, mask=mask)
                rgb_pixels = masked_image[mask == 255]
                
                # Calculate average RGB value
                if len(rgb_pixels) > 0:
                    avg_rgb = np.mean(rgb_pixels, axis=0)
                    row_averages.append(avg_rgb.tolist())
                else:
                    row_averages.append([0, 0, 0])  # If no pixel found, return black
            average_rgb_values.append(row_averages)
        return average_rgb_values
    
        
    

    
    