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
    create_project_data = {
        'name': config.get('repo_name'),
        'description': config.get('description'),
    }

    r = requests.post("http://git.anvil8.com/api/v3/projects?private_token={}".format(config.get('gitlab_token'),), data=create_project_data)
    response = r.json()
    print("Create git repo on http://git.anvil8.com")
    config['git_url'] = 'git@git.anvil8.com:{}.git'.format(response.get('path_with_namespace'),)

    add_member_data = {
        'id': response.get('id'),
        'user_id': 28,
        'access_level': 20
    }
    r = requests.post("http://git.anvil8.com/api/v3/project/{}/members?private_token={}".format(config.get('gitlab_token'), response.get('id')), data=add_member_data)

local('git init')
local('git remote add origin {}'.format(config.get('git_url')))

print('Create project on Jenkins')
new_job = J.copy_job('template_project', config.get('repo_name'))
new_job.modify_scm_url(config.get('git_url'))

shutil.rmtree('./config')