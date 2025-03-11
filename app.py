from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit as st
from urllib.parse import urlparse, parse_qs

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }

        [data-testid="stHeading"] {
            text-align: center;
            color: #4A90E2;
        }

        [data-testid="stTextInput"] input {
            border-radius: 8px;
            border: 2px solid #4A90E2;
            padding: 12px;
            font-size: 16px;
        }

        [data-testid="stButton"] button {
            background-color: #4A90E2;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 12px 24px;
            transition: 0.3s;
            width: 100%;
        }

        [data-testid="stButton"] button:hover {
            background-color: #357ABD;
        }

        [data-testid="stExpander"] {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
        }

        [data-testid="stMarkdownContainer"] {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)


genai.configure(api_key="AIzaSyA88oZBMR3T_ZROvjr8xgkPuRD4AP58JpM")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def video_id_changer(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    parsed_url = urlparse(url)
    changed_in_id = parse_qs(parsed_url.query).get('v')
    return changed_in_id[0] if changed_in_id else None 

def Transcript(link):
    video_id = video_id_changer(link)
    if not video_id:
        st.error("Invalid YouTube URL! Please enter a correct video link.")
        return
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text_transcript = " ".join([entry["text"] for entry in transcript])
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        short_text = text_transcript[:3000]
        summurize_text = model.generate_content(f"Summarize This Content: {short_text}")
        st.write(f"Summary of The Video {summurize_text.text}")
    except Exception as e:
        if "NoTranscriptFound" in str(e):
            st.error("⚠️ No transcript found for this video! It may be private or does not have captions.")
        else:
            st.error(f"❌ Error: {e}")

st.title("🎬 YouTube Video Summarizer")
videoLink = st.text_input("🔗 Enter YouTube Video URL")

if st.button("🔍 Summarize"):
    if videoLink.strip():  
        Transcript(videoLink)
    else:
        st.warning("⚠️ Please enter a YouTube video link first.")

with st.expander("ℹ️ Important Information"):
    st.write("""
    - This tool **only works for YouTube videos with subtitles (captions) enabled.**  
    - **Only English subtitles** can be processed.  
    - If a video has **no captions available**, this tool won't work.  
    - Some videos (e.g., music videos) may have **auto-generated captions**, which might not be accurate.  
    """)
