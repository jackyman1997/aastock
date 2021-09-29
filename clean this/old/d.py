import json

with open('./output/恆指期貨 (即月)-2021731-205752.json', 'r') as f: 
    data = json.load(f)

new = [row['Datetime'] for row in data if row['Datetime'].split()[0] == data[-1]['Datetime'].split()[0]]
with open('./ff.json', 'w') as f:
    f.write(json.dumps(new, indent='\t'))
    print(len(new))