def getFonts(fontname,savepath):
    import requests

    headers = {
        'origin': 'https://www.kaoshibao.com',
        'referer': 'https://www.kaoshibao.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    }
    fontpath = fontname+'.ttf'
    response = requests.get(f'https://resource-cdn.kaoshibao.com/fonts/{fontpath}', headers=headers)
    with open(savepath, 'wb') as f:
        f.write(response.content)
    print(f'下载完成,保存到{savepath}')


