import os
import shutil
import random
import asyncio
import tempfile

import pytest
from aioes import Elasticsearch
from aioes.exception import NotFoundError


@pytest.fixture
def index():
    return 'test_elasticsearch'


@pytest.fixture
def client(es_params, index, loop, repo_name, snapshot_name):
    client = Elasticsearch([{'host': es_params['host']}], loop=loop)
    try:
        loop.run_until_complete(client.delete(index, '', ''))
    except NotFoundError:
        pass
    yield client

    # cleaning up just in case
    try:
        loop.run_until_complete(
            client.snapshot.delete(repo_name, snapshot_name))
    except NotFoundError:
        pass
    try:
        loop.run_until_complete(
            client.snapshot.delete_repository(repo_name))
    except NotFoundError:
        pass

    client.close()


@pytest.fixture
def repo_path():
    '''
    Sice elasticsearch may be launched under the other user,
    tempfile.TemporaryDirectory can't be used, because python
    can't cleanup it after elasticsearch user.
    So we are just leaving it there.
    '''
    characters = "abcdefghijklmnopqrstuvwxyz0123456789_"
    temp_dir = tempfile.gettempdir()
    temp_prefix = '/' + tempfile.gettempprefix()
    temp_name = temp_prefix + ''.join(
        [random.choice(characters) for _ in range(8)]
    )

    dir_path = os.path.join(temp_dir + temp_name)
    os.makedirs(dir_path)
    yield dir_path

    try:
        shutil.rmtree(dir_path)
    except PermissionError:
        # if subdirs were created by other user
        pass


@pytest.fixture
def repo_name():
    return 'test_repo'


@pytest.fixture
def snapshot_name():
    return 'test_snapshot'


@asyncio.coroutine
def test_repository(client, repo_path, repo_name):
    ret = yield from client.snapshot.get_repository()
    assert not ret

    b = {
        "type": "fs",
        "settings": {
            "location": repo_path,
        }
    }
    ret = yield from client.snapshot.create_repository(repo_name, b)
    assert ret['acknowledged']

    ret = yield from client.snapshot.get_repository(repo_name)
    assert ret[repo_name] == b

    ret = yield from client.snapshot.delete_repository(repo_name)
    assert ret['acknowledged']


@asyncio.coroutine
def test_snapshot(client, repo_name, repo_path, snapshot_name):
    # creating index
    yield from client.create(
        index, 'tweet',
        {
            'user': 'Bob',
        },
        '1'
    )

    # creating repo
    repo_body = {
        "type": "fs",
        "settings": {
            "location": repo_path,
        }
    }

    ret = yield from client.snapshot.create_repository(
        repo_name, repo_body)
    assert ret['acknowledged']

    # creating snapshot
    yield from client.snapshot.create(
        repo_name, snapshot_name,
        wait_for_completion=True
    )

    # checking that snapshot was created
    ret = yield from client.snapshot.get(repo_name, snapshot_name)
    assert ret['snapshots'][0]['snapshot'] == snapshot_name
    assert ret['snapshots'][0]['state'] == 'SUCCESS'

    # restoring snapshot
    restore_body = {
        "indices": index,
    }
    yield from client.indices.close(index)
    ret = yield from client.snapshot.restore(
        repo_name, snapshot_name,
        body=restore_body
    )
    assert ret['accepted']

    # deleting snapshot
    ret = yield from client.snapshot.delete(
        repo_name, snapshot_name,
    )
    assert ret['acknowledged']

    # deleting repo
    ret = yield from client.snapshot.delete_repository(
        repo_name
    )
    assert ret['acknowledged']


@asyncio.coroutine
def test_status(client):
    ret = yield from client.snapshot.status()
    assert {'snapshots': []} == ret
