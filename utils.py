import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from multiprocessing import current_process
from config import DESKTOP_AGENTS

def random_headers():
    return {
        'User-Agent': random.choice(DESKTOP_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

def clear(text):
    return ' '.join(text.replace("\n", " ").split())

def get_parameter(url, parameter_name):
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query).get(parameter_name, [None])[0]

def get_proc_pos():
    return (current_process()._identity[0]) - 1
