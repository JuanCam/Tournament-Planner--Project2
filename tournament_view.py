#Front-end of the tournament application

import tournament
#Modules for running a web-server
import cgi
from wsgiref.simple_server import make_server
from wsgiref import util

HTML = '''\
	   <!doctype html>
	   <html>
	      <head>
	       <title>Swiss torunament</title>
	      </head>
	      <body>
	       <h2>New tournament</h2>
	       <form method=post action="/torunament">
	         <input type="text" name="torunament_name">
                 <button type="submit">Create Tournament</button>
               </form>
	      </body>
	   </html>
'''

HTML_T = '''\
	   <!doctype html>
	   <html>
	      <head>
	       <title>Swiss torunament</title>
	      </head>
	      <body>
	       <h2>Tournamet Name</h2>
	       <form method=post action="/torunament2">
	         <input type="text" name="player_name">
                 <button type="submit">Create Player</button>
               </form>
	      </body>
	   </html>
'''
def create_tournament_view(env, resp):
    tournament.connect()
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    return [HTML]

## Request handler for posting - inserts to database
def torunament_view(env, resp):
    '''Post handles a submission of the forum's form.
  
    The message the user posted is saved in the database, then it sends a 302
    Redirect back to the main page so the user can see their new post.
    '''
    # Get post content
    input = env['wsgi.input']
    
    length = int(env.get('CONTENT_LENGTH', 0))
    
    # If length is zero, post is empty - don't save it.
    if length > 0:
        db = tournament.connect()
        postdata = input.read(length)
        fields = cgi.parse_qs(postdata)
        content = fields['torunament_name'][0]
        # If the post is just whitespace, don't save it.
        content = content.strip()
        if content:
            # Save it in the database
            tournament.createTournament(content,db)
    # 302 redirect back to the main page
    headers = [('Location', '/'),
               ('Content-type', 'text/html')]
    resp('200 OK', headers) 
    return [HTML_T]

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': create_tournament_view,
            'torunament': torunament_view
        }
## Dispatcher forwards requests according to the DISPATCH table.
def dispatcher(env, resp):
    '''Send requests to handlers based on the first path component.'''

    page = util.shift_path_info(env);
    
    if page in DISPATCH:
        return DISPATCH[page](env, resp)
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        resp(status, headers)    
        return ['Not Found: ' + page]


# Run this bad server only on localhost!
httpd = make_server('', 5000, dispatcher)
print "Serving HTTP on port 5000..."
httpd.serve_forever()
