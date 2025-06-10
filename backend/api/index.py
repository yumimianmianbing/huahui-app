from flask import Flask, request, jsonify, render_template
import os
import sys

# 添加父目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# 现在可以导入 models 模块
from models.predictor import FlowerPredictor

app = Flask(__name__, template_folder='../templates')
predictor = None

# 添加错误处理和日志
try:
    predictor = FlowerPredictor()
    print("模型加载成功！")
except Exception as e:
    print(f"模型加载失败: {str(e)}")

# ...existing code...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    print("\n=== 开始处理预测请求 ===")
    print(f"请求内容类型: {request.content_type}")
    
    if 'image' not in request.files:
        print("错误: 未找到上传的图片")
        return jsonify({'error': '未上传图片'}), 400
    
    try:
        file = request.files['image']
        if not file.filename:
            print("错误: 文件名为空")
            return jsonify({'error': '无效的文件'}), 400
            
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"错误: 不支持的文件类型 - {file.filename}")
            return jsonify({'error': '不支持的文件类型，请上传 JPG 或 PNG 图片'}), 400
        
        print(f"处理图片: {file.filename}")
        result = predictor.predict(file)
        print(f"预测结果: {result}")
        return jsonify(result)
        
    except Exception as e:
        import traceback
        print(f"预测错误: {str(e)}")
        print("详细错误信息:")
        print(traceback.format_exc())
        return jsonify({
            'error': f'预测失败: {str(e)}',
            'details': traceback.format_exc()
        }), 500

    finally:
        print("=== 请求处理完成 ===\n")

# 本地测试用
if __name__ == '__main__':
    print(f"当前工作目录: {os.getcwd()}")
    print(f"启动 Flask 应用...")
    app.run(debug=True, host='0.0.0.0', port=5000)