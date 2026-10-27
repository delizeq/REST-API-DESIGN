from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, Team, Tournament, Match
from .serializers import (GameSerializer, TeamSerializer,
                          TournamentSerializer, MatchSerializer)


class BaseListView(APIView):
    model = None
    serializer_class = None

    def filter_queryset(self, qs, params):
        return qs

    def get(self, request):
        qs = self.model.objects.all().order_by('id')
        try:
            qs = self.filter_queryset(qs, request.query_params)
        except (DjangoValidationError, ValueError):
            raise ValidationError('Некоректне значення в параметрах запиту.')
        return Response(self.serializer_class(qs, many=True).data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseDetailView(APIView):
    model = None
    serializer_class = None
    name = 'Об\'єкт'

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(f'{self.name} з id={pk} не знайдено.')

    def blocking_message(self, obj):
        """Якщо видаляти не можна, повертає текст причини. Інакше None."""
        return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(self.serializer_class(obj).data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        message = self.blocking_message(obj)
        if message:
            return Response({'error': message}, status=status.HTTP_409_CONFLICT)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Ігри ----------
class GameListView(BaseListView):
    model = Game
    serializer_class = GameSerializer

    def filter_queryset(self, qs, p):
        if p.get('search'):
            qs = qs.filter(name__icontains=p['search'])
        return qs


class GameDetailView(BaseDetailView):
    model = Game
    serializer_class = GameSerializer
    name = 'Гру'

    def blocking_message(self, obj):
        count = obj.tournaments.count()
        if count:
            return f'Неможливо видалити гру, оскільки за нею закріплено турнірів: {count}.'


# ---------- Команди ----------
class TeamListView(BaseListView):
    model = Team
    serializer_class = TeamSerializer

    def filter_queryset(self, qs, p):
        if p.get('search'):
            qs = qs.filter(name__icontains=p['search'])
        if p.get('country'):
            qs = qs.filter(country__iexact=p['country'])
        return qs


class TeamDetailView(BaseDetailView):
    model = Team
    serializer_class = TeamSerializer
    name = 'Команду'

    def blocking_message(self, obj):
        count = Match.objects.filter(Q(team1=obj) | Q(team2=obj)).count()
        if count:
            return f'Неможливо видалити команду, оскільки вона бере участь у матчах: {count}.'


# ---------- Турніри ----------
class TournamentListView(BaseListView):
    model = Tournament
    serializer_class = TournamentSerializer

    def filter_queryset(self, qs, p):
        if p.get('search'):
            qs = qs.filter(name__icontains=p['search'])
        if p.get('game'):
            qs = qs.filter(game_id=int(p['game']))
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        sorting = {
            'start_date_asc': 'start_date',
            'start_date_desc': '-start_date',
            'prize_desc': '-prize_pool',
        }
        if p.get('sort') in sorting:
            qs = qs.order_by(sorting[p['sort']])
        return qs


class TournamentDetailView(BaseDetailView):
    model = Tournament
    serializer_class = TournamentSerializer
    name = 'Турнір'

    def blocking_message(self, obj):
        count = obj.matches.count()
        if count:
            return f'Неможливо видалити турнір, оскільки в ньому є матчі: {count}.'


# ---------- Матчі ----------
class MatchListView(BaseListView):
    model = Match
    serializer_class = MatchSerializer

    def filter_queryset(self, qs, p):
        if p.get('date'):
            qs = qs.filter(start_time__date=p['date'])
        if p.get('from'):
            qs = qs.filter(start_time__date__gte=p['from'])
        if p.get('to'):
            qs = qs.filter(start_time__date__lte=p['to'])
        if p.get('tournament'):
            qs = qs.filter(tournament_id=int(p['tournament']))
        if p.get('team'):
            team_id = int(p['team'])
            qs = qs.filter(Q(team1_id=team_id) | Q(team2_id=team_id))
        if p.get('game'):
            qs = qs.filter(tournament__game_id=int(p['game']))
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        if p.get('sort') == 'date_asc':
            qs = qs.order_by('start_time')
        elif p.get('sort') == 'date_desc':
            qs = qs.order_by('-start_time')
        return qs


class MatchDetailView(BaseDetailView):
    model = Match
    serializer_class = MatchSerializer
    name = 'Матч'


# ---------- Вкладені адреси ----------
class GameTournamentsView(APIView):
    def get(self, request, pk):
        if not Game.objects.filter(pk=pk).exists():
            raise NotFound(f'Гру з id={pk} не знайдено.')
        qs = Tournament.objects.filter(game_id=pk).order_by('id')
        return Response(TournamentSerializer(qs, many=True).data)


class TournamentMatchesView(APIView):
    def get(self, request, pk):
        if not Tournament.objects.filter(pk=pk).exists():
            raise NotFound(f'Турнір з id={pk} не знайдено.')
        qs = Match.objects.filter(tournament_id=pk).order_by('start_time')
        return Response(MatchSerializer(qs, many=True).data)


class TeamMatchesView(APIView):
    def get(self, request, pk):
        if not Team.objects.filter(pk=pk).exists():
            raise NotFound(f'Команду з id={pk} не знайдено.')
        qs = Match.objects.filter(Q(team1_id=pk) | Q(team2_id=pk)).order_by('start_time')
        return Response(MatchSerializer(qs, many=True).data)