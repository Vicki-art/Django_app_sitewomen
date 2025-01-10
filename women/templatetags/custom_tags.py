from django import template
from women.models import Category, TagPost
from django.db.models import Count
from women.utils import menu


register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('women/categories_list.html')
def show_cats(cat_selected=0):
    categories = Category.objects.annotate(total=Count('women')).filter(total__gt=0)
    return {'categories': categories, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags(cat_selected=0):
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}
