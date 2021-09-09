from itertools import dropwhile


def is_comment(s):
    """ function to check if a line
         starts with some character.
         Here # for comment
    """
    # return true if a line starts with #
    return s.startswith('#')


with open('common-passwords.txt', 'r') as fr:
    with open('common-passwords-words.txt', 'w') as fw:
        for curline in dropwhile(is_comment, fr):
            parts = curline.split(sep=':')
            if len(parts) == 3:
                fw.write(parts[2])
            elif len(parts) == 2:
                fw.write(parts[1])





