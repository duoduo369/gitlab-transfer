#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import logging
import time

from git import Repo

CLONE_PATH = '/data/apps'
GIT_REPO_FILE_PATH = '/tmp/gitlab_projects.txt'
OSC_REPO_BASE = 'https://gitee.com/duoduo369/'
LIMIT = 5
SLEEP_TIME = 3

def get_repo_pairs(offset, limit, filter_fun=None):
    pairs = []
    with open(GIT_REPO_FILE_PATH) as f:
        for line in f:
            repo = line.strip()
            repo_name = line.split('/')[-1].split('.')[0]
            pairs.append((repo_name, repo))
    if filter_fun:
        pairs = filter_fun(pairs)
    return pairs[offset: limit]


def filter_unlike_projects(pairs):
    return [each for each in pairs if 'test' not in each[0]]


def clone_projects(offset, limit):
    pairs = get_repo_pairs(offset, limit, filter_unlike_projects)
    for pair in pairs:
        repo_name, repo = pair
        path = os.path.join(CLONE_PATH, repo_name)
        if os.path.exists(path):
            continue
        print '============ clone {} ======='.format(repo_name)
        try:
            Repo.clone_from(repo, path)
            time.sleep(SLEEP_TIME)
        except Exception as ex:
            logging.error(ex, exc_info=1)


def new_project_and_push(offset, limit):
    pairs = get_repo_pairs(offset, limit, filter_unlike_projects)
    for pair in pairs:
        repo_name, repo = pair
        path = os.path.join(CLONE_PATH, repo_name)
        if not os.path.exists(path):
            continue
        # 创建开源中国项目
        osc_repo = '{}{}.git'.format(OSC_REPO_BASE, repo_name)
        try:
            print '=============  create repo {} =========='.format(repo_name)
            raise NotImplementedError(' 手动在 gitee 创建一个项目，拿到 curl，里面的 token 等，例如下面')
            cmd = '''
                curl 'https://gitee.com/duoduo369/projects' -H 'authority: gitee.com' -H 'accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' -H 'sec-fetch-dest: empty' -H 'x-csrf-token: IrmAYsnEyQ=' -H 'x-requested-with: XMLHttpRequest' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' -H 'origin: https://gitee.com' -H 'sec-fetch-site: same-origin' -H 'sec-fetch-mode: cors' -H 'referer: https://gitee.com/projects/new' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6' -H 'cookie: user_locale=zh-CN; oschina_new_user=false; gr_user_id=7fd42a24-ea1e-4393-; grwng_uid-45da-9b1e-76f4a983cbf1; Serve_State=true; tz=Asia%2FShanghai; Hm_lvt_24f17767262929947cc3631f99bfd274=1581306676; Hm_lpvt_24f17767262929947cc3631f99bfd274=1581307178; gitee-session-n=BAhONjM2OWEyODIxMjk3OWY4Y2VlMWFiBjsAVEkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsHWwZpA4suAUkiIiQyYSQxMCRNc09xQjhkSlU0ZUFEWENpWTg0RVkuBjsAVEkiHXdhcmRlbi51c2VyLnVzZXIuc2Vzc2lvbgY7AFR7BkkiFGxhc3RfcmVxdWVzdF9hdAY7AFRJdToJVGltZQ1DBR7AH1dn7gk6DW5hbm9fbnVtaQIQAjoNbmFub19kZW5pBjoNc3VibWljcm8iB1KAOgl6b25lSSIIVVRDBjsARkkiEF9jc3JmX3Rva2VuBjsARkkiMVFjYUJZRklHWUZnVUtSczgrY2F3RlFmTG4rWCtuWHFBeklybUFZc25FeVE9BjsARg%3D%3D--ce7172cc3e34e4f990b0db77a6612602a982411b' --data 'utf8=%E2%9C%93&authenticity_token=QcaB%2BX%2BnXqAzIrmAYsnEyQ%3D&project%5Bname%5D={}&project%5Bnamespace_path%5D=duoduo369&project%5Bpath%5D={}&project%5Bdescription%5D=&project%5Bpublic%5D=0&language=0&ignore=no&license=no&model=1&prod=master&dev=develop&feat=feature&rel=release&bugfix=hotfix&tag=&project%5Bimport_url%5D=&user_sync_code=&password_sync_code=' --compressed
                '''.format(repo_name, repo_name) # 抓一下 gitlab 创建「 私有」项目的 curl
            os.system(cmd)
        except Exception as ex:
            logging.error(ex, exc_info=1)
        time.sleep(SLEEP_TIME)
        try:
            print '=============  push repo {} =========='.format(repo_name)
            os.system('cd {} && git push {} master'.format(path, osc_repo))
        except Exception as ex:
            logging.error(ex, exc_info=1)
        else:
            time.sleep(SLEEP_TIME)
        time.sleep(SLEEP_TIME)


def fetch_and_push(offset, limit, branchs=['develop', 'master', 'dev']):
    pairs = get_repo_pairs(offset, limit, filter_unlike_projects)
    for pair in pairs:
        repo_name, repo = pair
        path = os.path.join(CLONE_PATH, repo_name)
        osc_repo = '{}{}.git'.format(OSC_REPO_BASE, repo_name)
        if not os.path.exists(path):
            continue
        for branch in branchs:
            try:
                print '=============  push repo {} =========='.format(repo_name)
                cmd1 = 'cd {} &&git fetch origin {}:{}'.format(path, branch, branch)
                cmd2 = 'cd {} && git push {} {}:{}'.format(path, osc_repo, branch, branch)
                print cmd1
                print cmd2
                os.system(cmd1)
                os.system(cmd2)
            except Exception as ex:
                logging.error(ex, exc_info=1)
            else:
                time.sleep(SLEEP_TIME)
            time.sleep(SLEEP_TIME)


def main():
    offset = 0
    limit = LIMIT
    while offset < 1000:
        clone_projects(offset, offset + limit)
        new_project_and_push(offset, offset + limit)
        fetch_and_push(offset, offset+limit)
        offset += limit

if __name__ == '__main__':
    main()
