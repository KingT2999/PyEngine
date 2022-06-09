# Game Scripts
START_SCRIPTS = []
UPDATE_SCRIPTS = []
PRE_RENDER_UPDATE_SCRIPTS = []
RENDER_UPDATE_SCRIPTS = []

def Start(func):
	START_SCRIPTS.append(func)

def Update(func):
	UPDATE_SCRIPTS.append(func)

def RenderUpdate(func):
	RENDER_UPDATE_SCRIPTS.append(func)

def PreRenderUpdate(func):
	PRE_RENDER_UPDATE_SCRIPTS.append(func)