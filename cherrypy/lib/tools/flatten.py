import cherrypy


def flatten(debug=False):
    """Wrap response.body in a generator that recursively iterates over body.

    This allows cherrypy.response.body to consist of 'nested generators';
    that is, a set of generators that yield generators.
    """
    import types

    def flattener(input):
        numchunks = 0
        for x in input:
            if not isinstance(x, types.GeneratorType):
                numchunks += 1
                yield x
            else:
                for y in flattener(x):
                    numchunks += 1
                    yield y
        if debug:
            cherrypy.log('Flattened %d chunks' % numchunks, 'TOOLS.FLATTEN')
    response = cherrypy.serving.response
    response.body = flattener(response.body)