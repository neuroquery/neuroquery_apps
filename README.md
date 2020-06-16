# neuroquery_apps

[![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fminimal_dashboard.py)

A set of small apps implemented as [Voilà dashboards](https://github.com/voila-dashboards/voila). These apps are simpler and less complete than the main NeuroQuery website -- they are meant to prototype new features or demonstrate new models, for instance.

These contain, among others:

- A [stripped-down version](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fminimal_dashboard.py) of the [NeuroQuery](https://neuroquery.org) website.
- An [ensemble model demo](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fensemble_model_demo.py)
- A [decoding app](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fdecoding.py)
- A [game](https://notebooks.gesis.org/binder/v2/gh/neuroquery/neuroquery_apps/master?urlpath=%2Fvoila%2Frender%2Fguess_activations.py) in which we have to guess which of two brain activation patterns belongs to a given neuroimaging study, based on its title and abstract.

## Running the applications locally

Some of the apps are a bit too memory and computation intensive for mybinder.
You may find it easier to run them locally. Just clone this repo, then run:

```
pip install -r binder/requirements.txt
python download_datasets.py
voila --VoilaConfiguration.extension_language_mapping='{".py": "python"}'
```
