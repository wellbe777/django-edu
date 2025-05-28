from django import template
register = template.Library()
from courses.models import Category

@register.inclusion_tag('menu.html')
def cat_menu():
	obj = Category.objects.all() 
	return {'categoryitems': obj}
	


