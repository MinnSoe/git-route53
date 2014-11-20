import pytest
import git
import shutil
import os

import gitroute53


def _create_hello_file(in_folder):
    with open(in_folder + '/hello', 'w') as f:
        f.write('Hello')


def _create_first_commit(repo):
    index = repo.index
    _create_hello_file(repo.working_dir)
    index.add(['hello'])
    index.commit('Salut! Hola! Ciao!')


def _create_sample_remote_refs(repo, sha):
    for name in ['HEAD', 'master', 'remote-branch', 'feature']:
        repo.git.update_ref('refs/remotes/origin/%s' % name, sha)


def _create_sample_refs(repo):
    commit_sha = repo.head.object.hexsha
    repo.create_head('local-branch')
    repo.create_remote('origin', 'NO-URL')
    _create_sample_remote_refs(repo, commit_sha)


def create_tmp_repo(folder='tmp/repo'):
    repo = git.Repo.init(folder)
    _create_first_commit(repo)
    _create_sample_refs(repo)
    return repo



@pytest.fixture(scope='module')
def repo(request):
    folder = 'tmp/git_repo'
    r = create_tmp_repo(folder)

    def remove_repo():
        shutil.rmtree(folder)

    request.addfinalizer(remove_repo)

    return r


@pytest.mark.parametrize('name', ['HEAD', 'master', 'remote-branch', 'feature'])
def test_get_remote_ref_names(repo, name):
    assert name in gitroute53.get_remote_ref_names(repo.working_dir)


@pytest.mark.parametrize('name', ['HEAD', 'master', 'remote-branch', 'feature'])
def test_remote_ref_names_in_current_git_directory(repo, name):
    prev_working_dir = os.getcwd()
    os.chdir(repo.working_dir)
    assert name in gitroute53.get_remote_ref_names()
    os.chdir(prev_working_dir)


def test_no_local_refs_included(repo):
    remote_ref_names = gitroute53.get_remote_ref_names(repo.working_dir)
    assert 'local-branch' not in remote_ref_names
