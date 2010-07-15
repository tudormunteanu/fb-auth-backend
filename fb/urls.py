# -*- coding: utf-8 -*-
# fb.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('fb/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'fb/index': 'fb.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
    ViewGroup(
        Rule('/', endpoint='index', view='fb.views.index'),
        Rule('/login/', endpoint='login', view='fb.views.login'),
        Rule('/fb_login/', endpoint='fb_login', view='fb.views.fb_login'),
        Rule('/set_test_session/', endpoint='set_test_session', view='fb.views.set_test_session'),
        Rule('/test_graph_api/', endpoint='test_graph_api', view='fb.views.test_graph_api'),

    )
]

