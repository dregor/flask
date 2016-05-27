from wtforms.widgets.core import HTMLString, html_params, escape
from wtforms.widgets import CheckboxInput


class InputWithText(object):
	html_params = staticmethod(html_params)

	def __init__(self, input_type=None):
		if input_type is not None:
			self.input_type = input_type

	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		kwargs.setdefault('type', self.input_type)
		kwargs.setdefault('text', field.name)
		if 'value' not in kwargs:
			kwargs['value'] = field._value()
		return HTMLString('<input %s> %s' % (self.html_params(name=field.name, **kwargs), kwargs['text']))


class ChekBoxTextWidget(InputWithText):
	input_type='checkbox'

	def __call__(self, field, **kwargs):
		if getattr(field, 'checked', field.data):
			kwargs['checked'] = True
		return super(ChekBoxTextWidget, self).__call__(field, **kwargs)