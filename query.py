#!/usr/bin/env python3

"""Answer queries."""

import gzip
import json
import os
import pathlib
import pprint

import unidecode


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


def main():
    """Get the ball rolling."""
    keys = set()
    for json_document in get_json_documents():
        for key in json_document:
            keys.add(key)
    pprint.pprint(keys)


if __name__ == '__main__':
    main()
