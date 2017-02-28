from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from itertools import chain

from . import forms
from . import models

from items import models as item_models
from locations import models as location_models

import json


@login_required
def character_detail(request, character_pk=None):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    characters = sorted(models.Character.objects.filter(user=user),
        key=lambda character: character.name.lower()
        )
    if character_pk:
        this_character = get_object_or_404(models.Character, pk=character_pk)
        if this_character.user == request.user:
            return render(request, 'characters/character_detail.html', {'this_character': this_character, 'characters': characters})
        else:
            raise Http404
    elif len(characters) > 0:
        this_character = characters[0]
        if this_character.user == request.user:
            return render(request, 'characters/character_detail.html', {'this_character': this_character, 'characters': characters})
        else:
            raise Http404
    else:
        this_character = None
    return render(request, 'characters/character_detail.html', {'this_character': this_character, 'characters': characters})

@login_required
def character_create(request):
    characters_raw = models.Character.objects.filter(user=request.user).order_by('name')
    characters = {}
    for character in characters_raw:
        characters[character.pk] = character.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    worlds_raw = location_models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = location_models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    form = forms.CharacterForm()
    if request.method == 'POST':
        form = forms.CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            messages.add_message(request, messages.SUCCESS, "Character created!")
            return HttpResponseRedirect(character.get_absolute_url())
    return render(request, 'characters/character_form.html', {'form': form, 'characters': characters, 'items': items, 'worlds': worlds, 'locations': locations})

@login_required
def character_update(request, character_pk):
    characters_raw = models.Character.objects.filter(user=request.user).order_by('name')
    characters = {}
    for character in characters_raw:
        characters[character.pk] = character.name
    items_raw = item_models.Item.objects.filter(user=request.user).order_by('name')
    items = {}
    for item in items_raw:
        items[item.pk] = item.name
    worlds_raw = location_models.World.objects.filter(user=request.user).order_by('name')
    worlds = {}
    for world in worlds_raw:
        worlds[world.pk] = world.name
    locations_raw = location_models.Location.objects.filter(user=request.user).order_by('name')
    locations = {}
    for location in locations_raw:
        locations[location.pk] = location.name
    character = get_object_or_404(models.Character, pk=character_pk)
    if character.user == request.user:
        form = forms.CharacterForm(instance=character)
        if request.method == 'POST':
            form = forms.CharacterForm(instance=character, data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Updated character: {}".format(form.cleaned_data['name']))
                return HttpResponseRedirect(character.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/character_form.html', {'form': form, 'character': character, 'characters': characters, 'items': items, 'worlds': worlds, 'locations': locations})

@login_required
def character_delete(request, character_pk):
    character = get_object_or_404(models.Character, pk=character_pk)
    if character.user == request.user:
        form = forms.DeleteCharacterForm(instance=character)
        if request.method == 'POST':
            form = forms.DeleteCharacterForm(request.POST, instance=character)
            if character.user.pk == request.user.pk:
                character.delete()
                messages.add_message(request, messages.SUCCESS, "Character deleted!")
                return HttpResponseRedirect(reverse('characters:character_detail'))
    else:
        raise Http404
    return render(request, 'characters/character_delete.html', {'form': form, 'character': character})

@login_required
def character_copy(request, character_pk):
    character = get_object_or_404(models.Character, pk=character_pk)
    if character.user == request.user:
        form = forms.CopyCharacterForm(instance=character)
        if request.method == 'POST':
            form = forms.CopyCharacterForm(request.POST, instance=character)
            if character.user.pk == request.user.pk:
                character.pk = None
                character.name = character.name + "_Copy"
                character.save()
                messages.add_message(request, messages.SUCCESS, "Character Copied!")
                return HttpResponseRedirect(character.get_absolute_url())
    else:
        raise Http404
    return render(request, 'characters/character_copy.html', {'form': form, 'character': character})

@login_required
def character_import(request):
    user_import = None
    form = forms.ImportCharacterForm()
    if request.method == 'POST':
        if request.POST.get('user_import'):
            user_import = request.POST.get('user_import')
            user_import = json.loads(user_import, strict=False)
        else:
            return Http404
        form = forms.ImportCharacterForm(request.POST)
        if "characters" in user_import: 
            for character, character_attributes in user_import["characters"].items():
                new_character = models.Character(
                    user=request.user,
                    name=character,
                    alignment=character_attributes["alignment"],
                    size=character_attributes["size"],
                    languages=character_attributes["languages"],
                    strength=character_attributes["strength"],
                    dexterity=character_attributes["dexterity"],
                    constitution=character_attributes["constitution"],
                    intelligence=character_attributes["intelligence"],
                    wisdom=character_attributes["wisdom"],
                    charisma=character_attributes["charisma"],
                    armor_class=character_attributes["armor_class"],
                    hit_points=character_attributes["hit_points"],
                    speed=character_attributes["speed"],
                    saving_throws=character_attributes["saving_throws"],
                    skills=character_attributes["skills"],
                    creature_type=character_attributes["creature_type"],
                    damage_vulnerabilities=character_attributes["damage_vulnerabilities"],
                    damage_immunities=character_attributes["damage_immunities"],
                    damage_resistances=character_attributes["damage_resistances"],
                    condition_immunities=character_attributes["condition_immunities"],
                    senses=character_attributes["senses"],
                    challenge_rating=character_attributes["challenge_rating"],
                    traits=character_attributes["traits"],
                    actions=character_attributes["actions"],
                    notes=character_attributes["notes"],
                    character_class=character_attributes["character_class"],
                    age=character_attributes["age"],
                    height=character_attributes["height"],
                    weight=character_attributes["weight"],
                    proficiency_bonus = character_attributes["proficiency_bonus"],
                    race = character_attributes["race"],
                    xp = character_attributes["xp"],
                    background = character_attributes["background"],
                    initiative = character_attributes["initiative"],
                    personality = character_attributes["personality"],
                    bonds = character_attributes["bonds"],
                    ideals = character_attributes["ideals"],
                    flaws = character_attributes["flaws"],
                    feats = character_attributes["feats"],
                    attacks = character_attributes["attacks"],
                    spells = character_attributes["spells"],
                    proficiencies = character_attributes["proficiencies"],
                    equipment = character_attributes["equipment"],
                )
                new_character.save()
            return HttpResponseRedirect(reverse('characters:character_detail'))
    return render(request, 'characters/character_import.html', {'form': form, 'user_import': user_import})

@login_required
def character_export(request):
    user = None
    if request.user.is_authenticated():
        user = request.user.pk
    characters = sorted(models.Character.objects.filter(user=user),
        key=lambda character: character.name.lower()
        )
    if characters:
        for character in characters:
            character.traits = json.dumps(character.traits)
            character.actions = json.dumps(character.actions)
            character.notes = json.dumps(character.notes)
        return render(request, 'characters/character_export.html', {'characters': characters})
    else:
        raise Http404

@login_required
def character_srd(request):
    form = forms.SRDCharacterForm()
    characters = sorted(models.Character.objects.filter(user=3029),
        key=lambda character: character.name.lower()
        )
    if request.method == 'POST':
        form = forms.CharacterForm(request.POST)
        selected_characters = []
        for character_pk in request.POST.getlist('character'):
            character = models.Character.objects.get(pk=character_pk)
            selected_characters.append(character)
        empty_queryset = models.Character.objects.none()
        character_queryset = list(chain(empty_queryset, selected_characters))
        for character in character_queryset:
            character.traits = json.dumps(character.traits)
            character.actions = json.dumps(character.actions)
            character.notes = json.dumps(character.notes)
        return render(request, 'characters/character_export.html', {'characters': character_queryset})
    return render(request, 'characters/character_srd_form.html', {'form': form, 'characters': characters})

@login_required
def characters_delete(request):
    form = forms.DeleteCharacterForm()
    characters = sorted(models.Character.objects.filter(user=request.user),
        key=lambda character: character.name.lower()
        )
    if request.method == 'POST':
        form = forms.DeleteCharacterForm(request.POST)
        selected_characters = []
        for character_pk in request.POST.getlist('character'):
            character = models.Character.objects.get(pk=character_pk)
            selected_characters.append(character)
        empty_queryset = models.Character.objects.none()
        character_queryset = list(chain(empty_queryset, selected_characters))
        for character in character_queryset:
            character.delete()
        return HttpResponseRedirect(reverse('characters:character_detail'))
    return render(request, 'characters/characters_delete.html', {'form': form, 'characters': characters})