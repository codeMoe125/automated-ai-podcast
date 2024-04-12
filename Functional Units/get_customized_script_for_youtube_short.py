from AutomatedAIPodcast import SpecsForEpisode, NAME_OF_PODCAST_TO_PUBLISH_FOR, SpecsForPodcast

dict_for_youtube_short_customization = {
    'NAME_OF_EPISODE': SpecsForEpisode.DESCRIPTOR_FOR_BOOK,
    'NAME_OF_PODCAST': NAME_OF_PODCAST_TO_PUBLISH_FOR,
}

customized_script_for_youtube_short = SpecsForPodcast.TEXT_FOR_YOUTUBE_SHORT.format(
    **dict_for_youtube_short_customization)

with open(SpecsForEpisode.PATH_FOR_GENERATED_SCRIPT_FOR_YOUTUBE_SHORT, "w") as file_for_yt_short_script:
    file_for_yt_short_script.write(customized_script_for_youtube_short)