import streamlit as st
import numpy as np

def create_progress_bar(value, labels=None, color="blue"):
    """
    Create a custom progress bar with labels.
    
    Parameters:
    value (float): Value between 0 and 1
    labels (list): List of labels for the progress bar
    color (str): Color of the progress bar
    
    Returns:
    None
    """
    # Create a container to hold the progress bar and labels
    container = st.container()
    
    # Create the progress bar
    container.progress(value)
    
    # If labels are provided, create the label row
    if labels:
        cols = container.columns(len(labels))
        for i, label in enumerate(labels):
            cols[i].write(label)

def create_emotion_bar(value, labels=None):
    """
    Create a custom emotion bar (negative to positive).
    
    Parameters:
    value (float): Value between 0 and 1 (0 = negative, 1 = positive)
    labels (list): List of labels for the emotion bar [negative, positive]
    
    Returns:
    None
    """
    # Create a container for the emotion bar
    container = st.container()
    
    # Create a colored bar
    emotion_html = f"""
    <style>
    .emotion-container {{
        width: 100%;
        background-color: #f0f0f0;
        height: 10px;
        border-radius: 5px;
        position: relative;
    }}
    .emotion-level {{
        width: {value * 100}%;
        background: linear-gradient(to right, #ff9999, #ffcc99, #ffff99, #99ff99);
        height: 10px;
        border-radius: 5px;
    }}
    .emotion-marker {{
        position: absolute;
        top: -5px;
        left: {value * 100}%;
        width: 4px;
        height: 20px;
        background-color: #333;
        transform: translateX(-50%);
    }}
    </style>
    <div class="emotion-container">
        <div class="emotion-level"></div>
        <div class="emotion-marker"></div>
    </div>
    """
    container.markdown(emotion_html, unsafe_allow_html=True)
    
    # If labels are provided, create the label row
    if labels:
        cols = container.columns(len(labels))
        for i, label in enumerate(labels):
            cols[i].write(label)
