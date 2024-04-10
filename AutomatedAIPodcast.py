from datetime import datetime, timedelta
import pytz
import re
import sys
import time
import random
import pyperclip
from typing import List, Any
import openai
import datetime
import json
from datetime import datetime
from elevenlabslib.helpers import *
from elevenlabslib import *
from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.crop import crop
import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import *
import time
from googleapiclient.http import MediaFileUpload
import pandas as pd
from google_apis import create_service
import textwrap
from PIL import Image, ImageDraw, ImageFont
import subprocess
from pydub import AudioSegment
import requests
import subprocess
import pytz
from google.oauth2 import credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from google_auth_httplib2 import AuthorizedHttp
import atexit
import my_credentials
import my_constants

# did.com (AI Avatar for YouTube)
# import did

# Amazon S3 (for storing input for did.com)
# import amazonS3

# OpenAI Whisper (can be used for YouTube subtitles)
# import whisper


def terminate(proc):
    proc.terminate()
    proc.wait()
    print(f'\n\nProcess "{proc.args[0]} {proc.args[1]}" with PID {proc.pid} terminated.')


caffeinate_process = subprocess.Popen(['caffeinate', '-d'])
atexit.register(terminate, caffeinate_process)


def are_all_resources_stored_locally() -> bool:
    is_everything_stored_locally = True
    for resource in os.listdir(SpecsForPodcast.PATH_OF_FOLDER_FOR_RESOURCES):
        if resource[-7:] == '.icloud':
            is_everything_stored_locally = False
            print(resource)
    if is_everything_stored_locally == False:
        print('Please download the above files to local storage.')
    return is_everything_stored_locally


def get_seconds_since_the_epoch() -> str:
    return str(int(time.time()))


def should_renew_youtube_token() -> bool:
    # Remove 'GMT' from the date string and add a leading zero to the timezone offset
    youtube_token_creation_date = CREATION_DATETIME_OF_YOUTUBE_TOKEN.replace("GMT", "").replace("+2", "+0200")

    # Convert the token creation date string to a datetime object
    datetime_format = "%d %B %Y at %H:%M:%S %z"
    token_creation_datetime = datetime.strptime(youtube_token_creation_date, datetime_format)

    # Add 7 days to the token creation datetime
    token_expiry_datetime = token_creation_datetime + timedelta(days=7)

    # Get the current datetime in the same timezone as the token creation datetime
    current_datetime = datetime.now(token_creation_datetime.tzinfo)

    # Calculate the remaining time
    time_remaining_until_token_expiry = token_expiry_datetime - current_datetime

    print(f"Time remaining until YouTube Token expiry: {time_remaining_until_token_expiry}")

    if time_remaining_until_token_expiry.days < 0:
        return True

    return False


# NAME_OF_PODCAST_TO_PUBLISH_FOR = sys.argv[1]
NAME_OF_PODCAST_TO_PUBLISH_FOR = 'Deep Empowerment'
SHOULD_UPLOAD_AS_DRAFT = True
CREATION_DATETIME_OF_YOUTUBE_TOKEN = '3 June 2023 at 16:36:09 GMT+2'
START_TIME = get_seconds_since_the_epoch()

print('Publishing for:', NAME_OF_PODCAST_TO_PUBLISH_FOR)


class SpecsForPodcast:
    with open(my_constants.PATH_OF_JSON_WITH_DICT_FOR_ALL_PODCASTS, 'r') as json_with_dict_for_all_podcasts:
        dict_for_this_podcast = json.load(json_with_dict_for_all_podcasts)[NAME_OF_PODCAST_TO_PUBLISH_FOR]
    SHOW_ID_ON_TRANSISTOR = dict_for_this_podcast['show id on transistor']
    DICT_OF_SPEAKERS = dict_for_this_podcast['speakers']
    DICT_OF_SPEAKER_1 = DICT_OF_SPEAKERS['speaker 1']
    DICT_OF_SPEAKER_2 = DICT_OF_SPEAKERS['speaker 2']
    NAME_OF_SPEAKER_1_IN_PODCAST = DICT_OF_SPEAKER_1['name in podcast']
    NAME_OF_SPEAKER_2_IN_PODCAST = DICT_OF_SPEAKER_2['name in podcast']
    NAME_OF_SPEAKER_1_IN_ELEVENLABS = DICT_OF_SPEAKER_1['name in elevenlabs']
    NAME_OF_SPEAKER_2_IN_ELEVENLABS = DICT_OF_SPEAKER_2['name in elevenlabs']
    DICT_OF_WHERE_TO_LISTEN = dict_for_this_podcast['where to listen']
    DESCRIPTION_OF_PODCAST = dict_for_this_podcast['description']
    LINK_FOR_DONATIONS = dict_for_this_podcast['donations']
    PATH_OF_FOLDER_FOR_RESOURCES = my_constants.PATH_OF_FOLDER_FOR_RESOURCES + '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR
    DICT_OF_PATHS_TO_RESOURCES = dict_for_this_podcast['paths of resources']
    PATH_TO_FONT = DICT_OF_PATHS_TO_RESOURCES['path to font']
    PATH_TO_THUMBNAIL_FOR_YOUTUBE = DICT_OF_PATHS_TO_RESOURCES['path to thumbnail for youtube']
    PATH_TO_IMAGE_FOR_YOUTUBE_SHORT = DICT_OF_PATHS_TO_RESOURCES['path to image for youtube short']
    PATH_TO_PODCAST_IMAGE = DICT_OF_PATHS_TO_RESOURCES['path to podcast image']
    PATH_TO_THEME_MUSIC = DICT_OF_PATHS_TO_RESOURCES['path to theme music']
    URL_TO_PODCAST_IMAGE = DICT_OF_PATHS_TO_RESOURCES['url to podcast image']
    TEXT_FOR_YOUTUBE_SHORT = dict_for_this_podcast['text for youtube short']
    DISCLAIMER = dict_for_this_podcast['disclaimer']
    AMAZON_ASSOCIATES_LINK_FOR_AUDIBLE_PREMIUM_PLUS_TRIAL = dict_for_this_podcast[
        'amazon associates link for audible premium plus trial']
    URL_TO_IMPRESSUM = dict_for_this_podcast['url to impressum']


def take_book_dict_from_book_list_for_podcast() -> dict:
    with open(my_constants.PATH_OF_JSON_WITH_DICT_FOR_ALL_PODCASTS, 'r') as json_with_dict_for_all_podcasts:
        dict_for_all_podcasts = json.load(json_with_dict_for_all_podcasts)
    dict_for_this_podcast = dict_for_all_podcasts[NAME_OF_PODCAST_TO_PUBLISH_FOR]
    list_of_books_still_to_recommend = dict_for_this_podcast['featured books']['still to recommend']
    dict_of_fetched_book = list_of_books_still_to_recommend[0]
    list_of_books_still_to_recommend.remove(dict_of_fetched_book)
    dict_for_this_podcast['featured books']['already recommended'].append(dict_of_fetched_book)
    with open(my_constants.PATH_OF_JSON_WITH_DICT_FOR_ALL_PODCASTS, 'w') as json_with_dict_for_all_podcasts:
        json.dump(dict_for_all_podcasts, json_with_dict_for_all_podcasts, indent=2)
    return dict_of_fetched_book


if not are_all_resources_stored_locally() or should_renew_youtube_token():
    exit()


class SpecsForEpisode:
    DICT_OF_BOOK_TO_RECOMMEND = take_book_dict_from_book_list_for_podcast()
    TITLE_OF_BOOK_TO_RECOMMEND = DICT_OF_BOOK_TO_RECOMMEND['title']
    AUTHORS_OF_BOOK_TO_RECOMMEND = DICT_OF_BOOK_TO_RECOMMEND['authors']
    ID_FOR_BOOK = TITLE_OF_BOOK_TO_RECOMMEND + ' by ' + AUTHORS_OF_BOOK_TO_RECOMMEND  # Think Big by Ben James
    DESCRIPTOR_FOR_BOOK = f'"{TITLE_OF_BOOK_TO_RECOMMEND}" by {AUTHORS_OF_BOOK_TO_RECOMMEND}'  # "Think Big" by Ben James
    AFFILIATE_LINK_TO_BOOK = DICT_OF_BOOK_TO_RECOMMEND['affiliate link']
    TITLE_OF_EPISODE = DESCRIPTOR_FOR_BOOK + ' | AI-Generated Book Review'
    PATH_FOR_CUSTOMIZED_PROMPT = my_constants.PATH_OF_FOLDER_FOR_CUSTOM_PROMPTS + \
                                 '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR + \
                                 '/' + TITLE_OF_EPISODE + ' ' + START_TIME + ' Custom Prompt.txt'
    PATH_FOR_GENERATED_SCRIPT = my_constants.PATH_OF_FOLDER_FOR_GENERATED_SCRIPTS + \
                                '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR + \
                                '/' + ID_FOR_BOOK + ' ' + START_TIME + ' Generated Script.txt'
    PATH_FOR_GENERATED_SCRIPT_FOR_YOUTUBE_SHORT = my_constants.PATH_OF_FOLDER_FOR_GENERATED_SCRIPTS + \
                                                  '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR + \
                                                  '/' + ID_FOR_BOOK + ' ' + START_TIME + ' Generated Script for YouTube Short.txt'
    PATH_TEMPLATE_FOR_GENERATED_CONTENT = my_constants.PATH_OF_FOLDER_FOR_GENERATED_CONTENT + \
                                          '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR + \
                                          '/' + ID_FOR_BOOK + ' ' + START_TIME
    PATH_FOR_GENERATED_TRANSCRIPT = my_constants.PATH_OF_FOLDER_FOR_GENERATED_CONTENT + \
                                    '/' + NAME_OF_PODCAST_TO_PUBLISH_FOR + \
                                    '/' + ID_FOR_BOOK + ' ' + START_TIME + ' Transcript.txt'


def publish_new_episode_for_podcast():
    print('Publishing episode for: ' + SpecsForEpisode.DESCRIPTOR_FOR_BOOK + '\n' +
          'Book that will be recommended: ' + SpecsForEpisode.DESCRIPTOR_FOR_BOOK + ', ' +
          'available via ' + SpecsForEpisode.AFFILIATE_LINK_TO_BOOK
          )

    dict_for_youtube_short_customization = {
        'NAME_OF_EPISODE': SpecsForEpisode.DESCRIPTOR_FOR_BOOK,
        'NAME_OF_PODCAST': NAME_OF_PODCAST_TO_PUBLISH_FOR,
    }

    customized_script_for_youtube_short = SpecsForPodcast.TEXT_FOR_YOUTUBE_SHORT.format(
        **dict_for_youtube_short_customization)

    with open(SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT_FOR_YOUTUBE_SHORT, "w") as file_for_yt_short_script:
        file_for_yt_short_script.write(customized_script_for_youtube_short)

    def create_prompt() -> str:
        dict_for_prompt_customization = {
            'DISCLAIMER': SpecsForPodcast.DISCLAIMER,
            'AUTHORS_OF_BOOK_TO_RECOMMEND': SpecsForEpisode.AUTHORS_OF_BOOK_TO_RECOMMEND,
            'NAME_OF_PODCAST': NAME_OF_PODCAST_TO_PUBLISH_FOR,
            'NAME_OF_SPEAKER_1_IN_PODCAST': SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST,
            'NAME_OF_SPEAKER_2_IN_PODCAST': SpecsForPodcast.NAME_OF_SPEAKER_2_IN_PODCAST,
            'TITLE_OF_BOOK_TO_RECOMMEND': SpecsForEpisode.TITLE_OF_BOOK_TO_RECOMMEND
        }
        with open(my_constants.PATH_OF_PROMPT_TEMPLATE_FOR_SCRIPT_WITHOUT_CHAPTERS, 'r') as prompt_template_for_script:
            prompt_template = prompt_template_for_script.read()
        customized_prompt = prompt_template.format(**dict_for_prompt_customization)
        return customized_prompt

    prompt_for_episode = create_prompt()

    with open(SpecsForEpisode.PATH_FOR_CUSTOMIZED_PROMPT, "w") as file_for_prompt:
        file_for_prompt.write(prompt_for_episode)

    def get_script_from_gpt() -> str:
        # print('Prompt:', prompt_for_episode)
        openai.api_key = my_credentials.API_KEY_FOR_OPENAI

        def start_conversation_with_gpt(conversation):
            response = openai.ChatCompletion.create(model=my_constants.VERSION_OF_GPT_TO_USE, messages=conversation,
                                                    timeout=600)
            api_usage = response['usage']
            print('Total token consumed: {0}'.format(api_usage['total_tokens']))
            # stop means complete
            print(response['choices'][0].finish_reason)
            print(response['choices'][0].index)
            conversation.append(
                {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
            return conversation

        conversation = []
        conversation.append({'role': 'system', 'content': prompt_for_episode})
        conversation = start_conversation_with_gpt(conversation)
        reply = conversation[-1]['content'].strip()
        return reply

    count_of_gpt_access_tries = 0
    desired_number_of_gpt_access_tries = 0
    was_api_access_successful = False
    script_for_episode = ''

    while count_of_gpt_access_tries < desired_number_of_gpt_access_tries:
        count_of_gpt_access_tries += 1
        try:
            script_for_episode = get_script_from_gpt()
            print('GPT-4 reply:', script_for_episode)
            with open(SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT, "w") as file_for_script:
                file_for_script.write(script_for_episode)
            was_api_access_successful = True
            break
        except:
            print(
                f'''Try {count_of_gpt_access_tries} of {desired_number_of_gpt_access_tries} to access API of {my_constants.VERSION_OF_GPT_TO_USE} was unsuccessful.''')
            if count_of_gpt_access_tries < desired_number_of_gpt_access_tries:
                print(f'''Trying again...''')
            continue

    if not was_api_access_successful:
        pyperclip.copy(prompt_for_episode)
        with open(SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT, 'w') as _: pass
        print(f'''The custom-made prompt has been copied to your clipboard. Please paste it into ChatGPT and paste
        the generated script into the newly created text file (REMEMBER TO SAVE) at {SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT}''')
        input('Press enter when you have save the text file.')

    with open(SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT, "r") as file_for_script:
        script_for_episode = file_for_script.read()

    conversation_follows_symbol = '🟢'
    description_follows_symbol = '⚠️'
    tags_follow_symbol = '🏷️'

    index_of_conversation_follows_symbol = script_for_episode.find(conversation_follows_symbol)
    index_of_description_follows_symbol = script_for_episode.find(description_follows_symbol)
    index_of_tags_follow_symbol = script_for_episode.find(tags_follow_symbol)

    assert index_of_conversation_follows_symbol != -1
    assert index_of_description_follows_symbol != -1
    assert index_of_tags_follow_symbol != -1

    start_index_of_conversation = index_of_conversation_follows_symbol + len(conversation_follows_symbol)
    start_index_of_description = index_of_description_follows_symbol + len(description_follows_symbol)
    start_index_of_tags = index_of_tags_follow_symbol + len(tags_follow_symbol)

    script_for_conversation = script_for_episode[start_index_of_conversation:index_of_description_follows_symbol]
    description_of_episode = script_for_episode[start_index_of_description:index_of_tags_follow_symbol]
    string_of_keywords_for_episode = script_for_episode[start_index_of_tags:]
    list_of_keywords_for_episode = string_of_keywords_for_episode.split(", ")

    print(script_for_conversation)
    print('\n')
    print(description_of_episode)
    print('\n')
    print(string_of_keywords_for_episode)
    print('\n')
    print(list_of_keywords_for_episode)

    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' Description of Episode.txt', 'w') as file:
        file.write(description_of_episode)

    time.sleep(20)

    def create_html_link_with_text(url, link_text):
        return f'<a href="{url}">{link_text}</a>'

    def generate_info_on_where_to_listen(using_format_for_youtube: bool) -> str:

        info_on_where_to_listen = ''

        if using_format_for_youtube == True:
            # must post full links in YouTube Comments and Description
            for platform_url_pair in SpecsForPodcast.DICT_OF_WHERE_TO_LISTEN.items():
                info_on_where_to_listen += f'🎧 {platform_url_pair[0]}: {platform_url_pair[1]}\n\n'
            return info_on_where_to_listen

        # can post HTML tag links in Podcast Show Notes
        for platform_url_pair in SpecsForPodcast.DICT_OF_WHERE_TO_LISTEN.items():
            text_to_display = f'Listen on {platform_url_pair[0]}'
            wrapped_link = f'{platform_url_pair[1]}'
            info_on_where_to_listen += f'🎧 {create_html_link_with_text(wrapped_link, text_to_display)}\n\n'
        return info_on_where_to_listen

    text_for_affiliate_link_to_book = f'{SpecsForEpisode.DESCRIPTOR_FOR_BOOK} on Amazon'
    text_for_affiliate_link_to_audible_premium_plus_trial = f'Free trial of Audible Premium Plus'
    text_addition_for_affiliate_link_to_audible_premium_plus_trial = f', where, as of the date this episode is published, you can listen to the audiobook version of {SpecsForEpisode.DESCRIPTOR_FOR_BOOK}'
    text_for_donations_link = f'Donating to {NAME_OF_PODCAST_TO_PUBLISH_FOR}'
    disclaimer_for_affiliate_links = f'Feel free to check out the book recommendation and the free Audible Premium Plus trial via these Amazon affiliate links (Kindly note: As an Amazon Associate {NAME_OF_PODCAST_TO_PUBLISH_FOR} earns from qualifying purchases and trial sign-ups. Thank you so much for your support! 🙂)'
    goodbye_phrase = 'Thanks for listening! Take care & see you soon! ✌️🙂'
    etsy_ad_for_youtube_descriptions = 'Unique Wall Art from abstractartmoShop on Etsy: https://www.etsy.com/de-en/shop/abstractartmoShop?ref=seller-platform-mcnav'

    #placeholder_for_string_for_youtube_chapters = '{string_for_youtube_chapters}'
    placeholder_for_string_for_youtube_chapters = ''

    dict_for_text_snippets = {
        'Greeting for YouTube Video and Show Notes': f'''🙋 Hello and welcome to this episode of the {NAME_OF_PODCAST_TO_PUBLISH_FOR} podcast! {SpecsForPodcast.DISCLAIMER}''',
        'Greeting for YouTube Short Description': f'''🙋 Hello and welcome to this short-form video of the {NAME_OF_PODCAST_TO_PUBLISH_FOR} podcast! {SpecsForPodcast.DISCLAIMER}''',
        'Greeting for Description of YT Short': f'''🙋 Hello and welcome to {NAME_OF_PODCAST_TO_PUBLISH_FOR}!''',
        'Greeting for Comment of YouTube Video': f'''🙋 Hello and welcome to this episode of the {NAME_OF_PODCAST_TO_PUBLISH_FOR} podcast!''',
        'Info on where to listen, YouTube Version': f'''You can listen to {NAME_OF_PODCAST_TO_PUBLISH_FOR} on all of the following platforms:\n\n{generate_info_on_where_to_listen(using_format_for_youtube=True)}''',
        'Info on where to listen, Show Notes Version': f'''You can listen to {NAME_OF_PODCAST_TO_PUBLISH_FOR} on all of the following platforms:\n\n{generate_info_on_where_to_listen(using_format_for_youtube=False)}''',
        'Goodbye': goodbye_phrase,
        'Goodbye with link to Impressum, YouTube Version': f'{goodbye_phrase}\n\n\n\nImpressum: {SpecsForPodcast.URL_TO_IMPRESSUM}',
        'Goodbye with link to Impressum, Show Notes Version': f'{goodbye_phrase}\n\n\n\n{create_html_link_with_text(SpecsForPodcast.URL_TO_IMPRESSUM, "Impressum")}',
        'Affiliate Links, YouTube Version': f'''{disclaimer_for_affiliate_links}\n\n👉 {text_for_affiliate_link_to_book}: {SpecsForEpisode.AFFILIATE_LINK_TO_BOOK}\n\n👉 {text_for_affiliate_link_to_audible_premium_plus_trial + text_addition_for_affiliate_link_to_audible_premium_plus_trial}: {SpecsForPodcast.AMAZON_ASSOCIATES_LINK_FOR_AUDIBLE_PREMIUM_PLUS_TRIAL}''',
        'Affiliate Links, Show Notes Version': f'''{disclaimer_for_affiliate_links}\n\n👉 {create_html_link_with_text(SpecsForEpisode.AFFILIATE_LINK_TO_BOOK, text_for_affiliate_link_to_book)}\n\n👉 {create_html_link_with_text(SpecsForPodcast.AMAZON_ASSOCIATES_LINK_FOR_AUDIBLE_PREMIUM_PLUS_TRIAL, text_for_affiliate_link_to_audible_premium_plus_trial)}{text_addition_for_affiliate_link_to_audible_premium_plus_trial}''',
        'Donation, YouTube Version': f'''You can donate here: {SpecsForPodcast.LINK_FOR_DONATIONS} | Thank you very much for your support! 😎''',
        'Donation, Show Notes Version': f'''You can donate here: {create_html_link_with_text(SpecsForPodcast.LINK_FOR_DONATIONS, text_for_donations_link)} | Thank you very much for your support! 😎''',
        'Description of Episode': f'''Episode Description:\n{description_of_episode}''',
        'Description of Podcast': f'''Podcast Description:\n{SpecsForPodcast.DESCRIPTION_OF_PODCAST}''',
        'Pointer to description': f'''Feel free to check out the description for more info 😎'''
    }

    text_for_description_of_youtube_video = f'''{dict_for_text_snippets['Greeting for YouTube Video and Show Notes']}\n\n⭐️ {dict_for_text_snippets['Affiliate Links, YouTube Version']}\n\n⭐️ {dict_for_text_snippets['Info on where to listen, YouTube Version']}\n\n⭐️ {dict_for_text_snippets['Donation, YouTube Version']}\n\n⭐️ {etsy_ad_for_youtube_descriptions}\n\n🎙️ {dict_for_text_snippets['Description of Episode']}\n\n{placeholder_for_string_for_youtube_chapters}\n\n🎙️ {dict_for_text_snippets['Description of Podcast']}\n\n{dict_for_text_snippets['Goodbye with link to Impressum, YouTube Version']}'''
    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_description_of_youtube_video.txt',
              'w') as file:
        file.write(text_for_description_of_youtube_video)

    text_for_comment_of_youtube_video = f'''{dict_for_text_snippets['Greeting for Comment of YouTube Video']}\n⭐️ {dict_for_text_snippets['Affiliate Links, YouTube Version']}\n\n{dict_for_text_snippets['Pointer to description']}\n\n{dict_for_text_snippets['Goodbye']}'''
    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_comment_of_youtube_video.txt',
              'w') as file:
        file.write(text_for_comment_of_youtube_video)

    text_for_description_of_youtube_short = f'''{dict_for_text_snippets['Greeting for YouTube Short Description']}\n\n⭐️ {dict_for_text_snippets['Affiliate Links, YouTube Version']}\n\n⭐️ {dict_for_text_snippets['Info on where to listen, YouTube Version']}\n⭐️ {dict_for_text_snippets['Donation, YouTube Version']}\n\n⭐️ {etsy_ad_for_youtube_descriptions}\n\n🎙️ {dict_for_text_snippets['Description of Episode']}\n\n🎙️ {dict_for_text_snippets['Description of Podcast']}\n\n{dict_for_text_snippets['Goodbye with link to Impressum, YouTube Version']}'''
    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_description_of_youtube_short.txt',
              'w') as file:
        file.write(text_for_description_of_youtube_short)

    text_for_comment_of_youtube_short = f'''{dict_for_text_snippets['Affiliate Links, YouTube Version']}\n\n{dict_for_text_snippets['Info on where to listen, YouTube Version']}\n{dict_for_text_snippets['Goodbye']}'''
    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_comment_of_youtube_short.txt',
              'w') as file:
        file.write(text_for_comment_of_youtube_short)

    text_for_show_notes = f'''{dict_for_text_snippets['Greeting for YouTube Video and Show Notes']}\n\n⭐️ {dict_for_text_snippets['Affiliate Links, Show Notes Version']}\n\n⭐️ {dict_for_text_snippets['Info on where to listen, Show Notes Version']}\n\n⭐️ {dict_for_text_snippets['Donation, Show Notes Version']}\n\n🎙️ {dict_for_text_snippets['Description of Episode']}\n\n🎙️ {dict_for_text_snippets['Description of Podcast']}\n\n{dict_for_text_snippets['Goodbye with link to Impressum, Show Notes Version']}'''
    with open(SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_show_notes.txt', 'w') as file:
        file.write(text_for_show_notes)

    dict_of_character_limits_for_youtube_content = {
        'video title truncation': 70,
        'video title': 100,
        'video description': 4600,  # chapter string will still be added at the end
        'video comment': 10000
    }

    title_for_youtube_video = SpecsForEpisode.TITLE_OF_EPISODE
    title_for_youtube_short = SpecsForEpisode.TITLE_OF_EPISODE + ' Teaser'

    is_any_hard_limit_breached = False
    will_any_title_be_truncated = False

    def does_string_respect_youtube_character_limit_for(string_to_check: str, type: str):
        nonlocal is_any_hard_limit_breached
        nonlocal will_any_title_be_truncated

        is_character_limit_respected = len(string_to_check) <= dict_of_character_limits_for_youtube_content[type]
        if not is_character_limit_respected:
            if type == 'video title truncation':
                will_any_title_be_truncated = True
            else:
                is_any_hard_limit_breached = True
        return is_character_limit_respected

    print('Do all the texts conform to the character limits?')
    print(
        f'''text_for_description_of_youtube_video: {does_string_respect_youtube_character_limit_for(text_for_description_of_youtube_video, 'video description')}''')
    print(
        f'''text_for_comment_of_youtube_video: {does_string_respect_youtube_character_limit_for(text_for_comment_of_youtube_video, 'video comment')}''')
    print(
        f'''text_for_description_of_youtube_short: {does_string_respect_youtube_character_limit_for(text_for_description_of_youtube_short, 'video description')}''')
    print(
        f'''text_for_comment_of_youtube_short: {does_string_respect_youtube_character_limit_for(text_for_comment_of_youtube_short, 'video comment')}''')
    print(
        f'''title_for_youtube_video: {does_string_respect_youtube_character_limit_for(title_for_youtube_video, 'video title')}''')
    print(
        f'''title_for_youtube_video trunc : {does_string_respect_youtube_character_limit_for(title_for_youtube_video, 'video title truncation')}''')
    print(
        f'''title_for_youtube_short: {does_string_respect_youtube_character_limit_for(title_for_youtube_short, 'video title')}''')
    print(
        f'''title_for_youtube_short trunc: {does_string_respect_youtube_character_limit_for(title_for_youtube_short, 'video title truncation')}''')

    if is_any_hard_limit_breached:
        return

    #exit()

    wait_seconds_after_start = 0.0
    secondsPassed = wait_seconds_after_start

    def convert_to_timestamp_string(seconds_passed: float) -> str:
        adjusted_seconds = int(seconds_passed + 0.5)
        minutes, seconds = divmod(adjusted_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    #def generate_chapter_metadata_entry(start_in_seconds, end_in_seconds, title):
    #    return f'\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={round(start_in_seconds * 1000)}\nEND={round(end_in_seconds * 1000)}\ntitle={title}'

    #chapter_metadata = f';FFMETADATA1'
    transcript = ""
    name_of_speaker_to_go = SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST
    transcript += SpecsForEpisode.TITLE_OF_EPISODE + '\n\n' + name_of_speaker_to_go + ': '
    speaker_segment_to_come = 1
    list_of_speaker_audio_file_clips = []

    #timestamp_of_last_begun_chapter = 0
    #last_chapter_title = ""
    list_of_speaker_text_parts = script_for_conversation.split("🔄")
    elevenlabs_user = ElevenLabsUser(my_credentials.API_KEY_FOR_ELEVENLABS)

    elevenlabs_user.get_voices_by_name(SpecsForPodcast.NAME_OF_SPEAKER_1_IN_ELEVENLABS)[0].edit_settings(
        SpecsForPodcast.DICT_OF_SPEAKER_1['stability in elevenlabs'],
        SpecsForPodcast.DICT_OF_SPEAKER_1['clarity in elevenlabs']
    )

    elevenlabs_user.get_voices_by_name(SpecsForPodcast.NAME_OF_SPEAKER_2_IN_ELEVENLABS)[0].edit_settings(
        SpecsForPodcast.DICT_OF_SPEAKER_2['stability in elevenlabs'],
        SpecsForPodcast.DICT_OF_SPEAKER_2['clarity in elevenlabs']
    )

    #string_for_youtube_chapters = ''

    def generate_audio_data_from_elevenlabs(name_of_speaker_in_podcast, text):
        if name_of_speaker_in_podcast == SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST:
            return elevenlabs_user.get_voices_by_name(
                SpecsForPodcast.NAME_OF_SPEAKER_1_IN_ELEVENLABS
            )[0].generate_audio_bytes(text)
        else:
            return elevenlabs_user.get_voices_by_name(
                SpecsForPodcast.NAME_OF_SPEAKER_2_IN_ELEVENLABS
            )[0].generate_audio_bytes(text)

    for speaker_text_part in list_of_speaker_text_parts:
        try:
            #if speaker_text_part[0] == "❓":
                #chapter_title = speaker_text_part.split("❓")[1]
                #speaker_text_part = speaker_text_part.split("❓")[2]

                #string_for_youtube_chapters += convert_to_timestamp_string(
                    #secondsPassed
                #) + " - " + chapter_title + "\n"

                #if secondsPassed > 0:
                    #pass
                    #chapter_metadata += generate_chapter_metadata_entry(
                    #timestamp_of_last_begun_chapter,
                    #secondsPassed,
                    #last_chapter_title
                    #)
                #last_chapter_title = chapter_title
                #timestamp_of_last_begun_chapter = secondsPassed

            info_for_speaker_audio_file = f' Segment number {speaker_segment_to_come} – {name_of_speaker_to_go}.wav'
            path_for_speaker_audio = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + info_for_speaker_audio_file
            save_bytes_to_path(
                path_for_speaker_audio,
                generate_audio_data_from_elevenlabs(name_of_speaker_to_go, speaker_text_part)
            )
            audio_file_clip_of_speaker_part_audio = AudioFileClip(path_for_speaker_audio, fps=44100)
            list_of_speaker_audio_file_clips.append(audio_file_clip_of_speaker_part_audio)
            secondsPassed += audio_file_clip_of_speaker_part_audio.duration

        except requests.exceptions.RequestException:
            print("Couldn't generate an output, likely out of tokens; or another issue occurred.")

        transcript += speaker_text_part

        if speaker_segment_to_come + 1 > len(list_of_speaker_text_parts):
            break

        transcript += '\n\n'

        if name_of_speaker_to_go == SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST:
            transcript += SpecsForPodcast.NAME_OF_SPEAKER_2_IN_PODCAST + ": "
            name_of_speaker_to_go = SpecsForPodcast.NAME_OF_SPEAKER_2_IN_PODCAST

        else:
            transcript += SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST + ": "
            name_of_speaker_to_go = SpecsForPodcast.NAME_OF_SPEAKER_1_IN_PODCAST

        speaker_segment_to_come += 1

    #chapter_metadata += generate_chapter_metadata_entry(timestamp_of_last_begun_chapter, secondsPassed,
     #                                                   last_chapter_title)

    #dict_for_inserting_youtube_chapters = {
    #    'string_for_youtube_chapters': string_for_youtube_chapters
    #}

    #text_for_description_of_youtube_video_with_chapters = text_for_description_of_youtube_video.format(
    #    **dict_for_inserting_youtube_chapters)

    #with open(
            #SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' text_for_description_of_youtube_video_with_chapters.txt',
            #'w') as file:
        #file.write(text_for_description_of_youtube_video_with_chapters)

    #path_of_metadata_file = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' Chapter Metadata for M4A.txt'
    #with open(path_of_metadata_file, "w") as metadata_file:
    #    metadata_file.write(chapter_metadata)

    with open(SpecsForEpisode.PATH_FOR_GENERATED_TRANSCRIPT, 'w') as transcript_file:
        transcript_file.write(transcript)

    audio_file_clip_with_concatenated_speaker_parts = concatenate_audioclips(list_of_speaker_audio_file_clips)
    path_for_audio_with_concatenated_speaker_parts = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + \
                                                     ' Concatenated Speaker Parts Audio.wav'

    audio_file_clip_with_concatenated_speaker_parts.write_audiofile(
        path_for_audio_with_concatenated_speaker_parts,
        fps=44100
    )

    def optimize_audio_add_metadata_and_get_path(
            title_of_auphonic_production: str,
            id_of_auphonic_preset_to_use: str,
            path_of_audio_to_optimize: str,
            path_of_metadata=None
    ) -> str:

        modified_title_of_auphonic_production = \
            f'{title_of_auphonic_production} {NAME_OF_PODCAST_TO_PUBLISH_FOR} {SpecsForEpisode.ID_FOR_BOOK} {START_TIME}'

        payload_for_request = {
            "preset": id_of_auphonic_preset_to_use,
            "title": title_of_auphonic_production,
            "action": "start"
        }

        with open(path_of_audio_to_optimize, "rb") as audio_to_optimize:
            file_tuple_for_request = {
                "input_file": (path_of_audio_to_optimize, audio_to_optimize)
            }

            response_from_auphonic_production = requests.post(
                my_constants.URL_OF_AUPHONIC_PRODUCTIONS,
                auth=(my_credentials.USERNAME_FOR_AUPHONIC, my_credentials.PASSWORD_FOR_AUPHONIC),
                data=payload_for_request,
                files=file_tuple_for_request,
                timeout=180 * 60)

        json_from_response_from_auphonic_production = response_from_auphonic_production.json()
        print(json_from_response_from_auphonic_production)
        production_uuid = json_from_response_from_auphonic_production["data"]["uuid"]

        while True:
            status_url = f'https://auphonic.com/api/production/{production_uuid}.json'
            status_response = requests.get(
                status_url,
                auth=(my_credentials.USERNAME_FOR_AUPHONIC, my_credentials.PASSWORD_FOR_AUPHONIC)
            )
            json_from_status_response = status_response.json()

            if json_from_status_response["data"]["status_string"] == "Done":
                break

            print("Auphonic is processing audio, waiting 15 seconds...")
            time.sleep(15)

        download_url = json_from_status_response["data"]["output_files"][0]["download_url"]
        path_of_auphonic_output_file = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + \
                                       f'{title_of_auphonic_production} Audio Optimized by Auphonic.wav'
        response_from_auphonic_production = requests.get(
            download_url,
            auth=(my_credentials.USERNAME_FOR_AUPHONIC, my_credentials.PASSWORD_FOR_AUPHONIC),
            stream=True
        )

        with open(path_of_auphonic_output_file, "wb") as audio_from_auphonic:
            for chunk in response_from_auphonic_production.iter_content(chunk_size=8192):
                if chunk:
                    audio_from_auphonic.write(chunk)

        print("Auphonic output file saved as:", path_of_auphonic_output_file)
        time.sleep(3)

        path_of_output_m4a = path_of_auphonic_output_file

        def add_metadata_to_m4a_and_get_path(path_of_m4a_to_add_metadata_to: str, path_of_metadata_file: str):

            path_of_m4a_with_metadata = f"{path_of_m4a_to_add_metadata_to[:-4]} with Metadata.m4a"
            command = f'ffmpeg -i "{path_of_m4a_to_add_metadata_to}" -i "{path_of_metadata_file}" -map_metadata 1 -codec copy "{path_of_m4a_with_metadata}"'
            subprocess.run(command, shell=True)

            time.sleep(3)

            print("Chapters added successfully!")

            return path_of_m4a_with_metadata

        if path_of_metadata is not None:
            path_of_output_m4a = add_metadata_to_m4a_and_get_path(path_of_auphonic_output_file, path_of_metadata)

        return path_of_output_m4a

    path_of_final_audio_for_video_and_podcast = optimize_audio_add_metadata_and_get_path(
        title_of_auphonic_production='Convo',
        id_of_auphonic_preset_to_use=my_credentials.PRESET_ID_FOR_AUPHONIC,
        path_of_audio_to_optimize=path_for_audio_with_concatenated_speaker_parts,
        #path_of_metadata=path_of_metadata_file
    )

    audiofileclip_for_youtube_video = AudioFileClip(path_of_final_audio_for_video_and_podcast, fps=44100)

    image_clip_for_youtube_video = ImageClip(
        SpecsForPodcast.PATH_TO_PODCAST_IMAGE,
        duration=audiofileclip_for_youtube_video.duration + 2
    )

    image_clip_for_youtube_video = image_clip_for_youtube_video.set_audio(audiofileclip_for_youtube_video)

    path_of_video_for_youtube_video = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' YouTube Video.mp4'

    image_clip_for_youtube_video.write_videofile(path_of_video_for_youtube_video,
                                                 codec='libx264',
                                                 audio_codec='aac',
                                                 bitrate='5000k',
                                                 fps=1
                                                 )

    # Write Short
    import random

    dict_of_random_speaker = random.choice(list(SpecsForPodcast.DICT_OF_SPEAKERS.items()))[1]

    elevenlabs_speaker_name_for_youtube_short = dict_of_random_speaker['name in elevenlabs']
    # gender_of_speaker_for_youtube_short = dict_of_random_speaker['gender']
    stability_for_speaker_for_youtube_short = dict_of_random_speaker['stability in elevenlabs']
    clarity_for_speaker_for_youtube_short = dict_of_random_speaker['clarity in elevenlabs']
    path_to_avatar_image_for_speaker_for_youtube_short = dict_of_random_speaker['path to avatar image']

    elevenlabs_user.get_voices_by_name(
        elevenlabs_speaker_name_for_youtube_short
    )[0].edit_settings(
        stability_for_speaker_for_youtube_short,
        clarity_for_speaker_for_youtube_short
    )

    generated_audio_bytes_for_youtube_short = elevenlabs_user.get_voices_by_name(
        elevenlabs_speaker_name_for_youtube_short
    )[0].generate_audio_bytes(customized_script_for_youtube_short)

    path_of_youtube_short_audio = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' YouTube Short Audio.wav'
    save_bytes_to_path(path_of_youtube_short_audio, generated_audio_bytes_for_youtube_short)

    path_of_optimized_m4a_for_youtube_short = optimize_audio_add_metadata_and_get_path(
        title_of_auphonic_production='YouTube Short',
        id_of_auphonic_preset_to_use=my_credentials.PRESET_ID_FOR_AUPHONIC,
        path_of_audio_to_optimize=path_of_youtube_short_audio
    )

    '''###### D-ID


    # use mp3 preset of auphonic
    my_credentials.MP3_PRESET_ID_FOR_AUPHONIC
    path_to_avatar_image_for_speaker_for_youtube_short'''

    video_width = 1080
    video_height = 1920
    square_size = min(video_width, video_height)

    audiofileclip_for_short = AudioFileClip(path_of_optimized_m4a_for_youtube_short, fps=44100)

    music = AudioFileClip(my_constants.PATH_TO_INSPIRING_TECHNO_BEAT, fps=44100)

    # Make the music the same duration as the video
    music = music.subclip(0, audiofileclip_for_short.duration + 1)

    # Reduce music volume
    music = music.volumex(0.4)

    # Fade out music in the last 3 seconds
    music = music.audio_fadeout(3)

    # Combine original audio and music
    final_audio = CompositeAudioClip([audiofileclip_for_short, music])

    image_clip_for_short = ImageClip(
        SpecsForPodcast.PATH_TO_IMAGE_FOR_YOUTUBE_SHORT,
        duration=final_audio.duration
    )

    image_clip_for_short = image_clip_for_short.set_audio(final_audio)
    image_clip_for_short = image_clip_for_short.resize(width=square_size)

    background = ColorClip((video_width, video_height), color=(0, 0, 0), duration=image_clip_for_short.duration)

    pos_x = (video_width - square_size) // 2
    pos_y = (video_height - square_size) // 2

    final_video_for_youtube_short = CompositeVideoClip([background, image_clip_for_short.set_position((pos_x, pos_y))])
    path_of_video_for_youtube_short = SpecsForEpisode.PATH_TEMPLATE_FOR_GENERATED_CONTENT + ' YouTube Shorts Video.mp4'
    final_video_for_youtube_short.write_videofile(path_of_video_for_youtube_short,
                                                  codec='libx264',
                                                  audio_codec='aac',
                                                  bitrate='5000k',
                                                  fps=30
                                                  )

    print('----------------------------------')
    print('Uploading to Transistor')
    print('----------------------------------')

    # Upload Podcast Episode

    time.sleep(20)

    filename_for_transistor_upload = SpecsForEpisode.TITLE_OF_EPISODE + START_TIME + ".m4a"

    response_from_transistor_upload_auth = requests.get(
        my_constants.URL_OF_TRANSISTOR_UPLOAD_AUTHORIZATION,
        headers={
            'x-api-key': my_credentials.API_KEY_FOR_TRANSISTOR
        },
        params={
            "filename": filename_for_transistor_upload
        }
    )

    json_of_response_from_transistor_upload_auth = response_from_transistor_upload_auth.json()

    print(json_of_response_from_transistor_upload_auth)

    upload_url = json_of_response_from_transistor_upload_auth["data"]["attributes"]["upload_url"]
    content_type = json_of_response_from_transistor_upload_auth["data"]["attributes"]["content_type"]
    audio_url = json_of_response_from_transistor_upload_auth["data"]["attributes"]["audio_url"]

    # Upload audio file
    with open(path_of_final_audio_for_video_and_podcast, "rb") as audio_file:
        upload_headers = {"Content-Type": content_type}
        upload_response = requests.put(upload_url, headers=upload_headers, data=audio_file)

    if upload_response.status_code == 200:
        print(f"Audio file uploaded successfully. Audio URL: {audio_url}")

    else:
        print("Failed to upload audio file.")

    data_of_episode_to_upload = {
        "episode[show_id]": SpecsForPodcast.SHOW_ID_ON_TRANSISTOR,
        "episode[title]": SpecsForEpisode.TITLE_OF_EPISODE,
        #"episode[description]": text_for_show_notes + "\n\n" + "{{chapters}}",
        "episode[description]": text_for_show_notes,
        "episode[transcript_text]": transcript,
        "episode[audio_url]": audio_url,
        "episode[keywords]": string_of_keywords_for_episode,
        "episode[image_url]": SpecsForPodcast.URL_TO_PODCAST_IMAGE
    }

    response = requests.post(
        my_constants.URL_OF_TRANSISTOR_EPISODES,
        headers={
            'x-api-key': my_credentials.API_KEY_FOR_TRANSISTOR
        },
        data=data_of_episode_to_upload
    )

    if response.status_code == 201:
        print("Episode created successfully!")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    from _datetime import datetime

    if not SHOULD_UPLOAD_AS_DRAFT:
        # Set the episode status to 'published' and set the published_at timestamp
        payload_for_updating_episode_status_on_transistor = {
            "episode": {
                "status": "published",
                "published_at": datetime.now(pytz.timezone("Europe/Berlin")).isoformat()
            }
        }

        response = requests.patch(
            my_constants.URL_OF_TRANSISTOR_EPISODES + f'/{response.json()["data"]["id"]}/publish',
            json=payload_for_updating_episode_status_on_transistor,
            headers={
                'x-api-key': my_credentials.API_KEY_FOR_TRANSISTOR
            }
        )

        if response.status_code == 200:
            print("Episode published successfully")
        else:
            print("Error:", response.status_code, response.text)

    import datetime

    def upload_to_youtube_and_post_comment(
            title_for_snippet_for_request_body: str,
            description_for_snippet_for_request_body: str,
            category_id_for_snippet_for_request_body: str,
            tags_for_snippet_for_request_body: list,
            should_notify_subscribers: bool,
            path_of_videofile_to_upload: str,
            comment_to_post: str):

        service = create_service(
            my_constants.PATH_TO_GOOGLE_CLIENT_SECRET_JSON,
            'youtube',
            'v3',
            [my_constants.URL_OF_YOUTUBE_SCOPE],
            timeout=120 * 60
        )

        time.sleep(7)

        request_body = {
            'snippet': {
                'title': title_for_snippet_for_request_body,
                'description': description_for_snippet_for_request_body,
                'categoryId': category_id_for_snippet_for_request_body,
                'tags': tags_for_snippet_for_request_body
            },
            'status': {
                'privacyStatus': 'private',
                'publishedAt': (datetime.datetime.now() + datetime.timedelta(days=0, seconds=3)).isoformat() + '.000Z',
                'selfDeclaredMadeForKids': False
            },
            'notifySubscribers': should_notify_subscribers
        }

        media_file = MediaFileUpload(path_of_videofile_to_upload)
        response_of_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        ).execute()

        id_of_uploaded_video = response_of_upload.get('id')

        time.sleep(20)

        # Switch privacy status
        counter = 0

        response_update_video = service.videos().list(id=id_of_uploaded_video, part='status').execute()
        update_video_body = response_update_video['items'][0]

        while 100 > counter:
            if update_video_body['status']['uploadStatus'] == 'processed':
                update_video_body['status']['privacyStatus'] = 'unlisted' if SHOULD_UPLOAD_AS_DRAFT else 'public'
                service.videos().update(
                    part='status',
                    body=update_video_body
                ).execute()
                print('Video {0} privacy status is updated to "{1}"'.format(update_video_body['id'],
                                                                            update_video_body['status'][
                                                                                'privacyStatus']))
                break
            # adjust the duration based on your video size
            time.sleep(25)
            response_update_video = service.videos().list(id=id_of_uploaded_video, part='status').execute()
            update_video_body = response_update_video['items'][0]
            counter += 1

        time.sleep(25)  # Adjust the duration as needed

        def post_comment(service, video_id, text):
            try:
                body = {
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": text
                            }
                        }
                    }
                }
                response = service.commentThreads().insert(
                    part="snippet",
                    body=body
                ).execute()

                print(f"Comment posted: {response['snippet']['topLevelComment']['snippet']['textOriginal']}")

            except HttpError as error:
                print(f"An error occurred: {error}")
                raise error

        creds = credentials.Credentials.from_authorized_user_file(my_constants.PATH_TO_YOUTUBE_TOKEN_JSON)
        post_comment(service, id_of_uploaded_video, comment_to_post)

    print('----------------------------------')
    print('Uploading to YouTube')
    print('----------------------------------')

    upload_to_youtube_and_post_comment(
        title_for_snippet_for_request_body=title_for_youtube_video,
        #description_for_snippet_for_request_body=text_for_description_of_youtube_video_with_chapters,
        description_for_snippet_for_request_body=text_for_description_of_youtube_video,
        category_id_for_snippet_for_request_body='24',
        tags_for_snippet_for_request_body=list_of_keywords_for_episode,
        should_notify_subscribers=False,
        path_of_videofile_to_upload=path_of_video_for_youtube_video,
        comment_to_post=text_for_comment_of_youtube_video
    )

    upload_to_youtube_and_post_comment(
        title_for_snippet_for_request_body=title_for_youtube_short,
        description_for_snippet_for_request_body=text_for_description_of_youtube_short,
        category_id_for_snippet_for_request_body='24',
        tags_for_snippet_for_request_body=list_of_keywords_for_episode,
        should_notify_subscribers=False,
        path_of_videofile_to_upload=path_of_video_for_youtube_short,
        comment_to_post=text_for_comment_of_youtube_short
    )

    if will_any_title_be_truncated:
        print('The title of at least one uploaded YouTube video might be truncated. Please check.')


publish_new_episode_for_podcast()
