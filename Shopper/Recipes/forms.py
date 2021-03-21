from .models import Ingredient, Recipe
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from .models import Tag


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        exclude = ()


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, fields=['type', 'quantity', 'unit'], extra=1, can_delete=True)


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'source', 'tags']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True

        self.helper.label_class = 'create-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('source'),
                Field('tags'),
                Fieldset('Dodaj składniki',
                Formset('ingredients')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Zapisz')),
                )
            )


class FilterForm(forms.Form):

    Tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          queryset=Tag.objects.all())
