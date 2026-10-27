from rest_framework import serializers
from .models import Game, Team, Tournament, Match


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'description']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country', 'description']


class TournamentSerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(source='game', queryset=Game.objects.all())

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'game_id', 'start_date', 'end_date', 'prize_pool', 'status']

    def validate(self, data):
        start = data.get('start_date', getattr(self.instance, 'start_date', None))
        end = data.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end and end < start:
            raise serializers.ValidationError('Дата завершення не може бути раніше за дату початку.')
        return data


class MatchSerializer(serializers.ModelSerializer):
    tournament_id = serializers.PrimaryKeyRelatedField(source='tournament', queryset=Tournament.objects.all())
    team1_id = serializers.PrimaryKeyRelatedField(source='team1', queryset=Team.objects.all())
    team2_id = serializers.PrimaryKeyRelatedField(source='team2', queryset=Team.objects.all())

    class Meta:
        model = Match
        fields = ['id', 'tournament_id', 'team1_id', 'team2_id',
                  'start_time', 'format', 'score', 'status']

    def validate(self, data):
        team1 = data.get('team1', getattr(self.instance, 'team1', None))
        team2 = data.get('team2', getattr(self.instance, 'team2', None))
        if team1 and team2 and team1 == team2:
            raise serializers.ValidationError('Команда не може грати сама з собою.')
        return data