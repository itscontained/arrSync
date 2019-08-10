from sys import exit
from requests import Session
from os import environ as env


def run():
    app = env.get('ARRSYNC_APP', 'Empty').lower()
    search_on_add = True if env.get('ARRSYNC_SEARCH_ON_ADD', 'False').lower() == 'true' else False

    url_master = env.get('ARRSYNC_URL_MASTER', '').rstrip('/')  # e.g. 'http://192.168.1.100/sonarr'
    api_key_master = env.get('ARRSYNC_API_KEY_MASTER', '')
    media_base_path_master = env.get('ARRSYNC_MEDIA_BASE_PATH_MASTER', '')

    url_slave = env.get('ARRSYNC_URL_SLAVE', '').rstrip('/')  # e.g. 'http://192.168.1.101/sonarr'
    api_key_slave = env.get('ARRSYNC_API_KEY_SLAVE', '')
    quality_profile_id_slave = env.get('ARRSYNC_QUALITY_PROFILE_ID_SLAVE', '')
    media_base_path_slave = env.get('ARRSYNC_MEDIA_BASE_PATH_SLAVE', '')

    opts = {
        'sonarr': {
            'idtype': 'tvdbId',
            'endpoint': 'series'
        },
        'radarr': {
            'idtype': 'tmdbId',
            'endpoint': 'movie'
        }
    }

    if app not in opts:
        exit(f"Error: {app} does not equal 'sonarr' or 'radarr'")
    if not all([url_master, url_slave, api_key_master, api_key_slave, quality_profile_id_slave, media_base_path_master,
                media_base_path_slave]):
        exit(f"Error: Missing one or more required environment variables")

    full_url_master = f"{url_master}/api/{opts[app]['endpoint']}"
    full_url_slave = f"{url_slave}/api/{opts[app]['endpoint']}"

    session_master = Session()
    session_master.params = {'apikey': api_key_master}
    session_slave = Session()
    session_slave.params = {'apikey': api_key_slave}

    get_master = session_master.get(full_url_master).json()
    get_slave = session_slave.get(full_url_slave).json()

    id_list_master = [m[opts[app]['idtype']] for m in get_master]
    id_list_slave = [m[opts[app]['idtype']] for m in get_slave]
    missing = [m for m in get_master if m[opts[app]['idtype']] not in id_list_slave]
    removed = [m for m in get_slave if m[opts[app]['idtype']] not in id_list_master]

    for media in missing:
        payload = {
            'title': media['title'],
            'qualityProfileId': quality_profile_id_slave,
            'titleSlug': media['titleSlug'],
            'images': [],
            'path': media['path'].replace(media_base_path_master, media_base_path_slave),
            'monitored': True,
            opts[app]['idtype']: media[opts[app]['idtype']]
        }
        if app == 'sonarr':
            payload.update({'seasons': [], 'addOptions': {'searchForMissingEpisodes': search_on_add}})
        elif app == 'radarr':
            payload.update({'year': media['year'], 'minimumAvailability': 'inCinemas',
                            'addOptions': {'searchForMovie': search_on_add}})

        print('Adding {} to slave instance'.format(media['title']))
        p = session_slave.post(full_url_slave, json=payload)
        print(p.json())

    for media in removed:
        print('Removing {} from slave instance'.format(media['title']))
        d = session_slave.delete(f"{full_url_slave}/{media['id']}")
        print(d.json())


if __name__ == "__main__":
    run()
