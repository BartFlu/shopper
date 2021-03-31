from .models import Ingredient, Recipe, Category, Product
from django.contrib.auth.models import User
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
                Field('name', css_class='form-control'),
                Field('source', css_class='form-control'),
                Field('tags', css_class='form-control'),
                Fieldset('Dodaj składniki',
                Formset('ingredients'), css_class='form-control'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Zapisz')),
                )
            )


class FilterForm(forms.Form):

    Tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          queryset=Tag.objects.all())


ProductFormSet = forms.inlineformset_factory(Category, Product, fields=('name',), extra=1, can_delete=False)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Potwierdź hasło')
    username = forms.CharField(label='Nazwa użytkownika')
    email = forms.EmailField(label='Email')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')

