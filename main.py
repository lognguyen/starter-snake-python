import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"
    headType = "pixel"
    tailType = "hook"

    return start_response(color),start_response(headType),start_response(tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))
    x = [2]
    y = [2] 
    length = 1
    directions = ['up', 'down', 'left', 'right']
    move = 'down'
    # head update
    if move == 'right':
        x.append(x[0])
        y.append(y[0])
        x[0] +=1
    elif move == 'left':
        x.append(x[0])
        y.append(y[0])
        x[0] -=1
    elif move == 'up':
        y.append(y[0])
        x.append(x[0])
        y[0] -=1
    elif move == 'down':
        y.append(y[0])
        x.append(x[0])
        y[0] +=1

    if (y[0]==y[1]):
        if x[0] == x[len(x)-1]+1 or x[0] == x[len(x)-1]-1:
            if y[(len(x)-1)//2] > y[0]:
                move = 'up'
            else: 
                move ='down'

    elif (x[0]==x[1]):
        if y[0] == y[len(x)-1]+1 or y[0] == y[len(x)-1]-1:
            if x[(len(x)-1)//2] > x[0]:
                move = 'left'
            else:
                move = 'right'
    

    elif x[0] == 1:
        if (y[0] == 1 and x[0]==x[1]):
            move ='left'
        if (y[0] == 1):
            move = 'down'
        elif (y[0] == 7):
            move = 'up'
        elif (y[0] != y[1]):
            move = 'left'
        else:
            move = random.choice(['up','down'])
 
    
    elif x[0] == 7:
        if (y[0] == 1 and x[0]==x[1]):
            move ='right'
        if (y[0] == 1):
            move = 'down'
        elif (y[0] == 7):
            move = 'up'
        elif (y[0] != y[1]):
            move = 'right'
        else:
            move = random.choice(['up','down'])

    elif y[0] == 1:
        if (x[0] != x[1]):
            move = 'down'
        else:
            move = random.choice(['left','right'])

    elif y[0] == 7:
        if (x[0] != x[1]):
            move = 'up'
        else:
            move = random.choice(['left','right'])

    elif (y[0]==y[1]):
        if x[0] == x[len(x)-1]+1 or x[0] == x[len(x)-1]-1:
            if y[(len(x)-1)//2] > y[0]:
                move = 'up'
        

    return move_response(move)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
