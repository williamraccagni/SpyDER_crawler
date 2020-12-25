def load(file : str) -> list:

    fi = open(file, 'r')
    lines = [line.rstrip('\n') for line in fi.readlines()]

    return lines