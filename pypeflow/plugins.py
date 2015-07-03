# coding: utf-8
from concurrent.futures import ThreadPoolExecutor
import re
import asyncio
from time import time


class Bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BasePlugin(object):

    name = 'BasePlugin'
    description = ''

    def __init__(self, filter_pattern=None, filter_collections=None):
        self.filter_pattern = filter_pattern
        self.filter_collections = filter_collections or []
        self.files_created = []

    def log_error(self, message):
        print('{}{}{}'.format(Bcolors.FAIL, message, Bcolors.ENDC))

    def log_sucess(self, message):
        print('{}{}{}'.format(Bcolors.OKGREEN, message, Bcolors.ENDC))

    def get_filtered_files(self, pypeflow, files):
        filtered_files = {}
        filter_pattern = self.filter_pattern
        filter_collections = self.filter_collections

        if filter_collections:
            for collection in filter_collections:
                for file in pypeflow.collections.get(collection, {}).get('files', []):
                    if filter_pattern and re.search(filter_pattern, file['path']):
                        filtered_files[file['path']] = file
                    else:
                        filtered_files[file['path']] = file

        elif filter_pattern:
            for path, file in files.items():
                if re.search(filter_pattern, path):
                    filtered_files[path] = file

        else:
            filtered_files = files

        return filtered_files

    def pre_run(self, pypeflow, files):
        pass

    def post_run(self, pypeflow, files):
        pass

    def run(self, pypeflow, files):
        started_at = time()
        filtered_files = self.get_filtered_files(pypeflow, files)

        self.pre_run(pypeflow, filtered_files)

        operations = self.process_files(pypeflow, filtered_files)

        for operation, data in operations:
            getattr(self, operation)(pypeflow, **data)

        self.post_run(pypeflow, filtered_files)

        self.log_sucess('{}: processed {} files in {:.5f}s'.format(self.name, len(filtered_files), time()-started_at))

    def process_files(self, pypeflow, files):
        operations = []
        for path, file in files.items():
            operation_list = self.process_file(path, file)
            if operation_list:
                operations.extend(operation_list)

        return (operation for operation in operations if operation)

    def process_file(self, path, file):
        raise NotImplementedError

    def add_file(self, pypeflow, file):
        pypeflow.add_file(file)

    def remove_file(self, pypeflow, path):
        pypeflow.remove_file(path)

    def rename_file(self, pypeflow, old_path, new_path):
        pypeflow.rename_file(old_path, new_path)

    def update_file(self, pypeflow, path, file):
        pypeflow.update_file(path, file)


class BaseAsyncPlugin(BasePlugin):

    name = 'BaseAsyncPlugin'

    def process_files(self, pypeflow, files):
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        loop.run_until_complete(self.process_files_async(future, files))
        operations = future.result()
        return (operation for operation in operations if operation)

    @asyncio.coroutine
    def process_files_async(self, future, files):
        coroutines = [self.process_file(path, file) for path, file in files.items()]
        result = yield from asyncio.gather(*coroutines)
        operations = []
        for operation_list in result:
            if operation_list:
                operations.extend(operation_list)
        future.set_result(operations)

    @asyncio.coroutine
    def process_file(self, path, file):
        raise NotImplementedError


class BaseThreadPlugin(BasePlugin):

    name = 'BaseThreadPlugin'

    def __init__(self, filter_pattern=r'\.html', filter_collections=None, max_workers=3):
        super().__init__(filter_pattern=filter_pattern, filter_collections=filter_collections)
        self.max_workers = max_workers

    def process_files(self, pypeflow, files):

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            result = [executor.submit(self.process_file, path, file) for path, file in files.items()]
            result = [p.result() for p in result]

        operations = []
        for operation_list in result:
            if operation_list:
                operations.extend(operation_list)

        return operations

    def process_file(self, path, file):
        raise NotImplementedError
