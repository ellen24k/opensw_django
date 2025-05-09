from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView

from .models import *


class IndexView(generic.ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'project_list'


class ProjectListView(generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'project_list'


class DetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


class ManagerView(generic.ListView):
    template_name = 'projects/admin_manager.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        projects = list(Project.objects.all())

        for project in projects:
            project.avg_vote = project.average_vote() or 0
            project.vote_count = project.vote_set.count()

        projects.sort(key=lambda x: x.avg_vote, reverse=True)

        for idx, project in enumerate(projects, start=1):
            project.rank = idx

        return projects


class AddView(generic.CreateView):
    model = Project
    fields = ['project_name', 'description', 'members']
    template_name = 'projects/admin_project_add.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project:manager')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_members'] = Member.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.set(self.request.POST.getlist('members'))
        return response


class EditView(generic.UpdateView):
    model = Project
    fields = ['project_name', 'description', 'members']
    template_name = 'projects/admin_project_edit.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project:manager')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_members'] = Member.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.set(self.request.POST.getlist('members'))
        return response


class RemoveView(generic.DeleteView):
    model = Project
    template_name = 'projects/admin_project_remove.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project:manager')


@require_POST
def vote(request, pk):
    project = get_object_or_404(Project, pk=pk)
    vote_value = request.POST.get('vote')

    if not vote_value or not vote_value.isdigit() or int(vote_value) not in range(1, 6):
        return JsonResponse({'error': 'Invalid vote'}, status=400)

    Vote.objects.create(project=project, vote=int(vote_value))
    return JsonResponse({'message': 'Vote recorded successfully'})


class AddMemberForm(forms.Form):
    name = forms.CharField(max_length=10, label='Member Name')

    def save(self):
        name = self.cleaned_data['name']
        member, created = Member.objects.get_or_create(name=name)
        return member

class AddMemberView(FormView):
    template_name = 'projects/admin_member_add.html'
    form_class = AddMemberForm
    success_url = reverse_lazy('project:member_add')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_members'] = Member.objects.all()
        return context


class DeleteMemberView(generic.View):
    def post(self, requests, pk):
        member = get_object_or_404(Member, pk=pk)
        member.delete()
        return HttpResponseRedirect(reverse_lazy('project:member_add'))
