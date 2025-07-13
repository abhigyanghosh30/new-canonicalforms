import os
import yaml

from hashlib import md5
from markupsafe import Markup

from flask import render_template_string, current_app

# Read meganav.yaml
with open("data/canonical_navigation.yaml") as meganav_file:
    canonical_meganav_data = yaml.load(meganav_file.read(), Loader=yaml.FullLoader)


def build_navigation(id, title):
    """
    Takes an id and title and returns the assosiate dropdown data.
    This function is made globally avaiable and then called from the
    jinja template 'dropdown.html'
    """
    meganav_section = canonical_meganav_data[id]
    html_string = render_template_string(
        '{% include "canonical_navigation/dropdown.html" %}',
        id=id,
        title=title,
        section=meganav_section,
    )
    return Markup(html_string)


def split_list(array, parts):
    """
    Split an array into multiple sub-arrays of approximately equal size.

    Parameters:
    array (list): The array to be split.
    parts (int): The number of parts to split the array into.

    Returns:
    list: A list of sub-arrays.
    """
    if parts <= 0:
        raise ValueError("Number of parts must be a positive integer")

    k, m = divmod(len(array), parts)
    return [
        array[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(parts)
    ]


def versioned_static(filename):
    """
    Template function for generating URLs to static assets:
    Given the path for a static file, output a url path
    with a hex hash as a query string for versioning
    """
    static_path = current_app.static_folder
    static_url = current_app.static_url_path

    file_path = os.path.join(static_path, filename)
    if not os.path.isfile(file_path):
        # File is missing, simply return the string so we don't break anything
        return f"{static_url}/{filename}?v=file-not-found"

    # Use MD5 as we care about speed a lot
    # and not security in this case
    file_hash = md5()
    with open(file_path, "rb") as file_contents:
        for chunk in iter(lambda: file_contents.read(4096), b""):
            file_hash.update(chunk)

    return f"{static_url}/{filename}?v={file_hash.hexdigest()[:7]}"
