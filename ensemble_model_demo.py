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
# website](https://neuroquery.saclay.inria.fr).

# ## Encode a query into a statistical map of the brain

from neuroquery import fetch_neuroquery_model
from neuroquery.encoding import SimpleEncoder
from neuroquery.tokenization import get_html_highlighted_text
from nilearn.plotting import plot_img, view_img
import ipywidgets as widgets
from IPython.display import display, display_html, Markdown

EXAMPLE_QUERY = (
    "Theory of mind is the ability to attribute mental states — beliefs, "
    "intents, desires, emotions, knowledge, etc. — to oneself, and to others, "
    "and to understand that others have beliefs, desires, intentions, and "
    "perspectives that are different from one's own. (from wikipedia)")

# %%capture
encoder = SimpleEncoder.from_data_dir(
    fetch_neuroquery_model(model_name="ensemble_model_2020-02-12"))

query = widgets.Textarea(value=EXAMPLE_QUERY)
button = widgets.Button(description="Run query")
display(widgets.HBox([query, button]))
output = widgets.Output()
display(output)


def run_and_display_query(_):
    result = encoder(query.value)
    with output:
        output.clear_output()
        display_html(
            get_html_highlighted_text(result["highlighted_text"]), raw=True)
        display_html(
            view_img(result["brain_map"], threshold="97%",
                     colorbar=False).get_iframe(),
            raw=True)


button.on_click(run_and_display_query)

run_and_display_query(None)
