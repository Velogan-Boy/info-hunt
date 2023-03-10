import json
import glob


def checkcount(filename):
   try:
      with open(filename,encoding='utf-8') as f:
         data = json.load(f)
   
   except json.decoder.JSONDecodeError as e:
         data = []
           
   count = len(data)

   print(f'The {filename} contains {count} articles.')


if __name__ == '__main__':
   for filename in glob.glob('*.json'):
      checkcount(filename)
   
      
      
    