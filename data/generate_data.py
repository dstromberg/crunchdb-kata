"""Provide a Very naive utility to simulate random chunks of survey data."""

import gzip
# import itertools
import json
import os
import random
import sys
import uuid

import constants


def main():
    """Start the ball rolling."""
    os.makedirs("../json-data", exist_ok=True)
    # num_docs = 1005
    num_docs = int(sys.argv[1])
    for answerno in range(num_docs):
        print('Creating document', answerno, 'of', num_docs)
        basename = "../json-data/chunck_%s" % uuid.uuid4()
        tempname = basename + '.temp.gz'
        longtermname = basename + '.json.gz'

        # We compress with gzip.
        # It's relatively fast compression.
        # We could compress with bzip2 or zlib instead if we have the CPU time available.
        # We could do bits and bytes, but that's harder to debug, and only worth it if there's a LOT of data to store.
        # We could eliminate all unanswered responses, but that is a little prone to surprises.
        # We also have the option of using bson instead of json.
        with gzip.open(tempname, "w") as answerfile:
            row = {"pk": "%d" % answerno}
            for carvar in constants.carvars:
                row[carvar] = random.choice(constants.carbrands)
            for carvar in constants.mrcarvars:
                for carbrand in constants.carbrands:
                    row["%s.%s" % (carvar, carbrand)] = random.choice(constants.answers)
            for singvar in constants.singervars:
                row[singvar] = random.choice(constants.singers)
            for singvar in constants.mrsingervars:
                for singer in constants.singers:
                    row["%s.%s" % (singvar, singer)] = random.choice(constants.answers)
            string = json.dumps(row)
            answerfile.write(string.encode('UTF-8'))
        os.rename(tempname, longtermname)


if __name__ == '__main__':
    main()
