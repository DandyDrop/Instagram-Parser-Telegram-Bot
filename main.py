# default modules:
import os
import time
import base64

# external modules:
import telebot
import requests
import psycopg2
from instagrapi import Client
from io import BytesIO
from PIL import Image

conn = psycopg2.connect(os.environ["DB_STRING"])
cur = conn.cursor()
bot = telebot.TeleBot(os.environ["TGB_TOKEN"])
cl = Client()

# bot.create_forum_topic(chat_id=-1001779546974, name="mus.limovam")
count_b = int(input("Need to do this to database > \n"))
count = count_b

def get_by_user(username: str, topic_id):
    # L = instaloader.Instaloader()
    # L.login("privetmalysh4", "uUi,!856#@2x)?h")
    # profile = instaloader.Profile.from_username(L.context, username)
    # for post in profile.get_posts():
    #     print(post.url)
    user_id = cl.user_id_from_username(username)  # get the user id of the profile you want
    medias = cl.user_medias_gql(int(user_id))  # get a list of media objects
    for media in medias:   # extract only the urls
        print(media)
        print(media.code)
        print(media.id)
        if media.media_type == 8:
            for photo in media.resources:
                send_photo(photo.thumbnail_url, topic_id)
                time.sleep(3)
            final_caption = f'<a href="https://www.instagram.com/p/{media.code}">Post</a>\n\n'
            final_caption += f'Taken at {str(media.taken_at)}\n\n'
            if len(media.caption_text) != 0:
                final_caption += f"Caption:\n{media.caption_text}\n\n"
                if media.user.username != username:
                    final_caption += f"Collaboration with {media.user.username}\n\n"

            bot.send_message(chat_id="-1001779546974", message_thread_id=topic_id,
                             text=final_caption, parse_mode='html')
            global count
            count += 1

        elif media.media_type == 1:
            send_photo(media.thumbnail_url, topic_id)

        time.sleep(3)

def send_photo(link, topic_id):
    try:
        bot.send_photo(chat_id="-1001779546974", message_thread_id=topic_id, photo=link)
        global count
        count += 1

    except Exception as e:
        if "Bad Request" in str(e):
            print(e)
        else:
            raise e

# needs to be finished
def upscale(image_url):
    url = "https://nightfury-image-face-upscale-restoration-g-c878a3a.hf.space/api/predict"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}
    response = requests.get(image_url)
    base64_image = base64.b64encode(response.content).decode('utf-8')
    base64_url = "data:image/jpeg;base64," + base64_image
    input_payload = {"data": [base64_url, 'v1.4', 2]}
    r = requests.post(url, headers=headers, json=input_payload, timeout=200)

    json_r = r.json()
    # for el in json_r['data']:
    #     print(el, "\n\n\n\n\n\n\n\n\n")

    image_data = json_r['data'][0].split(",")[1]
    decoded_image_data = base64.b64decode(image_data)
    image = Image.open(BytesIO(decoded_image_data))
    image.save("imager3.png")


get_by_user("mus.limovam", count_b)
print(f"\n\nCounter:\n {count}\n\n{count - count_b} messages sent")










