import cv2

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),       # thumb
    (0,5),(5,6),(6,7),(7,8),       # index
    (0,9),(9,10),(10,11),(11,12),  # middle
    (0,13),(13,14),(14,15),(15,16),# ring
    (0,17),(17,18),(18,19),(19,20) # pinky
   # (5, 9), (9, 13), (13, 17)     # palm
]

def draw_landmarks(frame, hand_landmarks):
    """draw hand landmarks as green circles"""
    if hand_landmarks:
        for hand in hand_landmarks:
            for lm in hand:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

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