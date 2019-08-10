# arrSync

## Instructions

Environment Variables:
* ARRSYNC_APP: `sonarr` or `radarr`
* ARRSYNC_SEARCH_ON_ADD: `true` (Default: `false`)
* ARRSYNC_URL_MASTER: `http://192.168.1.100/sonarr`
* ARRSYNC_API_KEY_MASTER: `yourapikey`
* ARRSYNC_MEDIA_BASE_PATH_MASTER: `/tv/`
* ARRSYNC_URL_SLAVE: `http://192.168.1.101/sonarr`
* ARRSYNC_API_KEY_SLAVE: `yourotherapikey`
* ARRSYNC_QUALITY_PROFILE_ID_SLAVE: `1`
* ARRSYNC_MEDIA_BASE_PATH_SLAVE: `/tv4k/`
* ARRSYNC_CRON_SCHEDULE: (Default: `*/15 * * * *`) (Docker only)

### Lambda
1. Create a function
    1. Name: `arrSync-<Radarr or Sonarr>`
    2. Runtime: `Python 3.7`
    3. Permissions: `Create a new role with basic Lambda permissions`
2. Clone the repo then run this code starting in the git directory:
    ```
    python3 -m pip install --system --target ./deps -r requirements.txt
    cd deps
    zip -r9 ../arrSync.zip .
    cd ..
    zip -g arrSync.zip arrSync.py
    aws lambda update-function-code --function-name arrSync-<Radarr or Sonarr> --zip-file fileb://arrSync.zip
    ```
3. Refresh the page, then change the Handler to arrSync.aws
4. Fill out the environment variables
5. Change the timeout based on your library size (I set to 30 seconds)
6. Add a CloudWatch Event for every 15 minutes

### Docker
todo