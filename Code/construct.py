"""
discord bot - Nanawoakari
"""

from __future__ import unicode_literals  # must be placed top
import os
import sys
import discord
import datetime
import time
import json
import math
import urllib.request
from twitter import Api
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# parameter json loader
token_file_dir = os.path.join(*os.getcwd().split('\\')[1:-1])
with open(os.path.join(os.sep, token_file_dir, "tokens.json")) as f:
    access_info = json.load(f)

# parameters
targetChannels = access_info["targetChannel"]
target_ID = access_info["target_id"]
discord_token = access_info["discord_token"]
authentication = access_info["authentication"]

# twitter api authentication
api = Api(
    consumer_key=authentication["consumer_key"],
    consumer_secret=authentication["consumer_secret"],
    access_token_key=authentication["access_token_key"],
    access_token_secret=authentication["access_token_secret"]
)

# Get User ID
# It will be updated as list
nanawoakari = api.GetUser(screen_name=target_ID[0]).id_str
nanawo_staff = api.GetUser(screen_name=target_ID[1]).id_str

def strftime(data):
    return datetime.datetime.fromtimestamp(data + 3600 * 9).strftime('%Y-%m-%d %H:%M:%S')


def writeLog(header, data):
    with open("log.json", "a") as fp:
        fp.write("%s\n" % json.dumps(
            {"datetime": strftime(time.time()), "timestamp": math.floor(time.time()), "on": "kidarintwitter.py",
             "header": header, "data": data}, ensure_ascii=False))


def papago(text):
    data = "source=ja&target=ko&text=" + urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", "")
    request.add_header("X-Naver-Client-Secret", "")
    response = urllib.request.urlopen(request, data=data.encode("UTF-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return json.loads(response_body.decode("UTF-8"))["message"]["result"]["translatedText"]
    else:
        return ""


async def getTweet(screen_name, discord):
    archiveData = load_archive()
    tweetData = api.GetUserTimeline(screen_name=screen_name, count=200, exclude_replies=True)

    visit = []

    for i in range(len(archiveData)):
        visit.append(archiveData[i]["id"])

    for data in tweetData:
        if data.retweeted_status != None:
            continue
        if data.id in visit:
            continue

        newData = {"text": data.full_text, "id": data.id, "created_at": data.created_at}
        archiveData.append(newData)
        visit.append(data.id)

        translate = papago(newData["text"])

        if data.media != None:
            await discord.get_channel(targetChannel).send("@%s: %s" % (screen_name, translate))
        else:
            await discord.get_channel(targetChannel).send(
                "@%s: %s https://twitter.com/%s/status/%d" % (screen_name, translate, screen_name, data.id))

    save_archive(archiveData)


class KidarinTwitter(discord.Client):
    async def on_ready(self):
        writeLog("system", "Logged on as %s" % self.user)

        while True:
            try:
                await getTweet("nanawoakari", self)
            except:
                pass
            try:
                await getTweet("nanawo_STAFF", self)
            except:
                pass
            try:
                await getTweet("77ooooooooakrn", self)
            except:
                pass

            time.sleep(30)


if __name__ == "__main__":
    clientTwitter = KidarinTwitter()
    clientTwitter.run(discord_token)