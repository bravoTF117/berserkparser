import os
import json
import flatten_json
import datetime
import codecs

#allNames = input('\nEnter the directory you want to parse: ')
dirName = 'c:/users/jb/desktop/1'

# Get the list of all the files in directory at given path
listOfFiles = list()

for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
            
#Make nested directory file_sohrtName : flat_json
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

#create file for output
outfilename = (user_unique_id +'_tiktok_profile.txt')
outfile=codecs.open(outfilename,'w+', encoding='utf8')


def Parser():
    #find/extract/print basic info from target profile by parsing JSON file with lowest extra_now
    outfile.write('--- START ---------------------------\n** BASIC INFORMATION **\n')
    for k in mainDict.keys():
        for item in search_list:
            if mainDict[k].get('extra_now') == extra_now_min:
                if item == 'aweme_list_0_author_short_id':
                    outfile.write('\nShort ID:\n')
                elif item == 'aweme_list_0_author_region':
                    outfile.write('\nAuthor Region:\n')
                elif item =='aweme_list_0_author_language':
                    outfile.write('\nAuthor Region:\n')
                elif item == 'user_avatar_larger_url_list_0':
                    outfile.write('\nLarger Avatar URL:\n')
                elif item == 'aweme_list_0_author_video_icon_url_list':
                    outfile.write('\nVideo Icon URL:\n')
                elif item == 'user_aweme_count':
                    outfile.write('\nNumber of videos:\n')
                elif item == 'user_ins_id':
                    outfile.write('\nInstagram ID:\n')
                else:
                    item_p=(str(item.replace('_',' ')))
                    outfile.write('\n' + item_p.capitalize() +': ')
                    outfile.write('\n')
                if mainDict[k].get(item) is not None and mainDict[k].get(item) !=0:
                    outfile.write(str(mainDict[k].get(item)))
                    outfile.write('\n')
                else:
                    outfile.write('\n')
    outfile.write('\n..............................................................................................................')

    #find/extract/print extended information from followers_X
    outfile.write('\n** Extended information found in metadata (following):')
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
                        outfile.write('\n')
                        outfile.write('\n' + item_p.capitalize() +': ')
                        outfile.write('\n')
                        if item == 'unique_id_modify_time' or item == 'download_prompt_ts' and item_list != [0] :
                            outfile.write(str(*item_list))
                            outfile.write('\n')
                            outfile.write(datetime.datetime.fromtimestamp(int(*item_list)).strftime('%d-%m-%Y %H:%M:%S'))
                            outfile.write('\n')
                        else:
                            outfile.write(str(*item_list))
                            outfile.write('\n')
    outfile.write('\n..............................................................................................................')

    #find/extract/print videos list
    outfile.write('\n** List of videos seen while browsing:\n')
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
                                outfile.write('\nVideo ID: ')
                            elif item == 'desc':
                                outfile.write('\nVideo description: ')
                            elif item =='statistics_digg_count':
                                outfile.write('\nNumber of "diggs": ')
                            elif item =='music_play_url_url_list_0':
                                outfile.write('\nVideo music/sound: ')
                            elif item == 'statistics_comment_count':
                                outfile.write('\nNumber of comments: ')
                            elif item == 'statistics_download_count':
                                outfile.write('\nNumber of downloads: ')
                            elif item == 'statistics_play_count':
                                outfile.write('\nNumber of time video was played: ')
                            elif item == 'statistics_whatsapp_share_count':
                                outfile.write('\nNumber of times video was shared on WhatsApp: ')
                            elif item == 'video_play_addr_url_list_0':
                                outfile.write('\nURL for video without watermarks (stickers still present): ')
                            elif item == 'video_download_addr_url_list_0':
                                outfile.write('\nURL for full video: ')
                            else:
                                outfile.write('\n' + item_p.capitalize() +': ')
                            if item == 'create_time' and item_list_vid != [0] :
                                outfile.write('\n')
                                outfile.write(str(item_list_vid))
                                outfile.write('\n')
                                outfile.write(datetime.datetime.fromtimestamp(int(item_list_vid)).strftime('%d-%m-%Y %H:%M:%S'))
                            else:
                                outfile.write('\n')
                                outfile.write(str(item_list_vid))
                                outfile.write('\n')
                            outfile.write('.')
                            if item == ('video_download_addr_url_list_0'):
                                outfile.write('\n******************************')
    outfile.write('\n..............................................................................................................')


def ListFollow(z):
    #find/extract/print followings or followers depending on argument
    outfile.write('\n** List of '+ z +' (nickname, unique ID and UID) seen while browsing:\n')
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
                    outfile.write('\n')
                    outfile.write(item_list_n)
                    outfile.write('\n')
                    outfile.write(item_list_uni)
                    outfile.write('\n')
                    outfile.write(item_list_uid)
                    outfile.write('\n')
                    outfile.write('.')
                    outfile.write('\n')
    outfile.write('\n..............................................................................................................')


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
    outfile.write('Done @ ' + str(datetime.datetime.now()))
    outfile.write('\n')
    outfile.write('\n BerserkParser by BTF117\n')
    outfile.write('--- END --------------------------- ')
    #close file and finish it
    outfile.close
    print('\n','\n')
    print('Done... you can go check '+outfilename +'\n')


if __name__ == '__main__':
    main()