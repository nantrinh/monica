import json
import pandas as pd
import glob


def parse_chat(chat):
    row = {}
    row['engagementId'] = chat['info']['engagementId']
    row['startTime'] = chat['info']['startTime']
    row['endTime'] = chat['info']['endTime']
    row['visitorId'] = chat['info']['visitorId']
    row['visitorName'] = chat['info']['visitorName']
    row['agentLoginName'] = chat['info']['agentLoginName']
    row['agentFullName'] = chat['info']['agentFullName']
    row['skillName'] = chat['info']['skillName']

    row['text'] = []
    row['by'] = []
    row['source'] = []

    for line in chat['transcript']['lines']:
        row['text'].append(line['text'])
        row['by'].append(line['by'])
        row['source'].append(line['source'])

    df = pd.DataFrame(row)
    return df


def json_to_df(data, name):
    parsed = parse_chat(data)
    parsed.to_csv(name + '.csv', index=False)


if __name__ == '__main__':
    filenames = glob.glob('chat_*.txt')
    for filename in filenames:
      with open(filename, 'r') as read_file:
          data = json.load(read_file)
          json_to_df(data, filename[:-4])
