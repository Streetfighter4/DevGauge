from git import Repo


repo = Repo('./repo')

git = repo.git

print git.blame('master', 'file.txt', show_email=True)
