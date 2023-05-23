import os
from os.path import exists


def get_playlist():
    playlist = "[Your Link Here!]"
    getplist = "youtube-dl --get-filename '"+ playlist +"' >> temp_plist"
    file_exist = exists("temp_plist")
    if file_exist == True:
        os.remove("temp_plist")
        fp = open('temp_plist', 'w')
        fp.close()
    else:
        fp = open('temp_plist', 'w')
        fp.close()


    os.system(getplist)
    print("Cleaning Data")
    with open('temp_plist', 'r') as file:
        content = file.read()
        content = content.replace(".mp4", "")
        content = content.replace(".webm", "")
    with open(r'temp_plist', 'w') as file:
        file.write(content)


def get_local_list():
    global path
    path = "/path/to/playlist/"
    getllist = "ls "+ path +"*.mp3 >> temp_llist"
    file_exist = exists("temp_llist")
    if file_exist == True:
        os.remove("temp_llist")
        fp = open('temp_llist', 'w')
        fp.close()
    else:
        fp = open('temp_llist', 'w')
        fp.close()
    os.system(getllist)
    with open('temp_llist', 'r') as file:
        content = file.read()
        content = content.replace(path, "")
        content = content.replace(".mp3", "")
    with open(r'temp_llist', 'w') as file:
        file.write(content)


def conv_file_to_list():
    global plist
    global llist
    with open('temp_plist') as pfile:
         plist = pfile.readlines()
         pfile.close()
    os.remove("temp_plist")
    with open('temp_llist') as lfile:
         llist = lfile.readlines()
         lfile.close()
    os.remove("temp_llist")
    plist.sort(reverse=False)
    llist.sort(reverse=False)


def comp_lists():
    global newllist
    global newplist
    newlist  = list(set(plist) & set(llist))
    newplist = list(set(plist) - set(newlist))
    newllist = list(set(llist) - set(newlist))



def get_missing_file():
    for i in newplist:
        os.system("youtube-dl -x --audio-format mp3 ytsearch:'"+ i +"' -o'"+ path +"%(title)s-%(id)s.%(ext)s'")


def main():
    print("Getting Youtube playlist")
    get_playlist();
    print("Getting local list")
    get_local_list();
    conv_file_to_list();
    if plist != llist:
        print("Discrepancy detected, updating..")
        comp_lists();
        get_missing_file();
        print("Update finished.")
        if len(newllist) != 0:
            print("Titles not existend in the Youtube playlist:"+ str(newllist))
    else:
        print("Everything is updated.")

if __name__ == "__main__":
    main()
