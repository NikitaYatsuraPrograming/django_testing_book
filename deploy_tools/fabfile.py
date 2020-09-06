from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/NikitaYatsuraPrograming/django_testing_book.git'


def _create_directory_structure_if_necessary(site_folder):
    """
    Создание структуры каталога если нужно
    :param site_folder:
    :return:
    """

    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """
    Получить самый свежий код из git
    :param source_folder:
    :return:
    """

    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')


def _update_settings(source_folder, site_name):
    """
    Обновить настройки
    :param source_folder:
    :param site_name:
    :return:
    """

    settings_path = source_folder + '/app/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        "ALLOWED_HOSTS = .+$",
        f'ALLOWED_HOSTS= ["{site_name}"]')

    secret_key_file = source_folder + '/app/secret_key.py'
    if not exists(secret_key_file):
        chars = '#_(g7&&=s)^)_&ncm8g5c32_kyn+%wvbakh9x=ck=!q!t72+x#'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    """
    Обновить виртуальную среду
    :param source_folder:
    :return:
    """

    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip3'):
        run(f'python3 -m venv {virtualenv_folder}')

    run(f'{virtualenv_folder}/bin/pip3 install -r {source_folder}/requirements.txt')
    
    
def _update_static_files(source_folder):
    """
    Обновить статические файлы
    :param source_folder:
    :return:
    """

    run(
        f'cd {source_folder} && ../virtualenv/bin/python3 manage.py migrate --noinput'
    )


def deploy():
    """
    Развернуть
    :return:
    """

    run('apt-get install python3 git-all python3-pip python3-venv')

    site_folder = f'/root/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    # _update_database(source_folder)
