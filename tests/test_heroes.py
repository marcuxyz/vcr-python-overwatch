from unittest import TestCase
from requests import Session
from betamax  import Betamax
from bs4      import BeautifulSoup


with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassetes'


class TestHeroes(TestCase):
    def setUp(self):
        self.session = Session()

    def test_must_returns_heroes(self):
        with Betamax(self.session) as vcr:
            vcr.use_cassette('heroes_cassette')
            response = self.session.get('https://playoverwatch.com/pt-br/heroes/')

            html = BeautifulSoup(response.text, 'html.parser')
            heroes = html.select('.hero-portrait-detailed-container span.portrait-title')
            names = [hero.text for hero in heroes]

            self.assertEqual(len(heroes), 32)
            self.assertIn('Moira', names)
            self.assertIn('D.Va', names)
            self.assertIn('Genji', names)
