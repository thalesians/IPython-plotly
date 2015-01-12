
#### Repo structure

```
IPython-plotly/
    README.md
    CONTRIBUTING.md
    requirements.txt 
    notebooks/
        <some-notebook>/
            config.json
            <some-notebook>.ipynb
            <data>.* (optional)
            requirements.txt (auto-gen by `make run`)
            <some-notebook>.py (auto-gen by `make run`)
            <some-notebook>.zip (auto-gen if <data>.* by `make run`)
        <some-other-notebook>/ 
            ...
    makefile (setup, run, publish, push)
    _makescripts/
        *.py (scripts used `make`)
    _published/ (auto gen by `make publish`)
        sitemaps.py
        urls.py
        redirects.py
        includes/
            references.json
            <some-notebook>/
                references.json
                body.html
            <some-other-notebook>/
                ...
        static/
            image/
                <some-notebook>_image01.*
                ...
                <some-other-notebook>_image01.*
                ...
    .gitignore
```


#### Config file

`notebooks/<some-notebook>/config.json`

See [model]().
 

#### Step 1: Install requirements

```
pip install -r requirements.txt
```



#### References files

##### Domain references (auto-generated)

[`_published/includes/references.json`](...)


##### Notebook references (auto-generated)

`published/includes/<some-notebook>/references.json`

```json
{
    last_modified: '',
    name: (copied over from notebooks/),
    title: (copied over from notebooks/),
    meta_description: (copied over from notebooks/),
    file_ipynb: 'link to ipynb file',
    file_py: 'link to py file',
    file_zip: false or 'link to zip file (w/ data file)',
    requirements: [
        <some-python-package>: version-number,
        ...
    ],
    non_pip_deps: [] (copied form notebooks/)
}
```
