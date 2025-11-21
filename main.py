import cv2, os, time

if os.path.exists("output.mp4"):
    os.remove("output.mp4")

# Initialize video capture object for the default camera (index 0)
# Use a different index if you have multiple cameras or an IP camera URL
cap = cv2.VideoCapture(0) 
FPS = 10.0
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Define the codec and create VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Or other codecs like 'MJPG', 'mp4v'
out = cv2.VideoWriter('output.mp4', fourcc, FPS, (640, 480)) # Adjust resolution and FPS

import asyncio
from threading import Thread
import sys

init_time = time.time()

async def main():
    frame_count = 0
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def blocking_input():
        while True:
            line = sys.stdin.readline()
            loop.call_soon_threadsafe(queue.put_nowait, line)

    Thread(target=blocking_input, daemon=True).start()

    print("input: ")
    line = ""

    

    while True:
        try:
            line = await asyncio.wait_for(queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            pass  # timeout just means "no input", keep going

        # Meanwhile do other things:

        if line.strip() == "stop":
            break
        ret, frame = cap.read() # Read a frame from the camera
        frame_count += 1
        if not ret:
            print("Error: Failed to read frame.")
            break
        # Process the frame (e.g., apply filters, object detection)
        # For headless, you likely won't display it, but save it directly
        out.write(frame) # Write the frame to the output video file
        # Example: Stop after a certain number of frames or based on acondition
        # For a continuous headless capture, this might not be needed
        # if some_condition_is_met:
        #     break
    return frame_count

frame_count = asyncio.run(main())
cap.release() # Release the camera
out.release() # Release the VideoWriter

end_time = time.time()
print(f"{frame_count/FPS} seconds of video in {end_time - init_time} seconds irl")