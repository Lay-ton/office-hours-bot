
def RepInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def chop(s):
    results = []
    while len(s) >= 2000:
        cut = s[0:2000]
        j = len(cut)-1
        while cut[j] != '\n':
            j -= 1
        results.append(cut[0:j+1])
        s = s[j+1:]

    results.append(s)
    return results
