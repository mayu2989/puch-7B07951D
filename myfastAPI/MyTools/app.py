from deepface import DeepFace
from PIL import Image
import numpy as np
import streamlit as st
from textblob import TextBlob

# Define which playlists to recommend for each mood
MOOD_PLAYLISTS = {
    "happy": ["Pop Hits Playlist", "Dance Party Playlist"],
    "sad": ["Acoustic Chill Playlist", "Blues Classics Playlist"],
    "relaxed": ["Jazz Vibes Playlist", "Classical Music Playlist"],
    "angry": ["Rock Anthems Playlist", "Rap Battle Playlist"],
    "excited": ["EDM Bangers Playlist", "Hip-Hop Hits Playlist"]
}


def detect_mood(text):
    """
    Detect the mood of the input text using sentiment polarity.
    Returns one of 5 moods.
    """
    polarity = TextBlob(text).sentiment.polarity  # -1 (negative) to 1 (positive)
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    else:
        return "relaxed"

def suggest_music(mood):
    """
    Suggests playlists based on detected mood.
    Default to pop playlists if mood not found.
    """
    return MOOD_PLAYLISTS.get(mood, ["Pop Hits Playlist"])

# Build Streamlit UI
st.title("Emotion-Based Music Recommender")

# Wait for user input text
user_input = st.text_input("How are you feeling today?")

if user_input:
    mood = detect_mood(user_input)
    st.write(f"Detected mood: **{mood.capitalize()}**")
    playlists = suggest_music(mood)
    st.write("Recommended Playlists:")
    for playlist in playlists:
        st.write(f"- {playlist}")
else:
    st.write("Type your current feeling above to get music recommendations!")

st.subheader("Or upload your selfie for emotion detection")

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Convert to RGB array for DeepFace
    img_array = np.array(img.convert('RGB'))

    try:
        # Analyze emotion
        result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)
        detected_emotion = result['dominant_emotion']
        st.write(f"**Detected emotion from face:** {detected_emotion.capitalize()}")

        # Map DeepFace emotion to your app mood categories
        EMOTION_TO_MOOD = {
            "happy": "happy",
            "sad": "sad",
            "neutral": "relaxed",
            "angry": "angry",
            "surprise": "excited",
            "fear": "relaxed",
            "disgust": "sad"
        }

        mood = EMOTION_TO_MOOD.get(detected_emotion.lower(), "relaxed")
        playlists = suggest_music(mood)
        st.write("Recommended Playlists based on your facial emotion:")
        for playlist in playlists:
            st.write(f"- {playlist}")
    except Exception as e:
        st.error("Could not detect emotion in the image. Please try another photo.")
