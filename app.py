import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import io
import os
import json
from audio_analyzer import AudioAnalyzer
from utils import create_progress_bar, create_emotion_bar

# Set page configuration
st.set_page_config(
    page_title="Music Analysis",
    page_icon="🎵",
    layout="wide"
)

# Initialize the audio analyzer
analyzer = AudioAnalyzer()

# Custom CSS to improve UI and hide header
st.markdown("""
<style>
    /* Dark theme compatibility */
    :root {
        --background-color: rgba(49, 51, 63, 0.2);
        --secondary-background-color: rgba(0, 0, 0, 0.1);
        --text-color: var(--text-color, #F0F2F6);
        --accent-color: #4a86e8;
        --accent-color-dark: #1e3a8a;
        --border-color: rgba(250, 250, 250, 0.2);
        --card-bg-light: rgba(255, 255, 255, 0.1);
        --card-bg-dark: rgba(0, 0, 0, 0.2);
    }

    /* Hide header and footer */
    header {display: none !important;}
    footer {display: none !important;}
    
    /* Main container */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 0.5rem;
        width: 250px !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1px;
        padding: 0 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 25px;
        padding: 0 8px;
        font-size: 0.8rem;
    }
    
    /* Content containers */
    .content-container {
        padding: 0.25rem;
        height: calc(100vh - 1rem);
        overflow: hidden;
    }
    
    /* Analysis cards */
    .analysis-card {
        background-color: var(--card-bg-light);
        padding: 0.25rem;
        border-radius: 6px;
        text-align: center;
        margin: 0.15rem;
        border: 1px solid var(--border-color);
    }
    
    /* Visualization containers */
    .visualization-container {
        background-color: var(--secondary-background-color);
        border-radius: 6px;
        padding: 0.25rem;
        margin: 0.15rem;
        border: 1px solid var(--border-color);
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: var(--accent-color);
    }
    
    /* Text elements */
    .metric-value {
        font-size: 1rem;
        font-weight: bold;
        color: var(--accent-color);
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.7;
        color: var(--text-color);
    }
    
    /* Section headers */
    h3 {
        font-size: 1rem !important;
        margin-bottom: 0.25rem !important;
    }

    /* Spacing adjustments */
    .stMarkdown {
        margin-bottom: 0.25rem !important;
    }
    
    /* Card hover effects */
    .analysis-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .pill {
        display: inline-block;
        background: #f3f3f3;
        color: #222;
        border-radius: 16px;
        padding: 2px 12px;
        margin: 2px 4px 2px 0;
        font-size: 0.95rem;
        font-weight: 500;
        border: 1px solid #e0e0e0;
    }
    .pill-instrument {
        background: #fff6e0;
        color: #b26a00;
        border: 1px solid #ffe0b2;
    }
    .pill-usecase {
        background: #e3f0ff;
        color: #1565c0;
        border: 1px solid #bbdefb;
    }
    .pill-quality {
        background: #43a047;
        color: #fff;
        border: none;
        font-weight: 600;
    }
    .section-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #888;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
    }
    .divider {
        border-bottom: 1px solid #e0e0e0;
        margin: 1.2rem 0 1rem 0;
    }
    .metric-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Create sidebar for upload and settings
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h2 style="color: var(--text-color);">Audio Analyzer Joco</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Upload Audio")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "flac", "ogg"])
    
    st.markdown("### Analysis Settings")
    sample_rate = st.selectbox("Sample Rate", [22050, 44100, 48000], index=0)
    duration = st.selectbox("Analysis Duration", ["Full song", "30 seconds", "60 seconds", "90 seconds"], index=1)

    # Define duration mapping
    duration_mapping = {
        "Full song": None,
        "30 seconds": 30,
        "60 seconds": 60,
        "90 seconds": 90
    }
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; opacity: 0.7;">
        Supported formats: MP3, WAV, FLAC, OGG
    </div>
    """, unsafe_allow_html=True)

# Main content area
if uploaded_file is not None:
    try:
        # Save the uploaded file temporarily
        with open("temp_audio.mp3", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Display audio player
        st.audio("temp_audio.mp3", format="audio/mp3")
        
        # Load and analyze the audio
        y, sr = librosa.load("temp_audio.mp3", sr=sample_rate, duration=duration_mapping[duration])
        analysis_results = analyzer.analyze_audio(y, sr)
        
        # Remove the temp file
        os.remove("temp_audio.mp3")
        
        # --- Custom CSS for pills and layout ---
        st.markdown("""
        <style>
        .pill {
            display: inline-block;
            background: #f3f3f3;
            color: #222;
            border-radius: 16px;
            padding: 2px 12px;
            margin: 2px 4px 2px 0;
            font-size: 0.95rem;
            font-weight: 500;
            border: 1px solid #e0e0e0;
        }
        .pill-instrument {
            background: #fff6e0;
            color: #b26a00;
            border: 1px solid #ffe0b2;
        }
        .pill-usecase {
            background: #e3f0ff;
            color: #1565c0;
            border: 1px solid #bbdefb;
        }
        .pill-quality {
            background: #43a047;
            color: #fff;
            border: none;
            font-weight: 600;
        }
        .section-label {
            font-size: 0.85rem;
            font-weight: 700;
            color: #888;
            letter-spacing: 1px;
            margin-bottom: 0.2rem;
        }
        .divider {
            border-bottom: 1px solid #e0e0e0;
            margin: 1.2rem 0 1rem 0;
        }
        .metric-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.1rem;
        }
        .metric-value {
            font-size: 1.15rem;
            font-weight: 600;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # --- Top Section: Genre, Mood, Instruments, Use Cases ---
        top_left, top_right = st.columns([2,2])
        with top_left:
            st.markdown('<div class="section-label">GENRE</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="pill">{analysis_results["genre"]["main_genre"]} {analysis_results["genre"]["confidence"]}%</span>', unsafe_allow_html=True)
            if "genre_description" in analysis_results["genre"]:
                st.markdown(f'<div style="margin-top:0.2rem; color:#444; font-size:0.95rem;">{analysis_results["genre"]["genre_description"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:0.7rem;">MOOD</div>', unsafe_allow_html=True)
            for mood, value in analysis_results["mood"].items():
                st.markdown(f'<span class="pill">{mood} {value}%</span>', unsafe_allow_html=True)
        with top_right:
            st.markdown('<div class="section-label">INSTRUMENTS</div>', unsafe_allow_html=True)
            for instrument in analysis_results["instruments"]:
                st.markdown(f'<span class="pill pill-instrument">{instrument}</span>', unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:0.7rem;">SUGGESTED USE CASES</div>', unsafe_allow_html=True)
            for use_case in analysis_results["use_cases"]:
                st.markdown(f'<span class="pill pill-usecase">{use_case}</span>', unsafe_allow_html=True)
        
        # --- Middle Section: Energy and Emotion ---
        mid_left, mid_right = st.columns([2,2])
        with mid_left:
            st.markdown('<div class="section-label">ENERGY</div>', unsafe_allow_html=True)
            energy_level = analysis_results["energy"]["level"]
            create_progress_bar(energy_level, ["Low", "Medium", "High"])
            if "variance" in analysis_results["energy"]:
                st.markdown(f'<div style="font-size:0.9rem; color:#666;">Variance: {analysis_results["energy"]["variance"]}</div>', unsafe_allow_html=True)
        with mid_right:
            st.markdown('<div class="section-label">EMOTION</div>', unsafe_allow_html=True)
            if "emotion" in analysis_results:
                create_emotion_bar(analysis_results["emotion"]["value"])
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # --- Vocal Analysis Section ---
        st.markdown('<div class="section-label">VOCAL ANALYSIS</div>', unsafe_allow_html=True)
        v1, v2, v3 = st.columns(3)
        with v1:
            st.markdown('<div class="metric-title">Instrumentation</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["vocal"]["instrumentation"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-title" style="margin-top:0.5rem;">Autotune Presence</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["vocal"]["autotune"]}</div>', unsafe_allow_html=True)
        with v2:
            st.markdown('<div class="metric-title">Vocal Register</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["vocal"]["register"]}</div>', unsafe_allow_html=True)
        with v3:
            st.markdown('<div class="metric-title">Vocal Presence</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["vocal"]["presence"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # --- Technical Specs Section ---
        st.markdown('<div class="section-label">TECHNICAL SPECS</div>', unsafe_allow_html=True)
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            st.markdown('<div class="metric-title">Key</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["technical"]["key"]}</div>', unsafe_allow_html=True)
        with t2:
            st.markdown('<div class="metric-title">BPM</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["technical"]["bpm"]}</div>', unsafe_allow_html=True)
        with t3:
            st.markdown('<div class="metric-title">Beat Consistency</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{analysis_results["technical"]["beat_consistency"]}</div>', unsafe_allow_html=True)
        with t4:
            st.markdown('<div class="metric-title">Quality</div>', unsafe_allow_html=True)
            quality = analysis_results["technical"]["quality"]
            st.markdown(f'<span class="pill pill-quality">{quality}</span>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error analyzing audio: {str(e)}")
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")

else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1 style="color: var(--text-color);">Welcome to Audio Analyzer</h1>
        <p style="color: var(--text-color); opacity: 0.8;">Upload an audio file to begin analysis</p>
    </div>
    """, unsafe_allow_html=True)