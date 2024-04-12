from moviepy.editor import VideoFileClip, AudioFileClip


from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_audio_to_video(path_of_video, path_of_music, output_path):
    # Load video
    video = VideoFileClip(path_of_video)
    original_audio = video.audio

    # Load music
    music = AudioFileClip(path_of_music)

    # Make the music the same duration as the video
    music = music.subclip(0, video.duration)

    # Reduce music volume
    music = music.volumex(0.4)

    # Fade out music in the last 3 seconds
    music = music.audio_fadeout(3)

    # Combine original audio and music
    final_audio = CompositeAudioClip([original_audio, music])

    # Set the final audio to the video
    video = video.set_audio(final_audio)

    # Write the result to a file
    video.write_videofile(output_path, codec='libx264')



video_paths = [
    '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/Downloads from Mac Mini/argaergaergaerg/YouTube Short The Pragmatic Programmer (2nd Edition) by David Thomas and Andrew Hunt.mov',
    '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/Downloads from Mac Mini/argaergaergaerg/YouTube Short The Infinite Game by Simon Sinek.mov',
    '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/Downloads from Mac Mini/argaergaergaerg/YouTube Short The 7 Habits of Highly Effective People by Stephen R. Covey.mov',
    '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/Downloads from Mac Mini/argaergaergaerg/YouTube Short Rich Dad Poor Dad by Robert T. Kiyosaki.mov'
]

for path in video_paths:
    add_audio_to_video(
        path_of_video=path,
        path_of_music='/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/Laid-Back Instrumental Tracks/Floating Uplifting Dance Beat 24 bit.wav',
        output_path=path[:-4] + " with Music.mov"
    )