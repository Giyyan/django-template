import shutil
import json
from jenkinsapi.jenkins import Jenkins
from fabric.api import local


config = json.loads(open('./config/config.json', 'r').read())

J = Jenkins('http://ci.anvil8.com',
            username=config.get('ci_username'),
            password=config.get('ci_apitoken'))

if not config.get('git_url'):
    pass

local('git init')
local('git remote add origin {}'.format(config.get('git_url')))


print('Create project on Jenkins')
new_job = J.copy_job('template_project', config.get('repo_name'))
new_job.modify_scm_url(config.get('git_url'))

shutil.rmtree('./config')