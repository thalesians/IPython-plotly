import sys
import os

import delightfulsoup as ds


# -------------------------------------------------------------------------------

class PathHandler():

    def __init__(self, name):
        self.NAME = name
        self.GLOBALS = self._get_globals()
        self.nbs = self.load_references()['notebooks']
        self.args = self._get_args()

    def _get_globals(self):
        return ds.load_json('_makescripts/data/globals.json')

    def _is_valid(self, arg_or_args):
        if isinstance(arg_or_args, list):
            return all([arg in self.nbs for arg in arg_or_args])
        else:
            return arg in self.nbs

    def _get_args(self):
        NOTEBOOKS = self.GLOBALS['NOTEBOOKS']
        _args = sys.argv[1:]

        if not _args:
            raise Exception(
                "No nb argument sent\n\n"
                "python {NAME}.py nb\n"
                "python {NAME}.py nb1 nb2 ... nbN\n"
                "The available directories are:\n"
                "  {nbs}".format(NAME=self.NAME,
                                 nbs='\n  '.join(nbs))
            )
        elif not self._is_valid(_args):
            raise Exception(
                'Invalid notebook directory.\n\n'
                'The available notebook directories are:\n'
                '  {}'.format('\n  '.join(self.nbs))
            )
        else:
            return [os.path.dirname(arg + '/') for arg in _args]

    def get_path(self, arg):
        NOTEBOOKS = self.GLOBALS['NOTEBOOKS']
        return os.path.join(NOTEBOOKS, arg) + '/'

    def get_file(self, arg, ext):
        NOTEBOOKS = self.GLOBALS['NOTEBOOKS']
        return os.path.join(NOTEBOOKS, arg, arg) + ext

    def load_config(self, arg):
        path_config = os.path.join(self.get_path(arg), 'config.json')
        return ds.load_json(path_config)

    def load_references(self):
        NOTEBOOKS = self.GLOBALS['NOTEBOOKS']
        path_references = os.path.join(NOTEBOOKS, 'references.json')
        return ds.load_json(path_references)

    def get_tree(self, arg):
        join = os.path.join
        PUBLISHED = self.GLOBALS['PUBLISHED']
        INCLUDES = join(PUBLISHED, 'includes')

        tree = join(INCLUDES, arg)
        if not os.path.exists(tree):
            os.makedirs(tree)

        return dict(
            urls=join(PUBLISHED, 'urls.py'),
            sitemaps=join(PUBLISHED, 'sitemaps.py'),
            redirects=join(PUBLISHED, 'redirects.py'),
            includes=dict(
                references=join(INCLUDES, 'references.json'),
                nb=dict(
                    body=join(INCLUDES, arg, 'body.html'),
                    config=join(INCLUDES, arg, 'config.json')
                )
            ),
            static=dict(
                image=join(PUBLISHED, 'static', 'image')
            )
        )

    def get_relative_urls(self):
        relative_urls = []
        for nb in self.nbs:
            relative_urls += [self.load_config(nb)['relative_url']]
        return relative_urls
