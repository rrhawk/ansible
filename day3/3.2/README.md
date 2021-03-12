# Asnible Day 3: Extending Ansible with Custom Modules

### Develop `wget` module

Create folder `./library` and place your code over there

Module works similar to `get_url`, accepts following parameters (get parameters description from `ansible-doc get_url`):

- version (=)
- dest (=)
- checksum (-)
- group (-)
- owner (-)
- mode (-)

Example:
```yaml
- name: Download Tomcat Archive
  wget:
    version: "8.5.58"
    dest: /opt
    checksum: "md5:9def3ec8010601a837373a1754e97d9d"
    group: tomcat
    owner: tomcat
    mode: 0644
```

### 2.2 Difference with `get_url` module

Original `get_url` module **always** downloads remote file, checks `checksum` - but only for validating downloaded file. We'd like to use this `checksum` for checking a file `dest` directory first, and **only** if it differs, it will proceed with downloading (performing update)

`checksum` can be `md5`, `sha1`, `sha256`, `sha384` or `sha512` - if available

### 2.3 Where to get tomcat binary and checksum?

Go to https://archive.apache.org/dist/tomcat/

### 2.3 Document this Module

```
ansible-doc wget -M path/to/custom/modules/
```

### 2.4 Use Ansible adhoc commad for testing your module


### 2.5 Create testing playbook

Define your case to test your `wget` module
