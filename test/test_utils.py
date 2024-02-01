from src.lib import utils
from unittest.mock import MagicMock

def test_config_get_dev_urls():
    utils.config_get_dev = MagicMock()
    utils.config_get_dev.return_value = {
        'urls': [
            'https://url1.com',
            'https://url2.com'
        ]
    }

    res = utils.config_get_dev_urls()
    print(res)

    assert res == [
            'https://url1.com',
            'https://url2.com'
        ]