import subprocess
import time

def add_metadata_to_m4a_and_get_path(path_of_m4a_to_add_metadata_to: str, path_of_metadata_file: str):
    path_of_m4a_with_metadata = f"{path_of_m4a_to_add_metadata_to[:-4]} with Metadata.m4a"
    command = f'ffmpeg -i "{path_of_m4a_to_add_metadata_to}" -i "{path_of_metadata_file}" -map_metadata 1 -codec copy "{path_of_m4a_with_metadata}"'
    subprocess.run(command, shell=True)

    time.sleep(3)

    print("Chapters added successfully!")

    return path_of_m4a_with_metadata


m4a = '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/Automated Motivational Video Channel/Generated Content/Deep Empowerment/Rich Dad Poor Dad by Robert T. Kiyosaki 2023-05-05 11 14 21 102988 Concatenated Speaker Parts Audio Auphonic 2.m4a'
meta = '/Users/moritzwiedemann/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/Automated Motivational Video Channel/Generated Content/Deep Empowerment/Rich Dad Poor Dad by Robert T. Kiyosaki 2023-05-05 11 14 21 102988 Chapter Metadata for M4A.txt'
add_metadata_to_m4a_and_get_path(m4a, meta)