import os

def move_file(old_filename, new_filename):
    old_file = open(old_filename, "rb")
    new_file = open(new_filename, "wb+")

    new_file.write(old_file.read())

    old_file.close()
    os.remove(old_filename)
    new_file.close()
    return True
