from django.contrib import admin

from .models import CharacterClass, CharacterRace, Character

admin.site.register(Character)
admin.site.register(CharacterClass)
admin.site.register(CharacterRace)