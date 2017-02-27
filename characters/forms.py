from django import forms

from . import models


class TinyMCEForm(forms.ModelForm):
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            )


class CharacterForm(TinyMCEForm):
    class Meta:
        model = models.Character
        fields = [
            'name',
            'alignment',
            'size',
            'languages',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
            'armor_class',
            'hit_points',
            'speed',
            'saving_throws',
            'skills',
            'creature_type',
            'damage_vulnerabilities',
            'damage_immunities',
            'damage_resistances',
            'condition_immunities',
            'senses',
            'challenge_rating',
            'traits',
            'actions',
            'notes',
            'character_class',
            'age',
            'height',
            'weight',
            'level',
            'xp',
            'race',
            'background',
            'initiative',
            'speed',
            'proficiency_bonus',
            'languages',
            'personality',
            'ideals',
            'bonds',
            'flaws',
            'feats',
            'attacks',
            'spells',
            'proficiencies',
            'equipment',
        ]


class DeleteCharacterForm(forms.ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']


class CopyCharacterForm(forms.ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']


class ImportCharacterForm(forms.ModelForm):
    class Meta:
        model = models.Character
        fields = [
            'name',
        ]


class SRDMonsterForm(forms.ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']


class SRDNPCForm(forms.ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']


CharacterFormSet = forms.modelformset_factory(
    models.Character,
    form=CharacterForm,
    extra=0,
)
