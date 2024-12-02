from django.test import TestCase
from api.models import Person, Team
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status



class PersonTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Team A", country="PL")
        self.person = Person.objects.create(
            name="Jan Kowalski", 
            shirt_size="M", 
            month_added=1, 
            team=self.team
        )

    def test_person_creation(self):
        self.assertEqual(self.person.name, "Jan Kowalski")
        self.assertEqual(self.person.shirt_size, "M")
        self.assertEqual(self.person.team.name, "Team A")

    def test_person_invalid_name(self):
        with self.assertRaises(ValidationError):
            self.person.name = "123"
            self.person.clean()

class ModelIdTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Team B", country="PL")
        self.person = Person.objects.create(
            name="Anna Nowak", 
            shirt_size="L", 
            month_added=3, 
            team=self.team
        )

    def test_person_id(self):
        self.assertIsInstance(self.person.id, int)
        self.assertTrue(self.person.id > 0)

    def test_team_id(self):
        self.assertIsInstance(self.team.id, int)
        self.assertTrue(self.team.id > 0)

class ViewTestCase(TestCase):
    def test_view_status_code(self):
        response = self.client.get(reverse('PersonView'))
        self.assertEqual(response.status_code, 200)

class PersonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token = Token.objects.create(user=self.user)
        self.person_data = {"name": "Marek Nowak", "shirt_size": "S", "month_added": 5}
        
    def test_create_person(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/api/person/', self.person_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)