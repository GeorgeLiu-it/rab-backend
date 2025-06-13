import uuid

def uuid_generate_list(count=10):
    return [uuid.uuid4().hex for _ in range(count)]

print(uuid_generate_list())