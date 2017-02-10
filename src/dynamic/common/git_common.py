from src.dynamic.common import windows_common
from git.repo.base import *

def git_blame(filename, line):
    #repoObject = Repo('D:/Progamming/testrepo')
    repo = Repo.clone_from(url='https://github.com/Streetfighter4/TESTREPO.git', to_path='D:/Progamming/testrepo1')
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

    windows_common.rmtree('D:/Progamming/testrepo1')
    return author