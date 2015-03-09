import delightfulsoup as ds

import common

# -------------------------------------------------------------------------------


def get_slice(array, cells):
    if cells[1] == 'end':
        return array[cells[0]:]
    else:
        return array[cells[0]:cells[1]]


def main():

    path_handler = common.PathHandler('trim')

    for arg in path_handler.args:

        file_ipynb = path_handler.get_file(arg, '.ipynb')
        nb_json = ds.load_json(file_ipynb)
        cells = path_handler.load_config(arg)['cells']

        if nb_json['nbformat'] == 4:
            nb_json_cells = nb_json['cells']
            nb_json['cells'] = get_slice(nb_json_cells, cells)
        else:
            nb_json_cells = nb_json['worksheets'][0]['cells']
            nb_json['worksheets'][0]['cells'] = get_slice(nb_json_cells, cells)

        file_tmp_ipynb = file_ipynb.replace('.ipynb', '.tmp.ipynb')
        ds.dump_json(nb_json, file_tmp_ipynb, indent=1)


if __name__ == "__main__":
    main()
