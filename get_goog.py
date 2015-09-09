#!/usr/bin/env python

'''An older example of code that searches using a google custom search
engine'''

from __future__ import print_function

from os.path import exists
from sys import exit
# We override the default open function
from codecs import open

# pandas is only necessary for the demo in main(), but you probably have it
# installed anyway
import pandas as pd
import requests


class GoogMatch:
    url = 'https://www.googleapis.com/customsearch/v1'

    # You can create a cx for all the web by removing all domains from a
    # "search the entire web, but emphasize..." engine. This may no longer be
    # necessary.
    # This dict will get mutated regularly with the search ('q') arg as well
    args = {'key': 'your key... we should add instructions',
            'cx': 'your cx string (for your custom engine)'}

    def get_results(self, text):
        '''Just pass in a string, get google results

        This is set up for writing to files, but is easy to change to returning
        a JSON parsed version as well.'''
        tokens = text.split()
        self.args['q'] = ' '.join(tokens[:32])
        return requests.get(self.url, params=self.args, verify=False)

    def process_cols(self, df):
        for colname, txts in df.iteritems():
            for id, txt in txts.iteritems():
                fname = 'google_searches/%s_%s.json' % (id, colname)
                if exists(fname):
                    continue
                res = self.get_results(txt)
                with open(fname, 'w', 'utf8') as ofile:
                    ofile.write(res.text)

                if 'error' in res.json():
                    print('Detected Error for %s %s' % (id, colname))
                    exit()


def main(csv_fname):
    '''A schema of how you might use the above. Data files are not actually
    provided, but you can imagine a CSV file with some suspicious text in some
    columns.'''
    # Trailing commas will result in final "Unnamed" rows (safe to ignore)
    core_df = pd.read_csv(csv_fname, encoding='utf8')

    gm = GoogMatch()
    gm.process_cols(core_df[['text1', 'text2']])


if __name__ == '__main__':
    from sys import argv

    # Not very safe...
    main(argv[1])
