import requests
import re
import uuid

#url: instagram复制地址；toFolder: 输出文件夹


def instaSave(url, toFolder):
    res = requests.get(url).text
    image_node = re.search(r'\[{"node":{"__typename":"GraphImage".+"edge_media_to_tagged_user":{"edges":\[\]}}}\]',
                           res).group()
    images_raw = re.findall(r'"display_url":"[^"]*', image_node)

    for image_raw in images_raw:
        image_url = image_raw[image_raw.find("https"):].replace("\\u0026", "&")

        img_data = requests.get(image_url).content
        with open(toFolder + str(uuid.uuid1()) + ".jpg", 'wb') as handler:
            handler.write(img_data)

if __name__ == '__main__':
    url = "https://www.instagram.com/p/B3e158wlm_r/?igshid=150ovg90qct4p"
    path = "E:/"

    instaSave(url, path)
