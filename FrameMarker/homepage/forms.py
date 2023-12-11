from django import forms

# Upload form
class UploadForm(forms.Form):
    file = forms.FileField()