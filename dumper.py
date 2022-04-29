import os
import shlex
import subprocess
import datetime
from typing import Optional


def _generate_default_dump_name(use_gzip: bool) -> str:
    now = datetime.datetime.now()
    filename = 'dump_' + now.strftime('%m_%d_%H_%M')
    filename = filename + '.gz' if use_gzip else filename + '.sql'
    return filename


class DockerPostgresDumper:
    def __init__(self,
                 container_name: str,
                 db_name: str,
                 db_user: str):
        self.container_name = container_name
        self.db_name = db_name
        self.db_user = db_user

    def create_dump(self,
                    dump_folder: str,
                    dump_name: Optional[str] = None,
                    use_gzip: bool = True):
        if not os.path.exists(dump_folder):
            raise ValueError('Folder {} does not exist'.format(dump_folder))

        if dump_name is None:
            dump_name = _generate_default_dump_name(use_gzip)
        full_path = os.path.join(dump_folder, dump_name)

        command = self.get_command_to_execute(full_path, use_gzip)
        with subprocess.Popen(command, shell=True, stderr=subprocess.PIPE) as process:
            _, output = process.communicate()

        self._check_command_output(output)
        if not os.path.exists(full_path):
            pass
            # raise OSError('Error. Dump exit with status {}'.format(dump_operation_status))

        return full_path

    def get_command_to_execute(self,
                               filename: str,
                               use_gzip: bool):
        dump_subcommand = self._get_dump_subcommand()
        write_subcommand = self._get_write_subcommand(filename, use_gzip)
        command = '{} {}'.format(dump_subcommand, write_subcommand)
        return command

    def _get_dump_subcommand(self):
        base = 'docker exec {} pg_dump -U {} -c --if-exists -x {}'
        return base.format(self.container_name, self.db_user, self.db_name)

    def _get_write_subcommand(self,
                              filename: str,
                              use_gzip: bool):
        if use_gzip:
            command = '| gzip > {}'.format(filename)
        else:
            command = '> {}'.format(filename)
        return command

    def _check_command_output(self,
                              output: bytes):
        output = output.decode('utf-8')
        if output != '':
            raise OSError(output)

