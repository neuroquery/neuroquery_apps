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

# Encoding with NeuroQuery
# ========================
#
# The model used here is the same as the one deployed on the [neuroquery
# website](https://neuroquery.org).

# ## Encode a query into a statistical map of the brain

from neuroquery import fetch_neuroquery_model, NeuroQueryModel
from neuroquery.tokenization import get_html_highlighted_text
from nilearn.plotting import plot_img, view_img
import ipywidgets as widgets
from IPython.display import display, display_html, Markdown

import utils

# %%capture
encoder = NeuroQueryModel.from_data_dir(fetch_neuroquery_model())

example_query = """Prosopagnosia,
also called face blindness,[2] is a cognitive disorder of face
perception in which the ability to recognize familiar faces, including one's own
face (self-recognition), is impaired, while other aspects of visual processing
(e.g., object discrimination) and intellectual functioning (e.g.,
decision-making) remain intact. (from wikipedia)
""".replace("\n", " ")

query = widgets.Textarea(value=example_query)
button = widgets.Button(description="Run query")
display(widgets.HBox([query, button]))
output = widgets.Output()
display(output)

def title_as_link(df):
    return df.apply(lambda x: f"<a href=\"{x['pubmed_url']}\" target=\"_blank\">{x['title']}</a>", axis=1)

def run_and_display_query(_):
    result = encoder(query.value)
    similar_docs = result["similar_documents"].head(20).copy()
    similar_docs.loc[:, 'title'] = title_as_link(similar_docs)
    with output:
        output.clear_output()
        display_html(
            get_html_highlighted_text(result["highlighted_text"]), raw=True)
        display_html(view_img(result["brain_map"], threshold=3.1).get_iframe(), raw=True)
        display_html(
            utils.download_img_link(result["brain_map"], query.value),
            raw=True)
        sw = result["similar_words"].head(12).drop("weight_in_query", axis=1)
        display(Markdown("## Similar Words"))
        display(sw.style.bar(subset=['similarity', 'weight_in_brain_map'], color='lightgreen', width=95))
        display(Markdown("## Similar Documents"))
        display(similar_docs[['title', 'similarity']].style.hide_index().bar(color='lightgreen'))

button.on_click(run_and_display_query)

run_and_display_query(None)
