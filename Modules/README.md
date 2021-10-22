# Modules

### Modules must include in code:
```python
complete = False

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data): 
    if not complete:
    	sio.send(data)
      complete = True
    else:
      sio.disconnect()
      
sio.connect('http://127.0.0.1:6001') # when done
```
