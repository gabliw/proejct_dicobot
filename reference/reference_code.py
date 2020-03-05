"""
original created and shared by Kano
reference code for nanawoakari discord Bot
"""

import discord
import datetime
import time
import json
import math
import urllib.request
from twitter import Api

targetChannel = None

api = Api("", "", "", "", tweet_mode="extended")
nanawoakari = api.GetUser(screen_name='nanawoakari').id_str
nanawo_staff = api.GetUser(screen_name='nanawo_STAFF').id_str


def loadArchive():
    with open("archive.json", encoding="utf8") as fp:
        data = json.load(fp)
    return data


def saveArchive(data):
    with open("archive.json", "w", encoding="utf8") as fp:
        fp.write(json.dumps(data, ensure_ascii=False, indent=4))


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
    archiveData = loadArchive()
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

    saveArchive(archiveData)


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


# if __name__ == "__main__":
#     clientTwitter = KidarinTwitter()
#     clientTwitter.run(None)
