from .expression_core import *
from .operations import SmartDiv
import numpy as np


class SmartNumber(SmartExpression):
	def __init__(self, **kwargs):
		self.children = []
		super().__init__(**kwargs)

	def compute(self):
		return float(self)


class SmartInteger(SmartNumber):
	def __init__(self, n, **kwargs):
		self.n = n
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return str(self.n)

	def __float__(self):
		return float(self.n)
	
	def compute(self):
		return self.n

	def is_identical_to(self, other):
		return type(self) == type(other) and self.n == other.n

	def is_negative(self):
		return self.n < 0

	@staticmethod
	def GCF(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.gcd.reduce(nums)))

	@staticmethod
	def LCM(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.lcm.reduce(nums)))

	def prime_factorization(self):
		...


class SmartReal(SmartNumber):
	def __init__(self, x, symbol=None, **kwargs):
		self.x = x
		self.symbol = symbol
		super().__init__(**kwargs)

	@tex
	def __str__(self, decimal_places=4, use_decimal=False):
		if self.symbol and not use_decimal:
			return self.symbol
		rounded = round(self.x, decimal_places)
		if rounded == self.x:
			return str(rounded)
		else:
			return f"{self.x:.{decimal_places}f}" + r"\ldots"

	def __float__(self):
		return float(self.x)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.x == other.x

	def is_negative(self):
		return self.x < 0


class SmartRational(SmartDiv):
	# Better to subclass SmartDiv than SmartNumber because 5/3 is no more a number than 5^3 or 5+3
	# Multiclassing is an option but seems to be more trouble than it's worth
	def __init__(self, a, b, **kwargs):
		if not isinstance(a, (SmartInteger, int)):
			raise TypeError (f"Unsupported numerator type {type(a)}: {a}")
		if not isinstance(b, (SmartInteger, int)):
			raise TypeError (f"Unsupported denominator type {type(b)}: {b}")
		super().__init__(a, b, **kwargs)

	def simplify(self):
		pass #idk will make later
