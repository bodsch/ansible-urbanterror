#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import urllib3
import requests
import json

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


class UrbanterrorAPI(object):
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
        self.get = module.params.get("get")
        self.platform = module.params.get("platform")
        self.query = module.params.get("query")

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
            if(self.get == 'api_version'):
                result = self.__parse_api_version(data)

                return dict(
                    failed=False,
                    api_version=result
                )

            if(self.get == 'version'):
                result = self.__parse_version(data)

                return dict(
                    failed=False,
                    versions=result
                )

            if(self.get == 'server_list'):
                result = self.__parse_server_list(data)

                return dict(
                    failed=False,
                    server_list=result
                )

            if(self.get == 'engine_list'):
                result = self.__parse_engine_list(data)

                return dict(
                    failed=False,
                    engine_list=result
                )

        self.module.log("--------------------------------------")
        self.module.log(
            msg="result {} ({})".format(result, type(result))
        )
        self.module.log("--------------------------------------")

        return dict(
            failed = True
        )

    def __parse_api_version(self, data):
        """
        """
        result = {}
        api_version = data.get('APIVersion')

        try:
            _list = json.loads(
                json.dumps(api_version)
            )
            result = _list

        except Exception as e:
            self.module.log(
                msg=" text: {} ({})".format(e, type(e))
            )
            pass

        return result

    def __parse_version(self, data):
        """
        """
        result = {}

        version_list = data.get('VersionList')

        self.module.log(
            msg=" - {} ({})".format(version_list, type(version_list))
        )

        try:
            versions = json.loads(
                json.dumps(version_list)
            )

            for i in versions.get('Version'):
                i['id'] = i.get('VersionNumber')
                i['version'] = i.get('VersionName').split(' ')[0]
                if(len(i.get('VersionName').split(' ')) == 2):
                    i['latest'] = True
                else:
                    i['latest'] = False

                result[i['version']] = dict(
                    latest=i.get('latest'),
                    id=i.get('id'),
                    release_date=i.get('ReleaseDate')
                )
        except Exception as e:
            self.module.log(
                msg=" text: {} ({})".format(e, type(e))
            )
            pass

        return result

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

    def __parse_engine_list(self, data):
        """
        """
        result = {}
        engine_list = data.get('EngineList')

        try:
            _list = json.loads(
                json.dumps(engine_list)
            )
            for i in _list.get('Engine'):
                _engine_name = i.get('EngineName').split(' ')
                _default_engine = False

                if('default' in _engine_name[1].lower()):
                    _default_engine = True

                i['name'] = _engine_name[0].lower()

                result[i['name']] = dict(
                    directory=i.get('EngineDir'),
                    id=int(i.get('EngineId')),
                    name=i.get('EngineName'),
                    launch_string=i.get('EngineLaunchString'),
                    default=_default_engine
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
            get=dict(required=True),
            engine=dict(required=False),
            server=dict(required=False),
            updaterVersion=dict(required=False),
            version=dict(required=False),
            platform=dict(required=False, default='Linux64'),
            query=dict(required=False, default='versionInfo'),
        ),
        supports_check_mode=False,
    )

    api = UrbanterrorAPI(module)
    result = api.run()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
