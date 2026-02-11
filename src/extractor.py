import re
from urllib.parse import urlparse

class URLExtractor:
    def extract_features(self, url):
        url = str(url).lower()
        parsed = urlparse(url)
        
        url_len = len(url)
        digit_count = sum(c.isdigit() for c in url)
        
        # New features to catch the 269 malicious samples
        features = {
            'url_len': url_len,
            'dot_count': url.count('.'),
            'special_chars': len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', url)),
            'digit_ratio': digit_count / url_len if url_len > 0 else 0,
            'subdomain_count': len(parsed.netloc.split('.')) - 2 if parsed.netloc else 0,
            'has_ip': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
            'has_at': 1 if '@' in url else 0,
            'is_https': 1 if parsed.scheme == 'https' else 0,
            'path_depth': len([p for p in parsed.path.split('/') if p]),
            'has_redirection': 1 if '//' in parsed.path else 0
        }
        return features