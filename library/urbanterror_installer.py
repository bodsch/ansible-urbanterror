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
        return_code, data = self.__api_data()

        if(return_code == 200):
            """
            """
            server_list = self.__parse_server_list(data)

            self.download_server = server_list.get('url')

            result = self.__parse_files(data)
            count_full = len(result)

            file_list = self.__check_data(result)
            count_download = len(file_list)

            if count_download > 0:
                state = self.__download(file_list)

                if state:
                    return dict(
                        changed=True,
                        failed=False,
                        msg="{0} files available, {1} downloaded".format(count_full, count_download)
                    )
                else:
                    return dict(
                        changed=True,
                        failed=True,
                        msg="{0} files should be available, but not all can be downloaded".format(count_full)
                    )

                file_list = self.__check_data(result)
            else:
                return dict(
                    changed=False,
                    failed=False,
                    msg="{0} files up-to-date".format(count_full)
                )

        return dict(
            failed = True,
            msg="no API data available"
        )

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def __check_data(self, data):
        """
        """
        need_download = []

        for f in data:
            directory = f.get('FileDir')
            # url = f.get('FileUrl')[-1:][0]
            file_name = f.get('FileName')
            file_size = f.get('FileSize')
            checksum = f.get('FileMD5')

            dest_file = os.path.join(self.destination, directory, file_name)

            _size, _checksum = self.__file_info(dest_file)

            if int(_size) == int(file_size) and _checksum == checksum:
                self.module.log(
                    msg="  - {0} - file okay".format(dest_file)
                )
            else:
                self.module.log(
                    msg="  - {0} - missmatch ...".format(dest_file)
                )
                need_download.append(f)

        return need_download

    def __download(self, data):
        """
        """
        self.module.log("download files")

        should_counter = 0
        is_counter = len(data)

        for f in data:
            directory = f.get('FileDir')
            url = f.get('FileUrl')[-1:][0]
            file_name = f.get('FileName')
            file_size = f.get('FileSize')
            checksum = f.get('FileMD5')

            # self.module.log(
            #     msg="  - {} : {} : {}".format(file_name, file_size, checksum)
            # )

            try:
                # Create target Directory
                os.mkdir(os.path.join(self.destination, directory))
            except FileExistsError:
                pass

            dest_file = os.path.join(self.destination, directory, file_name)

            with open(dest_file, "wb") as file:
                response = requests.get("{}/{}".format(self.download_server, url))
                file.write(response.content)
                file.close()

            _size, _checksum = self.__file_info(dest_file)

            if int(_size) == int(file_size) and _checksum == checksum:
                self.module.log(
                    msg="  -> successful"
                )

                should_counter = should_counter + 1

        return is_counter == should_counter

    def __file_info(self, file_name):
        _size = 0
        _checksum = ""

        if os.path.exists(file_name):
            _size = os.stat(file_name).st_size
            _checksum = self.md5(file_name)

        return _size, _checksum

    def __parse_files(self, data):
        """
        """
        # result = {}
        files = data.get('Files')[0].get('File')

        try:
            _list = json.loads(
                json.dumps(files)
            )

        except Exception as e:
            self.module.log(
                msg=" exception: {} ({})".format(e, type(e))
            )
            pass

        return _list

    def __parse_server_list(self, data):
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

    def __api_data(self):
        """
        """
        updater_data = dict()

        payload = {
            'platform': self.platform,
            'query': self.query,
            'password': '',
            'version': self.version,
            'engine': self.engine,
            'server': self.server,
            'updaterVersion': self.updaterVersion
        }

        self.module.log(msg=" payload: {}".format(payload))

        code, ret = self.__call_url(
            data=payload
        )

        if(code == 200 and len(ret) != 0):
            import xmltodict
            # obj = untangle.parse(XML)
            obj = xmltodict.parse(
                ret
            )
            updater_data = obj['Updater']

        return code, updater_data

    def __call_url(self, method='POST', data=None):
        """
        """

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }

        self.module.log(msg=" data   : {}".format(data))
        self.module.log(msg=" headers: {}".format(headers))

        try:
            if(method == 'POST'):
                ret = requests.post(
                    self.url,
                    data=data,
                    headers=headers,
                    verify=False
                )

            else:
                print("unsupported")

            ret.raise_for_status()

            self.module.log(msg="------------------------------------------------------------------")
            # self.module.log(msg=" text    : {}".format(ret.text))
            self.module.log(msg=" headers : {}".format(ret.headers))
            self.module.log(msg=" code    : {}".format(ret.status_code))
            self.module.log(msg="------------------------------------------------------------------")

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

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
