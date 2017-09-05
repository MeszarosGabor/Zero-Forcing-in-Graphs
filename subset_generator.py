def generate_given_sized_subsets(base_arr, subset_size):
	n = len(base_arr)
	k = subset_size
	if k <= 0 or k > n:
		return []
	if k == 1:
		return [[x] for x in base_arr]
	else:
		picked_element = base_arr[-1]
		smaller_sol_wo_picked = generate_given_sized_subsets(base_arr[0:-1],k)
		smaller_sol_w_picked = generate_given_sized_subsets(base_arr[0:-1],k-1)
		for x in smaller_sol_w_picked:
			x.append(picked_element)
		return smaller_sol_wo_picked + smaller_sol_w_picked

			
			
	
