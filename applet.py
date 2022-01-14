from config import BACKEND_URL, DASQ_HEADERS
import getNearestTaskStatus
import json
import requests


def main():
    color_hex = getNearestTaskStatus.main().hex_l
    signal = {
        'zoneId': 'KEY_K',
        'color': color_hex,
        'effect': 'SET_COLOR',
        'pid': 'DK5QPID',
        'clientName': 'Python script',
        'message': 'Placeholder message',
        'name': 'Placeholder name'
    }

    signal = json.dumps(signal)

    response = requests.post(
        BACKEND_URL + '/api/1.0/signals', data=signal, headers=DASQ_HEADERS)

    if response.ok:
        print('Success!')

    print(response.text)


if __name__ == '__main__':
    main()
