def write_binary_file(path, data):

    with open(path, 'wb') as file:
        file.write(data)


def read_binary_file(path):

    with open(path, 'rb') as file:
        return file.read()