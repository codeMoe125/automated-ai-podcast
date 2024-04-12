import os
from pydub import AudioSegment
import my_constants


def convert_wav_to_and_get_path_of_mp3(path_of_wav) -> str:
    path_of_mp3 = path_of_wav[:-3] + 'mp3'

    AudioSegment.converter = my_constants.PATH_OF_FFMPEG
    # audiosegment_from_wav = AudioSegment.from_wav(path_of_wav)
    audiosegment_from_file = AudioSegment.from_file(path_of_wav)

    audiosegment_from_file.export(
        path_of_mp3,
        format='mp3',
        bitrate='320k',
    )


    return path_of_mp3


path_of_wav_to_convert_to_mp3 = '''/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/Automated Motivational Video Channel/Generated Content/Deep Empowerment/The Miracle Morning by Hal Elrod 1684183471Convo Audio Optimized by Auphonic.wav'''

convert_wav_to_and_get_path_of_mp3(path_of_wav_to_convert_to_mp3)