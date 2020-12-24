from django.shortcuts import render
from django import template
from . import util
from django.shortcuts import redirect, reverse
from django import forms
from django.forms import ModelForm, Textarea
from django.http import HttpResponse
from .models import Product
from .modelform import product_form
from .modelform import RawProductForm
import os.path, sys
import random
from markdown2 import Markdown

path_of_entries = os.path.join(os.getcwd(), "entries/")
# filepath = os.path.join(
#     "/mnt/c/Users/krtl/Desktop/Programming/cs502019/Python/web/wiki/entries",
#     filename,
# )
#
register = template.Library()


def index(request):
    # print(
    #     os.path.join(
    #         "/mnt/c/Users/krtl/Desktop/Programming/cs502019/Python/web/wiki/entries",
    #         "a.md",
    #     )
    # )
    newList = []
    partial_List = []
    pageList = util.list_entries()  # names of all entries
    query = str(request.GET.get("q"))
    if query != "None":
        if query != "":
            print("AAAA")
            for i in range(len(pageList)):
                if query.lower() in pageList[i].lower():
                    if query.lower() == pageList[i].lower():
                        newList.append(pageList[i])
                    else:
                        partial_List.append(pageList[i])
            for i in range(len(newList)):
                newList[i] = markdown(util.get_entry(newList[i]))
                string = newList[0]
            if newList:
                return render(
                    request,
                    "encyclopedia/results.html",
                    {"entries": string, "query": query, "newList": newList},
                )
            else:
                if pageList:
                    return render(
                        request,
                        "encyclopedia/partialmatch.html",
                        {"entries": partial_List, "query": query},
                    )
                else:
                    return render(
                        request,
                        "encyclopedia/index.html",
                        {"entries": pageList, "query": query},
                    )
    else:
        return render(
            request,
            "encyclopedia/index.html",
            {"entries": pageList, "query": query},
        )


def wiki(request, title):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    markdowner = Markdown()
    if request.method == "POST":
        print("AAAAAAAA")
        return redirect(reverse(edit, args=[title]))
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "title": title,
            "content": util.get_entry(title),
        },
    )


# NORMAL FORM
def new(request):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    form = newEntryForm()

    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entryName"]
            text = form.cleaned_data["priority"]
            entryList = util.list_entries()
            if title in entryList:
                return redirect(reverse(error, args=[title]))
            with open(path_of_entries + f"{title}.md", "a+") as file:
                file.write(f"#{title}\n{text}")
                print(file.read())
            return redirect(reverse(wiki, args=[title]))
    return render(request, "encyclopedia/newEntry.html", {"form": form})


# EDIT ENTRY THROUGH FORM


def edit(request, entry):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    with open(path_of_entries + f"{entry}.md", "a+") as file:
        file.seek(0)
        form = newEntryForm(
            initial={
                "entryName": file.readline().rstrip().strip("#"),
                "priority": file.read(),
            }
        )
    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entryName".lstrip("#")]
            text = form.cleaned_data["priority"]
            entryList = util.list_entries()
            with open(path_of_entries + f"{entry}.md", "w+") as file:
                file.write(f"#{entry}\n{text}")
                print(file.read())
            return redirect(reverse(wiki, args=[entry]))
    return render(request, "encyclopedia/edit.html", {"form": form})
    # path_of_entries = os.path.join(os.getcwd(), "entries/")
    # if request.method == "POST":
    #     form = newEntryForm(request.POST)
    #     if form.is_valid():
    #         title = form.cleaned_data["entryName"]
    #         text = form.cleaned_data["priority"]
    #         entryList = util.list_entries()
    #         if title in entryList:
    #             return redirect(reverse(error, args=[title]))
    #         with open(path_of_entries + f"{title}.md", "a+") as file:
    #             file.write(f"#{title}\n{text}")
    #             print(file.read())
    #         return redirect(reverse(wiki, args=[title]))
    return render(request, "encyclopedia/edit.html", {"form": form})


# DATABASE FORM
def randomPage(request):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    pageList = util.list_entries()
    print(len(pageList))
    randm = random.randint(0, (len(pageList) - 1))
    print(randm)
    return redirect("wiki/" + pageList[randm])
    # return redirect(reverse("wiki") + "?q=" + query)
    # if request.method == "POST":
    #     my_form = RawProductForm(request.POST)
    #     if my_form.is_valid():
    #         print(my_form.cleaned_data)
    #         print(my_form.cleaned_data["title"])
    #         Product.objects.create(**my_form.cleaned_data)
    #     else:
    #         print(my_form.errors)
    # return render(request, "encyclopedia/random.html")


def error(request, errorName=""):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    return render(request, "encyclopedia/error.html", {"error": errorName})


def learning(request, ids):
    # form = product_form()
    obj = Product.objects.get(id=ids)
    # print(getattr(obj, "description"))
    if request.method == "POST":
        obj.delete()
        return redirect("../")
    form = product_form(request.POST or None, instance=obj)
    context = {"obj": obj}
    if form.is_valid():
        form.save()
    return render(request, "encyclopedia/learning.html", context)


class newEntryForm(forms.Form):
    entryName = forms.CharField(
        widget=forms.Textarea(
            attrs={"style": "height: 30px;width:500px; ", "placeholder": "Enry Title"}
        ),
        label="",
    )
    priority = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "style": "height: 400px;width:800px;  display:block",
                "placeholder": "Write Your Entry Here",
            }
        ),
    )
