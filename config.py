import multiprocessing

ENGINES = {
    "ahmia": "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion",
    "darksearchio": "http://darksearch.io",
    "onionland": "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion",
    "notevil": "http://hss3uro2hsxfogfq.onion",
    "darksearchenginer": "http://l4rsciqnpzdndt2llgjx3luvnxip7vbyj6k6nmdy4xs77tx6gkd24ead.onion",
    "phobos": "http://phobosxilamwcg75xt22id7aywkzol6q6rfl2flipcqoc4e4ahima5id.onion",
}

DESKTOP_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
]

AVAILABLE_CSV_FIELDS = ["engine", "name", "link", "domain"]

DEFAULT_PROXY = "localhost:9050"
DEFAULT_OUTPUT = "output_$SEARCH_$DATE.txt"
DEFAULT_MP_UNITS = multiprocessing.cpu_count() - 1



# Add a section to query automatically, not relying on SOCKS proxy. 