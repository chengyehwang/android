#!/usr/bin/python3

import os
import re

with open('repo_list','r') as file_handle:
    repo = file_handle.read()
proj_table = {}
for proj_line in repo.split('\n'):
    match = re.match('(\S+)\s*:\s*(\S+)', proj_line)
    if match:
        proj_dir = match[1]
        proj_name = match[2]
        proj_table[proj_dir] = proj_name
proj_table


def proj_search (dir):
    dir = os.path.normpath(dir)
    while len(dir)>0:
        if dir in proj_table:
            return proj_table[dir]
        dir = os.path.dirname(dir)
    return ''

selection = []
def search(path, name):
    name = os.path.normpath(name)
    if name in proj_table:
        selection.append(proj_table[name])
        return
    for dir in os.listdir(path):
        search(path + '/' + dir, name + '/' + dir)

search('android-10.0.0_r33_full/out/soong/.intermediates','.')

with open('im_sync.sh','w') as file_handle:
    file_handle.write('#!/bin/bash\n')
    file_handle.write('PRO="$@ "\n')
    file_handle.write('PRO+=" %s"\n'%(' '.join(selection)))
    file_handle.write('echo ${PRO}\n')
    file_handle.write('../repo sync -c ${PRO}\n')

