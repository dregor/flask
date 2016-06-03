from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms.widgets import CheckboxInput


class InputWithText(object):

	def __init__(self, input_type=None):
		if input_type is not None:
			self.input_type = input_type

	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		kwargs.setdefault('type', self.input_type)
		kwargs.setdefault('text', field.name)
		if 'value' not in kwargs:
			kwargs['value'] = field._value()
		return HTMLString('<input %s> %s' % (html_params(name=field.name, **kwargs), kwargs['text']))


class SubmitButtonWidget(object):

	def __init__(self, text='Button', glyph='glyphicon-ok'):
		self.text=text
		self.glyph=glyph


	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		kwargs.setdefault('text', self.text)
		kwargs.setdefault('type', 'submit')
		kwargs.setdefault('glyph', self.glyph)

		if kwargs['glyph'] != '' :
			glyphclass = html_params(class_='glyphicon ' + kwargs['glyph'])
		else:
			glyphclass = ''

		return HTMLString('<button %s> <span %s> %s </span> </button>' % (html_params(name=field.name, **kwargs), glyphclass, kwargs['text']))


class ChekBoxTextWidget(InputWithText):
	input_type='checkbox'

	def __call__(self, field, **kwargs):
		if getattr(field, 'checked', field.data):
			kwargs['checked'] = True
		return super(ChekBoxTextWidget, self).__call__(field, **kwargs)