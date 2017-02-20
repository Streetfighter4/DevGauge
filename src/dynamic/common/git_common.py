import os
import requests

from git.repo.base import *

def git_blame(git_repo, filename, line):
    git_repo_name = git_repo.split("/")[-1]
    repo_path = '/home/devmeter/devmeter/repos/' + git_repo_name + '/'
    if not os.path.exists(repo_path):
        repo = Repo.clone_from(url=git_repo, to_path=repo_path)
    else:
        repo = Repo(repo_path)

    returnOfGitBlame = repo.blame('HEAD', file=repo_path + filename)
    count = 0
    author = None
    for pair in returnOfGitBlame:
        count += len(pair[1])
        if count >= line:
            author = pair[0].author
            break

    return author.email