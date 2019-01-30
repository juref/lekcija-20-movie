from google.appengine.ext import ndb


class Movie(ndb.Model):
    movieTitle = ndb.StringProperty()
    movieExcerpt = ndb.StringProperty()
    movieThumb = ndb.StringProperty()
    movieRating = ndb.IntegerProperty()
    movieDeleted = ndb.BooleanProperty(default = False)