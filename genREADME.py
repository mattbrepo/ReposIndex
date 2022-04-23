#
# Generates the README.md containing the list of all my Github repositories
#
import os

class Repo(object):
  def __init__(self, name, description, language, year):
    self.name = name
    self.description = description
    self.language = language
    self.year = year

def getRepo(readmeFilePath):
  with open(readmeFilePath) as f:
    content = f.readlines()

  name = content[0].replace('# ', '').replace('\n', '')
  description = content[1].replace('\n', '')
  language = ''
  year = ''
  for str in content:
    if str.startswith('**Language'):
      language = str.replace('**Language: ', '').replace('**', '').replace('\n', '')
    if str.startswith('**Start'):
      year = str.replace('**Start: ', '').replace('**', '').replace('\n', '')

  if year == '':
    print(readmeFilePath)

  return Repo(name, description, language, int(year))

def getRepos():
  repos = []
  for (dirpath, dirnames, filenames) in os.walk('..'):
    if dirpath.startswith('..\__'): # exclude unfinished repos
      continue
    if dirpath.startswith('..\ReposIndex'): # exclude this repo
      continue

    for file in filenames:
      if file == 'README.md':
        readmeFilepath = os.path.join(dirpath, file)
        print('found: ' + readmeFilepath)
        r = getRepo(readmeFilepath)
        if r != None:
          repos.append(r)

  return repos

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
  for repo in repos:
    f.write('- ' + repo.name + ': ' + repo.description + '\n')
  f.write('\n')

  f.write('## Ordered by year\n')
  repos.sort(key=lambda x: x.year)
  lastYearStr = ''
  for repo in repos:
    repoYearStr = str(repo.year)
    if lastYearStr != repoYearStr:
      f.write('\n### ' + repoYearStr + '\n')
      lastYearStr = repoYearStr

    f.write('- ' + repo.name + ': ' + repo.description + '\n')
  f.write('\n')

  f.write('## Ordered by language\n')
  repos.sort(key=lambda x: x.language)
  lastLang = ''
  for repo in repos:
    repoLang = repo.language
    if lastLang != repoLang:
      f.write('\n### ' + repoLang + '\n')
      lastLang = repoLang

    f.write('- ' + repo.name + ': ' + repo.description + '\n')
  f.write('\n')

