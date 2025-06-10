import os

def check_data_structure():
    # 修正路径的写法
    base_dir = os.path.join('C:\\', 'Microsoft VS Code', 'codes', 'huahui', 'data')
    print(f"当前工作目录: {os.getcwd()}")
    print(f"检查目录: {base_dir}")
    
    # ...existing code...
    
    # 检查主目录
    if not os.path.exists(base_dir):
        print(f"错误: 主数据目录不存在: {base_dir}")
        return False
        
    # 检查训练和验证目录
    for split in ['train', 'val']:
        split_dir = os.path.join(base_dir, split)
        print(f"\n检查 {split} 目录:")
        
        if not os.path.exists(split_dir):
            print(f"错误: {split} 目录不存在: {split_dir}")
            continue
            
        # 检查每个花卉类别
        for flower in ['rose', 'daisy', 'sunflower']:
            flower_dir = os.path.join(split_dir, flower)
            if os.path.exists(flower_dir):
                images = [f for f in os.listdir(flower_dir) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                print(f"- {flower}: {len(images)} 张图片")
                
                if len(images) == 0:
                    print(f"  警告: {flower} 目录为空")
            else:
                print(f"错误: {flower} 目录不存在: {flower_dir}")

if __name__ == '__main__':
    try:
        check_data_structure()
    except Exception as e:
        print(f"检查过程出错: {str(e)}")