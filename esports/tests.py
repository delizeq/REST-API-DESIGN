
from datetime import date, datetime, timezone

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Game, Team, Tournament, Match


class EsportsAPITests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create(
            name='Counter-Strike 2',
            description='Tactical shooter',
        )
        self.team1 = Team.objects.create(
            name='Team Alpha',
            country='UA',
        )
        self.team2 = Team.objects.create(
            name='Team Beta',
            country='PL',
        )
        self.tournament = Tournament.objects.create(
            name='Test Tournament',
            game=self.game,
            start_date=date(2026, 11, 1),
            end_date=date(2026, 11, 10),
            prize_pool=10000,
            status='upcoming',
        )
        self.match = Match.objects.create(
            tournament=self.tournament,
            team1=self.team1,
            team2=self.team2,
            start_time=datetime(2026, 11, 5, 15, 0, tzinfo=timezone.utc),
            format='bo3',
            status='upcoming',
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!',
        )

    def test_get_games(self):
        response = self.client.get('/games/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Counter-Strike 2')

    def test_create_game(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/games/',
            {'name': 'Dota 2', 'description': 'MOBA game'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Game.objects.filter(name='Dota 2').exists()
        )

    def test_search_games(self):
        Game.objects.create(name='Dota 2')

        response = self.client.get('/games/?search=dota')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Dota 2')

    def test_get_missing_game_returns_404(self):
        response = self.client.get('/games/99999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_teams(self):
        response = self.client.get('/teams/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_tournaments(self):
        response = self.client.get('/tournaments/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_matches(self):
        response = self.client.get('/matches/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_matches_by_team(self):
        response = self.client.get(
            f'/matches/?team={self.team1.id}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_create_match_with_same_team(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/matches/',
            {
                'tournament_id': self.tournament.id,
                'team1_id': self.team1.id,
                'team2_id': self.team1.id,
                'start_time': '2026-11-06T15:00:00Z',
                'format': 'bo3',
                'status': 'upcoming',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_delete_game_with_tournament(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f'/games/{self.game.id}/')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Game.objects.filter(id=self.game.id).exists())

    def test_cannot_create_game_without_authentication(self):
        response = self.client.post(
            '/games/',
            {'name': 'Unauthorized Game'},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_patch_game_with_authentication(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f'/games/{self.game.id}/',
            {'description': 'Updated description'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.game.refresh_from_db()
        self.assertEqual(self.game.description, 'Updated description')
        self.assertEqual(self.game.name, 'Counter-Strike 2')

    def test_patch_game_without_authentication(self):
        response = self.client.patch(
            f'/games/{self.game.id}/',
            {'description': 'Unauthorized change'},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.game.refresh_from_db()
        self.assertEqual(self.game.description, 'Tactical shooter')
