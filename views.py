from utils import load_data, load_template, json_writter, build_response
import urllib.parse

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            split = chave_valor.split('=')
            key = urllib.parse.unquote_plus(split[0])
            print(key)
            value = urllib.parse.unquote_plus(split[1])
            print(value)
            params[key] = value
        json_writter(params, "notes.json")

        return build_response(code=303, reason='See Other', headers='Location: /') 

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)
    return build_response(body = load_template('index.html').format(notes=notes))