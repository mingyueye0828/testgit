# -*- coding: utf-8 -*-
# @Time : 2023/8/14 8:35
# @Author : Jiweizhu
# @File : data_processing.py
# @Project : program
import json
import re
import cn2an
from zhon import hanzi

# 读取文本文件内容并合并分行数据，使每一行为一个完整的JSON数据
# 去除首位空白，去除转义字符
def read_and_merge_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    merged_lines = []
    current_str = ""
    for line in lines:
        line = line.strip()
        line = re.sub(r'\\(?![/bfnrt"\\\'])', '', line)
        if line.startswith("{") and line.endswith("}"):
            current_str = line
            merged_lines.append(current_str)
        else:
            current_str += line
    return merged_lines

# 处理文本内容，保留数字、汉字和英文,并将阿拉伯数字转换为中文
def process_text(text):
    cleaned_text = re.sub(f"[^{hanzi.characters}0-9a-zA-Z\u4e00-\u9fff]", " ", text)
    cleaned_text = cn2an.transform(cleaned_text, "an2cn")
    return cleaned_text

# 加载输入文件，处理输入文件，输出JSON规范格式文件
# 保留长度大于3小于50的字段，并将其保存
def main():
    merged_lines = read_and_merge_lines('fake_mark.txt')

    processed_result = []
    for line in merged_lines:
        try:
            data = json.loads(line)
            # 使用 .get() 方法来安全地获取字典中的值，避免出现 KeyError 错误。
            data_list = data.get("resultTxt", [])
            for text_one in data_list:
                text = text_one.get("text", "").strip()
                cleaned_text = process_text(text)
                if 3 <= len(cleaned_text) <= 50:
                    processed_result.append(cleaned_text)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

    with open('processed_result.txt', 'w', encoding='utf-8') as f:
        json.dump(processed_result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
