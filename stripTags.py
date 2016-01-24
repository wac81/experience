def stripTags(s):
    ''' Strips HTML tags.
        Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440481
    '''
    intag = [False]

    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True

    return ''.join(c for c in s if chk(c))