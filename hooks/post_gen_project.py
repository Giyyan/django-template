import shutil
import json
from jenkinsapi.jenkins import Jenkins
from fabric.api import local
import requests


config = json.loads(open('./config/config.json', 'r').read())

J = Jenkins('http://ci.anvil8.com',
            username=config.get('ci_username'),
            password=config.get('ci_apitoken'))

if not config.get('git_url'):
    data = {
        'name': config.get('repo_name'),
        'description': config.get('description'),
    }
    r = requests.post("http://git.anvil8.com/api/v3/projects?private_token={}".format(config.get('gitlab_token'),))
    response = json.loads(r.json())
    config['git_url'] = 'git@git.anvil8.com:{}.git'.format(response.get('path_with_namespace'),)

local('git init')
local('git remote add origin {}'.format(config.get('git_url')))


print('Create project on Jenkins')
new_job = J.copy_job('template_project', config.get('repo_name'))
new_job.modify_scm_url(config.get('git_url'))

shutil.rmtree('./config')