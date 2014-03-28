from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
from protorpc import messages
from protorpc import message_types
from google.appengine.ext.ndb import msgprop

import datetime

class CodeLanguage(ndb.Model):
    pass

class CodeEntry(messages.Message):
    key = messages.StringField(1, required=False)
    creation_time = message_types.DateTimeField(2, required=False)
    last_voted = message_types.DateTimeField(3, required=False)
    language = messages.StringField(4, required=True)
    score = messages.IntegerField(5, required=False)
    total_voted = messages.IntegerField(6, required=False)
    code_blob = messages.StringField(7, required=True)
    git_username = messages.StringField(8, required=True)
    name = messages.StringField(9, required=False)

class CodeEntryPut(messages.Message):
    language = messages.StringField(1, required=True)
    code_blob = messages.StringField(2, required=True)
    git_username = messages.StringField(3, required=True)
    name = messages.StringField(4, required=False)

class CodeEntryCollection(messages.Message):
    entries = messages.MessageField(CodeEntry, 1, repeated=True)

class CodeEntryPutCollection(messages.Message):
    entries = messages.MessageField(CodeEntryPut, 1, repeated=True)

class CodeEntryID(messages.Message):
    key = messages.StringField(1, repeated=False, required=True)

class CodeEntryIDCollection(messages.Message):
    keys = messages.MessageField(CodeEntryID, 1, repeated=True)

class MaxCodeEntryIndex(ndb.Model):
    max_index = ndb.IntegerProperty(required=True, default=0)

class CodeEntryStore(ndb.Model):
    creation_time = ndb.DateTimeProperty(required=True)
    last_voted = ndb.DateTimeProperty(required=False)
    language = ndb.KeyProperty(required=True,kind=CodeLanguage)
    git_username = ndb.StringProperty(required=False)
    name = ndb.StringProperty(required=False)
    score = ndb.IntegerProperty(required=True,default=0)
    total_voted = ndb.IntegerProperty(required=True,default=0)
    code_blob = ndb.TextProperty(required=True)

