import os
import random
import shutil
import platform
import sys
from pathlib import Path

# ==========================================
# 1. 丰富的素材库 (随机的灵魂)
# ==========================================
FILE_COUNT = 50
TARGET_FOLDER_NAME = "agent-test-files"

PREFIXES = [
    "【最终版】", "【草稿】", "复件-", "Temp_", "2023年度-", "2024年第一季度-", 
    "紧急-", "备份_", "来自微信的_", "扫描件_", "", "", "", ""
]

BASE_NAMES = [
    "项目Alpha汇报PPT", "Q1财务预算汇总表", "周一晨会纪要", "客户Logo源文件",
    "三亚团建照片_高清", "服务器错误日志_Dump", "用户数据库导出", "Python自动化脚本测试",
    "张伟_个人简历", "增值税电子发票(报销用)", "产品发布会演示文稿", "随手记",
    "配置文件", "数据导出_未清洗", "说明文档", "合同_甲方盖章版", "年终总结初稿"
]

EXT_GROUPS = {
    "Docs":    [".docx", ".pdf", ".xlsx", ".pptx", ".txt", ".md", ".doc"],
    "Images":  [".jpg", ".png", ".gif", ".svg", "截图.png"],
    "Code":    [".py", ".js", ".json", ".xml", ".html", ".css", ".sql"],
    "Archive": [".zip", ".rar", ".7z", ".tar.gz"],
    "Junk":    [".log", ".tmp", ".bak", ".old", ".ini"],
    "Media":   [".mp4", ".mp3", ".wav"]
}

# ==========================================
# 2. 核心逻辑
# ==========================================
def get_base_dir():
    """双保险：获取脚本所在目录，防止找不到家"""
    try:
        return Path(__file__).resolve().parent
    except NameError:
        # 如果是在交互式窗口运行
        return Path(os.getcwd())

def create_test_files():
    # --- 路径准备 ---
    current_dir = get_base_dir()
    target_path = current_dir / TARGET_FOLDER_NAME

    print(f"脚本位置: {current_dir}")
    print(f"目标目录: {target_path}")

    # --- 清理旧数据 ---
    if target_path.exists():
        print("发现旧目录，正在清理重置...")
        try:
            shutil.rmtree(target_path)
        except OSError as e:
            print(f"⚠️ 清理旧目录失败 (可能文件被打开): {e}")

    # --- 创建新目录 ---
    target_path.mkdir(parents=True, exist_ok=True)
    print(f"🚀 开始生成 {FILE_COUNT} 个随机文件...")

    # --- 循环生成 ---
    type_keys = list(EXT_GROUPS.keys())

    for i in range(1, FILE_COUNT + 1):
        # 1. 随机组合名字
        prefix = random.choice(PREFIXES)
        base_name = random.choice(BASE_NAMES)
        
        # 2. 随机选类型 (轮询大类，随机后缀)
        type_key = type_keys[i % len(type_keys)]
        extension = random.choice(EXT_GROUPS[type_key])
        
        # 3. 加个随机数防止重名
        random_suffix = random.randint(100, 999)

        # 4. 拼装完整路径
        file_name = f"{prefix}{base_name}_{random_suffix}{extension}"
        file_path = target_path / file_name

        try:
            # 创建文件 (写入一点点内容，防止某些系统把空文件当垃圾清理)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"这是 Agent 测试文件: {file_name}")
            
            # 打印进度点
            print(".", end="", flush=True)
            if i % 10 == 0:
                print(f" {i}")
                
        except Exception as e:
            print(f"\n❌ 创建失败: {e}")

    print("\n" + "=" * 40)
    print(f"✅ 大功告成！已生成 {FILE_COUNT} 个文件。")
    print(f"📂 请去这里查看: {target_path}")
    print("=" * 40)

    # --- 尝试自动打开文件夹 ---
    try:
        if platform.system() == "Windows":
            os.startfile(target_path)
        elif platform.system() == "Darwin":
            os.system(f"open '{target_path}'")
    except Exception:
        pass

if __name__ == "__main__":
    create_test_files()