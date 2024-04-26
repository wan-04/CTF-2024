import json
import dateutil.parser
from operator import itemgetter

data = []

with open('stage2') as f:
  for line in f:
    entry = json.loads(line)
    data.append(entry)

# Sort the data by "Created0x10" field in ascending order    
data.sort(key=itemgetter('Created0x10'))

# Write sorted data to new file
with open('output.txt', 'w') as f:
  for item in data:
    f.write(json.dumps(item) + '\n')