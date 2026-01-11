import streamlit as st
import os

# --- Song Class ---
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist):
        new_song = Song(title, artist)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        if self.head is None:
            return []

        playlist_songs = []
        current = self.head
        count = 1
        while current:
            playlist_songs.append(f"{count}. {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
        else:
            st.warning("Playlist is empty or no song is selected to play.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist. No next song.")
        else:
            st.warning("Playlist is empty.")

    def prev_song(self):
        if self.head is None or self.current_song is None:
            st.warning("Playlist is empty or no song is selected.")
            return
        if self.current_song == self.head:
            st.warning("Already at the beginning of the playlist.")
            return

        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def get_length(self):
        return self.length

    def delete_song(self, title):
        if self.head is None:
            st.error(f"Cannot delete '{title}'. Playlist is empty.")
            return

        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            if self.length == 0:
                self.current_song = None
            return

        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next_song

        if current:
            if self.current_song == current:
                if current.next_song:
                    self.current_song = current.next_song
                elif prev:
                    self.current_song = prev
                else:
                    self.current_song = None

            prev.next_song = current.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
        else:
            st.error(f"Song '{title}' not found in the playlist.")

# --- Streamlit App Layout ---
st.set_page_config(page_title="Music Playlist App", page_icon="🎶")
st.title("🎶 Music Playlist App")

# Initialize playlist in session state
if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# --- Sidebar for Adding Songs ---
st.sidebar.header("📂 Upload or Add Song")

# 1. Browse File Section
uploaded_file = st.sidebar.file_uploader("Choose a music file", type=["mp3", "wav"])
default_name = ""
if uploaded_file is not None:
    # Get filename without extension as default title
    default_name = os.path.splitext(uploaded_file.name)[0]

# 2. Input Fields
new_title = st.sidebar.text_input("Title", value=default_name)
new_artist = st.sidebar.text_input("Artist", placeholder="Unknown Artist")

if st.sidebar.button("Add Song to Playlist"):
    if new_title:
        # Use "Unknown Artist" if artist is empty
        artist_name = new_artist if new_artist else "Unknown Artist"
        st.session_state.playlist.add_song(new_title, artist_name)
    else:
        st.sidebar.warning("Please provide at least a song title.")

st.sidebar.markdown("---")
st.sidebar.header("🗑️ Delete Song")
delete_title = st.sidebar.text_input("Song Title to Delete")
if st.sidebar.button("Delete Song"):
    if delete_title:
        st.session_state.playlist.delete_song(delete_title)
    else:
        st.sidebar.warning("Please enter a song title to delete.")

# --- Main content ---
st.header("Your Current Playlist")
playlist_content = st.session_state.playlist.display_playlist()

if playlist_content:
    # แสดงรายการเพลงในรูปแบบกล่องสวยงาม
    for song_str in playlist_content:
        st.info(song_str)
else:
    st.write("Playlist is empty. Add some songs from the sidebar!")

st.markdown("---")
st.header("Playback Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous", use_container_width=True):
        st.session_state.playlist.prev_song()
        st.session_state.playlist.play_current_song()

with col2:
    if st.button("▶️ Play Current", use_container_width=True):
        st.session_state.playlist.play_current_song()

with col3:
    if st.button("⏩ Next", use_container_width=True):
        st.session_state.playlist.next_song()
        st.session_state.playlist.play_current_song()

st.markdown("---")
st.write(f"Total songs in playlist: **{st.session_state.playlist.get_length()}** song(s)")
