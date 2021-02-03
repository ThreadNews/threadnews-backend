import os
import random 
import json
"""file is responsible for creating a json file storing
the data that is required to create the category
bubbles in the layout"""

"""this is a tempory fix this will eventually be stored in
the database"""

cat_img_list = os.listdir("./threadnews-frontend/threadnews/public/assets/categoryIcons")
colors = ['#C56A68','#C56A68','#C5A268','#C5A268','#C5B468','#C3C568','#B1C568',
        '#9EC568','#8BC568','#79C568','#68C56A','#68C57C','#68C58F','#68C5A2',
        '#68C3C5','#68C5B4','#68B1C5','#689EC5','#688BC5','#6879C5','#6A68C5',
        '#7C68C5','#8F68C5','#A268C5','#B468C5','#C568C3','#C568B1','#C5689E',
        '#C5688B','#C56879']
item_list = []

for path in cat_img_list:
    item_data =  {}
    item_data["logo_path"] = path
    #item_data["name"] = path[:-4]
    item_data["bg_color"] = random.choice(colors)
    #item_data["children"] = None #maybe add sub categories? strucure as tree
    item_list.append(item_data)

data = {"topic_bubble_data": item_list}

with open("./threadnews-backend/topic_bubble_data.json","w") as f:
    json.dump(data,f)



print(cat_img_list)
