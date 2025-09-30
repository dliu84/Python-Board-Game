# Credit for A3 partA
# Main Author(s): Le Chanh Tin Luong
# Main Reviewer(s): Di Liu, Techatat Obun

# Credit for A1
# Main Author(s): Techatat Obun
# Main Reviewer(s): Di Liu, Le Chanh Tin Luong
import copy

from a1_partc import Queue


"""
	This function receives a 2D array ( grid of numbers ) and will loop through to look for any overflow cells.
	It returns a list of tuples (row, col) of the overflow cells.
	If there is no overflow will return None
"""
def get_overflow_list(grid):

	overflow_cell = []
	row_len = len(grid)
	column_len = len(grid[0])

	# Check how many neighbors each cell have and then compare if the value of the cell is equal to or greater than the number of neighbors
	for i in range(row_len):
		for j in range(column_len):

			# Check if the current cell is at the corner of the gird if yes it should be only 2 neighbors
			if ((i == 0 and j == 0) or  # top left corner
					(i == 0 and j == column_len - 1) or  # top right corner
					(i == row_len - 1 and j == 0) or  # bottom left corner
					(i == row_len - 1 and j == column_len - 1)):  # bottom right corner;
				if abs(grid[i][j]) >= 2:
					overflow_cell.append((i, j))

			# Check if the current cell is at the edge of the grid if yes it should be only 3 neighbors
			elif i == 0 or i == row_len - 1 or j == 0 or j == column_len - 1:
				if abs(grid[i][j]) >= 3:
					overflow_cell.append((i, j))

			# This one is for cell that has 4 neighbors
			else:
				if abs(grid[i][j]) >= 4:
					overflow_cell.append((i, j))
	return overflow_cell if overflow_cell else None


"""
	This function receives a 2D array (grid of numbers and a queue class ( from part c)
	It will check the grid if there are any overflow cells. if yes, it will create a
	new grid following these rules:
	- any cell that is overflowing becomes empty (assigned 0)
	- every neighbor of an overflowing cell gets one extra item
	- every neighbor of an overflowing cell takes on the same sign as the overflowing cell
	- all overflowing cells overflow at the same time to form the next grid
	Then it will push the new grid into a queue. It will keep forming a new grid until
	there is no overflow cell.
	It returns the number of times that a new grid was created. 
 	If no new grid is created, return zero.
  	If all the values of every square in the grid have the same sign, return 1.
"""
def overflow(grid, a_queue):

	overflow_list = get_overflow_list(grid)
	overflow_dict_list = []

	# Store all the information of the overflow cell, so we can use the sign to take over its neighbors later
	if overflow_list:
		for i in range(len(overflow_list)):
			index_i = overflow_list[i][0]
			index_j = overflow_list[i][1]
			cell_sign = -1 if grid[index_i][index_j] < 0 else 1
			overflow_dict = {
				'i': index_i,
				'j': index_j,
				'sign': cell_sign
			}
			overflow_dict_list.append(overflow_dict)
			# overflow cell becomes zero - this needs to be done before adding one to the neighbors
			grid[index_i][index_j] = 0
		row_len = len(grid) # to be used to get the cell index
		column_len = len(grid[0])

		# Define the directions for the neighbors
		# (0, 1) = right, (1, 0) = down, (0, -1) = left, (-1, 0) = up
		directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

		# Loop through the overflow_dict_list to get the index of the overflow cell to take over its neighbors
		for overflow_dict in overflow_dict_list:
			i = overflow_dict['i']
			j = overflow_dict['j']
			sign = overflow_dict['sign']

			# Loop through the directions to get the index of the neighbors
			for direction_i, direction_j in directions:
				# Get the index of the neighbor
				neighbor_i, neighbor_j = i + direction_i, j + direction_j
				# Check if the neighbor is inside the grid
				if 0 <= neighbor_i < row_len and 0 <= neighbor_j < column_len:
					grid[neighbor_i][neighbor_j] = (abs(grid[neighbor_i][neighbor_j]) + 1) * sign

		# If the values of every square has the same sign(including zero for both), the overflow() function adds the board to the queue and returns 1.
		if all(grid[i][j] >= 0 for i in range(len(grid)) for j in range(len(grid[0]))) or all(grid[i][j] <= 0 for i in range(len(grid)) for j in range(len(grid[0]))):
			# use deepcopy() so that the original gird won't be reflected
			a_queue.enqueue(copy.deepcopy(grid))
			return 1
		# If the values of every square does not have the same sign, the overflow() function adds the board to the queue and returns 1 plus the result of calling overflow() on the board.	
		else:
			a_queue.enqueue(copy.deepcopy(grid))
		
		return 1 + overflow(grid, a_queue)
	else:
		# Base case; if there are no more overflow cells return zero
		return 0

