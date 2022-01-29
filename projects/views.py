from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from projects.datatables import ProjectSerializer
from projects.forms import ProjectFrom
from projects.models import Project, Technology
from rest_framework import viewsets

# Create your views here.

class ProjectDatatable(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
def index(request):
    return render(request, 'pages/projects/index.html')

def create(request):
    form = ProjectFrom()
    exception = ""
    if request.method == "POST":
        form = ProjectFrom(request.POST or None)
        if form.is_valid():
            try:
                form.save(commit=False)
                project = Project.objects.create(
                    name = request.POST.get('name'),
                    overview_document = request.POST.get('overview_document'),
                    ssh_details = request.POST.get('ssh_details'),
                    cpanel_details = request.POST.get('cpanel_details'),
                    ftp_details = request.POST.get('ftp_details'),
                    key_link_url = request.POST.get('key_link_url'),
                )
                for technology in request.POST.getlist('technologies'):
                    result = Technology.objects.filter(name=technology)
                    if not result.exists():
                        result = Technology.objects.create(name=technology)
                        project.technologies.add(result)
                    else:
                        project.technologies.add(result.first().id)
                return redirect('/webpanel/projects')
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))            
    return render(request, 'pages/projects/form.html', {'form': form, 'error': exception})

def edit(request, id):
    id = int(id)
    exception = ""
    try:
        project = Project.objects.get(id=id)
        technologies = project.technologies.all().values_list('name',flat=True)
    except Project.DoesNotExist:
        return redirect('/webpanel/projects')
    form = ProjectFrom(request.POST or None, instance=project,initial = {"technologies":list(technologies)})
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save(commit=False)
                Project.objects.filter(id=id).update(
                    name = request.POST.get('name'),
                    overview_document = request.POST.get('overview_document'),
                    ssh_details = request.POST.get('ssh_details'),
                    cpanel_details = request.POST.get('cpanel_details'),
                    ftp_details = request.POST.get('ftp_details'),
                    key_link_url = request.POST.get('key_link_url'),
                )
                for technology in request.POST.getlist('technologies'):
                    result = Technology.objects.filter(name=technology)
                    if not result.exists():
                        result = Technology.objects.create(name=technology)
                        project.technologies.add(result)
                    else:
                        project.technologies.add(result.first().id)
                return redirect('/webpanel/projects')
            except Exception as error:
                exception = ValueError('Caught this error: ' + repr(error))  
    return render(request, 'pages/projects/form.html', {'form': form, 'error': exception})

def delete(request):
    return HttpResponse("Project delete");