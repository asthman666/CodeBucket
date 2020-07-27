# -*- coding: utf-8 -*-
import os
import re
import argparse

def process_folder(video_subtitle_path):
    with os.scandir(video_subtitle_path) as entries:
        for entry in entries:
            if re.search(r'\.txt$', entry.name):
                print('print {}'.format(entry.name))
                os.startfile(entry, "print")    
                #break

def process_file(video_subtitle_file):
    print('print {}'.format(video_subtitle_file))
    os.startfile(video_subtitle_file, "print")   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='send subtitle file to printer')
    parser.add_argument('--path', dest='video_subtitle_path',
                        help='video subtitle file path')
    parser.add_argument('--file', dest='video_subtitle_file',
                        help='video subtitle file file')                        

    args = parser.parse_args()
    print(args)
    if args.video_subtitle_path:
        process_folder(args.video_subtitle_path)
    if args.video_subtitle_file:
        process_file(args.video_subtitle_file)