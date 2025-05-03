# Riley Hanson
# 4/17/25
# Final Project: PyScript CSV Viewer (Weightlifting Edition)

import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display, when
from js import console

# These lines update the HTML page title and top message
title = "Olympic Weightlifting Viewer (First & Last 5 Rows)"
page_message = "This app loads a CSV from a URL and displays the first and last 5 rows."

pydom["title#header-title"].html = title
pydom["a#page-title"].html = title
pydom["div#page-message"].html = page_message

# ✅ Your actual dataset
default_url = "https://raw.githubusercontent.com/RileyHan1518/weightlifting-dataset/main/weightlifting.csv"
pydom["input#txt-url"][0].value = default_url

# Logging
def log(message):
    print(message)
    console.log(message)

# CSV loading logic
def loadFromURL(event):
    try:
        pydom["div#pandas-output-inner"].html = ""

        url = pydom["input#txt-url"][0].value
        log(f"Fetching CSV from {url}")

        df = pd.read_csv(open_url(url))
        summary = pd.concat([df.head(5), df.tail(5)])

        pydom["div#pandas-output"].style["display"] = "block"
        pydom["div#pandas-dev-console"].style["display"] = "block"

        display(summary, target="pandas-output-inner", append=False)

    except Exception as e:
        log(f"Error: {e}")
        pydom["div#pandas-output-inner"].html = f"<pre style='color:red;'>Error: {e}</pre>"

# Connect button click to handler
@when("click", selector="#btn-load")
def handle_button_click(evt):
    loadFromURL(evt)
