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

# Image search
# ==============================
#

# ## Find studies and terms relevant to a brain map
import tempfile
import pathlib
from nilearn import image
from nilearn.plotting import view_img
import requests
from neuroquery_image_search import (
    NeuroQueryImageSearch,
    studies_to_html_table,
    terms_to_html_table,
)
import ipywidgets as widgets
from IPython.display import display, display_html

# %%capture
search = NeuroQueryImageSearch()

uploader = widgets.FileUpload(accept="", multiple=False)
uploaded_button = widgets.Button(description="Search")
upload_info = widgets.HTML("Upload a .nii.gz image: ")
display(widgets.Box([upload_info, widgets.HBox([uploader, uploaded_button])]))

url_field = widgets.Text(
    value="https://neurovault.org/media/images/4563/auditory.nii.gz"
)
url_button = widgets.Button(description="Search")
url_info = widgets.HTML("Or paste a URL: ")
display(widgets.Box([url_info, widgets.HBox([url_field, url_button])]))

output = widgets.Output()
display(output)


def search_and_display_img(img_factory):
    try:
        img, img_name = img_factory()
    except Exception:
        with output:
            output.clear_output()
            display_html(
                "sorry, there was a problem with your image."
                "please upload a .nii.gz 3D image",
                raw=True,
            )
    else:
        results = search(img, n_terms=12)
        terms_table = terms_to_html_table(results["terms"])
        studies_table = studies_to_html_table(results["studies"])
        with output:
            output.clear_output()
            display_html("<h3>{}</h3>".format(img_name), raw=True)
            display_html(
                view_img(results["image"], threshold="95%").get_iframe(),
                raw=True,
            )
            display_html(f"<h3>Similar terms:</h3>\n{terms_table}", raw=True)
            display_html(
                f"<h3>Similar studies:</h3>\n{studies_table}", raw=True
            )


def _get_uploaded_img():
    uploaded, *_ = uploader.value.values()
    file_name, *_ = uploader.value.keys()
    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = str(pathlib.Path(tmp_dir) / "image.nii.gz")
        with open(image_path, "wb") as f:
            f.write(uploaded["content"])
        img = image.load_img(image_path)
    return img, file_name


def search_and_display_uploaded_img(_):
    if not uploader.value:
        with output:
            output.clear_output()
            display_html("please upload a .nii.gz 3D image", raw=True)
        return
    return search_and_display_img(_get_uploaded_img)


def _get_img_from_url():
    url = url_field.value
    resp = requests.get(url)
    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = str(pathlib.Path(tmp_dir) / "image.nii.gz")
        with open(image_path, "wb") as f:
            f.write(resp.content)
        img = image.load_img(image_path)
    return img, url


def search_and_display_img_from_url(_):
    return search_and_display_img(_get_img_from_url)


uploaded_button.on_click(search_and_display_uploaded_img)
url_button.on_click(search_and_display_img_from_url)
