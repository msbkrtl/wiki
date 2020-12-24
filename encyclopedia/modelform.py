from django import forms

from .models import Product


class product_form(forms.ModelForm):
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={"style": "height: 30px;width:500px; ", "placeholder": "Enry Title"}
        ),
        label="",
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "style": "height: 400px;width:800px;  display:block",
                "placeholder": "Write Your Entry Here",
            }
        ),
    )
    price = forms.DecimalField(
        label="",
    )

    class Meta:
        model = Product
        fields = ["title", "description", "price"]


# FORMS FORMS


class RawProductForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField()
    lo = forms.CharField()
