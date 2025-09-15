#!/usr/bin/env python3
"""
智能程式碼掃描器
精確識別真正的程式碼區塊（含行號和Line Description）
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Tuple
import re

class SmartCodeScanner:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.code_blocks = []
        self.screenshots_dir = Path("code_screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

    def analyze_entire_pdf(self):
        """分析整本PDF，找出所有程式碼區塊"""
        print("📚 開始分析整本PDF...")
        print(f"總頁數：{len(self.doc)}")

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()

            # 檢查是否包含程式碼特徵
            if self.has_code_features(text):
                # 提取頁面圖片
                mat = fitz.Matrix(2, 2)  # 2x放大
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")

                # 保存頁面截圖
                img_path = self.screenshots_dir / f"page_{page_num + 1:03d}.png"
                with open(img_path, 'wb') as f:
                    f.write(img_data)

                # 分析頁面內容
                code_info = self.analyze_page(page_num + 1, text, img_path)
                if code_info:
                    self.code_blocks.append(code_info)

            # 進度顯示
            if (page_num + 1) % 10 == 0:
                print(f"  已分析 {page_num + 1}/{len(self.doc)} 頁...")

        # 處理跨頁程式碼
        self.merge_continued_code()

        print(f"\n✅ 分析完成！找到 {len(self.code_blocks)} 個程式碼區塊")
        return self.code_blocks

    def has_code_features(self, text: str) -> bool:
        """檢查頁面是否包含程式碼特徵"""
        # 特徵1：有行號（連續的 1, 2, 3...）
        line_numbers = re.findall(r'^\s*(\d+)\s+', text, re.MULTILINE)
        has_line_numbers = len(line_numbers) > 2

        # 特徵2：包含Python關鍵字
        python_keywords = ['import', 'for', 'if', 'def', 'class', 'print',
                          'return', 'while', 'try', 'except']
        has_keywords = any(keyword in text for keyword in python_keywords)

        # 特徵3：包含Line Description標記
        has_line_desc = 'Line Description' in text or '說明' in text

        # 特徵4：包含Grasshopper相關內容
        has_gh = any(word in text for word in ['rhinoscriptsyntax', 'Rhino.Geometry',
                                                'GhPython', 'Grasshopper'])

        return (has_line_numbers and has_keywords) or has_line_desc or has_gh

    def analyze_page(self, page_num: int, text: str, img_path: Path) -> Dict:
        """分析單頁內容，提取程式碼資訊"""
        lines = text.split('\n')

        # 找程式碼開始和結束
        code_start = None
        code_end = None
        code_lines = []
        description_lines = []
        in_description = False

        for i, line in enumerate(lines):
            # 檢測行號開頭的程式碼行
            if re.match(r'^\s*\d+\s+', line):
                if code_start is None:
                    code_start = i
                code_end = i
                code_lines.append(line)

            # 檢測Line Description
            elif 'Line Description' in line or '說明' in line:
                in_description = True

            elif in_description:
                description_lines.append(line)

        if code_lines:
            # 檢查是否為跨頁（程式碼在頁面底部）
            is_continued = code_end and code_end > len(lines) - 5

            return {
                'page': page_num,
                'screenshot': str(img_path),
                'code_lines': code_lines,
                'description': '\n'.join(description_lines),
                'is_continued': is_continued,
                'line_count': len(code_lines),
                'has_description': len(description_lines) > 0
            }

        return None

    def merge_continued_code(self):
        """合併跨頁的程式碼"""
        merged = []
        i = 0

        while i < len(self.code_blocks):
            current = self.code_blocks[i]

            # 如果當前程式碼標記為跨頁
            if current.get('is_continued', False):
                # 檢查下一頁
                if i + 1 < len(self.code_blocks):
                    next_block = self.code_blocks[i + 1]
                    if next_block['page'] == current['page'] + 1:
                        # 合併程式碼
                        merged_block = {
                            'pages': [current['page'], next_block['page']],
                            'screenshots': [current['screenshot'], next_block['screenshot']],
                            'code_lines': current['code_lines'] + next_block['code_lines'],
                            'description': current['description'] + '\n' + next_block['description'],
                            'is_merged': True,
                            'line_count': current['line_count'] + next_block['line_count']
                        }
                        merged.append(merged_block)
                        i += 2  # 跳過下一個已合併的區塊
                        continue

            merged.append(current)
            i += 1

        self.code_blocks = merged
        print(f"  合併跨頁後：{len(self.code_blocks)} 個程式碼區塊")

    def identify_true_code_blocks(self) -> List[Dict]:
        """識別真正的程式碼區塊（包含行號和程式碼內容）"""
        true_blocks = []

        for block in self.code_blocks:
            # 檢查是否為真正的程式碼
            has_valid_code = False

            for line in block['code_lines']:
                # 移除行號後檢查是否有實際程式碼
                code_part = re.sub(r'^\s*\d+\s+', '', line)
                if code_part.strip() and not code_part.startswith('#'):
                    has_valid_code = True
                    break

            if has_valid_code:
                true_blocks.append(block)

        return true_blocks

    def generate_report(self):
        """生成程式碼清單報告"""
        report = {
            'total_pages': len(self.doc),
            'code_blocks': [],
            'statistics': {
                'total_blocks': len(self.code_blocks),
                'with_description': 0,
                'cross_page': 0,
                'by_chapter': {}
            }
        }

        for block in self.code_blocks:
            # 提取程式碼預覽（前3行）
            preview = '\n'.join(block['code_lines'][:3])

            block_info = {
                'id': len(report['code_blocks']) + 1,
                'pages': block.get('pages', [block.get('page', 0)]),
                'line_count': block['line_count'],
                'has_description': block.get('has_description', False),
                'preview': preview,
                'screenshot': block.get('screenshot', '')
            }

            report['code_blocks'].append(block_info)

            # 更新統計
            if block.get('has_description'):
                report['statistics']['with_description'] += 1
            if block.get('is_merged'):
                report['statistics']['cross_page'] += 1

        # 保存報告
        with open('code_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report

    def display_summary(self):
        """顯示分析摘要"""
        print("\n" + "="*60)
        print("📊 程式碼分析摘要")
        print("="*60)

        true_blocks = self.identify_true_code_blocks()

        print(f"總頁數：{len(self.doc)}")
        print(f"找到程式碼區塊：{len(self.code_blocks)}")
        print(f"真正的程式碼：{len(true_blocks)}")
        print(f"有Line Description：{sum(1 for b in self.code_blocks if b.get('has_description'))}")
        print(f"跨頁程式碼：{sum(1 for b in self.code_blocks if b.get('is_merged'))}")

        print("\n📑 程式碼清單：")
        for i, block in enumerate(true_blocks[:10], 1):  # 顯示前10個
            pages = block.get('pages', [block.get('page', 0)])
            page_str = f"第 {pages[0]} 頁" if len(pages) == 1 else f"第 {pages[0]}-{pages[1]} 頁"
            print(f"{i:2d}. {page_str}: {block['line_count']} 行程式碼")

            # 顯示預覽
            if block['code_lines']:
                preview = block['code_lines'][0]
                preview = re.sub(r'^\s*\d+\s+', '', preview)  # 移除行號
                print(f"    預覽: {preview[:50]}...")

        if len(true_blocks) > 10:
            print(f"\n... 還有 {len(true_blocks) - 10} 個程式碼區塊")

    def prepare_for_ocr(self):
        """準備OCR處理清單"""
        ocr_tasks = []

        for i, block in enumerate(self.identify_true_code_blocks()):
            task = {
                'id': i + 1,
                'pages': block.get('pages', [block.get('page', 0)]),
                'screenshots': block.get('screenshots', [block.get('screenshot', '')]),
                'estimated_lines': block['line_count'],
                'has_description': block.get('has_description', False),
                'output_file': f"code_{i+1:03d}_p{block.get('pages', [block.get('page', 0)])[0]}.py"
            }
            ocr_tasks.append(task)

        # 保存OCR任務清單
        with open('ocr_tasks.json', 'w') as f:
            json.dump(ocr_tasks, f, indent=2)

        print(f"\n✅ 已準備 {len(ocr_tasks)} 個OCR任務")
        return ocr_tasks

if __name__ == "__main__":
    scanner = SmartCodeScanner("../GH_Python_2020_04_19_23_52_15.pdf")

    # 步驟1：分析整本PDF
    scanner.analyze_entire_pdf()

    # 步驟2：顯示摘要
    scanner.display_summary()

    # 步驟3：生成報告
    report = scanner.generate_report()
    print(f"\n📄 報告已保存至：code_analysis_report.json")

    # 步驟4：準備OCR任務
    tasks = scanner.prepare_for_ocr()
    print(f"📝 OCR任務清單已保存至：ocr_tasks.json")

    print("\n" + "="*60)
    print("下一步：")
    print("1. 檢查 code_analysis_report.json 確認程式碼區塊")
    print("2. 確認後執行OCR提取")
    print("3. 按章節和頁碼分類儲存")
    print("="*60)