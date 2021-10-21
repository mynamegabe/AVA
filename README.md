# SecurIt

Modules must include in code:
complete = False


@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data): 
    if complete:
    	sio.send(data)
    	sio.disconnect()

# when module is complete
complete = True