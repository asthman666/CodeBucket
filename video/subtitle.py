# -*- coding: utf-8 -*-
import argparse
import os 
import subprocess
import re

def main(videopath):
    sub_paths = []
    with os.scandir(videopath) as entries:
        for entry in entries:
            if os.path.isdir(entry):
                sub_paths.append(entry)
    
    videos = []
    for entry in sub_paths:
        with os.scandir(entry) as entries:
            for video in entries:
                if os.path.isfile(video):
                    videos.append(video)
    
    process(videos)
                
def process(videos):
    for video in videos:
        cmd = ['mkvmerge', '-i', video]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        o, e = proc.communicate()
        #print(proc.returncode)
        #print('Output: ' + o.decode('utf8'))
        if proc.returncode == 0 and re.search(r'Track ID 6: subtitles', o.decode('utf8')):
            #print(video)
            folder_name = video.path.split('/')[-2]
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)   

            cmd = ['mkvextract', 'tracks', video, '6:{}/{}.srt'.format(folder_name, video.name)]
            #print(cmd)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()                

            process_subtitle('{}/{}.srt'.format(folder_name, video.name), video)
            #print('Output: ' + o.decode('utf8'))
            #print('Error: '  + e.decode('utf8'))
            #print('code: ' + str(proc.returncode))
        #break

def process_subtitle(subtitle_file, video):
    print('process subtitle: {}'.format(subtitle_file))
    new_file_lines = [video.name, os.linesep, os.linesep]
    with open(subtitle_file, mode='r', encoding='utf8') as fp:
        for line in fp:
            if re.search(r'^Dialogue', line):
                new_line = re.sub('\{\\\\r\}', '', line)
                new_line = re.sub('Dialogue.+\}', '', new_line)
                new_file_lines.append(new_line)
    
    with open('{}.format.txt'.format(subtitle_file), 'w') as wf:
        for l in new_file_lines:
            wf.write(l) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract video subtitle')
    parser.add_argument('--path', dest='videopath',
                        help='video file path')

    args = parser.parse_args()
    #print(args.videopath)
    main(args.videopath)