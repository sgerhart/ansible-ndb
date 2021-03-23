# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component

# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.


# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.urls import fetch_url
import json


def ndb_arg_spec():
    return dict(
        ndb_host=dict(type='str', required=True, aliases=['hostname']),
        ndb_port=dict(type='int', required=False, default=8443),
        ndb_username=dict(type='str', default='admin', aliases=['user']),
        ndb_password=dict(type='str', no_log=True),
    )


class NDBModule(object):
    def __init__(self, module):
        self.module = module
        self.resp = {}
        self.params = module.params
        self.result = dict(message="", changed=False)
        self.session_cookie = ""
        self.error = dict(code=None, text=None)
        self.version = ""
        self.http_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive'}
        self.login()

    def __del__(self):
        url = 'https://%(ndb_host)s:%(ndb_port)s/api/logout' % self.params
        resp, auth = fetch_url(self.module, url,
                               headers=self.http_headers,
                               data=None,
                               method='POST')

    def login(self):

        url = 'https://%(ndb_host)s:%(ndb_port)s/api/authenticate' % self.params

        user_credentials = json.dumps({"username": self.params.get(
            'ndb_username'), "password": self.params.get('ndb_password')})

        resp, auth = fetch_url(self.module, url,
                               headers=self.http_headers,
                               data=user_credentials,
                               method='POST')

        if auth.get('status') != 200:
            try:
                self.module.fail_json(
                    msg=json.loads(auth.get('body'))['messages'][0]['message'])
            except Exception:
                self.module.fail_json(
                    msg='Login failed for %(url)s. %(msg)s' % auth,)

        # Get accessToken from response for further processing
        token = json.loads(resp.read())['accessToken']['accessToken']

        self.http_headers['Authorization'] = 'Bearer ' + token

    def process_request(self, api_url, method_type, data):

        url = 'https://{}:{}/{}'.format(self.params.get('ndb_host'), str(self.params.get('ndb_port')), api_url)

        resp, auth = fetch_url(self.module, url,
                               headers=self.http_headers,
                               data=data,
                               method=method_type)

        if auth.get('status') != 200:
            try:
                self.module.fail_json(
                    msg=json.loads(auth.get('body')))
            except Exception:
                self.module.fail_json(
                    msg='Login failed for %(url)s. %(msg)s' % auth)

        return resp

    def get_user(self, username):

        users = []

        api_url = "api/user-management/users?slice={}".format(self.params.get('ndb_slice'))

        result = self.process_request(api_url, "GET", None)

        if username:
            for i in json.loads(result.read()):
                if username == i['user']:
                    return username
            return ""
        else:
            for i in json.loads(result.read()):
                users.append(i['user'])
            return users

    def delete_user(self):

        api_url = 'api/user-management/user/remove?slice={}&user={}'.format(self.params.get('ndb_slice'),
                                                                            self.params.get('username'))

        result = self.process_request(api_url, "DELETE", None)

        self.result['message'] = json.loads(result.read())

    def create_user(self):

        api_url = 'api/user-management/users/add?slice={}'.format(self.params.get('ndb_slice'))

        x = {"user": self.params.get('username'), "password": self.params.get('password'),
             "roles": [self.params.get('role')]}

        data = json.dumps(x)

        if self.get_user(self.params.get('username')) != self.params.get('username'):

            result = self.process_request(api_url, "POST", data)

            self.result['changed'] = True

            self.result['message'] = json.loads(result.read())

        else:

            self.result['skipped'] = True

            self.result['message'] = 'The user, {}, already exists'.format(self.params.get('username'))


    def get_slice(self):

        return

    def create_slice(self):

        return

    def delete_slice(self):

        return

