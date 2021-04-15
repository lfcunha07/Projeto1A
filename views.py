from utils import save_data, load_data, load_template, json_writter, build_response
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
            value = urllib.parse.unquote_plus(split[1])
            params[key] = value
        json_writter(params, "notes.json")

        return build_response(code=303, reason='See Other', headers='Location: /') 

    note_template = load_template('components/note.html')
    dados = load_data('notes.json')
    notes_li = [
        note_template.format(title=dados[i]['titulo'], details=dados[i]['detalhes'], id=i)
        for i in range(len(dados))
    ]
    notes = '\n'.join(notes_li)
    return build_response(body = load_template('index.html').format(notes=notes))

def editNote(request, note_id):
    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]

    note_to_edit = load_data('notes.json')[int(note_id)]
    if request.startswith('POST'):
        path = int(note_id)
        new_template = []
        dados = load_data('notes.json')

        for i in range(len(dados)):
            if path != i:
                new_template.append(dados[i])
            else:
                a = 0
                for divide in corpo.split('&'):
                    split = divide.split('=')
                    if a == 0:
                        dados[i]['titulo'] = urllib.parse.unquote_plus(split[1])
                    else:
                        dados[i]['detalhes'] = urllib.parse.unquote_plus(split[1])
                    a += 1
                new_template.append(dados[i])
        save_data(new_template, "notes.json")

        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(body = load_template('edit.html').format(title=note_to_edit["titulo"],content=note_to_edit["detalhes"]))

def deleteNote(path):
    path = int(path)
    new_template = []
    dados = load_data('notes.json')

    for i in range(len(dados)):
        if path != i:
            new_template.append(dados[i])
    save_data(new_template, "notes.json")

    return build_response(code=303, reason='See Other', headers='Location: /')




