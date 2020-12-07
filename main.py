import wget
import requests
import json
from bs4 import BeautifulSoup

i = 1

def get_user_uid(link):
    print("Getting user info...")
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script")
    res = script_tag.text.replace("window.data = ", '')
    final = res.replace("window.isEmpty = 0;", '')
    final = json.loads(final.replace(";", ''))
    return final['userinfo']['uid']

def get_user_info(uid):
    url = 'https://likee.video/official_website/UserApi/getUserPostInfo'
    api = json.loads(requests.post(url, data={"uid": uid}).text)
    video_count = api['data']['postInfoMap'][uid]['videoNums']
    print(f"User UID: {uid} | User Video Count: {video_count}")
    return uid, video_count

def parse_links(uid, count, lastPostId="None"):
    if lastPostId == "None":
        form = {'uid': uid, 'count': count, 'lastPostId':''}
    else:
        form = {'uid': uid, 'count': count, 'lastPostId': lastPostId}
    api = json.loads(requests.post('https://likee.video/official_website/VideoApi/getUserVideo', data=form).text)

    if int(count) > 100:
        count = int(count) - 100
        parse_links(uid, count, find_videos(api))
    else:
        return find_videos(api)

def find_videos(api_info):
    global i
    for data in api_info['data']['videoList']:
        if data['videoUrl'] == '':
            data['videoUrl'] = "No video Found!"
        print(f"[{i}] - {data['videoUrl']} | {data['postId']}")
        download(data['videoUrl'], data['postId'])
        i += 1
        if i % 100 == 0:
            return data['postId']

def download(url, filename):
    print("Starting Downloading...")
    try:
        wget.download(url, f'{filename}.mp4')
        print("Successfully Downloaded.")
    except:
        print("Eror on download")

def main():
    user_info = get_user_info(get_user_uid(input("Enter Likee page url: ")))
    print("Got user info!")
    parse_links(user_info[0], user_info[1])

if __name__ == '__main__':
    main()

