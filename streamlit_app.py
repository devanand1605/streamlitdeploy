import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

# Helper function to read video frames
def read_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Helper function to save video frames to a file
def save_video(frames, output_path, fps):
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()

# Global variables to store video and overlay layers
video_frames = []
overlays = []

# Streamlit UI
st.title("Simple Video Editor")

# File uploader
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
if uploaded_file:
    temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.video(temp_video_path)
    video_frames = read_frames(temp_video_path)
    st.write(f"Uploaded video with {len(video_frames)} frames.")

# Overlay upload
overlay_file = st.file_uploader("Upload an overlay (image)", type=["png", "jpg", "jpeg"])
if overlay_file:
    overlay_image = Image.open(overlay_file)
    overlay_np = np.array(overlay_image)
    overlays.append(overlay_np)
    st.image(overlay_image, caption="Uploaded Overlay")

# Render the timeline and overlays
if video_frames:
    st.header("Timeline and Overlays")
    frame_index = st.slider("Frame", 0, len(video_frames) - 1, 0)
    current_frame = video_frames[frame_index]
    
    # Apply overlays
    for overlay in overlays:
        x_offset = st.slider("Overlay X offset", 0, current_frame.shape[1], 0)
        y_offset = st.slider("Overlay Y offset", 0, current_frame.shape[0], 0)
        y1, y2 = y_offset, y_offset + overlay.shape[0]
        x1, x2 = x_offset, x_offset + overlay.shape[1]
        alpha_overlay = overlay[:, :, 3] / 255.0
        alpha_frame = 1.0 - alpha_overlay
        for c in range(0, 3):
            current_frame[y1:y2, x1:x2, c] = (alpha_overlay * overlay[:, :, c] +
                                              alpha_frame * current_frame[y1:y2, x1:x2, c])
    
    st.image(current_frame, channels="BGR")

# Split and delete functionality
if st.button("Split Video (Ctrl+B)"):
    split_time = st.number_input("Split Time (seconds)", min_value=0, step=1)
    fps = 24  # Assuming a default FPS of 24
    split_frame = int(split_time * fps)
    if split_frame < len(video_frames):
        first_part = video_frames[:split_frame]
        second_part = video_frames[split_frame:]
        save_video(first_part, "first_part.mp4", fps)
        save_video(second_part, "second_part.mp4", fps)
        st.write("Video split at frame", split_frame)
        st.video("first_part.mp4")
        st.video("second_part.mp4")

if st.button("Delete Selected Clip (Del)"):
    index_to_delete = st.number_input("Index of frame to delete", min_value=0, step=1)
    if 0 <= index_to_delete < len(video_frames):
        del video_frames[index_to_delete]
        st.write(f"Deleted frame at index {index_to_delete}")

# Render final video
if st.button("Render Final Video"):
    fps = 24  # Assuming a default FPS of 24
    save_video(video_frames, "final_output.mp4", fps)
    st.video("final_output.mp4")
    st.write("Final video saved as final_output.mp4")
