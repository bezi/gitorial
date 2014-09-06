#!/usr/bin/env python3
import re
'''
Get diffs for commits on Github with
```
curl -H "Accept: application/vnd.github.diff" \
  https://api.github.com/repos/bezi/gitorial/commits/d5f43a7a3f4b3cacfc0fea98751e70f65c9da79d
```
'''
def parse(diff_text):
    files = []
    for file_diff in re.split('diff --git a/.* b/.*\n', diff_text)[1:]:
        f = {}
        lines = file_diff.split('\n')
        f['name'] = lines[1][5:]
        f['lines'] = []
        for file_chunk_diff in file_diff.split('\n@@')[1:]:
            lines = file_chunk_diff.split('\n')
            old_line_numbers, new_line_numbers = ((int(s), int(e))
                for (s, e) in re.findall('[-+](\d*),(\d*) ', lines[0]))
            lines[0] = lines[0][re.search(' .* @@', lines[0]).end():]
            old_line_number = old_line_numbers[0]
            new_line_number = new_line_numbers[0]
            for line in lines:
                if len(line) < 1 or line[0] is ' ':
                    f['lines'].append({
                        'old_number': old_line_number,
                        'new_number': new_line_number,
                        'content': '' if len(line) is 0 else line[1:]
                    })
                    old_line_number += 1
                    new_line_number += 1
                elif line[0] is '-':
                    f['lines'].append({
                        'old_number': old_line_number,
                        'content': line[1:],
                        'deletion': True
                    })
                    old_line_number += 1
                elif line[0] is '+':
                    f['lines'].append({
                        'new_number': new_line_number,
                        'content': line[1:],
                        'addition': True
                    })
                    new_line_number += 1

        files.append(f)
    return files
