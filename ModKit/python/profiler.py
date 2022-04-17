import base, sys, debug

theProfilingInstances = {}
theUniqueIdCounter = -1

class Profiler_Begin( object ):

	def __init__(self, aDescription):
		global theProfilingInstances, theUniqueIdCounter
		
		strRep = "%s%d" % (sys._getframe(1).f_code.co_filename, sys._getframe(1).f_lineno)
				
		if theProfilingInstances.has_key(strRep):
			uniqueId = theProfilingInstances[strRep]
		else:
			theUniqueIdCounter += 1
			uniqueId = theUniqueIdCounter
			theProfilingInstances[strRep] = theUniqueIdCounter
			
		desc = "Py_%s" % aDescription
		
		base.StartProfiling(sys._getframe(1).f_code.co_filename, sys._getframe(1).f_lineno, desc, uniqueId)
		
	def __del__(self):
		base.StopProfiling()
