class QWidget:
	pass

class QApplication(object):
	def __init__(self, *k, **kw):
		print("False init...")
	@classmethod
	def instance(self):
		return 1


class QFontDatabase(object):
	@classmethod
	def addApplicationFont(a, b):
		return [1, 2]

	@classmethod
	def applicationFontFamilies(a, b):
		return [1, 2]
