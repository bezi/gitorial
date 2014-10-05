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
    print(diff_text)
    files = []
    for file_diff in re.split('diff --git a/.* b/.*\n', diff_text)[1:]:
        f = {}
        lines = file_diff.split('\n')
        if len(lines) is 0:
            continue
        while 'index ' not in lines[0]:
            lines = lines[1:]
        if '/dev/null' not in lines[1]:
            f['name'] = lines[1][5:]
        else:
            f['name'] = lines[2][5:]
        f['chunks'] = []
        for file_chunk_diff in file_diff.split('\n@@')[1:]:
            lines = file_chunk_diff.split('\n')
            try:
                old_line_numbers, new_line_numbers = ((int(s), int(e))
                    for (s, e) in re.findall('[-+](\d*),(\d*) ', lines[0]))
            except:
              continue
            lines[0] = lines[0][re.search(' .* @@', lines[0]).end():]
            old_line_number = old_line_numbers[0]
            new_line_number = new_line_numbers[0]
            chunk_lines = []
            for line in lines:
                def get_whitespace(l):
                    return re.match(r'\s*', l).group().replace(' ', '&nbsp;').replace('\t', '&#09;')
                if len(line) < 1 or line[0] is ' ':
                    chunk_lines.append({
                        'old_number': old_line_number,
                        'new_number': new_line_number,
                        'content': '' if len(line) is 0 else line[1:].strip()
                    })
                    old_line_number += 1
                    new_line_number += 1
                elif line[0] is '-':
                    chunk_lines.append({
                        'old_number': old_line_number,
                        'content': line[1:].strip(),
                        'whitespace': get_whitespace(line[1:]),
                        'deletion': True
                    })
                    old_line_number += 1
                elif line[0] is '+':
                    chunk_lines.append({
                        'new_number': new_line_number,
                        'content': line[1:].strip(),
                        'whitespace': get_whitespace(line[1:]),
                        'addition': True
                    })
                    new_line_number += 1
            f['chunks'].append(chunk_lines)

        files.append(f)
    return files

if __name__ == '__main__':
    with open('diff.txt') as f:
        import json
        print(json.dumps(parse(f.read())))
