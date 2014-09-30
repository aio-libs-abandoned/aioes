import os
import shutil
import random
import asyncio
import tempfile
import unittest
from aioes import Elasticsearch
from aioes.exception import NotFoundError


class TestSnapshot(unittest.TestCase):

    def _create_temp_dir(self):
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
        return dir_path

    def _cleanup_dirs(self, dir_path):
        try:
            shutil.rmtree(dir_path)
        except PermissionError:
            # if subdirs were created by other user
            pass

    def setUp(self):
        self._index = 'elastic_search'
        self.repo_name = 'test_repo'
        self.repo_path = self._create_temp_dir()
        # otherwise elasticsearch can't access it
        os.chmod(self.repo_path, 0o777)

        self.snapshot_name = 'test_snapshot'
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.cl = Elasticsearch([{'host': 'localhost'}], loop=self.loop)
        self.addCleanup(self.cl.close)
        try:
            self.loop.run_until_complete(
                self.cl.delete(self._index, refresh=True))
        except NotFoundError:
            pass

    def tearDown(self):
        self._cleanup_dirs(self.repo_path)
        # cleaning up just in case
        try:
            self.loop.run_until_complete(
                self.cl.snapshot.delete(self.repo_name, self.snapshot_name))
        except NotFoundError:
            pass
        try:
            self.loop.run_until_complete(
                self.cl.snapshot.delete_repository(self.repo_name))
        except NotFoundError:
            pass

        # close loop
        self.loop.close()

    def test_repository(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.snapshot.get_repository()
            self.assertFalse(ret)

            b = {
                "type": "fs",
                "settings": {
                    "location": self.repo_path,
                }
            }
            ret = yield from self.cl.snapshot.create_repository(
                self.repo_name, b
            )
            self.assertTrue(ret['acknowledged'])

            ret = yield from self.cl.snapshot.get_repository(
                self.repo_name
            )
            self.assertEqual(ret[self.repo_name], b)

            ret = yield from self.cl.snapshot.delete_repository(
                self.repo_name
            )
            self.assertTrue(ret['acknowledged'])

        self.loop.run_until_complete(go())

    def test_snapshot(self):
        @asyncio.coroutine
        def go():
            # creating index
            yield from self.cl.create(
                self._index, 'tweet',
                {
                    'user': 'Bob',
                },
                '1'
            )

            # creating repo
            repo_body = {
                "type": "fs",
                "settings": {
                    "location": self.repo_path,
                }
            }

            ret = yield from self.cl.snapshot.create_repository(
                self.repo_name, repo_body
            )
            self.assertTrue(ret['acknowledged'])

            # creating snapshot
            yield from self.cl.snapshot.create(
                self.repo_name, self.snapshot_name,
                wait_for_completion=True
            )

            # checking that snapshot was created
            ret = yield from self.cl.snapshot.get(
                self.repo_name, self.snapshot_name,
            )
            self.assertEqual(
                ret['snapshots'][0]['snapshot'],
                self.snapshot_name
            )
            self.assertEqual(
                ret['snapshots'][0]['state'],
                'SUCCESS'
            )

            # restoring snapshot
            restore_body = {
                "indices": self._index,
            }
            yield from self.cl.indices.close(self._index)
            ret = yield from self.cl.snapshot.restore(
                self.repo_name, self.snapshot_name,
                body=restore_body
            )
            self.assertTrue(ret['accepted'])

            # deleting snapshot
            ret = yield from self.cl.snapshot.delete(
                self.repo_name, self.snapshot_name,
            )
            self.assertTrue(ret['acknowledged'])

            # deleting repo
            ret = yield from self.cl.snapshot.delete_repository(
                self.repo_name
            )
            self.assertTrue(ret['acknowledged'])

        self.loop.run_until_complete(go())

    def test_status(self):
        @asyncio.coroutine
        def go():
            ret = yield from self.cl.snapshot.status()
            self.assertEqual({'snapshots': []}, ret)

        self.loop.run_until_complete(go())
