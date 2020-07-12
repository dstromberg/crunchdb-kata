#!/usr/bin/env python3

"""Answer queries."""

import collections
import gzip
import json
import os
import pathlib
# import pprint
import sys

# import pudb
import unidecode

import constants


def ascii_encode_dict(data):
    """
    Insist on ASCII data, so we can print to the console during debugging.

    Assumes 'data' isn't nested at all.

    Based on https://stackoverflow.com/questions/9590382/forcing-python-json-module-to-work-with-ascii
    """
    # This is converting the data to bytestrings at the moment.  But it's close to what I want, so I'm committing it anyway.
    def ascii_encode(string):
        assert isinstance(string, str)
        result = unidecode.unidecode(string)
        return result
    return {ascii_encode(key): ascii_encode(value) for key, value in data.items()}


def get_json_documents(convert=True):
    """Return new JSON documents, at least 50 at a time."""
    # We assume a single consumer process.
    path = pathlib.Path('json-data')
    json_filenames = list(path.glob('*.json.gz'))
    if json_filenames[50:]:
        for json_filename in json_filenames:
            with gzip.open(json_filename, "r") as answerfile:
                bytes_data = answerfile.read()
            os.unlink(json_filename)
            str_data = bytes_data.decode('UTF-8')
            if convert:
                # This is nice for debugging
                json_dict = json.loads(str_data, object_hook=ascii_encode_dict)
            else:
                json_dict = json.loads(str_data)
            yield json_dict


def usage(retval):
    """Output a usage message."""
    if retval == 0:
        file_ = sys.stdout
    else:
        file_ = sys.stderr
    print('{}: Must specify exactly one of:'.format(sys.argv[0]), file=file_)
    print('    --most-frequently-owned-car-brand', file=file_)
    print('    --favorite-car-brand', file=file_)
    print('    --most-frequently-listened-music-artist', file=file_)
    print('    --favourite-music-artist', file=file_)
    sys.exit(retval)


def main():
    """Get the ball rolling."""
    # pudb.set_trace()
    query = ''
    query_count = 0
    while sys.argv[1:]:
        if sys.argv[1] == '--most-frequently-owned-car-brand':
            query_count += 1
            query = 'owned-car-brand'
        elif sys.argv[1] == '--favorite-car-brand':
            query_count += 1
            query = 'favourite-car-brand'
        elif sys.argv[1] == '--most-frequently-listened-music-artist':
            query_count += 1
            query = 'listened-music-artist'
        elif sys.argv[1] == '--favourite-music-artist':
            query_count += 1
            query = 'favourite-music-artist'
        elif sys.argv[1] in ('-h', '--help'):
            usage(0)
        else:
            print('{}: Unrecognized option: {}'.format(sys.argv[0], sys.argv[1]), file=sys.stderr)
            usage(1)
        del sys.argv[1]

    if query_count != 1:
        usage(1)

    counter = collections.Counter()
    keys = set()
    for json_docno, json_document in enumerate(get_json_documents()):
        print(json_docno, file=sys.stderr)
        for key, value in json_document.items():
            base, dot, name = key.partition('.')
            if dot != '.':
                # print(key)
                continue
            assert '.' not in base
            assert dot == '.', "dot is {}".format(dot)
            assert name != ''
            # pudb.set_trace()
            keys.add(base)
            # Counter({'listened_singers': 558224,
            # 'known_singers': 558224,
            # 'disliked_singers': 558224,
            # 'liked_cars': 272084,
            # 'owned_cars': 272084,
            # 'ever_owned_cars': 272084})

            # pudb.set_trace()
            if (
                query == 'owned-car-brand' and base in constants.mrcarvars and value == 'yes' or
                query == 'favourite-car-brand' and base in constants.mrcarvars and value == 'yes' or
                query == 'listened-music-artist' and base in constants.mrsingervars and value == 'yes' or
                query == 'favourite-music-artist' and base in constants.singervars and value == 'yes'
            ):
                # FIXME: Do we have no favourite music artists in our sample data?
                # print(name, value, file=sys.stderr)
                counter[name] += 1

    list_ = counter.most_common(1)
    if len(list_) != 0:
        print(list_[0])
    else:
        print('No occurences found', file=sys.stderr)


if __name__ == '__main__':
    main()
