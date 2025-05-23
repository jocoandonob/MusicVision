import numpy as np
import librosa
import random
from scipy import stats

class AudioAnalyzer:
    def __init__(self):
        self.genres = ["Hip Hop", "Electronic", "Rock", "Pop", "Classical", "Jazz", "Country", "R&B", "Metal", "Folk"]
        self.moods = ["Bold", "Confident", "Restless", "Energetic", "Calm", "Melancholic", "Upbeat", "Tense"]
        self.instruments = ["Bass", "Beats", "Synth", "Guitar", "Piano", "Drums", "Strings", "Brass", "Woodwinds"]
        self.use_cases = ["extreme sports", "party", "beats", "workout", "relaxation", "focus", "driving", "meditation"]
        self.vocal_types = ["female and male", "female", "male", "group", "chorus", "instrumental"]
        self.keys = ["C major", "C# minor", "D major", "D# minor", "E major", "F minor", "F# major", 
                     "G minor", "G# major", "A minor", "A# major", "B minor"]
        
    def analyze_audio(self, y, sr):
        """
        Analyze the audio file and extract various features.
        
        Parameters:
        y (numpy.ndarray): Audio time series
        sr (int): Sample rate
        
        Returns:
        dict: Analysis results
        """
        # This is where we would use sophisticated audio analysis
        # For now, we'll create a deterministic analysis based on audio features
        
        # Extract actual features from the audio
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0].mean()
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0].mean()
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0].mean()
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0].mean()
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        
        # Get chromagram for key detection
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_means = np.mean(chroma, axis=1)
        key_idx = np.argmax(chroma_means)
        
        # Detect onsets for beat consistency
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        beat_consistency = 1.0 - stats.variation(onset_env)
        beat_consistency = max(0, min(1, beat_consistency))  # Normalize between 0 and 1
        
        # Use features to determine genre (this would be a machine learning model in a real app)
        # For now, use a simplified heuristic approach
        genre_idx = int((spectral_centroid / 5000) * len(self.genres)) % len(self.genres)
        genre = self.genres[genre_idx]
        
        # Set confidence based on spectral features
        confidence = int(min(100, max(50, (spectral_bandwidth / 5000) * 100)))
        
        # Determine energy level (low, medium, high) based on spectral features
        energy_value = (spectral_rolloff + zero_crossing_rate * 10000) / 10000
        energy_level = 0.0  # Between 0 and 1
        
        if energy_value < 1000:
            energy_level = 0.3  # Low
            energy_text = "Low"
        elif energy_value < 2000:
            energy_level = 0.6  # Medium
            energy_text = "Medium"
        else:
            energy_level = 0.9  # High
            energy_text = "High"
            
        # Determine energy variance
        energy_variance = "small" if np.var(y) < 0.01 else "medium" if np.var(y) < 0.05 else "large"
        
        # Select moods based on audio features
        mood_values = {}
        
        # Main mood is based on tempo and energy
        primary_mood_idx = 0
        if tempo > 120 and energy_level > 0.7:
            primary_mood_idx = 0  # Bold
            mood_values["Bold"] = 100
        elif tempo > 100 and energy_level > 0.5:
            primary_mood_idx = 1  # Confident
            mood_values["Confident"] = 87
        else:
            primary_mood_idx = 2  # Restless
            mood_values["Restless"] = 23
            
        # Set emotion based on spectral features and MFCCs
        # Negative to positive scale from 0 to 1
        mfcc_sum = np.sum(mfcc_means)
        emotion_value = (mfcc_sum + 100) / 200  # Normalize approximately to 0-1
        emotion_value = max(0, min(1, emotion_value))  # Clip to 0-1 range
        
        # Select instruments based on spectral features
        instruments = []
        
        # Bass detection
        if np.mean(y**2) > 0.005:
            instruments.append("Bass")
            
        # Beats detection based on tempo
        if tempo > 80:
            instruments.append("Beats")
            
        # Synth detection based on spectral centroid
        if spectral_centroid > 3000:
            instruments.append("Synth")
            
        # Ensure we have at least one instrument
        if not instruments:
            instruments.append(self.instruments[0])
        
        # Determine use cases based on genre and energy
        use_cases = []
        if genre == "Hip Hop" and energy_level > 0.7:
            use_cases.append("extreme sports")
            use_cases.append("party")
            use_cases.append("beats")
        elif genre == "Electronic" and energy_level > 0.6:
            use_cases.append("party")
            use_cases.append("workout")
        else:
            # Select at least some use cases
            use_cases = self.use_cases[:3]
        
        # Vocal analysis
        has_vocals = np.max(mfccs[1]) > 100  # Simplified vocal detection
        
        vocal_analysis = {
            "instrumentation": "Vocal" if has_vocals else "Instrumental",
            "register": random.choice(self.vocal_types) if has_vocals else "None",
            "presence": "High" if has_vocals and np.max(mfccs[1]) > 150 else "Medium" if has_vocals else "None",
            "autotune": "Low" if has_vocals else "None"
        }
        
        # Technical specifications
        key = self.keys[key_idx]
        bpm = int(tempo)
        
        # Quality assessment
        quality = "Very High"
        if sr < 44100:
            quality = "Medium"
        elif spectral_bandwidth < 1000:
            quality = "High"
        
        # Combine all results - ensure all values are JSON serializable (convert numpy types to Python native types)
        results = {
            "genre": {
                "main_genre": genre,
                "confidence": int(confidence),
                "elements": "Electronic" if genre != "Electronic" and spectral_centroid > 3000 else ""
            },
            "mood": mood_values,
            "instruments": instruments,
            "energy": {
                "level": float(energy_level),
                "text": energy_text,
                "variance": energy_variance
            },
            "emotion": {
                "value": float(emotion_value)
            },
            "use_cases": use_cases,
            "vocal": vocal_analysis,
            "technical": {
                "key": key,
                "bpm": int(bpm),
                "beat_consistency": f"{float(beat_consistency):.2f}",
                "quality": quality
            }
        }
        
        return results
