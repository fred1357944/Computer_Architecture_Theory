#!/usr/bin/env python3
"""
簡化版PDF掃描器
快速提取程式碼區塊
"""

import fitz  # PyMuPDF
import json
from pathlib import Path
from PIL import Image
import io

class SimpleScanner:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.output_dir = Path("extracted_codes")
        self.output_dir.mkdir(exist_ok=True)

    def scan_pdf(self, start_page: int = 1, end_page: int = None):
        """掃描PDF並截取所有圖片"""
        doc = fitz.open(self.pdf_path)

        if end_page is None:
            end_page = len(doc)

        print(f"📄 掃描第 {start_page} 到 {end_page} 頁...")

        screenshots = []
        for page_num in range(start_page - 1, min(end_page, len(doc))):
            page = doc[page_num]

            # 取得頁面截圖
            mat = fitz.Matrix(2, 2)  # 2x放大
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")

            # 儲存截圖
            img_path = self.output_dir / f"page_{page_num + 1:03d}.png"
            with open(img_path, 'wb') as f:
                f.write(img_data)

            screenshots.append({
                'page': page_num + 1,
                'path': str(img_path),
                'width': pix.width,
                'height': pix.height
            })

            print(f"  ✅ 第 {page_num + 1} 頁已截圖")

        doc.close()

        # 儲存索引
        index_file = self.output_dir / "screenshots_index.json"
        with open(index_file, 'w') as f:
            json.dump(screenshots, f, indent=2)

        print(f"\n✅ 完成！共截取 {len(screenshots)} 頁")
        print(f"📁 截圖儲存在：{self.output_dir}")
        print(f"📄 索引檔案：{index_file}")

        return screenshots

    def extract_specific_pages(self, page_list: list):
        """提取特定頁面"""
        doc = fitz.open(self.pdf_path)

        results = []
        for page_num in page_list:
            if page_num <= len(doc):
                page = doc[page_num - 1]
                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)

                img_path = self.output_dir / f"code_page_{page_num:03d}.png"
                pix.save(str(img_path))

                results.append({
                    'page': page_num,
                    'screenshot': str(img_path)
                })

                print(f"✅ 已提取第 {page_num} 頁")

        doc.close()
        return results

# 測試腳本
if __name__ == "__main__":
    scanner = SimpleScanner("../GH_Python_2020_04_19_23_52_15.pdf")

    print("📋 使用方法：")
    print("1. scanner.scan_pdf(1, 10) - 掃描1-10頁")
    print("2. scanner.extract_specific_pages([5, 10, 15]) - 提取特定頁")
    print("\n準備就緒！")