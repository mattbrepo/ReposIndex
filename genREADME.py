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
  f.write('My Github repositories index.\n')
  f.write('\n')
  
  f.write('- [Ordered by year](#ordered-by-year)\n')
  f.write('- [Ordered by programming language](#ordered-by-programming-language)\n')
  f.write('- [Alphabetic order](#alphabetic-order)\n')
  f.write('\n')

  f.write('## Alphabetic order\n')
  repos.sort(key=lambda x: x.name)
  for idx, repo in enumerate(repos):
    f.write(str(idx + 1) + '. ' + getRepoItemStr(repo))
  f.write('\n')

  f.write('## Ordered by year\n')
  repos.sort(key=lambda x: x.year, reverse=True)
  
  lastYearStr = ''
  listYears = ''
  for repo in repos:
    repoYearStr = str(repo.year)
    if lastYearStr != repoYearStr:
      listYears = '[' + repoYearStr + '](#' + repoYearStr + '), ' + listYears
      lastYearStr = repoYearStr
  f.write('List: ' + listYears[:-2] + '\n')
  
  lastYearStr = ''
  for repo in repos:
    repoYearStr = str(repo.year)
    if lastYearStr != repoYearStr:
      f.write('\n### ' + repoYearStr + '\n')
      lastYearStr = repoYearStr

    f.write('- ' + getRepoItemStr(repo))
  f.write('\n')

  f.write('## Ordered by programming language\n')
  repos.sort(key=lambda x: x.name)
  languages = { lang for repo in repos for lang in repo.languages}
  languages = list(languages)
  languages.sort()

  listLang = ''
  for lang in languages:
    listLang = listLang + '[' + lang + '](#' + lang.lower().replace(' ', '-').replace('#', '').replace('/', '').replace('+', '') + '), '
  f.write('List: ' + listLang[:-2] + '\n')

  for lang in languages:
    f.write('\n### ' + lang + '\n')
    for repo in repos:
      if lang in repo.languages:
        f.write('- ' + getRepoItemStr(repo))
  f.write('\n')

