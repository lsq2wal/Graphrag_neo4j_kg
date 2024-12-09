import os
import re
import glob
import csv

def process_and_store_biology_texts(directory_path, output_csv_path):
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['file_name', 'cleaned_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for file_path in glob.glob(os.path.join(directory_path, "*.txt")):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            # 简单的文本清理，例如移除多余的空格和特殊字符
            cleaned_text = re.sub(r'\s+', ' ', text)
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,]', '', cleaned_text)
            
            # 写入 CSV 文件
            writer.writerow({'file_name': os.path.basename(file_path), 'cleaned_text': cleaned_text})
