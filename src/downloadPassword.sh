#!/bin/bash
curl "https://www.freeopenvpn.org/$1" \
  -H 'authority: www.freeopenvpn.org' \
  -H 'accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: FreeOVPN_lang=en; _ym_d=1679219563; _ym_uid=1679219563570737545; _ga=GA1.1.1921877.1693143508; __gads=ID=a77cf08a777f1137-22bbcd7a5ede008d:T=1693144433:RT=1693144433:S=ALNI_MYUTjYRtBkVEwGVqoHrJcTRoVxvLw; __gpi=UID=00000c6968b68361:T=1693144433:RT=1693144433:S=ALNI_MarLgypFeE8X6rFNcIEIypGHvGGRA; FCNEC=%5B%5B%22AKsRol8kpdnb45SK6IJBP0VS2734Sa35XcxZpNeifwsZOIFYkvZVWTUiB0ZLWgzrTb65hTLciuTRcpq7Wg_Rydpqd3uDkLvxhRJ4KKrqxGzgtWj_pUBzpFbsganxta7ptSKlKoR47Aca_Ln-jCBzu65LsdVyBrKfdA%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; _ym_isad=2; _ga_23QP00NX1D=GS1.1.1693502897.4.1.1693504580.60.0.0' \
  -H 'dnt: 1' \
  -H 'referer: https://www.freeopenvpn.org/premium.php?cntid=Netherlands&lang=en' \
  -H 'sec-ch-ua: "Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: image' \
  -H 'sec-fetch-mode: no-cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36' \
  --compressed --output password.png