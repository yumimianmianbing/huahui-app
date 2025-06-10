import requests
import os

def test_prediction():
    # API 端点
    url = 'http://127.0.0.1:5000/api/predict'
    
    # 测试目录
    test_dir = os.path.join('C:\\', 'Microsoft VS Code', 'codes', 'huahui', 'data', 'test')
    
    # 遍历测试图片
    for class_name in ['rose', 'daisy', 'sunflower']:
        class_dir = os.path.join(test_dir, class_name)
        if os.path.exists(class_dir):
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(class_dir, img_name)
                    print(f"\n测试图片: {img_path}")
                    
                    # 发送请求
                    with open(img_path, 'rb') as f:
                        files = {'image': f}
                        response = requests.post(url, files=files)
                    
                    # 打印结果
                    if response.status_code == 200:
                        result = response.json()
                        print(f"预测类别: {result['class_name']}")
                        print(f"置信度: {result['confidence']:.2f}")
                    else:
                        print(f"请求失败: {response.status_code}")
                        print(response.text)

if __name__ == '__main__':
    test_prediction()