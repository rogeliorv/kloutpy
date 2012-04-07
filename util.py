import itertools

def make_chunks(iterable, n = 5):
    """ Divide an iterable into n-sized chunks and 
    yield the chunks as a result.
    
    Note: There are shorter versions but this is unreadable for the untrained eyes as is."""
    # Old version, does not work with unsuscriptable items
    #for i in xrange(0, len(l), n):  yield l[i:i+n]
    it = iter(iterable)
    chunk = list(itertools.islice(it, n))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(it, n))
