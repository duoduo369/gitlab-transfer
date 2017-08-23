#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import logging
import time

from git import Repo

CLONE_PATH = '/data/apps'
GIT_REPO_FILE_PATH = '/tmp/gitlab_projects.txt'
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
        osc_repo = 'https://git.oschina.net/duoduo369/{}.git'.format(repo_name)
        try:
            print '=============  create repo {} =========='.format(repo_name)
            os.system(
                '''''' # 抓一下 gitlab 创建「 私有」项目的 curl
            )
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
            try:
                os.system('rm -rf {}'.format(path))
            except Exception as ex:
                logging.error(ex, exc_info=SLEEP_TIME)
        time.sleep(SLEEP_TIME)


def main():
    offset = 0
    limit = LIMIT
    while offset < 1000:
        clone_projects(offset, offset + limit)
        new_project_and_push(offset, offset + limit)
        offset += limit

if __name__ == '__main__':
    main()
