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
# The model used here is the same as the one deployed on the neuroquery website
# ( https://neuroquery.saclay.inria.fr ).

# ## Encode a query into a statistical map of the brain

from neuroquery import fetch_neuroquery_model, NeuroQueryModel
from nilearn.plotting import plot_img, view_img
import ipywidgets as widgets
from IPython.display import display, display_html, Markdown

encoder = NeuroQueryModel.from_data_dir(fetch_neuroquery_model())

query = widgets.Text(value="brainstem")
button = widgets.Button(description="Run query")
display(widgets.HBox([query, button]))
output = widgets.Output()
display(output)

def run_and_display_query(_):
    result = encoder(query.value)
    with output:
        output.clear_output()
        display_html(view_img(result["z_map"], threshold=3.1).get_iframe(), raw=True)
        sw = result["similar_words"].head(12)
        display(Markdown("## Similar Words"))
        display(sw.style.bar(subset=['weight_in_brain_map', 'weight_in_query'], color='lightgreen'))
        sdocs = result["similar_documents"][['title', 'similarity']].head()
        display(Markdown("## Similar Documents"))
        display(sdocs.style.hide_index().bar(color='lightgreen'))

button.on_click(run_and_display_query)

run_and_display_query(None)


