import json

with open('data.json') as f:
  for line in f:
    obj = json.loads(line)
    try:
        if obj['Extension'] == '.zip' and '02-13' in obj['Created0x10']:
            print(obj)
    except KeyError:
        continue

f.close()