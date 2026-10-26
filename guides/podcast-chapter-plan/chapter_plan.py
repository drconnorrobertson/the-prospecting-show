"""Illustrative timing checks; no audio inspection, provider validation or publishing."""
import csv
import json
import re
import sys


def clock(seconds):
    return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'


def plan(rows, duration):
    if type(duration) is not int or duration <= 0:
        raise ValueError('Duration must be a positive integer number of seconds')
    chapters = []
    seen = set()
    for row in rows:
        item = row['chapter_id'].strip()
        title = row['title'].strip()
        start = row['start_seconds'].strip()
        if not item or item in seen or not title:
            raise ValueError('Unique IDs and nonempty titles are required')
        if not re.fullmatch(r'[0-9]+', start):
            raise ValueError('Starts must be integer seconds')
        start = int(start)
        if start >= duration or (chapters and start <= chapters[-1]['start_seconds']):
            raise ValueError('Starts must increase and precede the duration')
        seen.add(item)
        chapters.append({'chapter_id': item, 'title': title, 'start_seconds': start,
                         'start_time': clock(start)})
    if not chapters or chapters[0]['start_seconds'] != 0:
        raise ValueError('The illustrative plan must begin at zero')
    for i, item in enumerate(chapters):
        end = chapters[i+1]['start_seconds'] if i+1 < len(chapters) else duration
        item['end_seconds'] = end
        item['duration_seconds'] = end-item['start_seconds']
    return {'duration_seconds': duration, 'chapters': chapters}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python3 chapter_plan.py fictional-chapters.csv 2700')
    with open(sys.argv[1], newline='', encoding='utf-8') as source:
        result = plan(csv.DictReader(source), int(sys.argv[2]))
    print(json.dumps(result, indent=2))
