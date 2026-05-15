latest_frame = None

def send_frames(frame):
    global latest_frame
    latest_frame = frame

def recieve_frames():
    global latest_frame
    return latest_frame
