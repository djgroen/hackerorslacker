import endpoints
import datetime
import logging
import random
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'hackerorslacker'

from hos_models import *

def addLanguage(name):
    new_language=CodeLanguage(id=name)
    new_language.put()

@ndb.transactional
def addCodeBlob(params):
    language = ndb.Key( CodeLanguage, params['language'] ).get()
    max_num_entry = ndb.Key('MaxCodeEntryIndex', 'root').get()
    new_code_blob=CodeEntryStore(id=max_num_entry.max_index+1,
                                 creation_time=datetime.datetime.now(),
                                 git_username=params['git_username'],
                                 name=params['name'],
                                 language=language.key, code_blob=params['code'])
    new_code_blob.put()
    max_num_entry.max_index = max_num_entry.max_index + 1
    max_num_entry.put()

def deleteAllCodeBlobs():
    for blob_key in CodeEntryStore.query().fetch(keys_only=True):
        blob_key.delete()
    max_num = MaxCodeEntryIndex(id='root', max_index=0)
    max_num.put()


@endpoints.api(name='hackerorslacker', version='v1')
class HOSApi(remote.Service):
    @ndb.transactional(xg=True)
    def addCodeBlob(self,language,code_blob,git_username,name):
        max_num_entry = ndb.Key('MaxCodeEntryIndex', 'root').get()
        new_code_blob=CodeEntryStore(id=max_num_entry.max_index+1,
                                     creation_time=datetime.datetime.now(),
                                     git_username=git_username, name=name,
                                     language=language.key, code_blob=code_blob)
        new_key = new_code_blob.put()
        max_num_entry.max_index = max_num_entry.max_index + 1
        max_num_entry.put()
        return new_key

    @endpoints.method(CodeEntryPut, CodeEntry,
                      path='codeentry', http_method='POST',
                      name='codeentry.add')
    def code_put(self, request):
        language = ndb.Key( CodeLanguage, request.language ).get()
        code_key = self.addCodeBlob(language, request.code_blob, request.git_username, request.name)
        entry = code_key.get()
        if entry is None:
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))
        else:
            return CodeEntry(key=entry.key.urlsafe(),
                         creation_time=entry.creation_time,
                         last_voted=entry.last_voted,
                         git_username=entry.git_username,
                         name=entry.name,    
                         language=entry.language.id(),
                         score=entry.score,
                         total_voted=entry.total_voted,
                         code_blob=entry.code_blob)

    @endpoints.method(message_types.VoidMessage, CodeEntryCollection,
                      path='codeentry', http_method='GET',
                      name='codeentry.list')
    def code_list(self, request):
        request_size=1
        random_numbers = []
        max_num_entry = ndb.Key('MaxCodeEntryIndex', 'root').get()
        if max_num_entry.max_index == 0:
            raise endpoints.NotFoundException('Code entry not found.')
        for i in range(0, request_size):
            random_numbers.append(random.randint(0,max_num_entry.max_index-1))
        result = []
        for r_number in random_numbers:
            logging.info(r_number)
            entry_key = ndb.Key('CodeEntryStore', r_number+1)
            entry = entry_key.get()
            result.append(CodeEntry(key=entry_key.urlsafe(),
                                    creation_time=entry.creation_time,
                                    last_voted=entry.last_voted,
                                    language=entry.language.id(),
                                    score=entry.score,
                                    git_username=entry.git_username,
                                    name=entry.name,    
                                    total_voted=entry.total_voted,
                                    code_blob=entry.code_blob))
        return CodeEntryCollection(entries=result)

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.StringField(1))
    
    @ndb.transactional
    def do_code_vote(self,code_key,vote):
        entry = code_key.get()
        if entry is None:
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))
        else:
            entry.last_voted=datetime.datetime.now()
            entry.score = entry.score + vote
            entry.total_voted = entry.total_voted + 1
            entry.put()
            return entry


    @endpoints.method(ID_RESOURCE, CodeEntry,
                      path='codeentry/{id}/up', http_method='POST',
                      name='codeentry.up')
    def code_upvote(self, request):
        code_key = ndb.Key(urlsafe=request.id)
        entry=self.do_code_vote(code_key,1)
        return CodeEntry(key=entry.key.urlsafe(),
                         creation_time=entry.creation_time,
                         last_voted=entry.last_voted,
                         language=entry.language.id(),
                         git_username=entry.git_username,
                         name=entry.name,    
                         score=entry.score,
                         total_voted=entry.total_voted,
                         code_blob=entry.code_blob)

    @endpoints.method(ID_RESOURCE, CodeEntry,
                      path='codeentry/{id}/down', http_method='POST',
                      name='codeentry.down')
    def code_downvote(self, request):
        code_key = ndb.Key(urlsafe=request.id)
        entry=self.do_code_vote(code_key,-1)
        return CodeEntry(key=entry.key.urlsafe(),
                         creation_time=entry.creation_time,
                         last_voted=entry.last_voted,
                         language=entry.language.id(),
                         git_username=entry.git_username,
                         name=entry.name,    
                         score=entry.score,
                         total_voted=entry.total_voted,
                         code_blob=entry.code_blob)

    @endpoints.method(ID_RESOURCE, CodeEntry,
                      path='codeentry/{id}/ignore', http_method='POST',
                      name='codeentry.ignore')
    def code_ignorevote(self, request):
        code_key = ndb.Key(urlsafe=request.id)
        entry=self.do_code_vote(code_key,0)
        return CodeEntry(key=entry.key.urlsafe(),
                         creation_time=entry.creation_time,
                         last_voted=entry.last_voted,
                         language=entry.language.id(),
                         git_username=entry.git_username,
                         name=entry.name,    
                         score=entry.score,
                         total_voted=entry.total_voted,
                         code_blob=entry.code_blob)

    @endpoints.method(ID_RESOURCE, CodeEntry,
                      path='codeentry/{id}', http_method='GET',
                      name='codeentry.get')
    def code_get(self, request):
        code_key = ndb.Key(urlsafe=request.id)
        entry = code_key.get()
        if entry is None:
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))
        else:
            return CodeEntry(key=entry.key.urlsafe(),
                                    creation_time=entry.creation_time,
                                    last_voted=entry.last_voted,
                                    language=entry.language.id(),
                                    git_username=entry.git_username,
                                    name=entry.name,    
                                    score=entry.score,
                                    total_voted=entry.total_voted,
                                    code_blob=entry.code_blob)

APPLICATION = endpoints.api_server([HOSApi],restricted=False)
        
