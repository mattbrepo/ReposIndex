#
# Generates the README.md containing the list of all my Github repositories
#
import os

class Repo(object):
  def __init__(self, repoName, name, description, languages, year):
    self.name = name
    self.description = description
    self.languages = languages
    self.year = year
    self.GithubURL = 'https://github.com/mattbrepo/' + repoName

def getRepo(repoName, readmeFilePath):
  with open(readmeFilePath) as f:
    content = f.readlines()

  name = content[0].replace('# ', '').replace('\n', '')
  description = content[1].replace('\n', '')
  language = []
  year = ''
  for str in content:
    if str.startswith('**Language'):
      languages = str.replace('**Language: ', '').replace('**', '').replace('\n', '').split(' / ')
    if str.startswith('**Start'):
      year = str.replace('**Start: ', '').replace('**', '').replace('\n', '')

  if year == '':
    print(readmeFilePath)

  return Repo(repoName, name, description, languages, int(year))

def getRepos():
  repos = []
  for (dirpath, dirnames, filenames) in os.walk('..'):
    if dirpath.startswith('..\\__'): # exclude unfinished repos
      continue
    if dirpath.startswith('..\\ReposIndex'): # exclude this repo
      continue

    for file in filenames:
      if file == 'README.md':
        readmeFilepath = os.path.join(dirpath, file)
        print('found: ' + readmeFilepath)
        repoName = dirpath.replace('..\\', '')
        r = getRepo(repoName, readmeFilepath)
        if r != None:
          repos.append(r)

  return repos

def getRepoItemStr(repo):
  return '[' + repo.name + '](' + repo.GithubURL + '): ' + repo.description + '\n'

#
# Main
#

# get repos data
repos = getRepos()

# generate README.md
with open('README.md', 'w') as f:
  f.write('# ReposIndex\n')
  f.write('My Github repositories index\n')
  f.write('\n')
  
  f.write('- [Alphabetic order](#alphabetic-order)\n')
  f.write('- [Ordered by year](#ordered-by-year)\n')
  f.write('- [Ordered by language](#ordered-by-language)\n')
  f.write('\n\n')

  f.write('## Alphabetic order\n')
  repos.sort(key=lambda x: x.name)
  for idx, repo in enumerate(repos):
    f.write(str(idx + 1) + '. ' + getRepoItemStr(repo))
  f.write('\n')

  f.write('## Ordered by year\n')
  repos.sort(key=lambda x: x.year, reverse=True)
  lastYearStr = ''
  for repo in repos:
    repoYearStr = str(repo.year)
    if lastYearStr != repoYearStr:
      f.write('\n### ' + repoYearStr + '\n')
      lastYearStr = repoYearStr

    f.write('- ' + getRepoItemStr(repo))
  f.write('\n')

  f.write('## Ordered by language\n')
  repos.sort(key=lambda x: x.name)
  languages = { lang for repo in repos for lang in repo.languages}
  languages = list(languages)
  languages.sort()
  for lang in languages:
    f.write('\n### ' + lang + '\n')
    for repo in repos:
      if lang in repo.languages:
        f.write('- ' + getRepoItemStr(repo))
  f.write('\n')

