def read(pathname):
    with open(pathname, 'rb') as f:
        return f.read()

def read_chunks(pathname, size):
    with open(pathname, 'rb') as f:
        return [chunk for chunk in iter(lambda: f.read(size), '')]

def readlines(pathname):
    with open(pathname, 'rb') as f:
        return f.readlines()

def readlines_accumulated(pathname):
    with open(pathname, 'rb') as f:
        return [line for line in iter(lambda: f.readline(), '')]

