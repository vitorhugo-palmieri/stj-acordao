FIRST_URL = "https://www.stj.jus.br/sites/portalp/Inicio"
SEARCH_URL = "https://scon.stj.jus.br/SCON/"
ACORDAO_PDF = "https://scon.stj.jus.br/"
JUDGMENT_URL = "jurisprudencia/toc.jsp"
MONOCRATIC_DECISIONS_URL = "decisoes/toc.jsp"
PDF_URL="https://processo.stj.jus.br"
QUANTITY_REGISTRY = 50
MAX_ERRORS_ATTEMPTS = 3
DISCORD_WEBHOOK_DEV = 'https://discordapp.com/api/webhooks/1034990199639384124/XU10zP2DYemYcKL_HsmZwsWjR7BNbc0J_uZFoTfQVL0hTBYITTJjoCEnt2f__yQV2ivH'


HEADER_FIRST = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "scon.stj.jus.br",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
}

HEADERS_SEARCH = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "scon.stj.jus.br",
    "Origin": "https://scon.stj.jus.br",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
HEADERS_PDF= {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
"Accept-Language":"en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
"Accept-Encoding":"gzip, deflate, br",
"Referer":"https://scon.stj.jus.br/SCON/pesquisar.jsp",
"Connection":"keep-alive",
"Upgrade-Insecure-Requests":"1",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"same-site",
"Sec-Fetch-User":"?1",
"Cache-Control":"max-age=0",
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


