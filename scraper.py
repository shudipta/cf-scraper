import requests
# from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

class contest:
    @classmethod
    def list(self, gym=False):
        url = "https://codeforces.com/api/contest.list"
        if gym:
            url += "?gym=true"
        else:
            url += "?gym=false"
        print(url)
        resp = requests.get(url, timeout=5)
        try: assert (resp.status_code == 200)
        except AssertionError:
            print(resp)
            return

        # cont = BeautifulSoup(resp.content, "html.parser")
        contJson = json.loads(resp.text)

        try: assert (contJson['status'] == 'OK')
        except AssertionError:
            print("Bad Status: ", contJson['status'])
            return

        if len(contJson['result']) == 0:
            print("No contest here !")
            return

        upcomings = []
        pendings = []
        for c in contJson['result']:
            if c['phase'] == 'BEFORE':
                upcomings.append({
                    c['name']: {
                        # 'type': c['type'],
                        'duration': str(timedelta(seconds=c['durationSeconds'])),
                        'start': str(datetime.fromtimestamp(c['startTimeSeconds']))
                    }})
            elif c['phase'] == 'PENDING_SYSTEM_TEST':
                pendings.append(c['name'])

        print("""
        ===================
            upcomings ...
        ===================
""", json.dumps(upcomings, indent=2, ensure_ascii=False).encode('utf8').decode())
        print("""
        ===================
            pendings ...
        ===================
        """, pendings)

c = contest().list(True)
