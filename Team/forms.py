from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'character_class', 'character_race', 'sex']
