from django import forms

class MessageForm(forms.Form):
    content = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Escribe tu mensaje..."})
    )