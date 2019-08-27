import time
import random

def random_list(length):
	ret_list = []
	for _ in range(length):
		ret_list.append(random.randint(0, length*10))
	return ret_list

class AlgTimeCalc:
	def __init__(self, attempts = 10):
		self.__attempts = attempts if attempts > 1 else 1
		self.timings = []
		self.__context_start = None	

	def __call__(self, func):
		def wrapper(*args, **kwargs):
			self.timings = []			
			output = None
			for _ in range(self.__attempts):
				start = time.time()
				output = func(*args, **kwargs)
				end = time.time()
				self.timings.append(end-start)
				print("... %d/%d <%s::func> computed for %.5fs." % (_+1, self.__attempts, func.__name__, end-start))
			print("Average computing time is %.5fs for %d attempts." % (  sum(self.timings)/self.__attempts,  self.__attempts))
			return output
		return wrapper


	def __enter__(self):
		self.__context_start = time.time()
		return self
	def __exit__(self, *args):
		print("Total computing time is %.5f." % (time.time()-self.__context_start) )


@AlgTimeCalc(attempts = 5) #вызов dummy будет проверяться на время пять раз -- через __call__
def dummy():
	random_list(200000)

with AlgTimeCalc():	# Выведет Total computing time -- контекст
	dummy() # Выведет Average computing time -- через декоратор, описанный в методе __call__

AlgTimeCalc(attempts = 2)(dummy)() # Дважды вызовет функцию с декоратором, а потом укажет время этого двойного выполнения.