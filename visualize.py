from os import listdir
from os.path import isfile, join, splitext
import re
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import random
import seaborn as sns
import sys
import math

if (len(sys.argv) < 2):
    sys.exit('Please provide a KovaaK "/stats" path.')
path = sys.argv[1]
files = [f for f in listdir(path) if isfile(
    join(path, f)) and splitext(join(path, f))[1] == '.csv']
files.sort()
d = {}

for file in files:
    with open(f"{path}/{file}", newline='\n') as csvfile:
        for line in csvfile:
            filename = file.split(" - ")[0]
            date = re.findall(r'\d\d\d\d.\d\d.\d\d-\d\d.\d\d', file)[0]
            date = datetime.strptime(date, '%Y.%m.%d-%H.%M')
            date = date.timestamp()
            if "Score" in line:
                stripped = line.rstrip()
                score = re.findall(r'\d+.\d+', stripped)[0]
                score = float(score)
                if filename in d:
                    existing = d[filename]
                    existing.append({"date": date, "score": score})
                    d[filename] = existing
                else:
                    d[filename] = [{"date": date, "score": score}]

rows = int(math.ceil(len(d)/5)) if int(math.ceil(len(d)/5)) != 0 else 1
columns = math.ceil(len(d)/rows)
column = 0
fig, axes = plt.subplots(rows, columns, figsize=(12, 6), squeeze=False)
fig.tight_layout(h_pad=5, w_pad=0)
for i, key in enumerate(d.keys()):
    values = d[key]
    scores = [d['score'] for d in values]
    dates = [d['date'] for d in values]
    ax = axes[i % rows][column]
    column = column + 1 if i % rows != 0 else column
    sns.regplot(dates, scores, order=2, label=key, ax=ax)
    xticks = ax.get_xticks()
    ax.set_xticklabels([datetime.fromtimestamp(tm).strftime('%Y-%m-%d') for tm in xticks],
                       rotation=30, fontsize=6)
    for t in ax.yaxis.get_major_ticks():
        t.label.set_fontsize(6)
    ax.set_title(key, fontsize=8)
    if (i % columns) == 0:
        ax.set_ylabel('Score', fontsize=8)

fig.set_size_inches(12, fig.get_figheight())
plt.show()
