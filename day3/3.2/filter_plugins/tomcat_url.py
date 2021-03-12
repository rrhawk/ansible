#!/usr/bin/python
import requests

class FilterModule(object):

    def filters(self):
        return {
            'tomcat_url': self.tomcat_url,
            'tomcat_checksum': self.tomcat_checksum

        }
    def tomcat_url( self, tomcat_version ):
        tomcat_version_major = tomcat_version.split('.')[0]
        tomcat_url = 'https://archive.apache.org/dist/tomcat/tomcat-' + \
                     tomcat_version_major + '/v' + tomcat_version + \
                     '/bin/apache-tomcat-' + tomcat_version + '.tar.gz'
        r = requests.head(tomcat_url)
        if r.status_code == 200:
            return tomcat_url
        else:
            return "none"
    def tomcat_checksum( self, tomcat_version ):
        checksums = [
            'md5',
            'sha1',
            'sha256',
            'sha384',
            'sha512'
        ]
        tomcat_version_major = tomcat_version.split('.')[0]
        tomcat_url = 'https://archive.apache.org/dist/tomcat/tomcat-' + \
                     tomcat_version_major + '/v' + tomcat_version + \
                     '/bin/apache-tomcat-' + tomcat_version + '.tar.gz'
        for check in checksums:
                checksum_value_url = tomcat_url + '.' + check
                r = requests.head(checksum_value_url)
                if r.status_code == 200:
                    checksum_type = check
                    checksum_value_online = requests.get(checksum_value_url)
                    checksum_value = check + ':' + \
                    checksum_value_online.text.split(' ')[0]
                    return checksum_value
        return "none"
