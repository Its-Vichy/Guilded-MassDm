<h1 align="center">Guilded mass advertisser</h1>

<p align='center'>
    <b>Mass DM tool for guilded.gg.</b><br>
    <br>
    <img src='https://media.discordapp.net/attachments/979740086927261697/989122862428340275/unknown.png'>
</p>

-----

```
Known issue: proxy checker "crash/freeze".

⚠️ Information:
Due to guilded security patch, login-loading mode is patched (need to verify the e-mail). 
Please be sure to use proxy or vpn when you are using guilded otherwise they will ban your ip address.
Your account will be terminated every somes hours if you are making somes spam, account generation etc.. (i got termed every hours)
```

-----

- [X] **Server scraper (online/all/with pfp)**
- [X] **email:pass:cookie:id and cookie format**
- [X] **Proxy support - HTTP/S**
- [X] **Guild / Team joiner**
- [X] **Username scraper**
- [X] **Avatar scraper**
- [X] **Guild scraper**
- [X] **Proxy scraper**
- [X] **Proxy checker**
- [X] **Mass pfp, bio, avatar changer**
- [X] **Mass dm**
- [X] **Silent mode**

-----

| Name | Description | 
| ---  | ---  |
| `scrape_cookie` | The cookie of the account that you will use for scraping, this account need to be on the server. |
| `scrape_default_pfp` | Scrape members with default pfp, helpfull to ignore bots. |
| `with_role_only` | Scrape members with role only (ex: anti-bot verification), helpfull to ignore bots. |
| `scrape_online` | Scrape only connected members. |
| `loading_thread` | The number of thread that will be used to connect trought account. |
| `save_valid` | Save valid account on text file. |
| `debug` | If you want to see errors, or debug the code. |
| `join_main` | Join scrapped server with the scrape account. |
| `max_scrape` | Max invite to scrape. |
| `min_member` | Minimum members to scrape. |
| `overwrite_valid` | Overwrite valid account file. |
| `proxy_checking_thread` | How many threads will check proxies |
| `check_proxies` | If you want to check proxies |
| `scrape_proxies` | If you want to scrape proxy from url file |
| `overwrite_valid_proxies` | Delete dead proxy and replace them by checked one |
| `proxy_timeout` | Data transfer timeout |
| `proxy_connect_timeout` | Connection speed timeout |

-----

<details><summary>UPDATE LOGS:</summary>
<p>

0.0.61

- Handle Ratelimit on single channel spam.
- Console menu fix.

0.0.6

- Proxy config menu / file.
- Installation file.
- Channel spammer.
- Zombie dm fix.
- Proxy checker.
- Proxy scraper.
- Bug fix.

0.0.5

- Single Mass dm.
- New menu.
- Bugs fix.
- Reload config.
- Handle locked dms.
- Blacklist ratelimited tokens.
- Overwrite valid files.
- Silent login mode (load tokens without log in acc, but now require email:pass:token:id format.)

0.0.4

- Guild scraper
- Loading proxy error handling
    
0.0.3
    
- Scrapping menu
- Mass pfp changer.
- Config the tool.
- Onliner.
- Mass status changer.
- Mass bio changer.
- Mass spoof (bio+status+pfp+online).

0.0.2

- Add Server scraper (online/all/with pfp etc..)
- Add option to save mass-dm settings, because we are lazy guys :o
- Add "restart" option to massDm.
- Handle ratelimit (need to add timer).
- Add mass pfp changer.
- Fix duplicate dm / user id.
- Other bug fix and code change.

</p>
</details>

-----

<p align="center">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Its-Vichy/Guilded-MassDm?style=for-the-badge&logo=stylelint&color=gold">
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Its-Vichy/Guilded-MassDm?style=for-the-badge&logo=stylelint&color=gold">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Its-Vichy/Guilded-MassDm?style=for-the-badge&logo=stylelint&color=gold">
</p>
