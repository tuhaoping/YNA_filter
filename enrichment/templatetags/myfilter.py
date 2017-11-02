from django.template.defaulttags import register

@register.filter
def now_type(count):
	tlist = ['Enriched in Promoter', 'deprise in Promoter', 'Enriched in Coding Region', 'deprise in Coding Region', ]
	return tlist[count]

