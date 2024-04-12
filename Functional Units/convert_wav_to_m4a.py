import os
from pydub import AudioSegment
import my_constants


def convert_wav_to_and_get_path_of_m4a(path_of_wav) -> str:
    path_of_mp4 = path_of_wav[:-3] + 'mp4'

    AudioSegment.converter = my_constants.PATH_OF_FFMPEG
    audiosegment_from_wav = AudioSegment.from_wav(path_of_wav)

    audiosegment_from_wav.export(
        path_of_mp4,
        format='mp4',
        codec='aac',
        bitrate='320k'
    )

    path_of_m4a = path_of_mp4[:-3] + 'm4a'
    os.rename(path_of_mp4, path_of_m4a)
    return path_of_m4a


path_of_wav_to_convert_to_m4a = '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/Automated Motivational Video Channel/Generated Content/Deep Empowerment/Rich Dad Poor Dad by Robert T. Kiyosaki 2023-05-05 11 14 21 102988 Concatenated Speaker Parts Audio Auphonic 2.wav'

convert_wav_to_and_get_path_of_m4a(path_of_wav_to_convert_to_m4a)