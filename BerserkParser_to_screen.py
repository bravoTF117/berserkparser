import os
import json
import flatten_json
import datetime

allNames = input('\nEnter the directory you want to parse: ')

# Get the list of all the files in directory at given path
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
            
#Make nested directory file_shortName : flat_json
mainDict = {}
for elem in listOfFiles:
    if elem.endswith('.json'):
        shortName = elem.split("/")[-1].replace(".","")
        with open(elem, encoding='utf-8-sig') as f:
            datastore=flatten_json.flatten(json.load(f))
            mainDict[shortName] = datastore

# init variables/kw
search_list = ['user_unique_id', 'user_nickname', 'user_uid', 'aweme_list_0_author_short_id', 'user_birthday', 'user_city', 'user_province', 'user_location', 'aweme_list_0_author_region', 'user_gender', 'user_signature', 'user_signature_language', 'aweme_list_0_author_language', 'user_avatar_larger_url_list_0', 'aweme_list_0_author_video_icon_url_list', 'user_aweme_count', 'user_ins_id', 'user_twitter_id', 'user_twitter_name', 'user_youtube_channel_id', 'user_youtube_channel_title', 'user_apple_account', 'user_follower_count', 'user_following_count', 'user_total_favorited']

ext_search_list = ['unique_id_modify_time', 'download_prompt_ts', 'region', 'region_of_residence', 'bind_phone', 'has_email', 'school_name', 'google_account', 'weibo_name']

video_search_list = ['aweme_id', 'create_time', 'desc', 'music_play_url_url_list_0', 'statistics_comment_count', 'statistics_digg_count', 'statistics_download_count', 'statistics_play_count', 'statistics_share_count', 'statistics_whatsapp_share_count', 'video_play_addr_url_list_0', 'video_download_addr_url_list_0']

user_unique_id = 'NotFound'
extra_now_bingo=[]
extra_now_dict={}

#find lowest extra_now (timestamp at the beginning of the JSON files)
for k in mainDict.keys():
    if mainDict[k].get('extra_now') is not None:
        extra_now_dict.update({k:mainDict[k].get('extra_now')})
    else:
        continue
extra_now_min = min(extra_now_dict.values())

#find/extract uniqueid for target
for k in mainDict.keys():
    if mainDict[k].get('extra_now') == extra_now_min and mainDict[k].get('user_unique_id') is not None:
        user_unique_id = mainDict[k].get('user_unique_id')

#find extra_now for follower's profile
for k in mainDict.keys():
    if mainDict[k].get('user_unique_id') != user_unique_id and mainDict[k].get('user_unique_id') is not None:
        extra_now_bingo.append(mainDict[k].get('extra_now'))
extra_now_bingo = min(extra_now_bingo)

def Parser():
    print('\n** Profile for TikTok user ' + user_unique_id +':\n')
    #find/extract/print basic info from target profile by parsing JSON file with lowest extra_now
    print('** Basic information:')
    for k in mainDict.keys():
        for item in search_list:
            if mainDict[k].get('extra_now') == extra_now_min:
                if item == 'aweme_list_0_author_short_id':
                    print()
                    print('Short ID:')
                elif item == 'aweme_list_0_author_region':
                    print()
                    print('Author Region:')
                elif item =='aweme_list_0_author_language':
                    print()
                    print('Author Region:')
                elif item == 'user_avatar_larger_url_list_0':
                    print()
                    print('Larger Avatar URL:')
                elif item == 'aweme_list_0_author_video_icon_url_list':
                    print()
                    print('Video Icon URL:')
                elif item == 'user_aweme_count':
                    print()
                    print('Number of videos:')
                elif item == 'user_ins_id':
                    print()
                    print('Instagram ID:')
                else:
                    item_p=(str(item.replace('_',' ')))
                    print('\n' + item_p.capitalize() +': ')
                if mainDict[k].get(item) is not None and mainDict[k].get(item) !=0:
                    print(mainDict[k].get(item))
    print('\n..............................................................................................................')

    #find/extract/print extended information from followers_X
    print('\n** Extended information found in metadata (following):')
    for k in mainDict.keys():
        if mainDict[k].get('extra_now') is not None and mainDict[k].get('extra_now') > extra_now_bingo:
            for x in range(20):
                s=('followers_'+ str(x) +'_')
                if mainDict[k].get(s + 'unique_id') in user_unique_id:
                    for item in ext_search_list:
                        item_list=[]
                        item_list.append(mainDict[k].get(s + str(item)))
                        while("[]" in item_list):
                            item_list.remove("[]")
                        item_p=(str(item.replace('_',' ')))
                        print('\n' + item_p.capitalize() +': ')
                        if item == 'unique_id_modify_time' or item == 'download_prompt_ts' and item_list != [0] :
                            print(*item_list)
                            print(datetime.datetime.fromtimestamp(int(*item_list)).strftime('%d-%m-%Y %H:%M:%S'))
                        else:
                            print(*item_list)
    print('\n..............................................................................................................')

    #find/extract/print videos list
    print('\n** List of videos seen while browsing:\n')
    for k in mainDict.keys():
        if mainDict[k].get('extra_now') is not None and mainDict[k].get('extra_now') < extra_now_bingo:
            for x in range(20):                      
                s=('aweme_list_'+ str(x) +'_')
                if mainDict[k].get(s + 'author_unique_id') is not None and mainDict[k].get(s + 'author_unique_id') in user_unique_id:
                    for item in video_search_list:
                        item_list_vid = (mainDict[k].get(s + item))
                        item_p=(str(item.replace('_',' ')))
                        if item_list_vid == None:
                            continue
                        else:
                            if item == 'aweme_id':
                                print()
                                print('Video ID: ')
                            elif item == 'desc':
                                print()
                                print('Video description: ')
                            elif item =='statistics_digg_count':
                                print()
                                print('Number of "diggs": ')
                            elif item =='music_play_url_url_list_0':
                                print()
                                print('Video music/sound: ')
                            elif item == 'statistics_comment_count':
                                print()
                                print('Number of comments: ')
                            elif item == 'statistics_download_count':
                                print()
                                print('Number of downloads: ')
                            elif item == 'statistics_play_count':
                                print()
                                print('Number of time video was played: ')
                            elif item == 'statistics_whatsapp_share_count':
                                print()
                                print('Number of times video was shared on WhatsApp: ')
                            elif item == 'video_play_addr_url_list_0':
                                print()
                                print('URL for video without watermarks (stickers still present): ')
                            elif item == 'video_download_addr_url_list_0':
                                print()
                                print('URL for full video: ')
                            else:
                                print('\n' + item_p.capitalize() +': ')
                            if item == 'create_time' and item_list_vid != [0] :
                                print(item_list_vid)
                                print(datetime.datetime.fromtimestamp(int(item_list_vid)).strftime('%d-%m-%Y %H:%M:%S'))
                            else:
                                print(item_list_vid)
                            print('.')
                            if item == ('video_download_addr_url_list_0'):
                                print('******************************')
    print('\n..............................................................................................................')

def ListFollow(z):
    #find/extract/print followings or followers
    print('\n** List of '+ z +' (nickname, unique ID and UID) seen while browsing:\n')
    item_list_n=[]
    item_list_uni=[]
    item_list_uid=[]
    for k in mainDict.keys():
        if mainDict[k].get('extra_now') is not None and mainDict[k].get('extra_now') < extra_now_bingo:
            for x in range(20):
                s=(z +'_' + str(x) +'_')
                item_list_n = (mainDict[k].get(s + 'nickname'))
                item_list_uni = (mainDict[k].get(s + 'unique_id'))
                item_list_uid = (mainDict[k].get(s + 'uid'))

                if item_list_n == None:
                    continue
                else:
                    print(item_list_n)
                    print(item_list_uni)
                    print(item_list_uid)
                    print('.')
    print('\n..............................................................................................................')

def main():
    #banner 
    print()
    print('-----------------------------------------------')
    print('| BerserkParser: TikTok JSON parser by BTF117 |')
    print('-----------------------------------------------')
    print('......................................................................................................................................................')
    print('. This dirty script will find all the JSON files in given directory and subdirectories and search them for relevant information about a Tik Tok user .')
    print('. To collect these files, use a proxy and connect a smartphone/emulator to it.                                                                       .')
    print('. Export all the sessions with the string \'aweme/v1\' in the URL as JSON files.                                                                       .')
    print('. (For example, in Fiddler, File->Export->Selected Sessions->Raw Files)                                                                              .')
    print('......................................................................................................................................................\n')
    #invoke parsers
    Parser()
    ListFollow('followings')
    ListFollow('followers')
    #end
    print('Done @ ' + str(datetime.datetime.now()))
    print()

if __name__ == '__main__':
    main()