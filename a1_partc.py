#    Main Author(s): Le Chanh Tin Luong
#    Main Reviewer(s): Di Liu, Techatat Obun 

"""
Stack class implements a LIFO data structure using an array structure (a python list).
The latest item gets removed first.
It keep tracks of the top position, which is an index tracking next available position
"""
class Stack:

	# create a stack with array structure with a max capacity
	def __init__(self, cap = 10):
		self.data_stack = [None] * cap
		self.cap = cap
		self.top = 0

	# return the capacity of the stack
	def capacity(self):
		return self.cap

	# This function receives 1 element and adds it to the top
	# If the stack is full, doubling the capacity and adding the element
	# returns nothing
	def push(self, data):
		if self.top == self.cap: 
			self.cap *= 2
			new_arr = [None] * self.cap 

			for i in range(self.top):
				new_arr[i] = self.data_stack[i]

			self.data_stack = new_arr
		
		self.data_stack[self.top] = data
		self.top += 1

	# This functiontion removes 1 element at the top, and returns it
	# If empty stack, it reports error
	def pop(self):
		if self.top <= 0:
			raise IndexError('pop() used on empty stack')
		self.top -= 1
		return self.data_stack[self.top]

	# This function returns the element at the top, without removing it 
	# If empty stack, it returns None
	def get_top(self):
		if self.top == 0:
			return None
		return self.data_stack[self.top - 1]

	# This function returns true if the stack is empty
	def is_empty(self):
		if self.top == 0:
			return True
		return False

	# This function returns the number of elements in the stack
	def __len__(self):
		return self.top

"""
Queue class implements a FIFO data structure using an array structure (a python list).
The oldest item gets removed first.
It keep tracks of the front and back position, which are indices tracking the first element and the next available position.
"""
class Queue:

	# create a queue with array structure with a max capacity
	def __init__(self, cap = 10):
		self.data_queue = [None] * cap
		self.cap = cap
		self.front = 0
		self.back = 0
		self.size = 0

	# return the capacity of the queue
	def capacity(self):
		return self.cap

	# This function receives 1 element and adds it to the back
	# If the queue is full, doubling the capacity and adding the element to the back
	# Back moves to the NEXT available position
	# returns nothing
	def enqueue(self, data):
		# If the data array is full, resize by creating a new array with double capacity
		if self.size == self.cap:
			new_cap = self.cap * 2
			new_arr = [None] * new_cap

			# copy elements of the queue from the front to the start of the new array 
			for i in range(self.size):
				curr = (self.front + i) % self.cap
				new_arr[i] = self.data_queue[curr]
			self.cap = new_cap
			self.data_queue = new_arr

			# reset front and back
			self.front = 0
			self.back = self.size

		# add the new element to the back of the queue
		self.data_queue[self.back] = data
		self.back = (self.back +1) % self.cap
		self.size += 1

	# This function removes 1 element at the front, and returns it
	# If empty queue, it reports error
	# Front moves to the NEXT element
	def dequeue(self):
		if self.size == 0:
			raise IndexError('dequeue() used on empty queue')
		
		self.size -= 1
		curr = self.front
		self.front = (self.front + 1) % self.cap
		return self.data_queue[curr]
		
	# This function returns the element at the front, without removing it
	# If empty queue, it returns None
	def get_front(self):
		if self.size == 0:
			return None
		return self.data_queue[self.front]

	# This function checks if the queue is empty
	def is_empty(self):
		if self.size == 0:
			return True
		return False

	# This function returns the number of elements in the queue
	def __len__(self):
		return self.size


"""
Deque class implements a double ended queue data structure using an array structure (a python list).
It keep tracks of the front and back position, which are indices tracking the first element and the next available position.
This class allows adding and removing elements from both ends
"""
class Deque:

	# create a deque with array structure with a max capacity 
	def __init__(self, cap = 10):
		self.data_deque = [None] * cap
		self.cap = cap
		self.front = 0
		self.back = 0
		self.size = 0

	# This function return the capacity of the deque
	def capacity(self):
		return self.cap

	# This function receives 1 element and adds it to the FRONT.
	# If the deque is full, doubling the capacity and adding the element to the front
	# Front moves to the PREVIOUS available position.
	# If empty deque, use push_back to add the element.
	# returns nothing
	def push_front(self, data):		
		# If the data array is full, resize by creating a new array with double capacity
		if self.size == self.cap:
			new_cap = self.cap * 2
			new_arr = [None] * new_cap

			# put elements from the deque from the front to the start of the new array 
			for i in range(self.size):
				curr = (self.front + i) % self.cap
				new_arr[i] = self.data_deque[curr]
			self.cap = new_cap

			self.data_deque = new_arr
			# reset front and back
			self.front = 0
			self.back = self.size
		
		# If empty deque, use push_back to add the element to the back.
		if self.is_empty():
			self.push_back(data)

		# If not empty, move the front to the previous position and add the element to the front
		else:
			self.front = (self.front - 1) % self.cap
			self.data_deque[self.front] = data
			self.size += 1

	# This function receives 1 element and adds it to the back.
	# If the deque is full, doubling the capacity and adding the element to the back
	# Back moves to the NEXT available position
	# returns nothing
	def push_back(self, data):
		# If the data array is full, resize by creating a new array with double capacity
		if self.size == self.cap:
			new_cap = self.cap * 2
			new_arr = [None] * new_cap

			# put elements from the deque from the front to the start of the new array 
			for i in range(self.size):
				curr = (self.front + i) % self.cap
				new_arr[i] = self.data_deque[curr]
			self.cap = new_cap

			self.data_deque = new_arr
			# reset front and back
			self.front = 0
			self.back = self.size

		self.data_deque[self.back] = data
		self.back = (self.back + 1) % self.cap
		self.size += 1

	# This function removes 1 element at the front, and returns it
	# If empty deque, it reports error
	# Front moves to the NEXT element
	def pop_front(self):
		if self.size == 0:
			raise IndexError('pop_front() used on empty deque')
		
		self.size -= 1
		curr = self.front
		self.front = (self.front + 1) % self.cap
		return self.data_deque[curr]

	# This function removes 1 element at the back, and returns it
	# If empty deque, it reports error
	# Back moves to  the PREVIOUS element
	def pop_back(self):
		if self.size == 0:
			raise IndexError('pop_back() used on empty deque')
		
		self.size -= 1
		self.back = (self.back - 1) % self.cap
		return self.data_deque[self.back]

	# This function returns the element at the front, without removing it
	# If empty deque, it returns None
	def get_front(self):
		if self.size == 0:
			return None
		return self.data_deque[self.front]

	# This function returns the element at the back, without removing it
	# If empty deque, it returns None
	def get_back(self):
		if self.size == 0:
			return None
		return self.data_deque[self.back - 1]

	# This function returns true if the deque is empty
	def is_empty(self):
		if self.size == 0:
			return True
		return False

	# This function returns the number of elements in the deque
	def __len__(self):
		return self.size

	# This function returns the element at k'th position starting from the front, without removing it
	# If out of range, it reports error 
	def __getitem__(self, k): 
		if k >= self.size or k < 0:
			raise IndexError('Index out of range')
		return self.data_deque[(self.front + k) % self.cap]
