import sys
import subprocess
import os
from urllib.parse import parse_qsl
from xbmcaddon import Addon
from xbmcvfs import translatePath
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
MEDIA_DIR = os.path.join(ADDON_PATH, 'resources', 'media')


vodChannels = {
  'Amazon Prime': {
    'url': 'https://www.primevideo.com',
    'icon': os.path.join(MEDIA_DIR, 'amazon_prime_video_logo.svg'),
    'geoblocked': False
  }, 
  'Arte': {
    'url':'https://www.arte.tv/fr/',
    'icon': 'arte_logo.svg',
    'geoblocked': False
  },
  'Auvio': {
    'url': 'https://www.rtbf.be/auvio',
    'icon': 'auvio_logo.svg',
    'geoblocked': False
  },
  'Disney Plus': {
    'url': 'https://www.disneyplus.com/fr-be',
    'icon': 'disney+_logo.svg',
    'geoblocked': False
    },
  'Ketnet': {
    'url': 'https://www.ketnet.be',
    'icon': 'ketnet_logo.svg',
    'geoblocked': False
  }, 
  'Netflix': {
    'url': 'https://www.netflix.com/be-fr/', 
    'icon': 'netflix_logo.svg',
    'geoblocked': False
  }, 
  'Okoo': {
    'url': 'https://www.france.tv/enfants/',
    'icon': 'okoo_logo.svg',
    'geoblocked': 'FR'
  },
  'Rakuten TV': {
    'url': 'https://rakuten.tv',
    'icon': 'rakuten_logo.svg',
    'geoblocked': False
  },
  'RTL Play': {
    'url': 'https://www.rtlplay.be/',
    'icon': 'rtlplay_logo.png',
    'geoblocked': False
  }, 
  'VTM Go': {
    'url': 'https://vtm.be/vtmgo', 
    'icon': 'vtmgo_logo.png',
    'geoblocked': False
  },
  'Youtube': {
    'url': 'https://www.youtube.com', 
    'icon': 'youtube_logo.svg',
    'geoblocked': False
  },
  'Youtube Kids': {
    'url': 'https://www.youtubekids.com',
    'icon': 'youtube_kids_logo.svg',
    'geoblocked': False
  }
}

def show_name_list():
  listing = []

  for name, data in vodChannels.items():
    logo_path = os.path.join(MEDIA_DIR, data['icon'])
    list_item = xbmcgui.ListItem(label=name)
    list_item.setArt({'thumb': logo_path, 'icon': logo_path})
    url = '{0}?action={1}&name={2}'.format(URL, 'open_url', name)
    listing.append((url, list_item, True))

  # Add our listing to Kodi.
  # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
  # instead of adding one by ove via addDirectoryItem.
  xbmcplugin.addDirectoryItems(HANDLE, listing, len(listing))
  # Add a sort method for the virtual folder items (alphabetically, ignore articles)
  xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
  # Finish creating a virtual folder.
  xbmcplugin.endOfDirectory(HANDLE)

def open_url(name):
  data = vodChannels.get(name)
  if data:
    if data['geoblocked'] == 'FR':
      subprocess.Popen(['firefox', '-P VPN-FR', data['url']])
    else:
      subprocess.Popen(['firefox', '--kiosk', data['url']])

def router(paramstring):
  params = dict(parse_qsl(paramstring[1:]))
  if params:
    action = params.get('action')
    if action == 'open_url':
      name = params.get('name')
      open_url(name)
  else:
    show_name_list()

if __name__ == '__main__':
  router(sys.argv[2])