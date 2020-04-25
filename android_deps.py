# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import json
import pandas as pd
import re
import os

with open('android_bp.json','r') as file_handle:
    data = json.load(file_handle)

all_tag = []
for file in data:
    for section in data[file]:
        for tag in section[1]:
            if tag not in all_tag:
                all_tag.append(tag)
print(all_tag)

deps = {}
for file in data:
    deps[file] = {'feature':[],'deps':[]}
    for section in data[file]:
        section_name = section[0]
        if 'name' in section[1]:
            deps[file]['feature'].append(section[1]['name'])
        for tag in ['deps','static_libs','libs','shared_libs']:
            if tag in section[1]:
                tag_data = section[1][tag]
                deps[file]['deps'].extend(tag_data)

print('number of Android.bp: %d\n'%len(data))
pd.DataFrame.from_dict(deps, orient='index')

feature_map = {}
for file in deps:
    for feature in deps[file]['feature']:
        feature_map[feature]=file

pd.DataFrame({'file':feature_map})

selection = []
def select(file):
    global selection
    for dep in deps[file]['deps']:
        if dep not in selection:
            selection.append(dep)
            select(feature_map[dep])


# +
root = []
for file in deps:
    if re.search('simpleperf',file):
        root.append(file)

with open('sync.sh', 'w') as file_handle:
    file_handle.write('#!/bin/bash\n')
    for file in root:
        selection = []
        select(file)
        file_handle.write('#### %s\n'%file)
        for feature in selection:
            file_handle.write('# %s\n'%feature)
            dir=os.path.dirname(feature_map[feature])
            file_handle.write('PRO+="%s "\n'%dir)
    file_handle.write('echo ${PRO}\n')
    file_handle.write('repo sync -c ${PRO}\n')
# -




