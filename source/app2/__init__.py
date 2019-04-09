import sys
import os

_app_version = '0.9.3'


def load_project_config(path):
    """Prepend path to sys.path, try to load project module, and return config.

    :return: dict
    """
    sys.path.insert(0, os.path.abspath(path))

    try:
        import project
        # return (f'{path}/{project.data_dir}',
        #         project.repo, project.author, _app_version)

    except (ImportError, IndexError):
        # return dict(data_dir='.',
        #             app_version=_app_version)
        print('PROBLEMS!')