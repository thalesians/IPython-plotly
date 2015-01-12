import delightfulsoup as ds

import common

# -------------------------------------------------------------------------------


def main():

    path_handler = common.PathHandler('trim')

    for arg in path_handler.args:

        file_ipynb = path_handler.get_file(arg, '.ipynb')
        nb_json = ds.load_json(file_ipynb)
        cells = path_handler.load_config(arg)['cells']

        nb_json_cells = nb_json['worksheets'][0]['cells']
        nb_json['worksheets'][0]['cells'] = nb_json_cells[cells[0]:cells[1]]

        file_tmp_ipynb = file_ipynb.replace('.ipynb', '.tmp.ipynb')
        ds.dump_json(nb_json, file_tmp_ipynb, indent=1)

if __name__ == "__main__":
    main()
