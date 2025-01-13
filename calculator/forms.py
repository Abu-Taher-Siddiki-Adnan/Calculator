from django import forms

class ExpressionForm(forms.Form):
    expression = forms.CharField(label='Infix Expression', max_length=100)
