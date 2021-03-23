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


        # NDB host specific information
        ndb_host=dict(type='str', default=""),
        ndb_port=dict(type='int', default=""),
        ndb_username=dict(type='str', default=""),
        ndb_password=dict(type='str', default="", no_log=True),
        ndb_slice=dict(type='str', default='default'),
        validate_certs=dict(type='bool', default=False),

        # NDB Device
        device_type=dict(type='str', default="", choices=['NDB', 'NXOS', 'ACI']),
        username=dict(type='str', default=""),
        password=dict(type='str', default="", no_log=True),
        profile=dict(type='str', default=""),
        device_name=dict(type='str', default=""),
        port=dict(type='str', default=""),
        tcam=dict(type='bool', default=False),
        tcamscale=dict(type='bool', default=True),
        reboot=dict(type='bool', default=False),
        hybrid=dict(type='bool', default=True),
        modify=dict(type='bool', default=True),
        apic_primary=dict(type='str', default=""),
        apic_secondary=dict(type='str', default=""),
        apic_tertiary=dict(type='str', default=""),

        state=dict(type='str', default='present', choices=['absent',
                                                           'present', 'query', 'modify']),

    )

    module = AnsibleModule(argument_spec=arg_spec,
                           supports_check_mode=True,
                           required_if=[['state', 'absent', ['username']],
                                        ['state', 'present', ['username']]])

    ndb_host = module.params.get('ndb_host')
    ndb_port = module.params.get('ndb_port')
    ndb_username = module.params.get('ndb_username')
    ndb_password = module.params.get('ndb_password')
    ndb_slice = module.params.get('ndb_slice')

    state = module.params.get('state')

    device_type = module.params.get('device_type')
    device_name = module.params.get('device_name')
    port = module.params.get('port')
    tcam = module.params.get('tcam')
    tcamscale = module.params.get('tcamscale')
    modify = module.params.get('modify')
    reboot = module.params.get('reboot')
    hybrid = module.params.get('hybrid')
    username = module.params.get('username')
    password = module.params.get('password')
    role = module.params.get('role')
    user_type = module.params.get('user_type')
    apic_primary = module.params.get('apic_primary')
    apic_secondary = module.params.get('apic_secondary')
    apic_tertiary = module.params.get('apic_tertiary')

    ndb = NDBModule(module)

    if state == 'query' and device_name:
        device = ndb.get_user(username)
        if device == "":
            module.exit_json(
                msg='Device {0} does not exist'.format(username))
        ndb.result['Result'] = user
        module.exit_json(**ndb.result)
    elif state == 'query' and device_type:
        ndb.result['Result'] = ndb.get_user(username)
        module.exit_json(**ndb.result)
    elif state == 'query':
        ndb.result['Result'] = ndb.get_user(username)
        module.exit_json(**ndb.result)
    elif state == 'absent':
        ndb.remove_device()
        ndb.result['changed'] = True
        module.exit_json(**ndb.result)
    elif state == 'present':
        ndb.create_device()
        module.exit_json(**ndb.result)