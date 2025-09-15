#!/usr/bin/env python3
"""
PDF程式碼提取工具
自動識別並提取GH Python教材中的程式碼區塊
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class CodeExtractor:
    def __init__(self, pdf_path: str, output_dir: str = "examples"):
        self.pdf_path = pdf_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def split_pdf(self) -> List[str]:
        """分割PDF為單頁"""
        print("📄 分割PDF...")
        temp_dir = Path("temp_pages")
        temp_dir.mkdir(exist_ok=True)

        cmd = f"qpdf --split-pages {self.pdf_path} {temp_dir}/page-%d.pdf"
        subprocess.run(cmd, shell=True)

        pages = sorted(temp_dir.glob("page-*.pdf"))
        print(f"✅ 分割完成：{len(pages)} 頁")
        return pages

    def extract_code_from_image(self, image_path: str) -> Dict:
        """從圖片提取程式碼（使用Dots OCR）"""
        # 這裡可以整合Dots OCR
        # 暫時返回模擬資料
        return {
            'code': '',
            'line_numbers': [],
            'confidence': 0.0
        }

    def identify_code_blocks(self, text: str) -> List[str]:
        """識別程式碼區塊的特徵"""
        code_blocks = []

        # 特徵1：有行號（1, 2, 3...）
        # 特徵2：包含Python關鍵字（import, for, if, def）
        # 特徵3：縮排結構

        patterns = [
            r'^\d+\s+import\s+',  # import語句
            r'^\d+\s+for\s+\w+\s+in\s+',  # for迴圈
            r'^\d+\s+if\s+',  # if條件
            r'^\d+\s+def\s+',  # 函數定義
            r'^\d+\s+class\s+',  # 類別定義
        ]

        lines = text.split('\n')
        code_start = None
        current_block = []

        for i, line in enumerate(lines):
            # 檢查是否為程式碼行
            is_code = any(re.match(pattern, line.strip()) for pattern in patterns)
            has_line_number = re.match(r'^\d+\s+', line.strip())

            if has_line_number or is_code:
                if code_start is None:
                    code_start = i
                current_block.append(line)
            elif code_start is not None and len(current_block) > 2:
                # 結束當前程式碼區塊
                code_blocks.append('\n'.join(current_block))
                current_block = []
                code_start = None

        # 處理最後一個區塊
        if current_block and len(current_block) > 2:
            code_blocks.append('\n'.join(current_block))

        return code_blocks

    def clean_code(self, code_text: str) -> str:
        """清理程式碼，移除行號和多餘格式"""
        lines = code_text.split('\n')
        cleaned = []

        for line in lines:
            # 移除行號（如：1, 2, 3...）
            line = re.sub(r'^\d+\s+', '', line)
            # 修正常見OCR錯誤
            line = line.replace('．', '.')
            line = line.replace('，', ',')
            line = line.replace('（', '(')
            line = line.replace('）', ')')
            cleaned.append(line)

        return '\n'.join(cleaned)

    def save_example(self, code: str, example_num: int, description: str = ""):
        """儲存範例程式碼"""
        example_dir = self.output_dir / f"{example_num:02d}_{self.sanitize_name(description)}"
        example_dir.mkdir(exist_ok=True)

        # 儲存程式碼
        code_file = example_dir / "code.py"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)

        # 建立README
        readme_file = example_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# 範例 {example_num:02d}: {description}\n\n")
            f.write("## 程式碼\n\n")
            f.write("```python\n")
            f.write(code)
            f.write("\n```\n\n")
            f.write("## 說明\n\n")
            f.write("待補充...\n\n")
            f.write("## AI分析提示詞\n\n")
            f.write("```\n")
            f.write("請分析這段Grasshopper Python程式碼：\n")
            f.write("[貼上程式碼]\n")
            f.write("1. 主要功能是什麼？\n")
            f.write("2. 使用了哪些Rhino.Geometry方法？\n")
            f.write("3. 如何改進？\n")
            f.write("```\n")

        print(f"💾 已儲存範例 {example_num:02d}: {description}")

    def sanitize_name(self, name: str) -> str:
        """清理檔名"""
        name = re.sub(r'[^\w\s-]', '', name.lower())
        name = re.sub(r'[-\s]+', '_', name)
        return name[:50]  # 限制長度

# 主程式
if __name__ == "__main__":
    extractor = CodeExtractor(
        pdf_path="../GH_Python_2020_04_19_23_52_15.pdf",
        output_dir="examples"
    )

    # 您提供的第一個範例
    example1 = """import rhinoscriptsyntax as rs

pts = []

for i in range(x):
    if i < y:
        pt = rs.AddPoint(i,0,0)
        pts.append(pt)
    else:
        pt = rs.AddPoint(i,10,0)
        pts.append(pt)

pts_out = pts"""

    # 儲存範例
    extractor.save_example(example1, 1, "conditional_point_array")

    print("\n✅ 程式碼提取系統已建立")
    print("📌 下一步：")
    print("1. 安裝 qpdf: brew install qpdf")
    print("2. 執行分頁: python tools/extract_code.py")
    print("3. 手動檢查並修正OCR結果")