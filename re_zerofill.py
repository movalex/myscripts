import os
import re
# r = re.compile('(^.*)_(\d+)\.(.*$)')
rr = re.compile('^.*_0{2,}(\d+\..*$)')
ls = os.listdir()
for f in ls:
    # print(r.sub('{}_{}.{}'.format(r'\1', r'\2'.zfill(4), r'\3'), f))
    # num = rr.match(f).group(1).zfill(4)
    # print(num)
    newname = rr.sub('DR2015_\\1', f)
    os.rename(f, newname)
