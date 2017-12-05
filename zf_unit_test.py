import zero_forcing

graphs = {
	"edge"     : [{1},{0}],
	"triangle" : [{1,2},{0,2},{0,1}],
	"path"     : [{1},{0,2},{1,3},{2,4},{3}],
	"earring"  : [{1},{0,2,3},{1,3},{1,2}],
	"cycle"    : [{1,4},{0,2},{1,3},{2,4},{3,0}], 
	"K_4"      : [{1,2,3},{0,2,3},{0,1,3},{0,1,2}]
}
forcing_nr = {
	"edge"     : 1,
	"triangle" : 2,
	"path"     : 1,
	"earring"  : 2,
	"cycle"    : 2, 
	"K_4"      : 3
}

def zf_unit_test(logging = False):
	success = True
	for graph, neighbors in graphs.items():
		zf_calculated = zero_forcing.calculate_zero_forcing_nr(neighbors)
		if  zf_calculated != forcing_nr[graph]:
			success = False
			if logging:
				print "   --> Test failed for graph ", graph,": zf_calculated = ", zf_calculated, "zf_real = ", forcing_nr[graph]
		elif logging:
				print "   --> Test succeeded for graph ", graph,": zf = ", zf_calculated
	if logging:
		print "Test Succeeded" if success else "Test Failed" 
	return success
zf_unit_test(True)			
	 
				
