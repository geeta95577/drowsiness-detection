import numpy as np

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def mouth_aspect_ratio(landmarks, MOUTH):
    # Commonly used mouth landmark pairs
    top_bottom_1 = euclidean_distance(landmarks[MOUTH[3]], landmarks[MOUTH[13]])  # 80 - 14
    top_bottom_2 = euclidean_distance(landmarks[MOUTH[4]], landmarks[MOUTH[14]])  # 81 - 87
    top_bottom_3 = euclidean_distance(landmarks[MOUTH[5]], landmarks[MOUTH[15]])  # 82 - 178

    # Horizontal mouth width
    left_right = euclidean_distance(landmarks[MOUTH[0]], landmarks[MOUTH[8]])    # 78 - 312

    # MAR formula
    MAR = (top_bottom_1 + top_bottom_2 + top_bottom_3) / (3.0 * left_right)
    return MAR
