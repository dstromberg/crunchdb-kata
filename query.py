#!/usr/bin/env python3

"""Answer queries."""

import gzip
import json
import os
import pathlib


def ascii_encode_dict(data):
    """
    Insist on ASCII data, so we can print to the console during debugging.

    Based on https://stackoverflow.com/questions/9590382/forcing-python-json-module-to-work-with-ascii
    """
    # This is converting the data to bytestrings at the moment.  But it's close to what I want, so I'm committing it anyway.
    def ascii_encode(x):
        print('barney 1', type(x))
        result = x.encode('ascii', 'replace')
        print('barney 2', type(result))
        return result
    return {ascii_encode(key): ascii_encode(value) for key, value in data.items()}


def get_json_documents():
    """Return new JSON documents, at least 50 at a time."""
    # We assume a single consumer process.
    path = pathlib.Path('json-data')
    json_filenames = list(path.glob('*.json.gz'))
    if json_filenames[50:]:
        for json_filename in json_filenames:
            with gzip.open(json_filename, "r") as answerfile:
                bytes_data = answerfile.read()
            # print('fred 1', bytes_data)
            os.unlink(json_filename)
            # convert to ascii and yield
            str_data = bytes_data.decode('UTF-8')
            # print('fred 2', str_data)
            json_dict = json.loads(str_data, object_hook=ascii_encode_dict)
            print('fred 3', json_dict)
            yield json_dict


def main():
    """Get the ball rolling."""
    for _json_document in get_json_documents():
        pass
        # print(json_document)


if __name__ == '__main__':
    main()
