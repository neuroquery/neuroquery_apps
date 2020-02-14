# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Naive decoding with NeuroQuery
# ==============================
#
# Here we show a very simple approach to decoding brain maps:
# we look for terms that are associated with similar maps by NeuroQuery.
# This is experimental and results will improve if we introduce a better
# method in the future.
#
# The model used here is the same as the one deployed on the [neuroquery
# website](https://neuroquery.org).

# ## Find terms relevant to a brain map
import tempfile
import numpy as np
import pathlib
from nilearn import image
from nilearn.plotting import view_img
import requests
from neuroquery import fetch_neuroquery_model, NeuroQueryModel, datasets
import ipywidgets as widgets
from IPython.display import display, display_html

# %%capture
encoder = NeuroQueryModel.from_data_dir(fetch_neuroquery_model())
voc = np.asarray(encoder.full_vocabulary())
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
term_maps = np.load(str(maps_file))
norms = np.linalg.norm(term_maps, axis=1)
norms[norms == 0] = 1
term_maps /= norms[:, None]

uploader = widgets.FileUpload(accept='', multiple=False)
uploaded_button = widgets.Button(description="Decode")
upload_info = widgets.HTML("Upload a .nii.gz image: ")
display(widgets.Box([upload_info, widgets.HBox([uploader, uploaded_button])]))

url_field = widgets.Text(
    value="https://neurovault.org/media/images/4563/auditory.nii.gz")
url_button = widgets.Button(description="Decode")
url_info = widgets.HTML("Or paste a URL: ")
display(widgets.Box([url_info, widgets.HBox([url_field, url_button])]))

output = widgets.Output()
display(output)


def decode(img):
    masked_query = encoder.get_masker().transform(img).ravel()
    # remove background noise
    abs_query = np.abs(masked_query)
    threshold = np.percentile(abs_query, 80)
    masked_query[abs_query < threshold] = 0
    similarities = np.abs(masked_query).dot(term_maps.T)
    similarities *= np.log(1 + encoder.document_frequencies().values.ravel())
    top_20 = np.argsort(similarities)[::-1][:20]
    top_terms = voc[top_20].ravel()
    return top_terms


def decode_and_display_uploaded_img(_):
    if not uploader.value:
        with output:
            output.clear_output()
            display_html("please upload a .nii.gz 3D image", raw=True)
        return
    try:
        uploaded, *_ = uploader.value.values()
        file_name, *_ = uploader.value.keys()
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = str(pathlib.Path(tmp_dir) / "image.nii.gz")
            with open(image_path, "wb") as f:
                f.write(uploaded["content"])
            img = image.load_img(image_path)
    except Exception:
        with output:
            output.clear_output()
            display_html(
                "sorry, there was a problem with your image."
                "please upload a .nii.gz 3D image",
                raw=True)
    else:
        top_terms = list(decode(img))
        with output:
            output.clear_output()
            display_html("<h3>{}</h3>".format(file_name), raw=True)
            display_html(view_img(img, threshold="95%").get_iframe(), raw=True)
            display_html(
                "<h3>Top terms:</h3>{}".format(", ".join(top_terms)), raw=True)


def decode_and_display_img_from_url(_):
    url = url_field.value
    try:
        resp = requests.get(url)
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = str(pathlib.Path(tmp_dir) / "image.nii.gz")
            with open(image_path, "wb") as f:
                f.write(resp.content)
            img = image.load_img(image_path)
    except Exception:
        with output:
            output.clear_output()
            display_html(
                "sorry, there was a problem with your image."
                "please enter a URL pointing to a .nii.gz 3D image",
                raw=True)
    else:
        top_terms = list(decode(img))
        with output:
            output.clear_output()
            display_html("<h3>{}</h3>".format(url), raw=True)
            display_html(view_img(img, threshold="95%").get_iframe(), raw=True)
            display_html(
                "<h3>Top terms:</h3>{}".format(", ".join(top_terms)), raw=True)


uploaded_button.on_click(decode_and_display_uploaded_img)
url_button.on_click(decode_and_display_img_from_url)
