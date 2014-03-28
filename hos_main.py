import webapp2
from hos_api import *

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/frontend/index.html")

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

