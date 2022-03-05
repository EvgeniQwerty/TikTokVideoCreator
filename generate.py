from pytube import Playlist
from pytube import YouTube
from moviepy.editor import *


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
    playlist = Playlist(playlist_url)
    counter = 1

    for video in playlist:

        try:
            yt = YouTube(video)
            print("{} track. {}, {} seconds".format(counter, yt.title, yt.length))
            counter += 1

            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

            clip = VideoFileClip("{}.mp4".format(yt.title), audio=True).subclip(yt.length - 90, yt.length - 75)
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

            clip_txt = TextClip(txt, color='white', align='West', fontsize=80, font='Arial-Bold', method='label',
                                stroke_color='black', stroke_width=3)

            final = CompositeVideoClip([clip, clip_txt.set_pos(('center', 'center'))], size=moviesize)

            final.set_duration(15).write_videofile("final//{}.mp4".format(yt.title))

        except:
            print("ERROR while downloading or creating clip")
            pass


if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLxnIGAClR9Jv5W2PW4N_XsZqL2bv8zwJc"
    main(playlist_url)
