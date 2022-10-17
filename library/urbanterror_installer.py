#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import urllib3
import requests
import json
import os
import hashlib

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: urbanterror_api

short_description: ""

description: ""

version_added: "0.1.0"
author: "..."
options:

'''

EXAMPLES = r"""

"""

RETURN = r"""


"""


class UrbanterrorInstaller(object):
    """
    Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.url = module.params.get("url")
        self.destination = module.params.get("destination")
        self.platform = module.params.get("platform")
        self.query = module.params.get("query")
        #
        self.engine = module.params.get("engine")
        self.server = module.params.get("server")
        self.updaterVersion = module.params.get("updaterVersion")
        self.version = module.params.get("version")

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def run(self):
        """

        """
        return_code, data = self.download_manifest()

        if return_code == 200:
            """
            """
            server_list = self.__parse_serverlist_section(data)

            self.download_server = server_list.get('url')

            result_data = self.__parse_files_section(data, 0)
            result_engine = self.__parse_files_section(data, 1)

            result = result_engine + result_data

            count_full = len(result)

            file_list = self.verify_data_integrity(result)
            count_download = len(file_list)

            if count_download > 0:
                state = self.__download(file_list)

                if state:
                    return dict(
                        changed=True,
                        failed=False,
                        msg=f"{count_full} files available, {count_download} new downloaded."
                    )
                else:
                    return dict(
                        changed=True,
                        failed=True,
                        msg=f"{count_full} files should be available, but not all can be downloaded."
                    )

                file_list = self.verify_data_integrity(result)
            else:
                return dict(
                    changed=False,
                    failed=False,
                    msg=f"{count_full} files up-to-date."
                )

        return dict(
            failed = True,
            msg="no manifest data available"
        )

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def verify_data_integrity(self, data):
        """
        """
        need_download = []

        for f in data:
            # self.module.log(msg="------------------------------------------------------------------")
            # self.module.log(msg=f"           {f}")
            directory = f.get('FileDir', "")
            # file_url = f.get('FileUrl')
            file_name = f.get('FileName')
            file_size = f.get('FileSize')
            checksum = f.get('FileMD5')
            # self.module.log(msg=f" directory : {directory}")
            # self.module.log(msg=f" file_name : {file_name}")
            # self.module.log(msg=f" file_size : {file_size}")
            # self.module.log(msg=f" file_url  : {file_url}")
            # self.module.log(msg=f" checksum  : {checksum}")
            # self.module.log(msg="------------------------------------------------------------------")

            if directory:
                dest_file = os.path.join(self.destination, directory, file_name)
            else:
                dest_file = os.path.join(self.destination, file_name)

            # self.module.log(msg=f" dest_file : {dest_file}")

            _size, _checksum = self.__file_info(dest_file)

            if int(_size) == int(file_size) and _checksum == checksum:
                self.module.log(msg=f"  - {dest_file} - file size and checksum okay")
            else:
                self.module.log(msg=f"  - {dest_file} - file size or checksum missmatch ...")
                need_download.append(f)

        return need_download

    def __download(self, data):
        """
        """
        should_counter = 0
        is_counter = len(data)

        for f in data:
            # self.module.log(msg="------------------------------------------------------------------")
            # self.module.log(msg=f"           {f}")

            directory = f.get('FileDir')
            file_url = f.get('FileUrl')
            file_name = f.get('FileName')
            file_size = f.get('FileSize')
            checksum = f.get('FileMD5')

            # self.module.log(msg=f" directory : {directory}")
            # self.module.log(msg=f" file_name : {file_name}")
            # self.module.log(msg=f" file_size : {file_size}")
            # self.module.log(msg=f" file_url  : {file_url}")
            # self.module.log(msg=f" checksum  : {checksum}")
            # self.module.log(msg="------------------------------------------------------------------")

            # self.module.log(
            #     msg=f"  - {file_name} : {file_size} : {checksum}"
            # )

            if isinstance(file_url, list):
                file_url = file_url[-1:][0]

            # Create target Directory
            if directory:
                try:
                    os.mkdir(os.path.join(self.destination, directory))
                except FileExistsError:
                    pass

                dest_file = os.path.join(self.destination, directory, file_name)
            else:
                dest_file = os.path.join(self.destination, file_name)

            # self.module.log(msg=f"  dest_file  : {dest_file}")

            with open(dest_file, "wb") as file:
                response = requests.get(f"{self.download_server}/{file_url}")
                file.write(response.content)
                file.close()

            _size, _checksum = self.__file_info(dest_file)

            if int(_size) == int(file_size) and _checksum == checksum:
                self.module.log(msg=f"  - {dest_file} - successfully downloaded")

                should_counter = should_counter + 1

        return is_counter == should_counter

    def __file_info(self, file_name):
        _size = 0
        _checksum = ""

        if os.path.exists(file_name):
            _size = os.stat(file_name).st_size
            _checksum = self.md5(file_name)

        return _size, _checksum

    def __parse_files_section(self, data, index=0):
        """
        """
        # result = {}
        files = data.get('Files')[int(index)].get('File')

        try:
            _list = json.loads(
                json.dumps(files)
            )

        except Exception as e:
            self.module.log(
                msg=f" exception: {e} ({type(e)})"
            )
            pass

        return _list

    def __parse_serverlist_section(self, data):
        """
        """
        result = {}
        server_list = data.get('ServerList')

        try:
            _list = json.loads(
                json.dumps(server_list)
            )

            result = dict(
                url=_list.get('Server').get('ServerURL'),
                id=_list.get('Server').get('ServerId'),
                name=_list.get('Server').get('ServerName'),
                location=_list.get('Server').get('ServerLocation')
            )

        except Exception as e:
            self.module.log(
                msg=" text: {} ({})".format(e, type(e))
            )
            pass

        return result

    def download_manifest(self):
        """
        """
        updater_data = dict()
        output_dict = dict()

        payload = {
            'platform': self.platform,
            'query': self.query,
            'password': '',
            'version': self.version,
            'engine': self.engine,
            'server': self.server,
            'updaterVersion': self.updaterVersion
        }
        # self.module.log(msg=f" payload: {payload}")

        code, ret = self.__call_url(data=payload)

        if code == 200 and len(ret) != 0:
            import xmltodict
            obj = xmltodict.parse(ret)
            updater_data = obj['Updater']
            # convert an OrderedDict to an regular dict
            output_dict = json.loads(json.dumps(updater_data))

        # self.module.log(msg=f"{type(output_dict)}")
        # self.module.log(msg=f"{json.dumps(output_dict, indent=2, sort_keys=True)}")

        return code, output_dict

    def __call_url(self, method='POST', data=None):
        """
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }

        try:
            if method == 'POST':
                ret = requests.post(
                    self.url,
                    data=data,
                    headers=headers,
                    verify=False
                )
            else:
                print("unsupported")

            ret.raise_for_status()

            # self.module.log(msg="------------------------------------------------------------------")
            # #self.module.log(msg=f" text    : {ret.text}")
            # self.module.log(msg=f" headers : {ret.headers}")
            # self.module.log(msg=f" code    : {ret.status_code}")
            # self.module.log(msg="------------------------------------------------------------------")

            return ret.status_code, ret.text

        except Exception as e:
            print(e)
            raise

# ===========================================
# Module execution.
#


def main():
    """
    """
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(required=True),
            destination=dict(required=True),
            # get=dict(required=True),
            engine=dict(required=False),
            server=dict(required=False),
            updaterVersion=dict(required=False),
            version=dict(required=False),
            platform=dict(required=False, default='Linux64'),
            query=dict(required=False, default='versionFiles'),
        ),
        supports_check_mode=False,
    )

    api = UrbanterrorInstaller(module)
    result = api.run()

    module.log(msg=f"= result : {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
