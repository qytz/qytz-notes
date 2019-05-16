#!/usr/bin/env python3

import sys
import re
import config

def parse_lrc(lrc_text):
    lrc_obj = {}
    lrc_obj['offset'] = 0
    lrc_obj['ti'] = ''
    lrc_obj['ar'] = ''
    lrc_obj['al'] = ''
    lrc_obj['content'] = []

    lbl_reg = re.compile('\[(offset|ti|ar|al):(.+?)\]')
    time_reg = re.compile('\[(\d{1,3}):(\d{2})([.:]\d{1,3})?\]')
    for line in lrc_text.splitlines():
        match = lbl_reg.match(line)
        if match != None:
            lbl_name, lbl_content = match.groups()
            if lbl_name == 'ti':  # title
                lrc_obj['ti'] = lbl_content
            elif lbl_name == 'ar':  # artist
                lrc_obj['ar'] = lbl_content
            elif lbl_name == 'al':  # album
                lrc_obj['al'] = lbl_content
            elif lbl_name == 'offset':
                lrc_obj['offset'] = int(lbl_content)
            continue
        match = time_reg.match(line)
        time_tags = []
        while match:
            match_offset = match.end()
            m, s, ms = match.groups()
            if ms == None:
                ms = 0
            else:
                # 毫秒可以为小数？
                ms = float(ms[1:])
            content_time = int(m) * 60 + int(s)
            content_time = content_time * 1000 + ms
            time_tags.append(content_time)
            match = time_reg.match(line, match_offset)

        if len(time_tags) > 0:
            content = line[match_offset:].strip()
            for tag in time_tags:
                lrc_obj['content'].append((tag, content))
        lrc_obj['content'].sort()
    return lrc_obj

if __name__ == '__main__':
    if (len(sys.argv)<2):
        print('{0} lrc_file\n'.format(sys.argv[0]))
        sys.exit(-1)

    with open(sys.argv[1], encoding=config.configs['lrc-encoding']) as f:
        lrc_obj = parse_lrc(f.read())
        print(lrc_obj['offset'])
        print(lrc_obj['ti'])
        print(lrc_obj['ar'])
        print(lrc_obj['al'])
        for c in lrc_obj['content']:
            print(c)
