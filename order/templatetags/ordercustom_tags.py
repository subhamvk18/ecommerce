from django import template

register = template.Library()


#templatetags og placeorder.html

@register.filter(name='findvalue')
def findvalue(rdict,key):
    return rdict[key]


@register.filter(name='mul')
def findvalue(value,key):
    return value*key