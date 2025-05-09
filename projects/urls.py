from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/add/', views.AddView.as_view(), name='project_add'),
    path('projects/<int:pk>/', views.DetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', views.EditView.as_view(), name='project_edit'),
    path('projects/<int:pk>/remove/', views.RemoveView.as_view(), name='project_remove'),
    path('projects/<int:pk>/vote/', views.vote, name='project_vote'),

    path('members/add/', views.AddMemberView.as_view(), name='member_add'),
    path('members/<int:pk>/delete/', views.DeleteMemberView.as_view(), name='member_delete'),

    path('manager/', views.ManagerView.as_view(), name='manager'),
]
