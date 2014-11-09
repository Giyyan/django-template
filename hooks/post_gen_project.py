import shutil
import json
import subprocess
from jenkinsapi.jenkins import Jenkins
import requests


config = json.loads(open('./config/config.json', 'r').read())
"""
Connecting to Jenkins
"""
J = Jenkins('http://ci.anvil8.com',
            username=config.get('ci_username'),
            password=config.get('ci_apitoken'))

if not config.get('git_url'):
    """
    Create repo on git.anvil8.com
    """
    create_project_data = {
        'name': config.get('repo_name'),
        'description': config.get('description'),
    }

    r = requests.post("http://git.anvil8.com/api/v3/projects?private_token={}".format(config.get('gitlab_token'),), data=create_project_data)
    response = r.json()
    print("Create git repo on http://git.anvil8.com")
    config['git_url'] = 'git@git.anvil8.com:{}.git'.format(response.get('path_with_namespace'),)

    """
    Add jenkins user as reporter to repo
    """
    add_member_data = {
        'id': response.get('id'),
        'user_id': 28,
        'access_level': 20
    }
    r = requests.post("http://git.anvil8.com/api/v3/projects/{}/members?private_token={}".format(response.get('id'), config.get('gitlab_token')), data=add_member_data)

"""
Init git repo and push project
"""
subprocess.call(['git', 'init'])
subprocess.call(['git', 'remote', 'add', 'origin', config.get('git_url')])
subprocess.call(['git', 'add', '.'])
subprocess.call(['git', 'commit', '-am', '"Initial commit"'])
subprocess.call(['git', 'push', 'origin', 'master'])

print('Create project on Jenkins')
new_job = J.copy_job('template_project_python3', config.get('repo_name'))
new_job.modify_scm_url(config.get('git_url'))
J.build_job(config.get('repo_name'))
shutil.rmtree('./config')