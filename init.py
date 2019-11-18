# coding: utf-8
import os
from _datetime import datetime as dt
from flask import Flask
from flask import request

print('voila')

source_dir = os.path.abspath('.') + os.path.sep
extensions = ['.jpeg', '.jpg']
app = Flask(__name__, static_folder=source_dir)


def get_images(source_dir):
    images = []
    for path, subdirs, files in os.walk(source_dir):
        for file in files:
            if str.lower(os.path.splitext(file)[1]) in extensions:
                full_path = os.path.join(path, file)
                rel_path = os.path.relpath(full_path, source_dir)
                images.append({'path': rel_path,
                               'date': dt.fromtimestamp(os.path.getmtime(full_path))})
    print(images)
    return images


def get_dates(images):
    dates = set([x['date'].date() for x in images])
    return dates


images = get_images(source_dir)
dates = get_dates(images)


@app.route('/', methods=['GET', 'POST'])
def get_index_page():
    global dates
    page_content = ' '.join(['<a href="/dates?date={}">{}</a>'.format(date,
                                                                      date.strftime('%y-%m-%d'))
                             for date in dates])
    return html.format(page_content)


@app.route('/dates', methods=['GET', 'POST'])
def get_images_page():
    global images
    date = request.args.get('date')
    print(date)
    cur_images = [x['path'] for x in images if str(x['date'].date()) == date]
    print(cur_images)
    page_content = (f'<h3>{date}</h3>' +
                    ''.join([f'<img src = "{x}" height=200>' for x in cur_images]))
    return page_content


html = '''
<html>
<head></head>
<body>{}</body>
</html>
'''


app.run('localhost', port='9000')
