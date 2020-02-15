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

# Match a study with its peak activations
# =======================================
#
# Below are displayed a study's title and abstract. Which of the two peak
# activation patterns belongs to this study?

import requests
from lxml import etree
import numpy as np
import pandas as pd
from nilearn import plotting
from neuroquery import datasets, img_utils
from neuroquery import NeuroQueryModel
import ipywidgets as widgets
from IPython.display import display, display_html

button = widgets.Button(description="Play")
score_display = widgets.HTML(value="")
display(widgets.HBox([score_display, button]))
output = widgets.Output()
display(output)

coordinates = pd.read_csv(datasets.fetch_peak_coordinates())
pmids = np.unique(coordinates["pmid"].values.ravel())
masker = img_utils.get_masker(target_affine=(4, 4, 4))

encoder = NeuroQueryModel.from_data_dir(datasets.fetch_neuroquery_model())
corpus_metadata = encoder.corpus_info["metadata"].set_index("pmid")

studies = {}
score = {"lose": 0, "win": 0}


def plot_from_pmid(pmid):
    coords = coordinates.query("pmid == {}".format(pmid))
    img = img_utils.gaussian_coord_smoothing(
        coords.loc[:, ["x", "y", "z"]].values, mask_img=masker,
        fwhm=6)
    return plotting.view_img(img, threshold=1e-5, colorbar=False)


def update_score_display():
    total = score["lose"] + score["win"]
    score_display.value = ("<span style='font-size: large;'>"
                           "Score: {} / {} ({:.0%}) </span>".format(
                               score["win"], total, score["win"] / total))


def lose(_):
    score["lose"] = score["lose"] + 1
    update_score_display()
    with output:
        output.clear_output()
        display_html("<h2>You lose!</h2>", raw=True)
        display_both_studies(None)


def win(_):
    score["win"] = score["win"] + 1
    update_score_display()
    with output:
        output.clear_output()
        display_html("<h2>You win!</h2>", raw=True)
        display_both_studies(None)


def get_abstract(pmid):
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
           "?db=pubmed&id={}&retmode=xml".format(pmid))
    resp = requests.get(url)
    tree = etree.XML(resp.content.decode("utf-8"))
    return tree.xpath("//AbstractText/text()")[0]


def title_as_link(title, pmid):
    return ("<a href='https://www.ncbi.nlm.nih.gov/pubmed/{}' "
            "target='blank'>{}</a>".format(pmid, title))


lose_button = widgets.Button(description="select")
lose_button.on_click(lose)
win_button = widgets.Button(description="select")
win_button.on_click(win)


def display_both_studies(_):
    button.description = "Play Again"
    button.layout.visibility = "visible"
    with output:
        display_html("<h4>Correct associations:</h4>", raw=True)
        display_html(
            "<h4>{}</h4>".format(
                title_as_link(corpus_metadata.loc[studies["pmid"]].title,
                              studies["pmid"])),
            raw=True)
        display(studies["positive_plot"])
        display_html(
            "<h4>{}</h4>".format(
                title_as_link(
                    corpus_metadata.loc[studies["negative_pmid"]].title,
                    studies["negative_pmid"])),
            raw=True)
        display(studies["negative_plot"])


def display_question(_):
    pmid = np.random.choice(pmids)
    negative_pmid = np.random.choice(pmids)
    title = corpus_metadata.loc[pmid]["title"]
    abstract = get_abstract(pmid)
    studies["pmid"] = pmid
    studies["negative_pmid"] = negative_pmid
    studies["positive_plot"] = widgets.HTML(plot_from_pmid(pmid).get_iframe())
    studies["negative_plot"] = widgets.HTML(
        plot_from_pmid(negative_pmid).get_iframe())
    win_box = widgets.HBox([studies["positive_plot"], win_button])
    lose_box = widgets.HBox([studies["negative_plot"], lose_button])
    button.layout.visibility = "hidden"
    with output:
        output.clear_output()
        display_html(
            "<h4>{}</h4>".format(title_as_link(title, pmid)), raw=True)
        display_html(
            "<details><summary>Abstract</summary>{}</details>".format(
                abstract),
            raw=True)
        display_html(
            "<h4>Which peak activations belong to this study?</h4>", raw=True)
        if np.random.randint(2):
            display(win_box)
            display(lose_box)
        else:
            display(lose_box)
            display(win_box)


button.on_click(display_question)
display_question(None)
