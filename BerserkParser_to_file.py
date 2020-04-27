import os
import json
import flatten_json
import codecs
import datetime

def main():
    print('-----------------------------------------------')
    print('| BerserkParser: TikTok JSON parser by BTF117 |')
    print('-----------------------------------------------')
    print('......................................................................................................................................................')
    print('. This dirty script will find all the JSON files in given directory and subdirectories and search them for relevant information about a Tik Tok user .')
    print('. To collect these files, use a proxy and connect a smartphone/emulator to it.                                                                       .')
    print('. Export all the sessions with the string \'aweme/v1\' in the URL as JSON files.                                                                       .')
    print('. (For example, in Fiddler, File->Export->Selected Sessions->Raw Files)                                                                              .')
    print('......................................................................................................................................................')

    dirName=input('\nEnter the directory you want to parse (format: c:/directory1/directory2): ')
        
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    #init all the variables for the flatten JSON
    user_birthday, user_twitter_id , user_location, user_youtube_channel_id, user_unique_id =([] for i in range(5))
    user_apple_account, user_city, user_province, user_signature, aweme_list_0_author_short_id, aweme_list_0_author_region, aweme_list_0_author_language=([] for i in range(7))
    aweme_list_0_author_video_icon_url_list, user_nickname,user_follower_count, user_uid, user_gender, user_following_count =([] for i in range(6))
    user_total_favorited, user_avatar_larger_url_list_0, user_youtube_channel_title,user_aweme_count,user_ins_id, user_signature_language =([] for i in range(6))
    user_twitter_id, user_twitter_name, followersALL, followingsALL = ([] for i in range(4))

    # start to work on the files    
    for elem in listOfFiles:
        if elem.endswith('.json'):
            with open(elem, encoding='utf-8-sig') as f:

                #flatten the JSON files

                datastore=flatten_json.flatten(json.load(f))
                for code in datastore:

                    #use dict.get to find the relevant keys

                    user_signature_language.append(datastore.get('user_signature_language'))
                    user_nickname.append(datastore.get('user_nickname'))
                    user_follower_count.append(datastore.get('user_follower_count'))
                    user_signature.append(datastore.get('user_signature'))
                    user_uid.append(datastore.get('user_uid'))
                    user_gender.append(datastore.get('user_gender'))
                    user_total_favorited.append(datastore.get('user_total_favorited'))
                    user_avatar_larger_url_list_0.append(datastore.get('user_avatar_larger_url_list_0'))
                    user_youtube_channel_title.append(datastore.get('user_youtube_channel_title'))
                    user_aweme_count.append(datastore.get('user_aweme_count'))
                    user_twitter_id.append(datastore.get('user_twitter_id'))
                    user_ins_id.append(datastore.get('user_ins_id'))
                    aweme_list_0_author_region.append(datastore.get('aweme_list_0_author_region'))
                    user_birthday.append(datastore.get('user_birthday'))
                    user_youtube_channel_id.append(datastore.get('user_youtube_channel_id'))
                    user_following_count.append(datastore.get('user_following_count'))
                    user_unique_id.append(datastore.get('user_unique_id'))
                    user_twitter_name.append(datastore.get('user_twitter_name'))
                    followersALL.append(datastore.get('followers_0_nickname'))
                    followersALL.append(datastore.get('followers_1_nickname'))
                    followersALL.append(datastore.get('followers_2_nickname'))
                    followersALL.append(datastore.get('followers_3_nickname'))
                    followersALL.append(datastore.get('followers_4_nickname'))
                    followersALL.append(datastore.get('followers_5_nickname'))
                    followersALL.append(datastore.get('followers_6_nickname'))
                    followersALL.append(datastore.get('followers_7_nickname'))
                    followersALL.append(datastore.get('followers_8_nickname'))
                    followersALL.append(datastore.get('followers_9_nickname'))
                    followersALL.append(datastore.get('followers_10_nickname'))
                    followersALL.append(datastore.get('followers_11_nickname'))
                    followersALL.append(datastore.get('followers_12_nickname'))
                    followersALL.append(datastore.get('followers_13_nickname'))
                    followersALL.append(datastore.get('followers_14_nickname'))
                    followersALL.append(datastore.get('followers_15_nickname'))
                    followersALL.append(datastore.get('followers_16_nickname'))
                    followersALL.append(datastore.get('followers_17_nickname'))
                    followersALL.append(datastore.get('followers_18_nickname'))
                    followersALL.append(datastore.get('followers_19_nickname'))
                    followingsALL.append(datastore.get('followings_0_nickname'))
                    followingsALL.append(datastore.get('followings_1_nickname'))
                    followingsALL.append(datastore.get('followings_2_nickname'))
                    followingsALL.append(datastore.get('followings_3_nickname'))
                    followingsALL.append(datastore.get('followings_4_nickname'))
                    followingsALL.append(datastore.get('followings_5_nickname'))
                    followingsALL.append(datastore.get('followings_6_nickname'))
                    followingsALL.append(datastore.get('followings_7_nickname'))
                    followingsALL.append(datastore.get('followings_8_nickname'))
                    followingsALL.append(datastore.get('followings_9_nickname'))
                    followingsALL.append(datastore.get('followings_10_nickname'))
                    followingsALL.append(datastore.get('followings_11_nickname'))
                    followingsALL.append(datastore.get('followings_12_nickname'))
                    followingsALL.append(datastore.get('followings_13_nickname'))
                    followingsALL.append(datastore.get('followings_14_nickname'))
                    followingsALL.append(datastore.get('followings_15_nickname'))
                    followingsALL.append(datastore.get('followings_16_nickname'))
                    followingsALL.append(datastore.get('followings_17_nickname'))
                    followingsALL.append(datastore.get('followings_18_nickname'))
                    followingsALL.append(datastore.get('followings_19_nickname'))

    #print the keys to file

    user_unique_id_set=set(user_unique_id)
    user_unique_id_set=(list(filter(None,user_unique_id_set)))
    outfilename = (str(*user_unique_id_set) +'_tiktok_profile.txt')
    outfile=codecs.open(outfilename,'w+', encoding='utf8')
    outfile.write('--- START ---------------------------\n** BASIC INFORMATION **\n')
    outfile.write('Unique ID: \n')
    outfile.write(str(*user_unique_id_set) + ', ' .join('\n'))

    user_nickname_set=set(user_nickname)
    user_nickname_set=(list(filter(None,user_nickname_set)))
    outfile.write('Nickname: \n')
    outfile.write(str(*user_nickname_set) + ', ' .join('\n'))


    outfile.write('UID: \n')
    user_uid_set=set(user_uid)
    user_uid_set=(list(filter(None,user_uid_set)))
    outfile.write(str(*user_uid_set) + ', ' .join('\n'))


    outfile.write('Signature: \n')
    user_signature_set=set(user_signature)
    user_signature_set=(list(filter(None,user_signature_set)))
    outfile.write(str(*user_signature_set) + ', ' .join('\n'))


    outfile.write('Signature language: \n')
    user_signature_language_set=set(user_signature_language)
    user_signature_language_set=(list(filter(None,user_signature_language_set)))
    outfile.write(str(*user_signature_language_set) + ', ' .join('\n'))


    outfile.write('Birthday: \n')
    user_birthday_set=set(user_birthday)
    user_birthday_set=(list(filter(None,user_birthday_set)))
    outfile.write(str(*user_birthday_set) + ', ' .join('\n'))


    outfile.write('Region: \n')
    aweme_list_0_author_region_set=set(aweme_list_0_author_region)
    aweme_list_0_author_region_set=(list(filter(None,aweme_list_0_author_region_set)))
    outfile.write(str(*aweme_list_0_author_region_set) + ', ' .join('\n'))


    outfile.write('Gender: \n')
    user_gender_set=set(user_gender)
    user_gender_set=(list(filter(None,user_gender_set)))
    outfile.write(str(*user_gender_set) + ', ' .join('\n'))


    outfile.write('Large Avatar Picture URL: \n')
    user_avatar_larger_url_list_0_set=set(user_avatar_larger_url_list_0)
    user_avatar_larger_url_list_0_set=(list(filter(None,user_avatar_larger_url_list_0_set)))
    outfile.write(str(*user_avatar_larger_url_list_0_set) + ', ' .join('\n'))


    outfile.write('____________________________________________________________________\n** EXTENDED INFORMATION **\n' )
    outfile.write('YouTube Channel: \n')
    user_youtube_channel_title_set=set(user_youtube_channel_title)
    user_youtube_channel_title_set=(list(filter(None,user_youtube_channel_title_set)))
    outfile.write(str(*user_youtube_channel_title_set)  + ', ' .join('\n'))


    outfile.write('YouTube Channel ID: \n')
    user_youtube_channel_id_set=set(user_youtube_channel_id)
    user_youtube_channel_id_set=(list(filter(None,user_youtube_channel_id_set)))
    outfile.write(str(*user_youtube_channel_id_set) + ', ' .join('\n'))


    outfile.write('Instagram ID: \n')
    user_ins_id_set=set(user_ins_id)
    user_ins_id_set=(list(filter(None,user_ins_id_set)))
    outfile.write(str(*user_ins_id_set) + ', ' .join('\n'))


    outfile.write('Twitter Name: \n')
    user_twitter_name_set=set(user_twitter_name)
    user_twitter_name_set=(list(filter(None,user_twitter_name_set)))
    outfile.write(str(*user_twitter_name_set) + ', ' .join('\n'))


    outfile.write('Twitter ID: \n')
    user_twitter_id_set=set(user_twitter_id)
    user_twitter_id_set=(list(filter(None,user_twitter_id_set)))
    outfile.write(str(*user_twitter_id_set) + ', ' .join('\n'))


    outfile.write('____________________________________________________________________\n** VIDEOS **\n' )
    outfile.write('Number of videos: \n')
    user_aweme_count_set=set(user_aweme_count)
    user_aweme_count_set=(list(filter(None,user_aweme_count_set)))
    outfile.write(str(*user_aweme_count_set) + ', ' .join('\n'))

    outfile.write('____________________________________________________________________\n** INTERACTIONS **\n')

    outfile.write('Number of followers: \n')
    user_follower_count_set=set(user_follower_count)
    user_follower_count_set=(list(filter(None,user_follower_count_set)))
    outfile.write(str(*user_follower_count_set) + ', ' .join('\n'))

    
    outfile.write('User following: \n')
    user_following_count_set=set(user_following_count)
    user_following_count_set=(list(filter(None,user_following_count_set)))
    outfile.write(str(*user_following_count_set) + ', ' .join('\n'))


    outfile.write('Favorited: \n')
    user_total_favorited_set=set(user_total_favorited)
    user_total_favorited_set=(list(filter(None,user_total_favorited_set)))
    outfile.write(str(*user_total_favorited_set) + ', ' .join('\n'))


    outfile.write('____________________________________________________________________\n** NICKNAME OF FOLLOWERS SEEN WHILE BROWSING **\n')
    followersALL_set=set(followersALL)
    followersALL_set=(list(filter(None,followersALL_set)))
    for item in followersALL_set:
        outfile.writelines(item)
        outfile.write('\n')

    outfile.write('\n! some characters may be f... up !\n')
    outfile.write('____________________________________________________________________\n** NICKNAME OF FOLLOWINGS SEEN WHILE BROWSING **\n')
    followingsALL_set=set(followingsALL)
    followingsALL_set=(list(filter(None,followingsALL_set)))
    for item in followingsALL_set:
        outfile.write(item)
        outfile.write('\n')

    outfile.write('\n! some characters may be f... up !\n')
    outfile.write('--- END --------------------------- ')
    outfile.write(str(datetime.datetime.now()))
    outfile.write('\n BerserkParser by BTF117')

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