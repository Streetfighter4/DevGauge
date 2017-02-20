import os
import requests

from dynamic.common import windows_common
from git.repo.base import *

def git_blame(git_repo, filename, line):
    git_repo_name = git_repo.split("/")[-1]
    if not os.path.exists('D:/Progamming/'+ git_repo_name):
        repo = Repo.clone_from(url=git_repo, to_path='D:/Progamming/'+ git_repo_name)
    else:
        repo = Repo('D:/Progamming/'+ git_repo_name)


    print (repo)
    returnOfGitBlame = repo.blame('HEAD', file=filename)
    print (returnOfGitBlame)
    count = 0
    author = None
    for pair in returnOfGitBlame:
        count += len(pair[1])
        if count >= line:
            author = pair[0].author
            break

    return requests.get("https://api.github.com/users/" + author)['email']