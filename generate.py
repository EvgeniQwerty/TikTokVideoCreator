from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *
from os import getcwd, listdir
from random import randint


def downloadVideosFromPlaylist(playlist_url):
    print('Downloading videos from playlist')
    playlist = Playlist(playlist_url)
    playlist = playlist[:10]
    print('{} videos in the playlist'.format(len(playlist)))
    for video in playlist:

        try:
            yt = YouTube(video)
            print('{}, length - {}'.format(yt.title, yt.length))
            print('Downloading video...')
            script_path = os.getcwd()
            final_path = '{}//visual'.format(script_path)
            path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')\
                .desc().first().download(output_path=final_path, filename='{} {}.mp4'.format(yt.length, yt.title))
            print(path)
            print('Complete!')
        except:
            print('Error while downloading video')


#generate text for the video
def concatTxt(artist_name, track_title, splitter=''):
    text = ""

    if track_title.find('[') >= 0:
        track_title = track_title.split('[')[0]

    if splitter:
        artist_name = artist_name.split(splitter)
        if track_title.find('(') >= 0:
            track_title = track_title.split('(')
            if len(track_title) == 2:
                text = "Techno Track\nof the Day\n\n{} &\n{} -\n{}\n({}".format(artist_name[0].strip(), artist_name[1].strip(),
                                                                               track_title[0].strip(), track_title[1].strip())
            else:
                text = "Techno Track\nof the Day\n\n{} &\n{} -\n{}".format(artist_name[0].strip(), artist_name[1].strip(),
                                                                          track_title[0].strip())
        else:
            text = "Techno Track\nof the Day\n\n{} &\n{} -\n{}".format(artist_name[0].strip(), artist_name[1].strip(),
                                                                      track_title.strip())
    else:
        if track_title.find('(') >= 0:
            track_title = track_title.split('(')
            if len(track_title) == 2:
                text = "Techno Track\nof the Day\n\n{} -\n{}\n({}".format(artist_name.strip(), track_title[0].strip(),
                                                                         track_title[1].strip())
            else:
                text = "Techno Track\nof the Day\n\n{} -\n{}".format(artist_name.strip(), track_title[0].strip())
        else:
            text = "Techno Track\nof the Day\n\n{} -\n{}".format(artist_name.strip(), track_title.strip())

    return text


def main(playlist_url):
    print('Music downloader')
    playlist = Playlist(playlist_url)
    counter = 1
    print('{} tracks in the playlist'.format(len(playlist)))

    for video in playlist:

        try:
            yt = YouTube(video)
            title = yt.title
            print("{} track. {}, {} seconds".format(counter, yt.title, yt.length))
            counter += 1

            #скачиваем трек
            script_path = os.getcwd()
            final_path = '{}//music'.format(script_path)
            print('Downloading...')
            yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=final_path)
            print('Done!')
            video_folder_files = listdir('{}//visual'.format(script_path))
            rand_video = video_folder_files[randint(0, len(video_folder_files)-1)]
            length_of_video = int(rand_video.split(' ')[0])
            position = randint(1, length_of_video - 200)
            clip = VideoFileClip('{}/visual/{}'.format(script_path, rand_video), audio=False).subclip(position, position + 7)
            music = AudioFileClip('{}/music/{}.webm'.format(script_path, yt.title)).subclip(yt.length - 90, yt.length - 83)
            w, h = clip.size
            w = int(w)
            h = int(h)
            clip = clip.crop(x_center=w // 2, y_center=h // 2, width=h, height=h)
            clip = clip.resize((1080, 1080))
            moviesize = 1080, 1080

            title = yt.title.split('-')
            txt = ""

            if len(title) == 2:
                if title[0].find(',') >= 0:
                    txt = concatTxt(title[0], title[1], ',')
                elif title[0].find('&') >= 0:
                    txt = concatTxt(title[0], title[1], '&')
                elif title[0].find('feat') >= 0:
                    txt = concatTxt(title[0], title[1], 'feat')
                else:
                    txt = concatTxt(title[0], title[1])
            else:
                # if title do not consist of name of artist or name of the track
                print("ERROR. Title do not consists of name of artist or name of the track")
                continue

            clip_txt = TextClip(txt, color='white', align='West', fontsize=80, font='Candara-Bold-Italic', method='label',
                                stroke_color='black', stroke_width=3)

            final = CompositeVideoClip([clip, clip_txt.set_pos(('center', 'center'))], size=moviesize)
            final = final.set_audio(music)
            final.set_duration(7).write_videofile("final//{}.mp4".format(yt.title))

        except:
            print("ERROR while downloading or creating clip")
            pass


if __name__ == "__main__":
    print('-------------------------')
    print('TikTok Video Creator v0.2')
    print('-------------------------')
    print()
    #visuals_playlist_url = "https://www.youtube.com/playlist?list=PLCqJefJxoW8wRGX7iAgImBcz084j9wM0h"
    #downloadVideosFromPlaylist(visuals_playlist_url)
    music_playlist_url = 'https://www.youtube.com/playlist?list=PLUGshIgZ8go9HT0dIUqnw3T2TjVB69ba8'
    main(music_playlist_url)
