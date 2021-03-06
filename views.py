#!/usr/bin/env python
# encoding: utf-8

"""
Created by Christian Klein on 2010-03-07.
Copyright (c) 2010 Christian Klein. All rights reserved.
"""

from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse, Http404
from django.template import Template, TemplateSyntaxError
import simplejson as json
from huTools.couch import setup_couchdb
from huTools.decorators import ajax_request
from uuid import uuid4

def couch():
    """Helper function"""
    return setup_couchdb(settings.TEMPLATE_COUCHDB_SERVER,
                         getattr(settings, 'TEMPLATE_COUCHDB_DATABASE', 'templates'))


def list_templates(request):
    db = couch()
    templates = []
    for row in db.view("_all_docs"):
        doc = db[row.key]
        templates.append((doc.id, doc['name']))
    
    return render_to_response("temple/temple.html",
                              {'templates': templates})


#@ajax_request
def get_template(request):
    doc_id = request.POST.get('id')
    if not doc_id:
        raise Http404("Not found.")
    doc = couch()[doc_id]
    return HttpResponse(doc['source'])


@ajax_request
def set_template(request):

    doc_id = request.POST.get('id')
    name = request.POST.get('name')
    source = request.POST.get('source')

    try:
        template = Template(source)
    except TemplateSyntaxError, exception:
        return {'status': 'error', 'msg': exception.message}
    
    db = couch()
    
    if doc_id == "-1":
        doc_id = uuid4().hex
        doc = {'_id': doc_id}
        print "new doc:", doc
    else:
        doc = db[doc_id]
    
    doc['name'] = name
    doc['source'] = source
    db[doc_id] = doc
    return {'status': 'ok', 'msg': "Changed"}
