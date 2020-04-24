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
            #print(section_dep)
            deps[file]['deps'].extend(section_dep)

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
        if feature_map[dep] not in selection:
            selection.append(file)
            select(feature_map[dep])


# +
root = []
for file in deps:
    if re.search('golang',file):
        root.append(file)

for file in root:
    print(file, select(file))
# -




