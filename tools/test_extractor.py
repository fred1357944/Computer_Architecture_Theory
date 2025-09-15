#!/usr/bin/env python3
"""
測試提取器 - 提取前10個程式碼範例
測試OCR品質和準確度
"""

import json
from pathlib import Path
from typing import List, Dict

class TestExtractor:
    def __init__(self):
        # 載入OCR任務清單
        with open('ocr_tasks.json', 'r') as f:
            self.tasks = json.load(f)

        self.output_dir = Path("test_extractions")
        self.output_dir.mkdir(exist_ok=True)

    def get_first_10_tasks(self):
        """獲取前10個任務"""
        return self.tasks[:10]

    def display_tasks(self):
        """顯示前10個任務資訊"""
        print("📋 前10個程式碼提取任務：")
        print("="*60)

        for task in self.get_first_10_tasks():
            print(f"\n任務 {task['id']:02d}:")
            print(f"  頁碼: {task['pages']}")
            print(f"  預估行數: {task['estimated_lines']}")
            print(f"  有說明: {'✅' if task['has_description'] else '❌'}")
            print(f"  輸出檔案: {task['output_file']}")
            print(f"  截圖: {len(task['screenshots'])} 張")

if __name__ == "__main__":
    extractor = TestExtractor()
    extractor.display_tasks()

    print("\n" + "="*60)
    print("準備提取前10個程式碼...")
    print("這些涵蓋第10頁到第52頁的內容")
    print("包含基礎Python語法和List操作")