import json
import pandas as pd
import glob
from tqdm import tqdm


class Chat:
    def __init__(self, json):
        self.json = json

    def to_csv(self, filename):
      if filename[-4::] != '.csv':
          filename = filename + '.csv'
      df = self.to_df()
      df.to_csv(filename, index=False)

    def to_df(self):
      row = {}
      row['engagementId'] = self.json['info']['engagementId']
      row['startTime'] = self.json['info']['startTime']
      row['endTime'] = self.json['info']['endTime']
      row['visitorId'] = self.json['info']['visitorId']
      row['visitorName'] = self.json['info']['visitorName']
      row['agentLoginName'] = self.json['info']['agentLoginName']
      row['agentFullName'] = self.json['info']['agentFullName']
      row['skillName'] = self.json['info']['skillName']
  
      row['text'] = []
      row['by'] = []
      row['source'] = []
  
      for line in self.json['transcript']['lines']:
          row['text'].append(line['text'])
          row['by'].append(line['by'])
          row['source'].append(line['source'])
  
      return pd.DataFrame(row)


class ChatFiles:
    def __init__(self, **kwargs):
        self.input_dir = kwargs.get('input_dir', 'input')
        self.input_filetype = kwargs.get('input_filetype', 'txt')
        self.output_dir = kwargs.get('output_dir', 'output')
        self.output_filename = kwargs.get('output_filename', 'output.csv')

        self.input_filenames = glob.glob(f'{self.input_dir}/chat_*.{self.input_filetype}')
        self.df = None 

    def to_csv(self, aggregate=True):
      for input_filename in tqdm(self.input_filenames):
        with open(input_filename, 'r') as read_file:
            chat = Chat(json.load(read_file))
            if aggregate:
                self.__compile_chats(chat.to_df())
            else:
                chat.to_csv(self.__output_filename(input_filename))
      if aggregate:
          self.df.to_csv(self.output_filename, index=False)

    def __compile_chats(self, chat_df):
        if self.df is None:
            self.df = chat_df
        else:
            self.df = self.df.append(chat_df, ignore_index=True)

    def __output_filename(self, input_filename):
        start_index = len(self.input_dir) + 1
        end_index = -(len(self.input_filetype) + 1)
        name = input_filename[start_index : end_index]
        return f'{self.output_dir}/{name}.csv'
    

if __name__ == '__main__':
    chatfiles = ChatFiles(input_dir='input',
                          input_filetype='txt',
                          output_dir='output',)
    chatfiles.to_csv()
