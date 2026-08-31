import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

# Setup paths for saving output
script_dir = os.path.dirname(os.path.abspath(__file__))
subfolder_depth = os.path.join(script_dir, "out/depth")
subfolder_rgb = os.path.join(script_dir, "out/rgb")
os.makedirs(subfolder_depth, exist_ok=True)
os.makedirs(subfolder_rgb, exist_ok=True)

# Path to the bag file
bag_file_path = r"D:\Intel RealSense SDK 2.0\tools\131224_SS_810_61_4.bag"

# Configure pipeline to stream from the .bag file
pipeline = rs.pipeline()
config = rs.config()
config.enable_device_from_file(bag_file_path, repeat_playback=False)  # End after the video completes

# Start streaming from the bag file
profile = pipeline.start(config)

# Get the depth sensor’s depth scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is:", depth_scale)

# Clipping distance in meters (optional, used if background filtering is needed)
clipping_distance_in_meters = 1  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Align depth to color
align_to = rs.stream.color
align = rs.align(align_to)

# Extract intrinsics once (they should be the same for all frames)
aligned_depth_frame = align.process(pipeline.wait_for_frames()).get_depth_frame()
intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
with open(os.path.join(script_dir, "out/cam_K.txt"), "w") as f:
    f.write(f"{intrinsics.fx} 0.0 {intrinsics.ppx}\n")
    f.write(f"0.0 {intrinsics.fy} {intrinsics.ppy}\n")
    f.write("0.0 0.0 1.0\n")

# Streaming loop to save each frame
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate frames
        if not aligned_depth_frame or not color_frame:
            break

        # Convert frames to numpy arrays
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Save frames
        timestamp = int(round(time.time() * 1000))
        cv2.imwrite(os.path.join(subfolder_depth, f"{timestamp}.png"), depth_image)
        cv2.imwrite(os.path.join(subfolder_rgb, f"{timestamp}.png"), color_image)

        print(f"Saved frame {timestamp}")

except RuntimeError as e:
    print("End of video or an error occurred:", e)

finally:
    pipeline.stop()
