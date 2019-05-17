imageConfig = {
    "url": "http://img1.mm131.me/pic/",

    "testPicUrl": "http://img1.mm131.me/pic/4942/42.jpg",

    "header": {
        "Host": "img1.mm131.me",
        "Referer": "http://www.mm131.com/xinggan/",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
    },
}

pageConfig = {
    "url": "http://www.mm131.com/",

    "categories": {
        "sexy": "xinggan/",
        "pure": "qingchun/",
        "carModel": "chemo/",
        "chiPao": "qipao/",
        "celebrity": "mingxing/",
    },

    "header": {
        "Host": "www.mm131.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
    },

    "encode": "gbk",
}

reConfig = {
    "pageMatch": r'http://www.mm131.com/[a-z]+/\d+.html',
    "pages": r'list_\d+_\d+.html',
    "lastPage": r'\d+',
    "image": r'http://img1.mm131.me/pic/\d+/\d+.jpg',
    "cardTitle": r'<h5>(.*)</h5>',
    "cardHolderAmount": r'共\d+页',
}

config = {
    "scratchFileName": "sexyScratchData",
}