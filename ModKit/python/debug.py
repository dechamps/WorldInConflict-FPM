import sys, linecache, base, wic


NONE		= 1
BRIEF		= 2
VERBOSE		= 4
EXCESSIVE	= 8

DebugWriter		= base.DebugMessage
TraceLines		= True
TraceCalls		= True
TraceCCalls		= False
TraceReturns	= True
GlobalTrace		= False


BannedEvents = [ 'Update' ]
BannedActions = [ 'Toggle()', 'SaveSettings()' ]
BannedExecutions = [ 'Update()' ]


DebugLevel = EXCESSIVE


def DebugMessage( aMessageString, anImportanceLevel = NONE ):
	""" Prints a message to the debugfile. Filtering can be set with
		anImportanceLevel
	"""
	global DebugLevel
	
	if DebugLevel >= anImportanceLevel:
		base.DebugMessage( aMessageString )


def debug( func, *keys, **k ):
	"""prints the name,  input parameters and output of a function to
	   stdout."""

	#retrieve the names of functionarguments via reflection:
	argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
	#retrieve the name of the function itself:
	fname = func.func_name

	def echo( *args,**kwargs ):
		"""instead of the original function, we return this echo function that
		calls the original one. This way, we can add additional behaviour:"""

		#call the original function and store the result:
		result = func(*args, **kwargs)

		#create a string that explains input, e.g: a=5, b=6
		in_str = ', '.join( '%s = %r' % entry
			for entry in zip( argnames, args ) + kwargs.items() )

		#print input and output:
		DebugWriter( "<DBG>%s: Input:%s Output:%s" % ( fname, in_str, result ) )

		return result
	#the function returned has the name 'echo'.
	#this is not very representative, so we rename it
	# "<original function name> (debug echo)"
	echo.func_name = "%s (debug echo)" % func.func_name
	return echo


def traceit( frame, event, arg ):
	""" Prints executed pythonlines to the debug console

	Args:
	 frame - (execution frame) Is the current stack frame
	 event - (string) Gives the type of event occured. We only handle 'line' at the moment
	 arg - (various) Extra data not used in line events

	Returns:
	 Returns itself or python execution will stop
	"""
	global TraceCalls, TraceLines, TraceReturns

	if event == "line" and TraceLines:		
		lineno = frame.f_lineno
		
		try:
			filename = frame.f_globals["__file__"]
			if (filename.endswith(".pyc") or
				filename.endswith(".pyo")):
				filename = filename[:-1]
		except KeyError:
			filename = "unknown_file"
		
		try:
			name = frame.f_globals["__name__"]
		except KeyError:
			name = "unknown_name"
		
		line = linecache.getline( filename, lineno )
		
		DebugWriter( "%s:%s: %s" % ( name, lineno, line.rstrip() ) )
		
		return traceit

	elif event == "return" and TraceReturns:
		returnString = ""
		
		obj = frame.f_locals.get( "self" )
		
		if obj:
			returnString += "%s::" % obj.__class__.__name__
		
		returnString += "%s returns" % ( frame.f_code.co_name )
		
		if TraceReturns > 1:
			returnString += ":\n"
			for currArg in arg:
				returnString += "%s" % currArg
		
		DebugWriter( returnString )
		
		return None
		
	elif event == "call" and TraceCalls:
		if frame.f_back:
			callframe = frame.f_back
			returnString = ""
			name = ""
			obj = frame.f_locals.get( "self" )
			
			lineno = callframe.f_lineno
			filename = callframe.f_globals["__name__"]
			
			if not obj is None:
				name += "%s::" % obj.__class__.__name__
			
			name += frame.f_code.co_name
			returnstring = "%s called from %s line %d" % ( name, filename, lineno )
			
			if TraceCalls > 1:
				returnString += "having the following locals defined:"
				
				for argument in frame.f_code.co_varnames:
					if argument == "self":
						returnstring += "\n\tself - %s" % frame.f_locals.get( argument )
					else:
						returnstring += "\n\t%s - %s" % ( argument, frame.f_locals.get( argument ) )
			
		else:
			returnString = ""
			name = ""
			obj = frame.f_locals.get( "self" )
			
			lineno = frame.f_lineno
			filename = frame.f_globals["__name__"]
			
			if obj:
				name += "%s::" % obj.__class__.__name__
			
			name += frame.f_code.co_name
			returnstring = "%s called from %s line %d" % ( name, filename, lineno )
			
			if TraceCalls > 1:
				returnString += "having the following locals defined:"
				
				for argument in frame.f_code.co_varnames:
					if argument == "self":
						returnstring += "\n\tself - %s" % frame.f_locals.get( argument )
					else:
						returnstring += "\n\t%s - %s" % ( argument, frame.f_locals.get( argument ) )
			
			DebugWriter( returnstring )
			
			return traceit
	
	return traceit


def trace( func, *keys, **k ):
	"""prints the name,  input parameters and output of a function to
	   stdout."""

	def echo( *args, **kwargs ):
		""" Instead of the original function, we return this echo function that
		calls the original one. This way, we can add additional behaviour:
		"""
		if not GlobalTrace:
			sys.settrace( traceit )

		#call the original function and store the result:
		result = func( *args, **kwargs )

		if not GlobalTrace:
			sys.settrace( None )

		return result

	echo.func_name = "%s (trace echo)" % func.func_name
	return echo


def frameUnfolder( aTracebackObject, anExcessiveDebugOutputFlag = False ):
	""" Unfolds a traceback object and returns as a string

	Args:
	 aTracebackObject - (tracebackframe) The execution frame to be unfolded

	Returns:
	 a string representation of the callstack at the time of the exception
	"""
	callStr	= ''
	depth	= 0
	
	while aTracebackObject:
		theInstance = aTracebackObject.f_locals.get( 'self' )
		
		if theInstance:
			callStr += '\n\t[%d] %s::%s ( at line %d in "%s" )' % ( depth, obj.__class__.__name__, aTracebackObject.f_code.co_name, aTracebackObject.f_lineno, aTracebackObject.f_code.co_filename )
		else:
			callStr += '\n\t[%d] %s ( at line %d in "%s" )' % ( depth, aTracebackObject.f_code.co_name, aTracebackObject.f_lineno, aTracebackObject.f_code.co_filename )
		
		depth += 1
		aTracebackObject = aTracebackObject.f_back
	
	return callStr


class PickleParser( object ):
	class PickleParserList( object ):
		def __init__( self, aKeyList, aValueList = None ):
			self.__keys = list( aKeyList )
			self.__values = aValueList
			
			if self.__values is None:
				self.__values = self.__keys
				self.__keys = range( len( self.__values ) )
			
			self.__values = list( self.__values )
		
		
		def pop( self ):
			return ( self.__keys.pop(), self.__values.pop() )
		
		
		def __len__( self ):
			return len( self.__values )
	
	
	def __init__( self, aMaxDepth = 20 ):
		self.__counter = 0
		self.__depth = 0
		self.__maxDepth = aMaxDepth
		self.__parsedItems = []
		self.__returnString = ''
		self.__objectStack = []
		self.__lastKey = ''
	
	
	def Parse( self, aFileName, anObject ):
		self.__counter = 0
		self.__depth = 0
		self.__parsedItems = []
		self.__returnString = ''
		self.__objectStack = []
		self.ParseObject( anObject )
		
		while len( self.__objectStack ):
			self.ParseItems()
		
		if aFileName is None:
			for line in self.__returnString.splitlines():
				wic.common.DebugMessage( line )
		else:
			wic.common.DumpToFile( aFileName, self.__returnString )
	
	
	def ParseObject( self, anObject ):
		if self.__depth >= self.__maxDepth:
			self.AppendBlankline()
			self.AppendOutput( "\t<<< At max depth %d. Returning" % ( self.__depth ) )
			return False
			
		elif anObject in self.__parsedItems:
			self.AppendBlankline()
			self.AppendOutput( "\t<<< This %s is already parsed. Returning" % ( anObject.__class__.__name__ ) )
			return False
			
		else:
			if type( anObject ) == type( [] ) or type( anObject ) == type( () ):
				self.__objectStack.append( PickleParser.PickleParserList( anObject[:] ) )
			elif type( anObject ) == type( {} ):
				self.__objectStack.append( PickleParser.PickleParserList( anObject.keys()[:], anObject.values()[:] ) )
			else:
				try:
					self.__objectStack.append( PickleParser.PickleParserList( anObject.__dict__.keys()[:], anObject.__dict__.values()[:] ) )
				except AttributeError:
					self.AppendBlankline()
					self.AppendOutput( "\t<<< The %s object was no list, nor a dictionary and had no __dict__. It's value was %s" % ( anObject.__class__.__name__, anObject ) )
					return False
			
			self.__parsedItems.append( anObject )
			self.__depth += 1
			return True
	
	
	def ParseItems( self ):
		import cPickle as pickle
		while True:
			try:
				item = self.__objectStack[-1].pop()
			except IndexError:
				self.__objectStack.pop()
				self.__depth -= 1
				return
			
			try:
				pickle.dumps( item[1] )
			except Exception, e:
				self.__counter += 1
				
				self.AppendBlankline()
				self.AppendOutput( "[%s]:" % item[0] )
				self.AppendOutput( "\tType: %s" % item[1].__class__.__name__ )
				try:
					self.AppendOutput( "\tValue: %s" % item[1] )
				except TypeError:
					self.AppendOutput( "\tValue: %s" % str( item[1] ) )
				self.AppendOutput( "\tException: %s" % e )
				
				if self.ParseObject( item[1] ):
					return
	
	
	def AppendOutput( self, aString ):
		self.__returnString += "%s%s\n" % ( InsertTabs( self.__depth ), aString )
	
	
	def AppendBlankline( self ):
		self.__returnString += "\n"


def InsertTabs( aNumberOfTabs ):
	tabs = ''
	
	for i in range( aNumberOfTabs ):
		tabs += "\t"
	
	return tabs
