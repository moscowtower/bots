import requests
from bs4 import BeautifulSoup


def get_title(url):
  bad_scp = ['Архив', 'Протокол', 'Статьи', 'Статья']
  parse = True
  while parse:
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'html.parser')
    title = bs.title.string.replace('- The SCP Foundation', '')
    if any(word in title for word in bad_scp):
      continue
    if not 'SCP' in title:
      continue
    break
  get_img(url)
  return title


def find_title(scp_num):
  url = 'http://scpfoundation.net/scp-' + str(scp_num)
  r = requests.get(url)
  bs = BeautifulSoup(r.text, 'html.parser')
  title = bs.title.string.replace('- The SCP Foundation', '')
  return title


def find_img(scp_num):
  url = 'http://scpfoundation.net/scp-' + str(scp_num)
  parse = True
  while parse:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('img'):
      link = str(link)
      if 'nav:side' not in link and 'Quantcast' not in link:
        print(link)
        beg = link.find('src="')
        end = link.find('"', beg + beg)
        img = link[beg:end].replace('src="', '')
        return img.strip()
    break


def get_img(url):
  parse = True
  while parse:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('img'):
      link = str(link)
      if 'nav:side' not in link and 'Quantcast' not in link:
        print(link)
        beg = link.find('src="')
        end = link.find('"', beg+beg)
        img = link[beg:end].replace('src="', '')
        return img.strip()
    break

def get_text(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  text = soup.get_text()
  # Находим класс объекта
  beg = text.find('Класс объекта: ')
  end = text.find('Особые', beg)
  classification = text[beg:end].strip().replace('Класс объекта:', '*Класс объекта:*')
  # Находим особые условия содержания
  beg = text.find('Особые условия содержания: ')
  end = text.find('Описание', beg)
  spec_cond = text[beg:end].replace('Особые условия содержания:', '*Особые условия содержания:*')
  # Находим описание
  beg = text.find('Описание: ')
  end = text.find('версия', beg)
  about = text[beg:end].replace('Описание:', '*Описание:*')
  if 'Авторство' in about:
    about = about[:about.index('Авторство')]
  about = about\
    .replace("_", "\\_")\
    .replace("*", "\\*")\
    .replace("[", "\\[")\
    .replace("`", "\\`");
  string = f'{classification}\n{spec_cond}\n{about}\n'
  return string



