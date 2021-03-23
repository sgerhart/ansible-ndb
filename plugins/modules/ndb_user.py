#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)



from __future__ import absolute_import, division, print_function
__metaclass__ = type








from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sgerhart.ndb.plugins.module_utils.ndb import NDBModule, ndb_arg_spec


def main():

    result = dict(changed=False, resp='')
    arg_spec = ndb_arg_spec()
    arg_spec.update(

        ndb_host=dict(type='str', default=""),
        ndb_port=dict(type='int', default=""),
        ndb_username=dict(type='str', default=""),
        ndb_password=dict(type='str', default="", no_log=True),
        ndb_slice=dict(type='str', default='default'),
        username=dict(type='str', default=""),
        password=dict(type='str', default="", no_log=True),
        role=dict(type='str', default=""),
        validate_certs=dict(type='bool', default=False),
        state=dict(type='str', default='present', choices=['absent',
                                                           'present', 'query', 'modify']),

    )

    module = AnsibleModule(argument_spec=arg_spec,
                           supports_check_mode=True,
                           required_if=[['state', 'absent', ['username']],
                                        ['state', 'present', ['username']]])

    state = module.params.get('state')
    username = module.params.get('username')
    password = module.params.get('password')
    role = module.params.get('role')
    ndb_host = module.params.get('ndb_host')
    ndb_port = str(module.params.get('ndb_port'))
    ndb_username = module.params.get('ndb_username')
    ndb_password = module.params.get('ndb_password')
    ndb_slice = module.params.get('ndb_slice')

    ndb = NDBModule(module)

    if state == 'query' and username:
        user = ndb.get_user(username)
        if user == "":
            module.exit_json(
                msg='User {0} does not exist'.format(username))
        ndb.result['Result'] = user
        module.exit_json(**ndb.result)
    elif state == 'query' and not username:
        ndb.result['Result'] = ndb.get_user(username)
        module.exit_json(**ndb.result)
    elif state == 'absent':
        ndb.delete_user()
        ndb.result['changed'] = True
        module.exit_json(**ndb.result)
    elif state == 'present':
        ndb.create_user()
        module.exit_json(**ndb.result)

    module.fail_json(msg='Incorrect params passed', **ndb.result)


if __name__ == '__main__':
    main()

