# DATA SCRAPER
# 1. Open a set of URLs one at a time
# 2. Scrape the data from the URLs based on their source type
# 3. Using pandas to generate a dataframe from the data, load up to 1GB at a time and flush to an output file
# 4. Display a progress bar along the way
# 5. Repeat until the URLs have been exhausted

import os
import pandas
import numpy
import json

# DA SCRAPINATOR!!!
from libs import scrapinator

# HTML magic
from bs4 import BeautifulSoup

scrapinator.scraper_source_urls = "scraped/urls.txt"
data_output_file = "scraped/prompt_output.csv"
scrapinator.test_file = True

walmart_id = "__NEXT_DATA__"

headers = {
    'host': 'www.walmart.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'dnt': '1',
    'sec-gpc': '1',
    'connection': 'keep-alive',
    'cookie': 'AID=wmlspartner=wlpa:reflectorid=0000000000000000000000:lastupd=1745960704645; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1746472854000@firstcreate:1745959280428"; ACID=aa44e95d-c21c-4891-817e-15bb75bfef8e; _m=9; assortmentStoreId=2927; hasACID=true; hasLocData=1; locDataV3=eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3sibm9kZUlkIjoiMjkyNyIsImRpc3BsYXlOYW1lIjoiV29vZCBWaWxsYWdlIFN1cGVyY2VudGVyIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiOTcwNjAiLCJhZGRyZXNzTGluZTEiOiIyMzUwMCBORSBTQU5EWSBCTFZEIiwiY2l0eSI6Ildvb2QgVmlsbGFnZSIsInN0YXRlIjoiT1IiLCJjb3VudHJ5IjoiVVMifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQ1LjU0MTEyMSwibG9uZ2l0dWRlIjotMTIyLjQyMDcwM30sInNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInVuU2NoZWR1bGVkRW5hYmxlZCI6dHJ1ZSwic3RvcmVIcnMiOiIwNjowMC0yMzowMCIsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJPUiJdLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJBQ0MiLCJBQ0NfSU5HUk9VTkQiLCJQSUNLVVBfSU5TVE9SRSIsIlBJQ0tVUF9TUEVDSUFMX0VWRU5UIiwiUElDS1VQX0NVUkJTSURFIiwiUElDS1VQX0JBS0VSWSJdLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzdG9yZUJyYW5kRm9ybWF0IjoiV2FsbWFydCBTdXBlcmNlbnRlciIsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCJ9LHsibm9kZUlkIjoiNTQ0MCJ9LHsibm9kZUlkIjoiNTQ2MiJ9LHsibm9kZUlkIjoiMzE3OCJ9LHsibm9kZUlkIjoiNTYyNyJ9LHsibm9kZUlkIjoiMzE0NCJ9LHsibm9kZUlkIjoiMjU1MCJ9LHsibm9kZUlkIjoiNTk5NCJ9LHsibm9kZUlkIjoiNTQ2MSJ9XSwic2hpcHBpbmdBZGRyZXNzIjp7ImxhdGl0dWRlIjo0NS40ODExLCJsb25naXR1ZGUiOi0xMjIuNDE1LCJwb3N0YWxDb2RlIjoiOTcwODAiLCJjaXR5IjoiR3Jlc2hhbSIsInN0YXRlIjoiT1IiLCJjb3VudHJ5Q29kZSI6IlVTQSIsImdpZnRBZGRyZXNzIjpmYWxzZSwidGltZVpvbmUiOiJBbWVyaWNhL0xvc19BbmdlbGVzIiwiYWxsb3dlZFdJQ0FnZW5jaWVzIjpbIk9SIl19LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjI5MjciLCJkaXNwbGF5TmFtZSI6Ildvb2QgVmlsbGFnZSBTdXBlcmNlbnRlciIsImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsibm9kZUlkIjoiMjkyNyIsImRpc3BsYXlOYW1lIjoiV29vZCBWaWxsYWdlIFN1cGVyY2VudGVyIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiOTcwNjAiLCJhZGRyZXNzTGluZTEiOiIyMzUwMCBORSBTQU5EWSBCTFZEIiwiY2l0eSI6Ildvb2QgVmlsbGFnZSIsInN0YXRlIjoiT1IiLCJjb3VudHJ5IjoiVVMifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjQ1LjU0MTEyMSwibG9uZ2l0dWRlIjotMTIyLjQyMDcwM30sInR5cGUiOiJERUxJVkVSWSIsInNjaGVkdWxlZEVuYWJsZWQiOmZhbHNlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOmZhbHNlLCJhY2Nlc3NQb2ludHMiOlt7ImFjY2Vzc1R5cGUiOiJERUxJVkVSWV9BRERSRVNTIn1dLCJpc0V4cHJlc3NEZWxpdmVyeU9ubHkiOmZhbHNlLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiT1IiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiREVMSVZFUllfQUREUkVTUyIsIkFDQyJdLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzdG9yZUJyYW5kRm9ybWF0IjoiV2FsbWFydCBTdXBlcmNlbnRlciIsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCJ9LCJpc2dlb0ludGxVc2VyIjpmYWxzZSwibXBEZWxTdG9yZUNvdW50IjowLCJyZWZyZXNoQXQiOjE3NDY0ODYzMzI3NTIsInZhbGlkYXRlS2V5IjoicHJvZDp2MjphYTQ0ZTk1ZC1jMjFjLTQ4OTEtODE3ZS0xNWJiNzViZmVmOGUifQ%3D%3D; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjI5MjciLCJ0aW1lc3RhbXAiOjE3NDU5NTkyODA0NzYsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifSwic2hpcHBpbmdBZGRyZXNzIjp7InRpbWVzdGFtcCI6MTc0NTk1OTI4MDQ3NiwidHlwZSI6InBhcnRpYWwtbG9jYXRpb24iLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInBvc3RhbENvZGUiOiI5NzA4MCIsImRlbGl2ZXJ5U3RvcmVMaXN0IjpbeyJub2RlSWQiOiIyOTI3IiwidHlwZSI6IkRFTElWRVJZIiwidGltZXN0YW1wIjoxNzQ1OTUyMzY3Mjg0LCJkZWxpdmVyeVRpZXIiOm51bGwsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifV0sImNpdHkiOiJHcmVzaGFtIiwic3RhdGUiOiJPUiJ9LCJwb3N0YWxDb2RlIjp7InRpbWVzdGFtcCI6MTc0NTk1OTI4MDQ3NiwiYmFzZSI6Ijk3MDgwIn0sIm1wIjpbXSwibXNwIjp7Im5vZGVJZHMiOlsiNTQ0MCIsIjU0NjIiLCIzMTc4IiwiNTYyNyIsIjMxNDQiLCIyNTUwIiwiNTk5NCIsIjU0NjEiXSwidGltZXN0YW1wIjoxNzQ1OTU5MjgwNDY4fSwibXBEZWxTdG9yZUNvdW50IjowLCJzaG93TG9jYWxFeHBlcmllbmNlIjpmYWxzZSwic2hvd0xNUEVudHJ5UG9pbnQiOmZhbHNlLCJtcFVuaXF1ZVNlbGxlckNvdW50IjowLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6YWE0NGU5NWQtYzIxYy00ODkxLTgxN2UtMTViYjc1YmZlZjhlIn0%3D; userAppVersion=usweb-1.198.0-ae3167bb7fb3551acd28406390909c5040cfb18b-5012002r; sod=torbit1745959280; abqme=true; vtc=ZKmBCEqBHiskbC5SG743Og; _pxhd=94b938e842770161644d38f2b42102c068b0f0727fe54c42d2bb6352635bdda1:4e7f009f-253a-11f0-b998-2f6afd00bd2f; xptwj=uz:d7d97da1764558bbb184:95kcwtKDGYw1/o2fEoH2WSbkuqeXmm7xMey/gFbSwmTrGCDK3rf0pN96vm+T22LHv6qlTZ+pFaH8k2GKTNnZywhvM3JUctPhlh8w3OgzAuNuFfTuL1WrLTCr3rKJCBMGH+KGWmkbYe8oYLYflPX4qmtTQfTlPx+tCILuRrfA5NC3+qFN; _pxvid=4e7f009f-253a-11f0-b998-2f6afd00bd2f; xptwg=129043160:25F460231995720:5D56BE8:6761FEC:EBB401D8:173EE2A8:; TS012768cf=01f6e65594df6174fae022bc781b8f1e663b7d24087c338fed7b3694e783015c7b7fae0de54858c973f70e54b1529997e42ce50a7a; TS01a90220=01f6e65594df6174fae022bc781b8f1e663b7d24087c338fed7b3694e783015c7b7fae0de54858c973f70e54b1529997e42ce50a7a; TS2a5e0c5c027=087496564dab2000a4ea9b4eb4bb4919e8104935ef3bff9a8d652dc022d02cf38a4377f36df4d7ef08cc245976113000498b07d0e26c82ea054afb8f303df8749483e63a0201587bff3321b44e6e5e99f5496e099e2442af833ec4a596e1367e; akavpau_p2=1746473169~id=fe3366075c1f0d292e6f073f084b96b5; _astc=956dc001a5682fe91eb222f4cb181c52; _xrps=false; pxcts=4f38876c-253a-11f0-ad3e-09a7bdeaa454; adblocked=true; ak_bmsc=41CF996F076773C09D0D6DE8C7533B10~000000000000000000000000000000~YAAQnkRnaL/c9pOWAQAA1X7YoRt4Jdn3BcsDqYYTe2NlCJ+DZjgNivp53MsU9UTogeDitUmr3fz2qJopjLZDXpEvq2p7ZmmJjhFcYzfYLwWm51ORaGPAPZybG/4jgNL32DHmtNz1QzLtYYamdA66f70R/2uj9RhWEjqoTRYyM2adQzwaHH7S6Ryk+EUjlmpsaZB0+CEY5Z3jCnD/6SahlHFtaHoJ6QmnaH6wHFREX2Cy21Sv5cmeU50AP2BeSXJQZJBwwIv+Y8seH/brfqZ2dP/Onvu0i0k5jLIKjsOJP4khOdTE7+JwEC1HBygBQL8M6u4RUPb0vB/AlmkPAU8zxEoTVXZSYYZeZ3S3DJtkUtq/NkCZAx7J8SqBYnFwfCw7HgI2I5tKDkOVuA==; bm_sv=22B89DD7EC8DE3FE0A6F7C8CABA1A323~YAAQjkRnaAOqPn6WAQAAnH7uoRsxVAvvs1sSS3VopxrtsoFfcDsZIl28CciL7ggeorjoVXFWuCc7rRRRPT/Z2OtQ/+aJVQK2CeH53Zvz9txPhp9ZrWNPmVgqTxSdPpW4yp+7C8PPF9xWjWd4FUl6M5WoLQVTsffDJQp4uyloYJMov19SCLpX3Yg61ACxKgOnOu3or8aFY5KTVdaSQ1lOpCk0G0LgE7jm+N7zRbEGNzTxkqSpojASAZcHWZ6X/As2zkI=~1; bstc=d3N1LkHPpdM8Ldjq9i2A-U; xptc=assortmentStoreId%2B2927~_m%2B9; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=-MY-A|227cg|3VCVY|3npQL|7YUeG|DoKdE|I-Dl8|IHmcP|KYwc8|LKsvQ|LRSst|M4X5y|OUzk6|SdvCG|UcDm0|UtF0i|VQvcl|X46tV|aqAqP|baEuS|fdm-7|g11Gw|gooWz|jM1ax|kbPOQ|l5hsi|sEbMS|xhGTF; xpm=1%2B1746472545%2BZKmBCEqBHiskbC5SG743Og~%2B0; exp-ck=-MY-A17YUeG1DoKdE2I-Dl84IHmcP1KYwc81M4X5y1OUzk61SdvCG2UcDm01UtF0i1aqAqP1baEuS1fdm-71g11Gw3gooWz1kbPOQ1l5hsi2xhGTF1; bm_mi=3BFA2ACDBB27AC4909B623B1C9A59608~YAAQlqhkaNYiiYmWAQAA+3/goRuXLc8+nrWv9YAndPjsBqH6LTBCltMDaqQIo6me2P9x/oDXUlbjsyPt7QjJVjJwboNecTxt+/ktatxIcQ6A8O0jxjjfn7/JueIeun1Mj5gKXuEnFPlj7iiECv/8P1/XwmpY+uBKn44dyEz3UzuInaPvLuW9sYkOWpy2zXtvm9kda8YCKDI/ZIiTi0S3MLGWBvbV3J/W1ikj7N4y/JjY5pzJxuLBLyHm6d4yAJjzcboTuVyehLi/0v6e1IDp6FPkmFlLJhJfkkihae4AyjP2iIdhOMrZyzMq+n222auqB6Cq5w==~1; _intlbu=false; _shcc=US; auth=MTAyOTYyMDE47iMFjvRGw%2FqDYIf5Qf1Ba7FdmU8uavKX70zitswMf1vt51sU00NnckwedoYZy9voP0ePPVEKxyehuZGSVN6uXyhEwzAdVVYXKzbhyYmOWDuu0sjgSWav8M71cIhnO4Ve767wuZloTfhm7Wk2KcjygobRHThsmZk%2BGcqTfIab85Q5yKXdldMb05fWF3f6mg8dsVFzWP35sW1Zd%2BriIzPNZSVCzTd5rh%2FPHc9Hy6tfAWkUMk70P8glgOEpLOprhDfMWpzMbgzyqWg6MoSOREDGWlFCaAOT7WhaeLTcDydBR7ruyQxePi7%2F9S0lhfR2pbKf2e6Yxz0vMZtugD3RQRXuNbX49%2FNs3rU76ugYVJqTnyc6gBfgKA9G5JzshuQ%2BNbGIIEULGgQnPP38vCTO%2BTpuLkjyrOXbKKhH072NS%2FW0j%2FU%3D',
    'upgrade-insecure-requests': '1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'priority': 'u=0, i',
    'te': 'trailers'
}

# At this point, we should have some data to parse. If not, throw our hands up and quit.
# Get a dictionary of info based on what's required
scraped_data = scrapinator.scrape_data(walmart_id, headers)
product_data = []

if (scraped_data):
    product_data.append(scraped_data.get('url_0', []))
else:
    exit()

mapped_list = []

for product in product_data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']:
    if not product.get('id'):
        continue # skip entries with no IDs

    if not product.get('category'):
        category = 'No Category'
    else:
        category = product.get('category').get('categoryPathId', 'No Category ID')

    if not product.get('canonicalUrl'):
        product_url = 'No URL'
    else:
        product_url = urllib.parse.unquote(product['canonicalUrl'])

    if not product.get('price'):
        product_price = 'No Price Given'
    else:
        product_price = '$' + str(product['price'])

    if not product.get('numberOfReviews'):
        product_rating = 'No Reviews'
        product_rating_count = ''
    else:
        product_rating = product.get('averageRating', 'None')
        product_rating_count = product.get('numberOfReviews')

    dict_item = {
        'Retailer Name': product.get('sellerName', 'Walmart'),
        'Category': category,
        'Product URL': product_url,
        'Product Name': product.get('name', 'No Name'),
        'Price': product_price,
        'Rating': product_rating,
        'Rating Count': product_rating_count,
        'Available Sizes': '',
        'Walmart Item #': product.get('usItemId', 'None'),
        'SKU': product.get('id', 'None')
    }
    mapped_list.append(dict_item)

df = pandas.DataFrame(mapped_list)
df.to_csv(data_output_file, index=False)

