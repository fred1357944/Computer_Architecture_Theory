#!/usr/bin/env python3
"""
PDF自動掃描與程式碼提取系統
自動識別灰色背景的程式碼區塊並提取
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
import pytesseract

class PDFCodeScanner:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.output_dir = Path("extracted_codes")
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

    def pdf_to_images(self, dpi: int = 200) -> List[Path]:
        """將PDF轉換為圖片"""
        print("📄 將PDF轉換為圖片...")
        doc = fitz.open(self.pdf_path)
        image_paths = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            mat = fitz.Matrix(dpi/72, dpi/72)
            pix = page.get_pixmap(matrix=mat)

            image_path = self.screenshots_dir / f"page_{page_num+1:03d}.png"
            pix.save(str(image_path))
            image_paths.append(image_path)

            if (page_num + 1) % 10 == 0:
                print(f"  已處理 {page_num + 1} 頁...")

        doc.close()
        print(f"✅ 完成：共 {len(image_paths)} 頁")
        return image_paths

    def detect_code_blocks(self, image_path: Path) -> List[Dict]:
        """檢測圖片中的程式碼區塊（灰色背景）"""
        img = cv2.imread(str(image_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 檢測灰色背景區域（程式碼區塊通常是灰色背景）
        # 灰色值範圍：230-245
        lower_gray = np.array([230])
        upper_gray = np.array([245])
        mask = cv2.inRange(gray, lower_gray, upper_gray)

        # 形態學操作，連接鄰近區域
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 找到輪廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        code_blocks = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # 過濾太小的區域（可能是噪音）
            if w > 200 and h > 50:  # 最小寬度200px，高度50px
                # 檢查是否包含行號（1, 2, 3...）
                roi = img[y:y+h, x:x+w]
                if self.has_line_numbers(roi):
                    code_blocks.append({
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'image': roi
                    })

        return code_blocks

    def has_line_numbers(self, image) -> bool:
        """檢查圖片是否包含行號"""
        # 轉換為灰度圖
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # 提取左側區域（行號通常在左側）
        height, width = gray.shape
        left_region = gray[:, :min(50, width//10)]

        # OCR識別
        try:
            text = pytesseract.image_to_string(left_region, config='--psm 6')
            # 檢查是否包含數字行號
            lines = text.strip().split('\n')
            numbers = [line.strip() for line in lines if line.strip().isdigit()]
            return len(numbers) > 2  # 至少有3個行號
        except:
            return False

    def extract_code_with_dots(self, image_path: Path) -> str:
        """使用Dots OCR提取程式碼"""
        # 這裡呼叫Dots OCR
        cmd = f"/opt/homebrew/Caskroom/miniconda/base/envs/dots_ocr/bin/python -m dots.ocr {image_path}"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout
        except:
            # 備用方案：使用pytesseract
            return pytesseract.image_to_string(str(image_path))

    def clean_code(self, raw_text: str) -> Tuple[str, str]:
        """清理提取的程式碼，分離程式碼和說明"""
        lines = raw_text.split('\n')

        code_lines = []
        description_lines = []
        in_description = False

        for line in lines:
            # 檢測"Line Description"標記
            if 'Line Description' in line or '說明' in line:
                in_description = True
                continue

            if not in_description:
                # 移除行號
                import re
                cleaned = re.sub(r'^\s*\d+\s+', '', line)
                if cleaned.strip():
                    code_lines.append(cleaned)
            else:
                if line.strip():
                    description_lines.append(line)

        code = '\n'.join(code_lines)
        description = '\n'.join(description_lines)

        # 修正常見OCR錯誤
        code = code.replace('．', '.')
        code = code.replace('，', ',')
        code = code.replace('（', '(')
        code = code.replace('）', ')')

        return code, description

    def process_page(self, page_num: int, image_path: Path) -> List[Dict]:
        """處理單頁"""
        print(f"📄 處理第 {page_num} 頁...")

        # 檢測程式碼區塊
        code_blocks = self.detect_code_blocks(image_path)

        results = []
        for i, block in enumerate(code_blocks):
            # 儲存程式碼區塊截圖
            block_path = self.screenshots_dir / f"page_{page_num:03d}_block_{i+1}.png"
            cv2.imwrite(str(block_path), block['image'])

            # 提取程式碼
            raw_text = self.extract_code_with_dots(block_path)
            code, description = self.clean_code(raw_text)

            if code.strip():
                results.append({
                    'page': page_num,
                    'block': i + 1,
                    'code': code,
                    'description': description,
                    'screenshot': str(block_path)
                })

                print(f"  ✅ 找到程式碼區塊 {i+1}")

        return results

    def scan_entire_pdf(self) -> Dict:
        """掃描整個PDF"""
        print("🔍 開始掃描PDF...")

        # 轉換PDF為圖片
        image_paths = self.pdf_to_images()

        all_codes = []
        for i, image_path in enumerate(image_paths):
            page_results = self.process_page(i + 1, image_path)
            all_codes.extend(page_results)

        # 儲存結果
        output_file = self.output_dir / "extracted_codes.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_codes, f, indent=2, ensure_ascii=False)

        print(f"\n✅ 掃描完成！")
        print(f"📊 統計：")
        print(f"  - 總頁數：{len(image_paths)}")
        print(f"  - 找到程式碼區塊：{len(all_codes)}")
        print(f"  - 結果儲存在：{output_file}")

        return {
            'total_pages': len(image_paths),
            'total_codes': len(all_codes),
            'codes': all_codes
        }

    def generate_examples(self, scan_results: Dict):
        """根據掃描結果生成範例檔案"""
        examples_dir = Path("examples")
        examples_dir.mkdir(exist_ok=True)

        # 分類程式碼
        categories = {
            'basic': [],
            'geometry': [],
            'architecture': [],
            'analysis': [],
            'advanced': []
        }

        for code_block in scan_results['codes']:
            code = code_block['code']

            # 簡單分類規則
            if 'for' in code and 'if' in code and 'curve' not in code:
                category = 'basic'
            elif any(word in code.lower() for word in ['curve', 'point', 'surface', 'mesh']):
                category = 'geometry'
            elif any(word in code.lower() for word in ['stair', 'window', 'wall', 'floor']):
                category = 'architecture'
            elif any(word in code.lower() for word in ['sun', 'analysis', 'optimize']):
                category = 'analysis'
            else:
                category = 'advanced'

            categories[category].append(code_block)

        # 生成範例檔案
        example_id = 2  # 從2開始（1已存在）
        for category, blocks in categories.items():
            for i, block in enumerate(blocks[:3]):  # 每類最多3個
                example_name = f"{example_id:02d}_{category}_{i+1}"
                example_dir = examples_dir / example_name
                example_dir.mkdir(exist_ok=True)

                # 儲存程式碼
                with open(example_dir / "code.py", 'w', encoding='utf-8') as f:
                    f.write(block['code'])

                # 儲存README
                with open(example_dir / "README.md", 'w', encoding='utf-8') as f:
                    f.write(f"# 範例 {example_id:02d}\n\n")
                    f.write(f"頁碼：{block['page']}\n\n")
                    f.write(f"## 程式碼\n```python\n{block['code']}\n```\n\n")
                    f.write(f"## 說明\n{block['description']}\n\n")

                example_id += 1

        print(f"✅ 已生成 {example_id - 2} 個範例")

if __name__ == "__main__":
    # 安裝依賴提醒
    print("⚠️  請先安裝依賴：")
    print("pip install pymupdf pillow opencv-python pytesseract numpy")
    print("brew install tesseract")
    print()

    scanner = PDFCodeScanner("../GH_Python_2020_04_19_23_52_15.pdf")

    # 執行掃描
    # results = scanner.scan_entire_pdf()
    # scanner.generate_examples(results)

    print("準備就緒！執行 scanner.scan_entire_pdf() 開始掃描")