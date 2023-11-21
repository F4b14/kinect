import zmq
import numpy as np
import cv2

context = zmq.Context()
socket1 = context.socket(zmq.SUB)
socket1.connect("tcp://10.171.22.235:5556")
socket1.setsockopt_string(zmq.SUBSCRIBE, "")
socket2 = context.socket(zmq.SUB)
socket2.connect("tcp://10.171.22.235:5555")
socket2.setsockopt_string(zmq.SUBSCRIBE, "")
print()

def process_rgbd(frame_data):
    # Assuming the RGBD frame is sent as a serialized OpenCV image
    rgbd_array = np.frombuffer(frame_data, dtype=np.uint8)
    rgbd = cv2.imdecode(rgbd_array, cv2.IMREAD_UNCHANGED)
    
    # Process the "rgbd" data
    # ...

    return rgbd

def process_depth(frame_data):
    # Assuming the depth frame is sent as a serialized OpenCV image
    depth_array = np.frombuffer(frame_data, dtype=np.uint8)
    depth = cv2.imdecode(depth_array, cv2.IMREAD_UNCHANGED)
    
    # Process the "depth" data
    # ...

    return depth

while True:
    
    # Receive the data based on the header
        # Receive the "rg" matrix data
    rgbd_data = socket1.recv()
    print("data")
    rgbd = process_rgbd(rgbd_data)
    print("data procesada")
    # Display or process the "rgbd" data as needed
    cv2.imshow("RG", rgbd)
    cv2.waitKey(1)  # Adjust as needed

    # Receive the "depth" matrix data
    depth_data = socket2.recv()
    depth = process_depth(depth_data)
    print("")
    # Display or process the "depth" data as needed
    cv2.imshow("depth", depth)
    cv2.waitKey(1)  # Adjust as needed