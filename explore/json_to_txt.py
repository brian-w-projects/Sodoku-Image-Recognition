import json
import re


with open('output.txt', 'w') as output:
    with open('data.json', 'r') as sodoku:
        for ele in sodoku:
            single = json.loads(ele)
            image = re.findall(r'__(train.*)$', single['content'])[0]
            count = 0
            print(image)
            for points in single['annotation']:
                height = points['imageHeight']
                label = points['label'][0]
                if label != '0':
                    continue
                count += 1
                ul = int(points['points'][0][0]*height), int(points['points'][0][1]*height)
                lr = int(points['points'][2][0]*height), int(points['points'][2][1]*height)

                length = max(lr[0]-ul[0], lr[1]-ul[1])
                out = 'train/{},{},{},{},{},{}\n'.format(image, ul[0], ul[1], ul[0]+length, ul[1]+length, label)
                output.write(out)
            print(count)