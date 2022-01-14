from config import DASQ_BACKEND_URL, DASQ_HEADERS, DASQ_SIGNALS_ROUTE, WORKSPACE_NAME
import getNearestTaskStatus
import json
import requests
import time


def main():
    color_hex = getNearestTaskStatus.main().hex_l
    signal = {
        'zoneId': 'KEY_K',
        'color': color_hex,
        'effect': 'SET_COLOR',
        'pid': 'DK4QPID',
        'clientName': 'Python script',
        'message': '',
        'name': f'New task in {WORKSPACE_NAME}',
        'isMuted': True
    }

    signal = json.dumps(signal)

    response = requests.post(
        DASQ_BACKEND_URL + DASQ_SIGNALS_ROUTE, data=signal, headers=DASQ_HEADERS)

    if response.ok:
        print('Success!')

    print(response.text)


if __name__ == '__main__':
    main()
