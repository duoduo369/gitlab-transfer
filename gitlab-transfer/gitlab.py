#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import requests
import urlparse

GITLAB_HOST = ''  # something like https://www.xxx.com
GITLAB_PRIVATE_TOKEN = ''  # /profile/account --> Private token
PER_PAGE = 50

assert GITLAB_HOST, u'配置缺失'
assert GITLAB_PRIVATE_TOKEN, u'配置缺失'


def get_groups(page):
    url = urlparse.urljoin(
            GITLAB_HOST,
            '/api/v3/groups?private_token={}&all_available=1&per_page={}&page={}'.format(GITLAB_PRIVATE_TOKEN, PER_PAGE, page)
    )
    r = requests.get(url)
    return r.json()


def get_all_groups():
    page = 1
    groups = []
    print '============  start get groups ==========='
    while 1:
        print '============  get groups, page: {} ==========='.format(page)
        try:
            data = get_groups(page)
            if not data:
                break
            for each in data:
                group_id = each['id']
                groups.append(group_id)
        except Exception as ex:
            logging.error(ex, exc_info=1)
        finally:
            page += 1
    return sorted(groups)

def get_one_page_data(group_id, page):
    url = urlparse.urljoin(
            GITLAB_HOST,
            '/api/v3/groups/{}/projects?private_token={}&per_page={}&page={}'.format(group_id, GITLAB_PRIVATE_TOKEN, PER_PAGE, page)
    )
    r = requests.get(url)
    return r.json()


def get_group_projects(group_id):
    page = 1
    projects = []
    print '============  start get group projects ==========='
    while 1:
        print '============  get group projects, group_id:{}, page: {} ==========='.format(group_id, page)
        try:
            data = get_one_page_data(group_id, page=page)
            if not data:
                break
            for each in data:
                repo_url = each['ssh_url_to_repo']
                projects.append(repo_url)
        except Exception as ex:
            logging.error(ex, exc_info=1)
        finally:
            page += 1

    return projects


def main():
    groups = get_all_groups()
    projects = []
    for group_id in groups:
        group_projects = get_group_projects(group_id)
        if group_projects:
            projects.extend(group_projects)
    with open('/tmp/gitlab_projects.txt', 'w') as f:
        f.write('\n'.join(projects))

if __name__ == '__main__':
    main()
