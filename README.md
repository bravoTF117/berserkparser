# BerserkParser
Dirty script written to parse TikTok JSON files.

## Origin

I wrote BerserkParser after publishing two [articles](https://medium.com/@BTF117/tiktok-osint-targeted-user-investigation-9e206f8bb794) on TikTok OSINT and the information that was available if you intercept JSON sessions from the app with a proxy.

When I saw how dirty and nuts this code looked like, it was clear that berserk was the right name for it! By the way: this is my first real Python stuff...that should explain a lot.

## Usage

First, you need a set of JSON files. To collect those, you can use [Fiddler](https://www.telerik.com/fiddler) or the proxy of your choice. There's a new Fiddler version, called ["Fiddler Everywhere"](https://www.telerik.com/fiddler-everywhere) that now runs on Windows, Linux and MacOS. This version is simpler than Fiddlerv4 (it has limited filters for example) but it will do the job.

To configure Fiddler and your device, use this post on [Telerik website](https://www.telerik.com/blogs/how-to-capture-android-traffic-with-fiddler).

Then, to filter the right files (if available), I suggest you head to the **Filters** and:

1. Tick **"Show only if URL contains"** and add _/aweme/v1/_
2. Choose **Show only JSON** in the _Response Type and Size_ zone - if you can't filter by type of file, don't worry: the scripts will deal with the files you exported
3. Get your device/emulator, launch **TikTok**
4. Search for the profile you want to investigate and **before** actually seeing it, _Remove all_ the sessions in Fiddler
5. Hit the target profile and **FOLLOW THE NEXT STEPS:**
6. Scroll down the **videos** you want to include in the report
7. Go to the **Followers** tab and scroll the profiles you want to include in the report
8. Go to the **Following** tab and scroll the profiles you want to include in the report
9. Choose a profile your target is following (_choose one that will not have a lot of followers / avoid verified/blue check mark accounts_) and **view this new profile**
10. Go to the **followers tab** and scroll down until you see your target
11. You are done with the app, **get back to Fiddler**
12. Go to _File->Export Sessions->All Sessions->Raw Files_ and hit _Next_
13. Choose an easy to remember PATH, copy it and click _Export >>_

Then you can run the Python script of your choice. You can either have the output written to the screen (_BerserkParser\_to\_screen.py_) or to a file (_BerserkParser\_to\_file.py_). 
There are many problems in the JSON files that require formatting and flattening. The end result may even be not correctly shown when emojis and other icons are used.

```
python3 .\BerserkParser_to_file.py
```

or

```
python3 .\BerserkParser_to_screen.py
```

Paste the directory path you copied before (or type it) and hit enter. The script will run for a few seconds.


_The scripts have to deal with the fact that it is very complex to determine which files contain relevant information. I chose to use a timestamp present in most of the JSON files (extra_nom). The script find the files with the smallest timestamp and the higher timestamp. Then it will find the file that contains the information about the profile the target is following. Everything collected before is basic/video information. Everything collected after is extended information_


Example of information collected:
```
--- START ---------------------------
** BASIC INFORMATION **

User unique id: 

User nickname: 

User uid: 

Short ID: 

User birthday: 

User city: 

User province: 

User location: 

Author Region: 

User gender: 

User signature: 

User signature language: 

Author Language: 

Larger Avatar URL: 

Video Icon URL: 

Number of videos: 

Instagram ID: 

User twitter id: 

User twitter name: 

User youtube channel id: 

User youtube channel title: 

User apple account: 

User follower count: 

User following count: 

User total favorited: 

..............................................................................................................
** EXTENDED INFORMATION FOUND IN METADATA (target as following): 

Language: 

Unique id modify time: 

Download prompt ts: 

Region: 

Region of residence: 

Bind phone: 

Has email: 

School name: 

Google account: 

Weibo name: 

..............................................................................................................
** LIST OF VIDEOS SEEN WHILE BROWSING:

Video ID: 

Create time: 

Video description: 

Video music/sound: 

Number of comments: 

Number of "diggs":

Number of downloads: 

Number of time video was played: 

Statistics share count: 

Number of times video was shared on WhatsApp: 

URL for video without watermarks (stickers still present): 

URL for full video: 

..............................................................................................................
** LIST OF FOLLOWING SEEN WHILE BROWSING:

Nickname
Unique ID
UID

..............................................................................................................
** LIST OF FOLLOWERS AS SEEN BROWSING: 

Nickname
Unique ID
UID

..............................................................................................................
Done @ 

 BerserkParser by BTF117
--- END --------------------------- 
```
