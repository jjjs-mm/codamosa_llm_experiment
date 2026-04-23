# simple_demo.py

def check_string(s: str):
    # 容易覆盖的路径
    if not s:
        return "Empty"
    
    # 极难通过随机变异覆盖的路径 (DeepSeek 应该能一眼看穿)
    if s == "DeepSeek-V3-Magic-Token":
        return "You found the secret!"
    
    return "Normal string"

def calculate(a: int, b: int):
    if a > 100 and b < 0:
        if a + b == 42:
            return "Complex logic hit!"
    return "Standard calc"