# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import jinja2
import os.path
import yaml

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader('templates'),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

# This only needs to be loaded once.
file = open('meta.yaml')
data = yaml.load(file.read())
file.close()


# Generate the path data from the project and page slugs.
for project in data['projects']:
  project['path'] = '/' + project['slug'] + '/'
  if 'pages' in project:
    for page in project['pages']:
      page['path'] = project['path'] + page['slug'] + '/'


# Set environment data if it's not already present.
if not 'env' in data:
  if (os.environ['SERVER_NAME'].rfind('googleplex.com') > -1 or
      os.environ['SERVER_NAME'].rfind('localhost') > -1 or
      os.environ['SERVER_NAME'].rfind('corp.google.com') > -1):
    data['env'] = 'development'
  else:
    data['env'] = 'production'


# Group all demos together
data['demos'] = [i for i in data['projects'] if i['type'] == 'demo']


# Group all tools together
data['tools'] = [i for i in data['projects'] if i['type'] == 'tool']


def __get_project(project):
  if project == 'index':
    return {
      'title': data['title'],
      'slug': data['slug'],
      'path': data['path'],
    }
  else:
    return [i for i in data['projects'] if i['slug'] == project][0]


def __get_page(project, page):
  project = __get_project(project)

  if page == 'index':
    return {
      'path': project['path'],
      'slug': project['slug']
    }
  else:
    return [i for i in project['pages'] if i['slug'] == page][0]

def render(project='index', page='index'):
  try:
    template_data = {
      'site': data,
      'project': __get_project(project),
      'page': __get_page(project, page)
    }

    if project == 'index':
      template_file = 'index.html'
    else:
      template_file = project + '/' + page + '.html'

    template = JINJA_ENVIRONMENT.get_template(template_file)
    return template.render(template_data)
  except:
    template = JINJA_ENVIRONMENT.get_template('404.html')
    return template.render({
      'site': data,
      'project': None,
      'page': None
    })
