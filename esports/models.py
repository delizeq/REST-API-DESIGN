from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=2, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished'),
    ]

    name = models.CharField(max_length=150)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='tournaments')
    start_date = models.DateField()
    end_date = models.DateField()
    prize_pool = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    # TODO: додати created_by, коли буде авторизація

    def __str__(self):
        return self.name


class Match(models.Model):
    FORMAT_CHOICES = [('bo1', 'bo1'), ('bo3', 'bo3'), ('bo5', 'bo5')]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT, related_name='matches')
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='matches_as_team2')
    start_time = models.DateTimeField()
    format = models.CharField(max_length=3, choices=FORMAT_CHOICES, default='bo3')
    score = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        return f'{self.team1} vs {self.team2}'
