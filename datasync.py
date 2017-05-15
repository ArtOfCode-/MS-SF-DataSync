import json
import requests
import websocket


config = {
    'ms_api_key': '9313bfd5dbb3ca94a49812d8e15df0888af374f7a791ae5c0193b8641098d8a7',
    'sf_stream_key': 'KzGD7QDp9jTW95v0aYGy',
    'sf_stream_secret': 'vbjNrnNp7mUWYaryBAVj'
}


def main():
    ws = open_websocket()

    while True:
        try:
            data = json.loads(ws.recv())
        except Exception as ex:
            if isinstance(ex, websocket._exceptions.WebSocketConnectionClosedException):
                ws = open_websocket()
                continue

            print(ex)
        
        if 'type' in data and data['type'] == 'ping':
            print('pong')
            continue

        if 'message' not in data:
            print('no message', data)
            continue

        message = data['message']
        if 'statistic' not in message:
            print('irrelevant')
            continue

        posts_scanned = message['statistic']['posts_scanned']
        url = 'https://data.sparkfun.com/input/{}?private_key={}&posts_scanned={}'.format(config['sf_stream_key'],
                                                                                          config['sf_stream_secret'],
                                                                                          posts_scanned)
        response = requests.get(url)
        print(response.status_code, url)


def open_websocket():
    ws = websocket.create_connection('wss://metasmoke.erwaysoftware.com/cable')
    ws.send(json.dumps({
        'identifier': json.dumps({
            'channel': 'ApiChannel',
            'key': config['ms_api_key']
        }),
        'command': 'subscribe'
    }))
    return ws


if __name__ == '__main__':
    main()
