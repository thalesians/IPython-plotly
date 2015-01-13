## General info


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

See [model](_makescripts/data/config-init.json).
 
#### References file

`notebooks/references.json` 

Simply fill in the notebook id. 

```json
{
    "notebooks": [
        "basemap",
        "collaborate"
    ]
}
```

These *need* to be hard-coded in order to preserve the order in which they will apper on the splash page.


## How to add a notebook?

#### Step 0: Make a directory and add ipynb file

#### Step 1: Install requirements

```
pip install -r requirements.txt
```

#### Step 2: 

```
make init nb=<notebook-id>
```

and fill in `config.json` (don't forget to remove the comments from the json file).

#### Step 3:

```
make run nb=<notebook-id>
```

This creates an `html` and `py` version of the notebook


#### Step 4:

```
make publish nb=<notebook-id>
```

This puts the html into publishable form, generates the `urls.py` and `sitemaps.py` files and appends the config and references files with auto-generatable fields.


#### Step 5:

```
make push
```

Pushes the published content over to streambed
