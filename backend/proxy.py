import requests
proxy = "http://bdtaasda-rotate:5k1swa337dfy@p.webshare.io:80"

requests.get(
    "https://ipv4.webshare.io/",
    proxies={
        "http": proxy,
        "https": proxy,
    },
    timeout=10,
)