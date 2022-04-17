def Load( someLoadData ):
	import mapvars, serverimports, debug, wic
	import cPickle as pickle
	
	loadData = pickle.loads( someLoadData )
	
	for key in loadData['mapvars']:
		mapvars.__dict__[key] = loadData['mapvars'][key]
	
	serverimports.theReactions = loadData['theReactions']
	serverimports.theGroups = loadData['theGroups']
	
	try:
		serverimports.Groups._Groups__GroupCounter = loadData['GroupCounter']
	except Exception:
		highestId = 0
		for g in serverimports.theGroups.myGroups.values():
			if g.myId > highestId:
				highestId = g.myId
								
		serverimports.Groups._Groups__GroupCounter = highestId
	
	try:
		serverimports.Groups._Groups__SpawnCounter = loadData['SpawnCounter']	
	except Exception:
		serverimports.Groups._Groups__SpawnCounter = 100000

	serverimports.theExecutionQueue = loadData['theExecutionQueue']
	serverimports.theExpressList = loadData['theExpressList']
	serverimports.theNameCounter = loadData['theNameCounter']
	serverimports.theGUIChunks = loadData['theGUIChunks']
	serverimports.theMessageboxCounter = loadData['theMessageboxCounter']
	serverimports.lastShownMessageBoxId = loadData['lastShownMessageBoxId']
	serverimports.lastShownFeedBackMessageBoxId = loadData['lastShownFeedBackMessageBoxId']
	serverimports.theBuyMenu = loadData['theBuyMenu']
	serverimports.theTAs = loadData['theTAs']
	serverimports.theTime = loadData['theTime']


def Save():
	import mapvars, serverimports, debug, wic
	import cPickle as pickle
	
	serverimports.theReactions.Pause()
	saveData = {}
	saveData['mapvars'] = {}
	
	for key in mapvars.__dict__:
		try:
			pickle.dumps( mapvars.__dict__[key] )
		except TypeError:
			continue
		else:
			saveData['mapvars'][key] = mapvars.__dict__[key]
	
	saveData['theReactions'] = serverimports.theReactions
	saveData['theGroups'] = serverimports.theGroups
	saveData['GroupCounter'] = serverimports.Groups._Groups__GroupCounter
	saveData['SpawnCounter'] = serverimports.Groups._Groups__SpawnCounter
	saveData['theExecutionQueue'] = serverimports.theExecutionQueue
	saveData['theExpressList'] = serverimports.theExpressList
	saveData['theNameCounter'] = serverimports.theNameCounter
	saveData['theGUIChunks'] = serverimports.theGUIChunks
	saveData['theMessageboxCounter'] = serverimports.theMessageboxCounter
	saveData['lastShownMessageBoxId'] = serverimports.lastShownMessageBoxId
	saveData['lastShownFeedBackMessageBoxId'] = serverimports.lastShownFeedBackMessageBoxId
	saveData['theBuyMenu'] = serverimports.theBuyMenu
	saveData['theTAs'] = serverimports.theTAs
	saveData['theTime'] = wic.common.GetCurrentTime()

		
	try:
		returnstring = pickle.dumps( saveData )
	except TypeError:
		parser = debug.PickleParser()
		parser.Parse( None, saveData )
		parser.Parse( 'PickleParser( %s ).txt' % wic.game.MAP_NAME, saveData )
		
		raise Exception( 'The game failed to save. There is a file called PickleParse( %s ) in your debug directory. Please attach this to your bug report', wic.game.MAP_NAME );
	
	serverimports.theReactions.Pause( False )
	
	return returnstring
