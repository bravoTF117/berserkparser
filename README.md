# BerserkParser
Dirty script written to parse TikTok JSON files.

## Origin

I wrote BerserkParser after publishing two [articles](https://medium.com/@BTF117/tiktok-osint-targeted-user-investigation-9e206f8bb794) on TikTok OSINT and the information that was available if you intercept JSON sessions with a proxy.

When I saw how dirty and nuts this code looked like, it was clear that berserk was the right name for it! By the way: this is my first real Python stuff...that should explain a lot.

## Usage

First, you need a set of JSON files. To collect those, you can use [Fiddler](https://www.telerik.com/fiddler) or the proxy of your choice.

To configure Fiddler and your device, use this post on [Telerik website](https://www.telerik.com/blogs/how-to-capture-android-traffic-with-fiddler).

Then, to filter the right files, I suggest you head to the **Filters** and:

1. Tick **"Show only if URL contains"** and add '''/aweme/v1/'''
2. Choose **Show only JSON** in the _Response Type and Size_ zone
3. Go to _File->Export Sessions->All Sessions->Raw Files_ and hit _Next_
4. Choose an easy to remember PATH, copy it and click _Export >>_

Then you can run the Python script of your choice. You can either have the output written to the screen (_BerserkParser\_to\_screen.py_) or to a file (_BerserkParser\_to\_file.py_). 
There are many problems in the JSON files that require formatting and flattening. The end result may even be not correctly shown when emojis and other icons are used.

Paste the directory you copied before (or type it) and hit enter. The script will run for a few seconds.




