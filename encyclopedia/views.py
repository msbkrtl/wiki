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
from django.core.files.storage import default_storage
import boto3
import markdown as md
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('wiki-msbkrtl')



# filepath = os.path.join(
#     "/mnt/c/Users/krtl/Desktop/Programming/cs502019/Python/web/wiki/entries",
#     filename,
# )
#
register = template.Library()


def index(request):
    # print(dir(my_bucket.objects.all()))
    # print(my_bucket.objects.all().all)
    # print(dir(default_storage))
    # print(dir(default_storage.path))
    # print(default_storage.path)

    # print(file.read())
    # print(s3)
    # print(
    #     os.path.join(
    #         "/mnt/c/Users/krtl/Desktop/Programming/cs502019/Python/web/wiki/entries",
    #         "a.md",
    #     )
    # )
    newList = []
    partial_List = []
    # pageList = util.list_entries()  # names of all entries
    pageList =[]
    for my_bucket_object in my_bucket.objects.all():
        pageList.append(str(my_bucket_object.key.split(".")[0]))
    query = str(request.GET.get("q"))
    if query != "None":
        if query != "":

            for i in range(len(pageList)):
                if query.lower() in pageList[i].lower():
                    if query.lower() == pageList[i].lower():
                        newList.append(pageList[i])
                    else:
                        partial_List.append(pageList[i])
            for i in range(len(newList)):
                newList[i] =  my_bucket.Object(f'{newList[i]}.md').get()["Body"].read()
                string = newList[0]

            if newList:
                return render(
                    request,
                    "encyclopedia/results.html",
                    {"entries": string, "query": query, "newList": newList},
                )
            else:
                if partial_List:
                    return render(
                        request,
                        "encyclopedia/partialmatch.html",
                        {"entries": partial_List, "query": query},
                    )
                else:
                    return render(
                        request,
                        "encyclopedia/results.html",
                        {"entries": partial_List, "query": query},
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
    if request.method == "POST":

        return redirect(reverse(edit, args=[title]))
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "title": title,
            "content":  my_bucket.Object(f'{title}.md').get()["Body"].read()
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
            file = my_bucket.Object(f'{title}.md').put(Body=f"#{title}\n{text}")

            return redirect(reverse(wiki, args=[title]))
    return render(request, "encyclopedia/newEntry.html", {"form": form})


# EDIT ENTRY THROUGH FORM


def edit(request, entry):
    query = str(request.GET.get("q"))
    if query != "None" and query != "":
        return redirect(reverse("index") + "?q=" + query)
    # print(dir(default_storage.open(f"{entry}.md")))
    # print(dir(default_storage.open(f"{entry}.md").read))
    # print(dir(my_bucket.Object(f'{entry}.md').get()["Body"].read()))
    test = my_bucket.Object(f'{entry}.md').get()["Body"].read().decode('utf-8')
    # file = default_storage.open(f"{entry}.md").read()
    with open("temp.txt","w+") as file:
        file.write(test)
        file.seek(0)
        # print(file.read())
        form = newEntryForm(
        initial={
            "entryName": file.readline().rstrip().strip("#"),
            "priority": file.read(),
        }
    )
    os.remove("temp.txt")
    # my_bucket.Object(f'{title}.md').put(Body=f"#{title}\n{text}")
    # print(test)
    # test = str(test)
    # print(type(str(test)))

    if request.method == "POST":
        form = newEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entryName".lstrip("#")]
            text = form.cleaned_data["priority"]
            entryList = util.list_entries()
            my_bucket.Object(f'{entry}.md').put(Body=f"#{entry}\n{text}")
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
    pageList =[]
    for my_bucket_object in my_bucket.objects.all():
        pageList.append(str(my_bucket_object.key.split(".")[0]))
    randm = random.randint(0, (len(pageList) - 1))
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
