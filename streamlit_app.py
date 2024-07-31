import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from streamlit_drag_drop import st_drag_and_drop

# Global variables
video_clips = []
audio_clips = []
overlays = []
current_frame = None

def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=["mp4", "avi", "mov", "wav", "mp3"])
    return uploaded_file

def add_clip(file):
    if file:
        temp_path = f"temp/{file.name}"
        with open(temp_path, "wb") as f:
            f.write(file.read())
        return temp_path
    return None

def split_video(video, time):
    video_clip = VideoFileClip(video)
    split_video = video_clip.subclip(0, time)
    return split_video

def delete_clip(index, clips):
    if index >= 0 and index < len(clips):
        del clips[index]

def render_timeline():
    st.sidebar.header("Timeline")
    st.sidebar.write("Drag and drop your assets here")

    timeline = st_drag_and_drop("Drag your assets", allowed_extensions=["mp4", "wav", "mp3"])

    if timeline:
        for file in timeline:
            if file['type'] == 'video':
                video_clips.append(file['file'])
            elif file['type'] == 'audio':
                audio_clips.append(file['file'])
            elif file['type'] == 'overlay':
                overlays.append(file['file'])

def render_preview(video_path):
    video_clip = VideoFileClip(video_path)
    st.video(video_path)
    st.write(f"Preview of: {video_path}")

def main():
    st.title("Simple Video Editor")

    if not os.path.exists("temp"):
        os.makedirs("temp")

    uploaded_file = upload_file()

    if uploaded_file:
        video_path = add_clip(uploaded_file)
        st.write(f"Uploaded video: {video_path}")
        video_clips.append(video_path)

    if st.button("Render Video"):
        if video_clips:
            final_clip = concatenate_videoclips([VideoFileClip(v) for v in video_clips])
            final_clip.write_videofile("output.mp4")
            st.video("output.mp4")
            st.write("Video saved as output.mp4")

    render_timeline()

    if st.button("Split Video (Ctrl+B)"):
        if video_clips:
            split_time = st.number_input("Split Time (seconds)", min_value=0, step=1)
            split_clip = split_video(video_clips[0], split_time)
            st.write(f"Video split at {split_time} seconds")

    if st.button("Delete Selected Clip (Del)"):
        if video_clips:
            index_to_delete = st.number_input("Index of clip to delete", min_value=0, step=1)
            delete_clip(index_to_delete, video_clips)
            st.write(f"Deleted clip at index {index_to_delete}")

if __name__ == "__main__":
    main()
