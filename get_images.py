import os
import requests
import shutil

terms = ['chair']
for searchTerm in terms:
    count = 100
    url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=" + searchTerm + "&imageType=line&count=" + str(count)

    image_urls = []
    urls_f = open('urls.txt', 'wr')

    for i in range(5):
        offset_url = url + "&offset=" + str(i * count)
        headers = {"Ocp-Apim-Subscription-Key": "a015c59688db4a188ba5a5a2bf3eb20f"}
        r = requests.get(offset_url, headers=headers)

        for image in r.json()['value']:
            if image['encodingFormat'] == 'jpeg':
                image_urls.append(image['contentUrl'])
                urls_f.write(image['contentUrl'])
                urls_f.write('\n')
        print len(image_urls)

    if not os.path.exists(searchTerm):
        os.mkdir(searchTerm)

    for index, image_url in enumerate(image_urls):
        try:
            r = requests.get(image_url, stream=True, allow_redirects=True)
            with open(searchTerm +'/' + str(index) + ".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            f.close()
        except Exception:
            print "ERROR:", index, image_url

