#!/usr/bin/env python3
"""
自動程式碼提取器
掃描所有頁面，識別並提取程式碼
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict

class AutoExtractor:
    def __init__(self):
        self.screenshots_dir = Path("extracted_codes")
        self.output_dir = Path("examples")
        self.output_dir.mkdir(exist_ok=True)

    def identify_code_regions(self, image_path: Path) -> List[Dict]:
        """識別圖片中的程式碼區域（灰色背景）"""
        img = cv2.imread(str(image_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 尋找灰色背景區域（程式碼通常在230-245的灰度值）
        mask = cv2.inRange(gray, 230, 245)

        # 形態學操作
        kernel = np.ones((10,10), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 找輪廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        code_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 過濾條件：寬度>300，高度>100
            if w > 300 and h > 100:
                code_regions.append({
                    'x': x, 'y': y, 'w': w, 'h': h,
                    'area': w * h
                })

        # 按面積排序，取最大的幾個
        code_regions.sort(key=lambda r: r['area'], reverse=True)
        return code_regions[:3]  # 最多3個區域

    def extract_region(self, image_path: Path, region: Dict) -> str:
        """提取特定區域並保存"""
        img = cv2.imread(str(image_path))
        x, y, w, h = region['x'], region['y'], region['w'], region['h']

        # 提取區域
        roi = img[y:y+h, x:x+w]

        # 保存區域圖片
        page_num = image_path.stem.split('_')[1]
        output_path = self.output_dir / f"code_p{page_num}_{x}_{y}.png"
        cv2.imwrite(str(output_path), roi)

        return str(output_path)

    def scan_all_screenshots(self):
        """掃描所有截圖"""
        screenshots = sorted(self.screenshots_dir.glob("page_*.png"))

        results = []
        for screenshot in screenshots:
            page_num = int(screenshot.stem.split('_')[1])

            # 識別程式碼區域
            regions = self.identify_code_regions(screenshot)

            if regions:
                print(f"📄 第 {page_num} 頁找到 {len(regions)} 個程式碼區塊")

                for i, region in enumerate(regions):
                    # 提取並保存區域
                    code_path = self.extract_region(screenshot, region)

                    results.append({
                        'page': page_num,
                        'region': i + 1,
                        'image': code_path,
                        'dimensions': f"{region['w']}x{region['h']}"
                    })

        # 保存結果
        with open(self.output_dir / "code_regions.json", 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n✅ 完成！找到 {len(results)} 個程式碼區塊")
        return results

    def process_with_ocr(self, image_path: str) -> str:
        """使用OCR處理圖片（這裡可以整合Dots OCR）"""
        # 暫時返回路徑，實際使用時呼叫Dots OCR
        return f"待處理: {image_path}"

if __name__ == "__main__":
    extractor = AutoExtractor()

    # 檢查是否有截圖
    if not Path("extracted_codes").exists():
        print("❌ 請先執行 simple_scanner.py 掃描PDF")
    else:
        print("🔍 開始識別程式碼區塊...")
        results = extractor.scan_all_screenshots()

        print("\n📋 接下來的步驟：")
        print("1. 檢查 examples/ 資料夾中的程式碼截圖")
        print("2. 使用 Dots OCR 或手動識別程式碼")
        print("3. 整理並分類到對應資料夾")