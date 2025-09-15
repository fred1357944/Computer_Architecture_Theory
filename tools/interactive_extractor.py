#!/usr/bin/env python3
"""
互動式程式碼提取工具
協助從PDF截圖中快速建立範例
"""

import os
import json
from pathlib import Path
from datetime import datetime

class InteractiveExtractor:
    def __init__(self):
        self.examples_dir = Path("examples")
        self.examples_dir.mkdir(exist_ok=True)
        self.load_progress()

    def load_progress(self):
        """載入進度"""
        self.progress_file = Path("extraction_progress.json")
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                "extracted": [],
                "next_id": 2,  # 從2開始（1已完成）
                "categories": {
                    "basic": [],
                    "geometry": [],
                    "architecture": [],
                    "analysis": [],
                    "advanced": []
                }
            }

    def save_progress(self):
        """儲存進度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def add_example(self, code: str, name: str, category: str, description: str):
        """新增範例"""
        example_id = self.progress["next_id"]
        example_dir = self.examples_dir / f"{example_id:02d}_{name}"
        example_dir.mkdir(exist_ok=True)

        # 儲存程式碼
        code_file = example_dir / "code.py"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)

        # 建立README
        readme_content = f"""# 範例 {example_id:02d}: {description}

## 類別
{category}

## 程式碼
```python
{code}
```

## 功能說明
{description}

## 學習重點
- 待補充...

## AI分析提示詞
```
分析這段Grasshopper Python程式碼的：
1. 核心功能
2. 使用的Rhino.Geometry方法
3. 可能的應用場景
4. 改進建議
```

## 常見問題
- Q: 待補充...
- A: 待補充...

## 相關範例
- 待補充...

## 加入日期
{datetime.now().strftime('%Y-%m-%d')}
"""
        readme_file = example_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        # 更新進度
        self.progress["extracted"].append({
            "id": example_id,
            "name": name,
            "category": category,
            "description": description,
            "date": datetime.now().isoformat()
        })
        self.progress["categories"][category].append(example_id)
        self.progress["next_id"] += 1
        self.save_progress()

        print(f"✅ 已新增範例 {example_id:02d}: {name}")
        return example_id

    def list_examples(self):
        """列出所有範例"""
        print("\n📚 已提取的範例：")
        for category, ids in self.progress["categories"].items():
            if ids:
                print(f"\n{category.upper()}:")
                for id in ids:
                    example = next(e for e in self.progress["extracted"] if e["id"] == id)
                    print(f"  {id:02d}. {example['description']}")

    def get_next_examples(self):
        """建議下一批要提取的範例"""
        suggestions = {
            "basic": [
                "迴圈與條件",
                "列表操作",
                "DataTree基礎"
            ],
            "geometry": [
                "點陣列生成",
                "曲線分割",
                "曲面細分",
                "Voronoi圖案"
            ],
            "architecture": [
                "參數化樓梯",
                "百葉窗系統",
                "空間框架",
                "立面開窗"
            ],
            "analysis": [
                "日照分析",
                "視線分析",
                "最短路徑"
            ],
            "advanced": [
                "遞迴分形",
                "遺傳演算法",
                "外部資料整合"
            ]
        }

        print("\n📋 建議提取的範例：")
        for category, examples in suggestions.items():
            existing = len(self.progress["categories"][category])
            needed = 3 - existing  # 每類別至少3個
            if needed > 0:
                print(f"\n{category.upper()} (還需要 {needed} 個):")
                for ex in examples[:needed]:
                    print(f"  - {ex}")

if __name__ == "__main__":
    extractor = InteractiveExtractor()

    # 顯示當前進度
    extractor.list_examples()
    extractor.get_next_examples()

    print("\n" + "="*50)
    print("📝 使用方法：")
    print("1. 截圖PDF中的程式碼")
    print("2. 用Claude識別程式碼")
    print("3. 執行：extractor.add_example(code, name, category, description)")
    print("4. 自動儲存並更新GitHub")
    print("="*50)