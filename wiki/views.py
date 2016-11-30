from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from . import models


@login_required
def wiki_home(request, section_pk=None, subsection_pk=None):
    sections = sorted(models.Section.objects.all(),
        key=lambda section: section.title)

    subsections = []
    for section in sections:
        subsections.append(sorted(
            models.Subsection.objects.filter(section=section),
            key=lambda subsection: subsection.order
            ))
    subsections = [item for sublist in subsections for item in sublist]

    if section_pk:
        this_section = get_object_or_404(models.Section, pk=section_pk)
        this_subsections = sorted(models.Subsection.objects.filter(section=this_section),
        key=lambda subsection: subsection.order)
        if subsection_pk:
            this_subsection = get_object_or_404(models.Subsection, pk=subsection_pk)
        else:
            this_subsection = None

        if this_subsection:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'this_subsection': this_subsection, 'sections': sections, 'subsections': subsections})
        else:
            return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})
    else:
        this_section = None
        sections = sorted(models.Section.objects.all(),
            key=lambda section: section.title)
        if len(sections) > 0:
            this_section = sections[0]
        return render(request, 'wiki/home.html', {'this_section': this_section, 'sections': sections, 'subsections': subsections})