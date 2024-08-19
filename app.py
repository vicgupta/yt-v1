import streamlit as st
from yt_functions import yt_download_video

st.title("Download Video from Youtube")

url = st.text_input("Enter the URL of the video")
download_button = st.button("Submit")
if download_button:
    with st.spinner("Downloading..."):
        filename = yt_download_video(url)
        with open(filename, "rb") as file:
            st.download_button(label="Download Video", data=file, file_name="video.mp4")

