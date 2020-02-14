import pathlib

import requests
from neuroquery import datasets

datasets.fetch_neuroquery_model()
datasets.fetch_neuroquery_model(model_name="ensemble_model_2020-02-12")
maps_url = "https://osf.io/n5avm/download"
data_dir = datasets.get_neuroquery_data_dir()
extra_data = pathlib.Path(data_dir) / "extra"
extra_data.mkdir(exist_ok=True, parents=True)
maps_file = extra_data / "masked_term_maps.npy"
if not maps_file.is_file():
    print("downloading neuroquery maps...")
    resp = requests.get(maps_url)
    with open(str(maps_file), "wb") as f:
        f.write(resp.content)
    print("done")
    del resp
