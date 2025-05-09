from django.contrib import admin
from .models import Project, Member, Vote


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'average_vote') 

    @admin.display(description='Average Vote')
    def average_vote(self, obj):
        avg = obj.average_vote()
        if avg is None:
            return 'No Votes Yet' 
        return round(avg, 2) 


class VoteAdmin(admin.ModelAdmin):
    list_display = ('project', 'vote') 


admin.site.register(Project, ProjectAdmin)
admin.site.register(Member)
admin.site.register(Vote, VoteAdmin)
