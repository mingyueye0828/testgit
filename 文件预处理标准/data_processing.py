# -*- coding: utf-8 -*-
# @Time : 2023/8/14 8:35
# @Author : Jiweizhu
# @File : data_processing.py
# @Project : program
import json
import re
from cn2an import Transform
from zhon import hanzi


# 读取文本文件内容并合并分行数据，使每一行为一个完整的JSON数据
def read_and_merge_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    merged_lines = []
    current_str = ""
    for line in lines:
        line = line.strip()
        # 去除首位空白，去除转义字符
        line = re.sub(r'\\(?![/bfnrt"\\\'])', '', line)
        if line.startswith("{") and line.endswith("}"):
            current_str = line
            merged_lines.append(current_str)
        else:
            current_str += line
    return merged_lines


# 分割进行转换，防止过大
def split_and_transform(text, chunk_size=16):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    transformer = Transform()
    transformed_chunks = [transformer.transform(chunk, "an2cn") for chunk in chunks]
    return "".join(transformed_chunks)


# 处理文本内容，保留数字、汉字和英文,并将阿拉伯数字转换为中文
def process_text(text):
    # 除了小数点、数字、汉字、英文其余都删去
    cleaned_text = re.sub(f"[^{hanzi.characters}0-9a-zA-Z\u4e00-\u9fff.-]", "", text)
    # 分割并进行传输，并清除.
    cleaned_text = split_and_transform(cleaned_text)
    # 清除.-
    cleaned_text = cleaned_text.replace(".", "").replace("-", "")
    return cleaned_text


# 加载输入文件，处理输入文件，输出JSON规范格式文件
# 保留长度大于3小于50的字段，并将其保存
def main(filename, processed_result):
    merged_lines = read_and_merge_lines(filename)
    f = open(processed_result, 'w', encoding='utf-8')
    for line in merged_lines:
        try:
            data = json.loads(line)
            # 使用 .get() 方法来安全地获取字典中的值，避免出现 KeyError 错误。
            sentences = data.get("resultTxt", [])
            # 如果检测到空，则进行提醒
            if not sentences:
                print("sentences is empty")
            else:
                for sentence in sentences:
                    text = sentence.get("text", "").strip()
                    cleaned_text = process_text(text)
                    if 3 <= len(cleaned_text) <= 50:
                        f.write(cleaned_text + "\n")
        except Exception as e:
            print("Error:", e)


# 修改代码，避免硬编码，可以进行传参,输入文件和输出文件
if __name__ == "__main__":
    main('fake_mark.txt', 'processed_result.txt')
