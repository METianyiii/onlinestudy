from django.template import Library
register = Library()


@register.filter
def iSin(arg1, arg2):
	return arg1[arg2]


@register.filter
def isStr(arg1, arg2):
	if '分数' in arg1[arg2]:
		return arg1[arg2]


@register.filter
def getAnswerID(arg1, arg2):
	return arg1[arg2]

