import cv2
import numpy as np
from hand_info import *

def draw_landmarks(frame, hand_landmarks):
    """draw hand landmarks as green circles"""
    if hand_landmarks:
        for hand in hand_landmarks:
            for lm in hand:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

def draw_triangles(frame, hand_landmarks):
    """draw triangles between thumb, index and middle fingertips"""
    if hand_landmarks:
        for hand in hand_landmarks:
            points = []
            for lm_idx in [THUMB_TIP, INDEX_TIP, MIDDLE_TIP]:
                lm = hand[lm_idx]
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                points.append((x, y))
            cv2.line(frame, points[0], points[1], (255, 0, 0), 2)
            cv2.line(frame, points[1], points[2], (255, 0, 0), 2)
            cv2.line(frame, points[2], points[0], (255, 0, 0), 2)

def draw_hand_skeleton(frame, hand_landmarks, connections = HAND_CONNECTIONS, color=(0,255,0)):
    """draw lines between hand joints"""
    if hand_landmarks:
        for hand in hand_landmarks:
            for start_idx, end_idx in connections:
                start = hand[start_idx]
                end = hand[end_idx]
                x1, y1 = int(start.x * frame.shape[1]), int(start.y * frame.shape[0])
                x2, y2 = int(end.x * frame.shape[1]), int(end.y * frame.shape[0])
                cv2.line(frame, (x1, y1), (x2, y2), color, 2)

def get_angle(result, hand_name, lm1, lm2, lm3):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None 
    v1 = np.array([hand[lm1].x - hand[lm2].x, hand[lm1].y - hand[lm2].y, hand[lm1].z - hand[lm2].z])
    v2 = np.array([hand[lm3].x - hand[lm2].x, hand[lm3].y - hand[lm2].y, hand[lm3].z - hand[lm2].z])
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    dot_product = np.dot(v1_norm, v2_norm)
    angle_radians = np.arccos(dot_product)
    angle_deg = np.degrees(angle_radians)
    return angle_deg

def get_triangle_area_2d(result, hand_name, lm1=INDEX_TIP, lm2=MIDDLE_TIP, lm3=THUMB_TIP):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_world_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None 
    x1, y1 = hand[lm1].x, hand[lm1].y
    x2, y2 = hand[lm2].x, hand[lm2].y
    x3, y3 = hand[lm3].x, hand[lm3].y
    area = abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
    return area

def get_triangle_area_3d(result, hand_name, lm1=INDEX_TIP, lm2=MIDDLE_TIP, lm3=THUMB_TIP):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_world_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None 
    p1 = np.array([hand[lm1].x, hand[lm1].y, hand[lm1].z])
    p2 = np.array([hand[lm2].x, hand[lm2].y, hand[lm2].z])
    p3 = np.array([hand[lm3].x, hand[lm3].y, hand[lm3].z])
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p1 - p3)
    s = (a + b + c) / 2
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

def get_finger_states(result, hand_name, threshold=90, thumb_threshold=130):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None
    finger_states = []
    finger_tips = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    finger_bases = [THUMB_KNUCKLE_2, INDEX_KNUCKLE_1, MIDDLE_KNUCKLE_1, RING_KNUCKLE_1, PINKY_KNUCKLE_1]
    for tip, base, i in zip(finger_tips, finger_bases, range(5)):
        angle = get_angle(result, hand_name, tip, base, WRIST)
        if i == 0:
            finger_states.append(angle > thumb_threshold)
        else:
            finger_states.append(angle > threshold)
    return finger_states

def is_hand_spread(result, hand_name, threshold=15):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_world_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None
    return get_angle(result, hand_name, INDEX_TIP, INDEX_KNUCKLE_1, MIDDLE_TIP) > threshold

def is_palm_front(result, hand_name):
    hand = None
    for hand_landmarks, hand_label in zip(result.hand_world_landmarks, result.handedness):
        if hand_label[0].category_name == hand_name:
            hand = hand_landmarks
            break
    if hand is None:
        return None
    if hand_name == "Left":
        return hand[INDEX_KNUCKLE_1].x < hand[PINKY_KNUCKLE_1].x
    else:
        return hand[INDEX_KNUCKLE_1].x > hand[PINKY_KNUCKLE_1].x