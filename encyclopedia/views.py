import markdown2
from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, page):
    # Checks if the page is there, if not displays error
    if util.get_entry(page) == None:
        return render(request, "encyclopedia/error.html")

    else:
        # Shows page
        return render(request, "encyclopedia/entry.html", {
        # Converts markdown to html
        "entry": markdown2.markdown(util.get_entry(page)),
        "title": page
    })

def search(request):
    results = []

    entries = util.list_entries()
    # Gets user search input from form 
    query = request.GET.get('q')

    
    for entry in entries:
        # Checks if search is the exact same as one of the entries
        if query == entry:
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown2.markdown(util.get_entry(query)),
                "title": query
            })
        # If not checks if the search is a part of each of the entries
        if query.lower() in entry.lower():
            results.append(entry)
    # Returns search page with all the results
    return render(request, "encyclopedia/search.html", {
        "results": results
    })