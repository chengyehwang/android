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

deps = {}
for file in data:
    deps[file] = {'feature':[],'deps':[]}
    for section in data[file]:
        section_name = section[0]
        if 'name' in section[1]:
            deps[file]['feature'].append(section[1]['name'])
        if 'deps' in section[1]:
            section_dep = section[1]['deps']
            deps[file]['deps'].extend(section_dep)
        if 'static_libs' in section[1]:
            static_libs = section[1]['static_libs']
            deps[file]['deps'].extend(static_libs)

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




