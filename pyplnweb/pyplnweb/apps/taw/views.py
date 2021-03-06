from django.shortcuts import render_to_response, get_object_or_404,redirect
from django.core.context_processors import csrf
from django.http import Http404,HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from taw.models import *
from taw.forms import CorpusForm
from django.conf import settings
import pymongo as PM


# Initialize mongo connection
connection = PM.Connection(settings.MONGODB, settings.MONGODB_PORT)


def main(request):
    return render_to_response("taw/workbench.html", context_instance=RequestContext(request))

def document(request):
    """
    This view assembles the document analysis page
    """
    pass
    #TODO: implement

def corpus(request):
    """
    This view assembles the corpus analysis page
    """
    pass
    #TODO: implement

def manage(request):
    """
    This view assembles the  management page
    """

def collection_browse(request):
    """
    This view assembles the collection browsw page
    """
    dbs = connection.database_names()
    collections = {}
    for db in dbs:
        d = connection[db]
        for col in d.collection_names():
            collections[col] = {'db':db, 'count':d[col].count()}

    data_dict = {'collections':collections,

    }
    data_dict.update(csrf(request))
    return render_to_response("taw/collections.html", data_dict, context_instance=RequestContext(request))

def document_browse(request, dbname,collname):
    """
    List of documents for a given collection.
    Also
    """
    docs = connection[dbname][collname].find(limit=100)
    keys = docs[0].keys()
    if request.user.is_authenticated():
        corpora = Corpus.objects.filter(owner=request.user)
    else:
        corpora = []
    cform = CorpusForm()
    data_dict = {'docs':docs,
                 'keys':keys,
                 'jkeys':simplejson.dumps(keys),
                 'db':simplejson.dumps(dbname),
                 'collection':simplejson.dumps(collname),
                 'corpora':corpora,
                 'corpusform':cform,
    }
    data_dict.update(csrf(request))
    return render_to_response("taw/document_browse.html", data_dict, context_instance=RequestContext(request))

@login_required
def create_corpus(request):
    """
    Handle the creation of a corpus
    """
    corpora = []
    if request.method == 'POST': # If the form has been submitted...
        form = CorpusForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            c = Corpus(title=title,description=description,owner=request.user)
            c.save()
            return HttpResponseRedirect('/taw/#corpustab/') # Redirect after POST
    else:
        corpora = Corpus.objects.all(owner=request.user)
#        form = CorpusForm() # An unbound form
    data_dict = {
#        'form': form,
        'corpora':corpora,
        }

    return redirect('/taw/collections/')
