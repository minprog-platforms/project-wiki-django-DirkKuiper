import markdown2
from django.shortcuts import render
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="content", widget = forms.Textarea)


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

def new_page(request):
    # Checks if user submitted a form on the page
    if request.method == "POST":
        
        # Fetches the form
        form = NewEntryForm(request.POST)

        # If form is valid, takes data from form and saves it
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Checks if entry is already present in list with all entries
            if title in util.list_entries():
                # In case entry already exists, returns the same page, but with an error message that tells the user entry already exists
                return render(request, "encyclopedia/new_page.html", {
                    "form": NewEntryForm(),
                    "error": "Error! This entry already exists, please try again!"
                })

            else:
                # Saves the entry
                util.save_entry(title, content)
                # Renders newly created page
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown2.markdown(util.get_entry(title)),
                    "title": title
                    })
    else:
        return render(request, "encyclopedia/new_page.html", {
                    "form": NewEntryForm()
                })
