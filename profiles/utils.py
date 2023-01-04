import uuid

def get_unique_id():
    code = str(uuid.uuid4())[:8].replace("-","").lower()
    return code