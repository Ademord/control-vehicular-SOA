lugares = [
    {
        'id': 1,
        'title': u'Buy groceries',
    },
    {
        'id': 2,
        'title': u'Learn Python',
    }
]
def getall():
    return lugares
def get(id):
    lugar = [lugar for lugar in lugares if lugar['id'] == id]
    if len(lugar) == 0:
        return None
    return lugar[0]

def add(temp):
    lugar = {
        'id': lugares[-1]['id'] + 1,
        'title': temp['title'],
    }
    lugares.append(lugar)
    return True

def remove(id):
    lugares.remove(get(id))
    return True

def update(id, temp):
    lugar = get(id)
    lugar['title'] = temp['title']
    return True

def valid(temp):
    if 'title' in temp and not isinstance(temp['title'], str):
        return False
    return True