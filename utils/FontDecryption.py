import hashlib
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.recordingPen import RecordingPen
import json
import os
from tqdm import tqdm

def get_glyph_hash(font, glyph_name):
    """
    使用RecordingPen提取字形的路径命令，然后序列化为字符串并计算MD5哈希
    """
    if glyph_name not in font.getGlyphSet():
        return None
    pen = RecordingPen()
    glyph = font.getGlyphSet()[glyph_name]
    glyph.draw(pen)
    serialized = str(pen.value)
    return hashlib.md5(serialized.encode('utf-8')).hexdigest()

def build_base_hash_db(ttc_path, db_path, font_index=0):
    """
    从微软雅黑TTC构建基准哈希数据库
    font_index: TTC集合中字体索引，0通常是Regular（微软雅黑常规）
    保存格式: {hash: char} （一个hash可能对应多个char，但常见汉字通常唯一）
    """
    collection = TTCollection(ttc_path)
    font = collection.fonts[font_index]  # 选择常规体
    cmap = font.getBestCmap()
   
    hash_to_char = {}
    for code, gname in tqdm(cmap.items(),desc="正在构建基准库"):
        h = get_glyph_hash(font, gname)
        if h:
            char = chr(code)
            if h not in hash_to_char:
                hash_to_char[h] = char
   
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(hash_to_char, f, ensure_ascii=False, indent=2)
   
    print(f"基准哈希库构建完成，保存到 {db_path}，共 {len(hash_to_char)} 个字形")
    collection.close()

def load_base_hash_db(db_path):
    """加载基准哈希库"""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"基准库不存在，请先运行 build_base_hash_db: {db_path}")
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_mapping_from_anti_font(ttf_path, base_hash_db):
    """
    从反爬字体中提取每个glyph的hash，对比基准库，构建映射
    返回 {'假字符': '真字符', glyph_name: '真字符'}  但最终map只取假字符部分
    """
    font = TTFont(ttf_path)
    glyph_names = font.getGlyphNames()
    cmap = font.getBestCmap()  
   
    mapping = {}  # 完整映射，包括glyph_name
    fake_to_real = {}  # 只包含 {'假字符': '真字符'}

    for gname in tqdm(glyph_names,desc="正在构建字符映射"):
        if gname in ['.notdef', '.null']:  # 跳过特殊glyph
            continue
        h = get_glyph_hash(font, gname)
        if h and h in base_hash_db:
            real_char = base_hash_db[h]
            mapping[gname] = real_char
            
            # 找到这个glyph对应的所有私有unicode（假字符）
            codes = [c for c, gn in cmap.items() if gn == gname]
            for code in codes:
                fake_char = chr(code)
                fake_to_real[fake_char] = real_char
                mapping[fake_char] = real_char  # 可选：也加到完整mapping
    
    font.close()
    # , mapping
    return fake_to_real  # 返回专注的fake_to_real 和 完整mapping

if __name__=='__main__':
        
    # ------------------- 使用示例 -------------------
    # 微软雅黑ttc文件路径（Windows系统字体，通常是ttc集合，包含Regular, Bold等）
    microsoft_yahei_path = r'C:\WINDOWS\FONTS\MSYH.TTC'  # 注意使用raw字符串避免转义问题

    # 哈希基准库存储路径（建议填写一个json文件路径，用于保存基准哈希）
    hash_db_Path = r'fonts\msyh_glyph_hashes.json'  # 示例：保存到当前目录

    # 反爬ttf路径（需要破解的自定义字体文件路径，通常是woff或ttf）
    # ttfpath = r'fonts\k1e4836accefe5a26f166f2ddedc2a57a.ttf'  # 请替换为实际的反爬字体文件路径
    fontname = 'kd132f2af9d57c28bfa85073d55790e41.ttf'
    ttfpath = f'fonts/{fontname.split('.')[0]}'
    # 最终映射表 {'假字符': '真字符'}  （假字符为私有区unicode字符，如 chr(0xE123)）
    map = {}

    # 1. 第一步：构建基准哈希库（只需运行一次）
    if not os.path.exists(hash_db_Path):
        build_base_hash_db(microsoft_yahei_path, hash_db_Path, font_index=0)

    # 2. 加载基准库
    base_db = load_base_hash_db(hash_db_Path)
    # if not os.path.exists(ttfpath):
    #     downloadFont(fontname,ttfpath)

    # 3. 构建映射表（每次有新反爬字体时运行）
    # , full_map 'unicode->真字符'

    map = build_mapping_from_anti_font(ttfpath, base_db)
    # map = fake_map  # 使用所需的结构：{'假字符': '真字符'}

    print(f"映射完成，共 {len(map)} 个假字符匹配项")
    text = "制列排序浪法中，占用辅儿存储空察骨晚的是"
    realText = ''
    for i in text:
        realText+= map.get(i,i)
    print(realText)