# Copyright 2011 Dataprev
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

from genshi.builder import tag

from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor, ITemplateProvider, add_stylesheet, add_script
from trac.wiki.model import *
from datetime import datetime
from trac.perm import IPermissionRequestor
from pyrity import *

class CatracModule(Component):
	"""
	Main plugin class to manage requests
	"""
	implements(INavigationContributor, ITemplateProvider, IRequestHandler, IPermissionRequestor)

	def get_active_navigation_item(self, req):
		"""
		Generate a new menu item.

		.. attribute: req

		HTTP Request object. See <link-to-Request-object>
		"""
		return 'catrac'

	def get_navigation_items(self, req):		
		"""
		Creates an item in the main menu checking your permission				
		"""
		if 'BASELINE_VIEW' in req.perm('BASELINE'):
			yield ('mainnav', 'catrac', tag.a('Catrac', href=req.href.catrac()))
	
	def match_request(self, req):		
		"""
		Create access link to the plugin considering the user's permission	
		"""
		if 'BASELINE_VIEW' in req.perm('BASELINE'):					
			return re.match(r'/catrac(?:_trac)?(?:/.*)?$', req.path_info)
	
	def get_permission_actions(self):        		
		return ['CATRAC_VIEW']
	
	def process_request(self, req): 		       		      
		add_stylesheet(req,'hw/css/catrac.css')
		add_stylesheet(req,'hw/js/jsTree/themes/apple/style.css')
		add_script(req,'hw/js/jsTree/jquery.jstree.js')
		data = {} 		 
		proj = Project("DTP.0196")
		teste =  proj.readProject()
		data['data'] = teste                
		return "catrac.html", data, None				
	
		
	def get_templates_dirs(self):
		from pkg_resources import resource_filename
		return [resource_filename(__name__, 'templates')]
	
	def get_htdocs_dirs(self):
		"""Return a list of directories with static resources (such as style
		sheets, images, etc.)
	
		Each item in the list must be a `(prefix, abspath)` tuple. The
		`prefix` part defines the path in the URL that requests to these
		resources are prefixed with.
	
		The `abspath` is the absolute path to the directory containing the
		resources on the local file system.
		"""
		from pkg_resources import resource_filename
		return [('hw', resource_filename(__name__, 'htdocs'))]
