# neuroquery_apps

[![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2F)

A set of small apps implemented as [Voilà dashboards](https://github.com/voila-dashboards/voila). These apps are simpler and less complete than the main NeuroQuery website -- they are meant to prototype new features or demonstrate new models, for instance.

These contain, among others:

- A [stripped-down version](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fneuroquery_encoding.py) of the [NeuroQuery](https://neuroquery.org) website.
- A [reverse NeuroQuery](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fimage_search.py): we input an image and search for terms and studies that have similar patterns of activation
- An [ensemble model demo](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fensemble_model_demo.py)

## Running the applications locally

Some of the apps are a bit too memory and computation intensive for mybinder.
You may find it easier to run them locally. Just clone this repo, then run:

```
pip install -r binder/requirements.txt
voila --VoilaConfiguration.extension_language_mapping='{".py": "python"}'
```
