from django import template

register = template.Library()

@register.filter
def star_rating(rating):
    filled_stars = int(rating)
    empty_stars = 5 - filled_stars
    return {'filled_stars': filled_stars, 'empty_stars': empty_stars}


