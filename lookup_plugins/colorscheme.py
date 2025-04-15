from colorscheme_generator import generate_full_palette

class LookupModule(object):
    def run(self, terms, variables=None, **kwargs):
        base_color = terms[0]
        count = kwargs.get('count', 100)
        shades = kwargs.get('shades', True)

        return [generate_full_palette(base_color, count=count, shades=shades)]