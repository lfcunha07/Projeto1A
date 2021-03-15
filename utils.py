import os, json
from io import StringIO
from pathlib import Path

def extract_route(request):
    lines = request.splitlines()
    line = lines[0]
    final = line[(line.index("/")+1):(line.index(" H"))]
    return final

def read_file(file):
    file_extension = file.suffix
    if file_extension == ".txt" or file_extension == ".html" or file_extension == ".css" or file_extension == ".js":
        with open(file, 'r') as data:
            conteudo = data.read()
            return conteudo
    else:
        with open(file, 'rb') as f:
            return f.read()

def load_data(path):
    file_path = str('data/' + path)
    with open(file_path, 'rt') as file:
        return json.load(file)

def load_template(name_file):
    path = str("templates/"+name_file)
    with open(path,'rt') as file:
        file_string = str(file.read())
        return file_string

def json_writter(params, path):
    file_path = str("data/"+path)
    loaded_file = load_data(path)
    loaded_file.append(params)
    with open(file_path, 'wt') as file:
        return json.dump(loaded_file, file)
'''
def json_deleter(params, path):
    file_path = str("data/"+path)
    loaded_file = load_data(path)
    loaded_file.append(params)
    with open(file_path, 'wt') as file:
        return json.dump(loaded_file, file)
'''
def build_response(body='', code=200, reason='OK', headers=''):
    if isinstance(body, str):
        body = body.encode()
    if headers == '':
        string = ('HTTP/1.1 ' + str(code) + ' ' + reason + headers + '\n\n').encode() + body
    else:
        string = ('HTTP/1.1 ' + str(code) + ' ' + reason + '\n' + headers + '\n\n').encode() + body
    return string