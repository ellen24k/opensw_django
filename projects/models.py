from django.db import models


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return f'{self.project_id}, {self.project_name}, {self.description}, {self.members}'

    def average_vote(self):
        votes = self.vote_set.all()
        if votes.count() > 0:
            total = sum(vote.vote for vote in votes)
            return total / votes.count()
        return None


class Vote(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE)
    vote = models.IntegerField(
        # 1~5 투표 가능
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def __str__(self):
        return f'Project: {self.project.project_name}, Vote: {self.vote}'
