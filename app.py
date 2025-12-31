import json
import time
import random
import os
from bs4 import BeautifulSoup,NavigableString
from tqdm import tqdm
from datetime import datetime
# 导入工具进行解析数据
from utils.solutionData import getTitleData
from utils.FontDecryption import build_mapping_from_anti_font,build_base_hash_db,load_base_hash_db
from fonts.fontDownload import getFonts

def replace_chars_with_mapping(text, mapping):
    new_text = ""
    for char in text:
        if char in mapping:
            new_text += mapping[char]
        else:
            new_text += char
    return new_text

def decrypt_html(html_content, mapping):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    def process_node(node):
        if isinstance(node, NavigableString):
            replaced_text = replace_chars_with_mapping(str(node), mapping)
            node.replace_with(replaced_text)
        elif node.name:
            for child in node.children:
                process_node(child)
    
    for child in soup.children:
        process_node(child)
    
    return str(soup)

def decrypt_data(data,map,is_export:bool=True):
    newData = []

    for i in tqdm(range(len(data)), desc="解密字符"):
        for j in range(len(data[i])):
            if 'parent_question' in data[i][j]:
                continue
            html_data = data[i][j]['question']
            decrypted_html = decrypt_html(html_data, map[data[i][j]['special_font']])
            data[i][j]['decrypted_question'] = decrypted_html
            data[i][j]['options'] = json.loads(data[i][j]['options'])
        newData.extend(data[i])

    json.dump(newData, open('result/titleData_decrypted.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print("解密完成，请查看result/titleData_decrypted.json")

def main():
    if not os.path.exists('title.json'):
        print("请去浏览器把文件复制回来在运行程序")
        exit()

    data_savepath = f"result/{datetime.now().strftime('%Y%m%d%H%M%S')}"
    if not os.path.exists(data_savepath):
        os.makedirs(data_savepath)

    data_savepath+='/titleData.json'
    # 解析试题
    data = json.load(open('title.json','r',encoding='utf-8'))

    # 保存数据
    fonts = getTitleData(data,False,data_savepath)

    # 下载字体
    for i in tqdm(range(len(fonts)),desc="正在下载字体请稍后"):
        getFonts(fonts[i],'fonts/'+fonts[i]+'.ttf')
        time.sleep(random.randint(1,3))


    microsoft_yahei_path = r'fonts\MSYH.TTC'
    # 哈希基准库
    hash_db_Path = r'fonts\msyh_glyph_hashes.json'  

    map = {}

    if not os.path.exists(hash_db_Path):
        build_base_hash_db(microsoft_yahei_path, hash_db_Path, font_index=0)

    base_db = load_base_hash_db(hash_db_Path)


    for i in tqdm(range(len(fonts)),desc="构建每个字体的字符映射"):
        ttfpath = 'fonts/'+fonts[i]+'.ttf'
        dicmap = build_mapping_from_anti_font(ttfpath, base_db)
        map[fonts[i]] = dicmap

    # 加载数据进行替换
    data = json.load(open(data_savepath,'r',encoding='utf-8'))
    

    decrypt_data(data,map)

main()