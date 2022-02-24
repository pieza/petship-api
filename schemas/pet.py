def petEntity(item) -> dict:
    return {
        'id': str(item['_id']),
        'owner': str(item['owner']),
        'name': item['name'],
        'type': item['type'],
        'gender': item['gender'],
        'race': item['race'],
        'weight': item['weight'],
        'image': item['image'],
        'birthday': item['birthday']
    }

def petsEntity(items) -> list:
    return [petEntity(item) for item in items]