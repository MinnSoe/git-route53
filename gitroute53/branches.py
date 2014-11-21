import git


def get_remote_ref_names(repo_directory=None, remote_name='origin'):
	repo = git.Repo(repo_directory)
	remote = repo.remotes[remote_name]
	return [i.remote_head for i in remote.refs]
