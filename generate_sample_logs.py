import random, json
from datetime import datetime, timedelta


levels = ['INFO','WARNING','ERROR','DEBUG']
services = ['auth','payments','worker','api']


def gen_line(i):
    ts = (datetime.utcnow() - timedelta(minutes=random.randint(0,1440))).isoformat() + 'Z'
    lvl = random.choices(levels, weights=[60,20,10,10])[0]
    src = random.choice(services)
    msg = f"Sample log {i} from {src} - simulated event (code {random.randint(100,599)})"
    return json.dumps({"timestamp":ts, "level":lvl, "source":src, "message":msg})


if __name__ == '__main__':
    for i in range(1000):
        print(gen_line(i))


