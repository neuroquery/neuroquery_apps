import re
import tempfile
import pathlib
from base64 import b64encode


def query_map_filename(s):
    s = re.sub(r'([^\sa-zA-Z0-9])+', '', s)
    s = s.strip()
    s = s.lower()
    s = re.sub(r'\s+', '_', s)
    s = s[:72]
    s = s or 'map'
    return "{}.nii.gz".format(s)


def download_img_link(
        img, description="brain_map", label="Download brain map"):
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = str(pathlib.Path(tmp_dir) / "image.nii.gz")
        img.to_filename(img_path)
        with open(img_path, "rb") as f:
            img_data = f.read()
    file_name = query_map_filename(description)
    return ("<a href='data:application/gzip;base64,{}' "
            "download='{}'>{}</a>".format(
                b64encode(img_data).decode("utf-8"), file_name, label))
