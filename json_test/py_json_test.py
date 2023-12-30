import json
import random

def publish():
  payload = {
    'data1': random.random(),
    'data2': random.random()
  }
  print(json.dumps(payload))

if __name__ == '__main__':
    publish()