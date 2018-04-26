#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 00:06:51 2018

@author: shahin

"""

import urllib.request, json, sys, shutil, glob, subprocess, datetime

#input data and time
#TVchannels = ['aztv', ]
vchannel = input("Input TV channel (aztv, ictimai, atvaz, xazer, idman - Find all other tv names from myvideo.az): ")
vdate = input("Input video date (YYYY-MM-DD): ")
vstart_time = input("Input video start time (HH:MM:SS): ")
vend_time = input("Input video end time (HH:MM:SS): ")
full_playlist_url = "http://www.myvideo.az/dvr_getfile.php?chan={0}&mode=fileJSON&date={1}%20{2}".format(vchannel, vdate, vstart_time)

#get playlist file url
with urllib.request.urlopen(full_playlist_url) as url:
    data = json.loads(url.read().decode())

#list contain piece of video downloading url (date + time and token)
video_url_list = [x for x in urllib.request.urlopen(data['file']).read().decode('utf-8').split('\n') if '.ts' in x
        and x.partition("-")[0].split("/")[3] == str(int(vend_time.split(":")[0]) - 4)]

#find the last URL of the video track
vtime = vend_time.replace(vend_time[:2], str( int( vend_time[:2]) - 4 ) ) 
end_of_video = datetime.datetime.strptime(vtime, '%H:%M:%S').time()
last_url = [ x for x in video_url_list   ]

for i in range(1,len(video_url_list)):
    url_index = i
    current_time = ':'.join(video_url_list[i].partition('-')[0].split('/')[3:])
    current_time = datetime.datetime.strptime(current_time, '%H:%M:%S').time()
    if current_time >= end_of_video:
        break

print('Downloading video files...')
ts_filenames = []
for vURL in video_url_list[:url_index]:
    file_name = vURL.partition(".ts")[0].split("/")[-1] + ".ts"
    download_url = "http://bak01-edge03.itdc.ge/{0}/tracks-v1a1/{1}".format(vchannel,vURL)
    urllib.request.urlretrieve(download_url, file_name)
    ts_filenames.append(file_name)
print('Downlad finished.')

print('Merging ts format files...')
# open one ts_file from the list after another and append them to merged.ts
with open('single.ts', 'wb') as merged:
    for ts_file in ts_filenames:
        with open(ts_file, 'rb') as mergefile:
            shutil.copyfileobj(mergefile, merged)
print('Merge process finished.')            
#convert ts file to mp4
print('Converting ts file to MP4 format...')
infile, outfile = 'single.ts', 'single.mp4'
#subprocess.run(['ffmpeg', '-i -loglevel quiet',infile, outfile])
#subprocess.call('ffmpeg %s %s %s' % ('-i',infile,outfile) , stderr=subprocess.DEVNULL, shell=True)
print('Convert finished.')
print('Good Luck!')
