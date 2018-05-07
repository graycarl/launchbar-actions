#!/usr/bin/env python
#
# LaunchBar Action Script
#
import sys
import json

choices = {
    'simple': 'Only lower case chars and numbers',
    'number': 'Only numbers',
    'char': 'Only lower case chars',
    'strong': 'With lower case and upper case chars and number and special characters'
}

try:
    prefix = sys.argv[1]
    items = filter(lambda i: i.startswith(prefix), choices.keys())
except IndexError:
    items = choices.keys()

items = [dict(title=i, subtitle=choices[i]) for i in items]

for item in items:
    item['alwaysShowsSubtitle'] = True
    if item['title'] == 'simple':
        item['label'] = 'Default'

print json.dumps(items)
