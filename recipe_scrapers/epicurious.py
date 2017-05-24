from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class Epicurious(AbstractScraper):

    @classmethod
    def host(self):
        return 'epicurious.com'

    def title(self):
        return self.soup.find('h1', {'itemprop': 'name'}).get_text()

    def total_time(self):
        return get_minutes(self.soup.find('dd', {'class': 'total-time'}))

    def ingredients(self):
        ingredients_html = self.soup.findAll('li', {'itemprop': "ingredients"})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
        ]

    def instructions(self):
        instructions_html = []
        for g in self.soup.find_all('li', {'class': 'preparation-group'}):
            instructions_html.extend(g.find_all('li', {'class': 'preparation-step'}))

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])
