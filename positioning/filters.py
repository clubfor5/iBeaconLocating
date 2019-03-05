def ewma(sumterm, newterm, beta):
	result = 0
	if sumterm <= -100:
		result = newterm
	else:
		result = sumterm * beta + newterm *(1-beta)
	return result
		
