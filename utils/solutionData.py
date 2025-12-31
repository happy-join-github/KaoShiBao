import json
from typing import List,Dict
import os
from tqdm import tqdm
# parent_question无字体加密
def getTitleData(data:Dict, is_show:bool=True, save_path:str='titleData.json')->List[str]:
    """
    提取题目数据中的指定字段
    
    参数:
        data: 原始数据列表
        is_show: 是否显示数据，False则保存到文件
        save_path: 保存路径（当is_show=False时）
    返回值:
        字体列表
    """
    newdata = []
    requireFields = ['question', 'qtype', 'options', 'answer', 'analysis', 'special_font']
    fonts = []
    # 遍历data数组
    # 十条数据
    for i in tqdm(len(data),desc='请在解析数据'):
        extracted = []
        fonts.append(data[i]['data'][0]['special_font'])
        # 处理每一条数据
        for item in data[i]['data']:
            obj = {}
            # 处理响应的字段
            for key in requireFields:
                obj[key] = item[key]
            if item.get('parent_question',False):
                obj['parent_question'] = item['parent_question']
            extracted.append(obj)
        newdata.append(extracted)
    
    # 根据is_show决定输出方式
    if not is_show:
        if not os.path.exists(save_path):
            name = save_path.split('/')[:-1]
            os.makedirs(name,exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(newdata, f, ensure_ascii=False, indent=2)
        print(f'数据已保存到 {save_path}')
    else:
        print(newdata)
    return list(set(fonts))
