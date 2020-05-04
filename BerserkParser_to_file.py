import os
import json
import flatten_json
import codecs
import datetime

def main():
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

    dirName=input('\nEnter the directory you want to parse: ')
        
    # Get the list of all files in directory at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    # init variables/kw
    search_list = ['user_unique_id', 'user_nickname', 'user_uid', 'aweme_list_0_author_short_id', 'user_birthday', 'user_city', 'user_province', 'user_location', 'aweme_list_0_author_region', 'user_gender', 'user_signature', 'user_signature_language', 'aweme_list_0_author_language', 'user_avatar_larger_url_list_0', 'aweme_list_0_author_video_icon_url_list', 'user_aweme_count', 'user_ins_id', 'user_twitter_id', 'user_twitter_name', 'user_youtube_channel_id', 'user_youtube_channel_title', 'user_apple_account', 'user_follower_count', 'user_following_count', 'user_total_favorited']
    
    ext_search_list=['language', 'unique_id_modify_time', 'download_prompt_ts', 'region', 'region_of_residence', 'bind_phone', 'has_email', 'school_name', 'google_account', 'weibo_name']

    video_search_list = ['aweme_id', 'create_time', 'desc', 'music_play_url_url_list_0', 'statistics_comment_count', 'statistics_digg_count', 'statistics_download_count', 'statistics_play_count', 'statistics_share_count', 'statistics_whatsapp_share_count', 'video_play_addr_url_list_0', 'video_download_addr_url_list_0']

    user_unique_id=[]
    extra_now_bingo=[]
    extra_now_dict={}

    #find lowest/highest extra_now (timestamp at the beginning of the JSON files)
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('extra_now') is not None:
                    extra_now_dict.update({elem:datastore.get('extra_now')})
                else:
                    continue                    
    extra_now_min = min(extra_now_dict.values())
    extra_now_max = max(extra_now_dict.values())
    
    #find/extract/print uniqueid for target
    for item in search_list:
        for elem in listOfFiles:
            if elem.endswith('.json'):
                with open(elem, encoding='utf-8-sig') as f:
                    datastore=flatten_json.flatten(json.load(f))
                    #find the file with the lowest extra_now to open the profile of the target and not the one visited later
                    if datastore.get('extra_now') is not None and datastore.get('extra_now') == extra_now_min and datastore.get('user_unique_id') is not None:
                        user_unique_id.append(datastore.get('user_unique_id'))
    user_unique_id_set=(set(datastore.fromkeys(filter(None, (user_unique_id)))))
    
    #create file for output
    outfilename = (str(*user_unique_id_set) +'_tiktok_profile.txt')
    outfile=codecs.open(outfilename,'w+', encoding='utf8')
    outfile.write('--- START ---------------------------\n** BASIC INFORMATION **\n')
    
    #find extra_now timestamp for profile followed by target
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                if datastore.get('user_unique_id') not in user_unique_id_set and datastore.get('user_unique_id') != None:
                    extra_now_bingo.append(datastore.get('extra_now'))
    extra_now_bingo = min(extra_now_bingo)

    #find/extract/print basic info from target profile by parsing JSON file with lowest extra_now
    for item in search_list:
        item_list=[]
        for elem in listOfFiles:
            if elem.endswith('.json'):
                with open(elem, encoding='utf-8-sig') as f:
                    datastore=flatten_json.flatten(json.load(f))
                    if datastore.get('extra_now') is not None and datastore.get('extra_now') == extra_now_min:
                        item_list.append(datastore.get(item))
        item_p=(str(item.replace('_',' ')))
        if item == 'aweme_list_0_author_short_id':
            outfile.write('\nShort ID: \n')
        elif item == 'aweme_list_0_author_region':
            outfile.write('\nAuthor Region: \n')
        elif item =='aweme_list_0_author_language':
            outfile.write('\nAuthor Language: \n')
        elif item == 'user_avatar_larger_url_list_0':
            outfile.write('\nLarger Avatar URL: \n')
        elif item == 'aweme_list_0_author_video_icon_url_list':
            outfile.write('\nVideo Icon URL: \n')
        elif item == 'user_aweme_count':
            outfile.write('\nNumber of videos: \n')
        elif item == 'user_ins_id':
            outfile.write('\nInstagram ID: \n')
        else:
            outfile.write('\n' + item_p.capitalize() +': \n')
        item_list=filter(None, (item_list))
        outfile.write(str(*item_list))
        outfile.write('\n')

    outfile.write('\n..............................................................................................................')

    #find/extract/print extended information from followings_X_
    outfile.write('\n** EXTENDED INFORMATION FOUND IN METADATA (target as following): \n')
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                # user_unique_id.append(datastore.get('user_unique_id'))
                # user_unique_id_set=(set(datastore.fromkeys(filter(None, (user_unique_id)))))
                ts3 = (datastore.get('extra_now'))
                if ts3 is not None and ts3 > extra_now_bingo:
                    for x in range(20):
                        s=('followers_'+ str(x) +'_')
                        if datastore.get(s + 'unique_id') in user_unique_id_set:
                            for item in ext_search_list:
                                item_list=[]
                                item_list.append(datastore.get(s + str(item)))
                                while("[]" in item_list):
                                    item_list.remove("[]")
                                item_p=(str(item.replace('_',' ')))
                                outfile.write('\n' + item_p.capitalize() +': \n')
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
    outfile.write('\n** LIST OF VIDEOS SEEN WHILE BROWSING:\n')
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                ts4 = datastore.get('extra_now')
                if ts4 is not None and ts4 < extra_now_bingo:
                    for x in range(20):
                        s=('aweme_list_'+ str(x) +'_')
                        authvid = datastore.get(s + 'author_unique_id')
                        if authvid in user_unique_id:
                            for item in video_search_list:
                                item_list_vid=[]
                                item_list_vid = (datastore.get(s + item))
                                item_p=(str(item.replace('_',' ')))
                                if item_list_vid == None:
                                    continue
                                else:
                                    if item == 'aweme_id':
                                        outfile.write('\n')
                                        outfile.write('Video ID: ')
                                    elif item == 'desc':
                                        outfile.write('\n')
                                        outfile.write('Video description: ')
                                    elif item =='statistics_digg_count':
                                        outfile.write('\n')
                                        outfile.write('Number of "diggs": ')
                                    elif item =='music_play_url_url_list_0':
                                        outfile.write('\n')
                                        outfile.write('Video music/sound: ')
                                    elif item == 'statistics_comment_count':
                                        outfile.write('\n')
                                        outfile.write('Number of comments: ')
                                    elif item == 'statistics_download_count':
                                        outfile.write('\n')
                                        outfile.write('Number of downloads: ')
                                    elif item == 'statistics_play_count':
                                        outfile.write('\n')
                                        outfile.write('Number of time video was played: ')
                                    elif item == 'statistics_whatsapp_share_count':
                                        outfile.write('\n')
                                        outfile.write('Number of times video was shared on WhatsApp: ')
                                    elif item == 'video_play_addr_url_list_0':
                                        outfile.write('\n')
                                        outfile.write('URL for video without watermarks (stickers still present): ')
                                    elif item == 'video_download_addr_url_list_0':
                                        outfile.write('\n')
                                        outfile.write('URL for full video: ')
                                    else:
                                        outfile.write('\n' + item_p.capitalize() +': ')
                                    outfile.write('\n')
                                    if item == 'create_time' and item_list_vid != [0] :
                                        outfile.write(str(item_list_vid))
                                        outfile.write('\n')
                                        outfile.write(datetime.datetime.fromtimestamp(int(item_list_vid)).strftime('%d-%m-%Y %H:%M:%S'))
                                    else:
                                        outfile.write(str(item_list_vid))
                                    outfile.write('\n')
                                    outfile.write('\n')
                                    if item == ('video_download_addr_url_list_0'):
                                        outfile.write('\n')
                                        outfile.write('******************************')

    outfile.write('\n..............................................................................................................')

    #find/extract/outfile.write following
    outfile.write('\n** LIST OF FOLLOWING SEEN WHILE BROWSING\n\n')
    for elem in listOfFiles:
        item_list_n=[]
        item_list_uni=[]
        item_list_uid=[]
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                ts4 = datastore.get('extra_now')
                if ts4 is not None and ts4 < extra_now_bingo:
                    for x in range(20):
                        s=('followings_'+ str(x) +'_')
                        item_list_n = (datastore.get(s + 'nickname'))
                        item_list_uni = (datastore.get(s + 'unique_id'))
                        item_list_uid = (datastore.get(s + 'uid'))
                        if item_list_n == None:
                            continue
                        else:
                            outfile.write(item_list_n)
                            outfile.write('\n')
                            outfile.write(item_list_uni)
                            outfile.write('\n')
                            outfile.write(item_list_uid)
                            outfile.write('\n')
                            outfile.write('\n')

    outfile.write('\n..............................................................................................................')

    #find/extract/print followers
    outfile.write('\n** LIST OF FOLLOWERS AS SEEN BROWSING: \n\n')
    for elem in listOfFiles:
        item_list_n=[]
        item_list_uni=[]
        item_list_uid=[]
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:
                datastore=flatten_json.flatten(json.load(f))
                ts5 = datastore.get('extra_now')
                if ts5 is not None and ts5 < extra_now_bingo:
                    for x in range(20):
                        s=('followers_'+ str(x) +'_')
                        item_list_n = (datastore.get(s + 'nickname'))
                        item_list_uni = (datastore.get(s + 'unique_id'))
                        item_list_uid = (datastore.get(s + 'uid'))
                        if item_list_n == None:
                            continue
                        else:
                            outfile.write(item_list_n)
                            outfile.write('\n')
                            outfile.write(item_list_uni)
                            outfile.write('\n')
                            outfile.write(item_list_uid)
                            outfile.write('\n')
                            outfile.write('\n')

    outfile.write('\n..............................................................................................................\n')
    outfile.write('Done @ ' + str(datetime.datetime.now()))
    outfile.write('\n')
    outfile.write('\n BerserkParser by BTF117\n')
    outfile.write('--- END --------------------------- ')

    outfile.close
    print('\n','\n')
    print('Done... you can go check '+outfilename +'\n')

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles
                
if __name__ == '__main__':
    main()