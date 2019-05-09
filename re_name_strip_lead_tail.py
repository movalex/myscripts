import os
import re

r = re.compile('^\d+_(.*)_roof')

lst = os.listdir('.')

for f in lst:
    target = r.sub('\\1', f)
    os.rename(f, target)
