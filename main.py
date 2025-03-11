from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit as st
from urllib.parse import urlparse, parse_qs


genai.configure(api_key="AIzaSyA88oZBMR3T_ZROvjr8xgkPuRD4AP58JpM")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def extract_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get("v")
    return video_id[0] if video_id else None

def userLink(link):
    video_id = extract_id(link)
    if not video_id:
        st.error("Invalid YouTube URL! Please enter a correct video link.")
        return
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_transcript = " ".join([entry["text"] for entry in transcript])
    short_text = text_transcript[:3000]
    summurize_text = model.generate_content(f"Summarize This Content: {short_text}")
    st.write(f"Summarized Text: {summurize_text.text}")

videoLink = st.text_input("Enter YouTube URL")
if st.button("Summarize"):
    userLink(videoLink)
