import markdown2
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, page):
    return render(request, "encyclopedia/entry.html", {
        # Converts markdown to html
        "entry": markdown2.markdown(util.get_entry(page)),
        "title": page
    })

