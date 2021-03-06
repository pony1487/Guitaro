ALLOWED_EXTENSIONS = set(['wav'])


def allowed_file(filename):
    """
    Code from http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    :param filename:
    :return: true if allowed file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_dictionary(**kwargs):
    d = dict()
    for key, value in kwargs.items():
        d[key] = value

    return d
