import io
import tempfile
import requests


PASSWORD_URL_TEMPLATE = "https://www.freeopenvpn.org/{image_path}"
OVPN_FILE_URL_TEMPLATE = "https://www.freeopenvpn.org/ovpn/{region}_freeopenvpn_tcp.ovpn"
REFERER_TEMPLATE = "https://www.freeopenvpn.org/premium.php?cntid={region}&lang=en"

PASSWORD_COOKIES = {
    "FreeOVPN_lang": "en",
    "_ym_d": "1679219563",
    "_ym_uid": "1679219563570737545",
    "_ga": "GA1.1.1921877.1693143508",
    "__gads": "ID=a77cf08a777f1137-22bbcd7a5ede008d:T=1693144433:RT=1693144433:S=ALNI_MYUTjYRtBkVEwGVqoHrJcTRoVxvLw",
    "__gpi": "UID=00000c6968b68361:T=1693144433:RT=1693144433:S=ALNI_MarLgypFeE8X6rFNcIEIypGHvGGRA",
    "FCNEC": "%5B%5B%22AKsRol8kpdnb45SK6IJBP0VS2734Sa35XcxZpNeifwsZOIFYkvZVWTUiB0ZLWgzrTb65hTLciuTRcpq7Wg_Rydpqd3uDkLvxhRJ4KKrqxGzgtWj_pUBzpFbsganxta7ptSKlKoR47Aca_Ln-jCBzu65LsdVyBrKfdA%3D%3D%22%5D%2Cnull%2C%5B%5D%5D",
    "_ym_isad": "2",
    "_ga_23QP00NX1D": "GS1.1.1693502897.4.1.1693504580.60.0.0",
}

PASSWORD_HEADERS = {
    "authority": "www.freeopenvpn.org",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "dnt": "1",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}


def get_password_image_url(image_path: str) -> str:
    return PASSWORD_URL_TEMPLATE.format(image_path=image_path)


def get_password_image_headers(region: str) -> str:
    referer = {"referer": REFERER_TEMPLATE.format(region=region)}
    return {**PASSWORD_HEADERS, **referer}


def get_password_image_bytes(image_path: str, region: str) -> bytes:
    url = get_password_image_url(image_path=image_path)
    headers = get_password_image_headers(region=region)
    response = requests.get(url, cookies=PASSWORD_COOKIES, headers=headers)
    return response.content


def get_region_page(region: str) -> str:
    url = REFERER_TEMPLATE.format(region=region)
    response = requests.get(url)
    return response.text

def get_ovpn_tcp_config(region: str):
    url = OVPN_FILE_URL_TEMPLATE.format(region=region)
    response = requests.get(url)
    open(f'{region}_freeopenvpn_tcp.ovpn', mode='wb').write(response.content) # не смог в tmpб для baseline пусть пока так