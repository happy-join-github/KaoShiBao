import json
def export_questions_to_html(data, output_file='questions.html'):
    """将题目数据导出为HTML表格"""
    
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>题目列表</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .question {{
            font-weight: bold;
            font-size: 16px;
            line-height: 1.6;
            min-width: 300px;
        }}
        .option {{
            margin: 5px 0;
            padding: 5px 10px;
            border-radius: 4px;
            background-color: #f8f8f8;
        }}
        .option.correct {{
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            font-weight: bold;
        }}
        .analysis {{
            font-size: 14px;
            color: #666;
            font-style: italic;
            min-width: 250px;
        }}
        .answer {{
            color: #28a745;
            font-weight: bold;
            font-size: 18px;
        }}
        .question-number {{
            color: #666;
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>题目列表</h1>
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">序号</th>
                    <th style="width: 40%;">题目</th>
                    <th style="width: 35%;">选项</th>
                    <th style="width: 15%;">答案与解析</th>
                </tr>
            </thead>
            <tbody>
{rows}
            </tbody>
        </table>
    </div>
</body>
</html>"""
    
    rows_html = ""
    
    for idx, item in enumerate(data, 1):
        # 获取题目（优先使用解密后的题目）
        question = item.get('decrypted_question', item.get('question', ''))
        
        # 获取选项，确保是列表格式
        options_raw = item.get('options', [])
        
        # 如果是字符串，解析为JSON
        if isinstance(options_raw, str):
            try:
                options = json.loads(options_raw)
            except:
                print(f"警告: 第{idx}题的options解析失败")
                options = []
        else:
            options = options_raw
        
        options_html = ""
        for opt in options:
            # 确保opt是字典
            if not isinstance(opt, dict):
                continue
                
            key = opt.get('Key', opt.get('keyC', ''))
            value = opt.get('Value', '')
            
            # 判断是否是正确答案
            is_correct = key == item.get('answer', '')
            correct_class = ' correct' if is_correct else ''
            options_html += f'<div class="option{correct_class}"><strong>{key}.</strong> {value}</div>'
        
        # 获取答案和解析
        answer = item.get('answer', '')
        analysis = item.get('analysis', '')
        
        # 构建行HTML
        row_html = f"""                <tr>
                    <td class="question-number">{idx}</td>
                    <td class="question">{question}</td>
                    <td>{options_html}</td>
                    <td>
                        <div class="answer">答案: {answer}</div>
                        <div class="analysis">{analysis}</div>
                    </td>
                </tr>"""
        rows_html += row_html
    
    # 填充模板
    html_content = html_template.format(rows=rows_html)
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML文件已导出到: {output_file}")
