# Encoding with NeuroQuery
# ========================
# 
# The model used here is the same as the one deployed on the neuroquery website
# ( https://neuroquery.saclay.inria.fr ).

# ## Encode a query into a statistical map of the brain

from neuroquery import fetch_neuroquery_model, NeuroQueryModel
from nilearn.plotting import plot_img, view_img
import ipywidgets as widgets
from IPython.display import display

encoder = NeuroQueryModel.from_data_dir(fetch_neuroquery_model())

query = widgets.Text(value="brainstem")
button = widgets.Button(description="Run query")
display(query)
display(button)
output = widgets.Output()

result = encoder(query)
plot_img(result["z_map"], threshold=3.1)

# (drag the mouse on this interactive plot to see other slices)

# ## Display some relevant terms:

print(result["similar_words"].head(15))

# ## Display some relevant studies:

print("\nsimilar studies:\n")
print(result["similar_documents"].head())

