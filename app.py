import streamlit as st
from yt_functions import yt_download_video, yt_get_transcript

st.title("Download Video from Youtube")

url = st.text_input("Enter the URL of the video")
download_button = st.button("Download Video")
transcript_button = st.button("Get Transcript")

if download_button:
    with st.spinner("Downloading..."):
        filename = yt_download_video(url)
        with open(filename, "rb") as file:
            st.download_button(label="Download Video", data=file, file_name="video.mp4")

if transcript_button:
    with st.spinner("Fetching transcript..."):
        transcript = yt_get_transcript(url)
        if transcript:
            st.text_area("Transcript", value=transcript, height=300)
        else:
            st.error("Transcript not available for this video.")
