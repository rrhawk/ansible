#!/usr/bin/env python

DOCUMENTATION = r'''
---
module: wget
version_added: 0.1
short_description: wget module for tomcat
description:   Module which download and update tomcat
#options:
 # "version" is mandatory, must be exist version of tomcat
 # "dest" is mandatory, folder for tomcat file
 # default "user" and "group" is "tomcat" "tomcat"
 # user and group must be created in system
 # for download in non /tmp folders could be use become: option
author:
    - "Sergey Kosolapov"
'''

EXAMPLES = """
# Standalone mode launch.
ansible localhost -c local -m wget
#example for testing
ansible localhost -M ./library -m wget -a 'dest='/tmp/1' src='https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.12/bin/apache-tomcat-8.0.12.tar.gz'' owner='user' group='user'' --become -K

"""

import requests
import os
import pwd
import grp
import hashlib
from ansible.module_utils.basic import *
#from urllib.parse import urlparse

def main():
    usr = pwd.getpwuid(os.getuid())[0]
    gr = pwd.getpwuid(os.getgid())[0]

    module = AnsibleModule(
        argument_spec=dict(
            src=dict(required=True),
            dest=dict(required=True),
            chksum=dict(required=False),
            group=dict(required=False, default=gr),
            owner=dict(required=False, default=usr),
            mode=dict(required=False, default='0644')

        )
    )
    ###env
    results = {}
    msg = module.params
    src = module.params["src"]
    owner = module.params["owner"]
    group = module.params["group"]
    filename = src[src.rfind("/")+1:]
    #url_for_name = urlparse(src)
    file_name = module.params["dest"] + '/' +  filename   ###os.path.basename(url_for_name.path)
    checksums = [
        'md5',
        'sha1',
        'sha256',
        'sha384',
        'sha512',
    ]
    try:
        pwd.getpwnam(owner)
    except KeyError:
        module.fail_json(msg='user ' + owner + ' not exist')
    try:
        grp.getgrnam(group)
    except KeyError:
        module.fail_json(msg='group ' + group + ' not exist')
    ###convert perrmissions from oct
    mode = int(module.params["mode"], 10)
    #checksum by default
    if module.params["chksum"]:
      checksum_type = module.params["chksum"].split(':')[0]
      checksum_value = module.params["chksum"].split(':')[1]
    ### check / in the end of the line with path
    if module.params["dest"][-1:] == '/':
        module.params["dest"] = module.params["dest"][:-1]

    ### if dest folder not exist create it
    if not os.path.exists(module.params["dest"]):
      os.makedirs(module.params["dest"])

    ###func for get hash of local file
    def get_hash_of_file(filename, check_type):
        with open(filename, 'rb') as f:
            if check_type == "md5":
                m = hashlib.md5()
            elif check_type == "sha1":
                m = hashlib.sha1()
            elif check_type == "sha256":
                m = hashlib.sha256()
            elif check_type == "sha384":
                m = hashlib.sha384()
            elif check_type == "sha512":
                m = hashlib.sha512()
            else:
                print("Wrong checksum type")

            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    ###func for write file to disk
    def write_file(filename, owner_f, group_f, mode_f):
        with open(filename, "wb") as file:
            response = requests.get(src)
            file.write(response.content)
            os.chmod(filename, mode_f)
            uid = pwd.getpwnam(owner_f).pw_uid
            gid = grp.getgrnam(group_f).gr_gid
            os.chown(filename, uid, gid)


    ###no file in local folder
    if not os.path.isfile(file_name):
        write_file(file_name, owner, group, mode)
        results.update({
            "changed": "True",
            "msg": "Download file",
            "meta": msg
        })
        module.exit_json(**results)
    ###if file exist check it's hash and compare with hash from repo
    else:
        local_checksum = get_hash_of_file(file_name, checksum_type)
        if local_checksum != checksum_value:
           write_file(file_name, owner, group, mode) ##update file if needed
           results.update({
               "changed": True,
               "msg": "Update file",
               "meta": msg
           })
           module.exit_json(**results)
        ###if file exists and hash are the same do nothing
        else:
            results.update({
                "changed": False,
                "msg": "File exists and hash are the same",
                "meta": msg
            })
            module.exit_json(**results)



main()
