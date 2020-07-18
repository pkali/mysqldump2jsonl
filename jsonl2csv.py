import sys
import json

separator = '\t'
for i,line in enumerate(sys.stdin):
    j = json.loads(line)
    if i==0:
        # create header
        head = j
        print(separator.join(head))
    vals = [str(j[key]) if j[key] is not None else 'NULL' for key in head]
    print(separator.join(vals))
        