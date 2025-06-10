import tensorflow as tf
import numpy as np
from PIL import Image
import io

class FlowerPredictor:
    def __init__(self):
        # 加载模型
        model_path = 'C:\\Microsoft VS Code\\codes\\huahui\\flower_model.keras'
        self.model = tf.keras.models.load_model(model_path)
        self.classes = ['daisy', 'rose', 'sunflower']
        self.class_names = {
            'daisy': '雏菊',
            'rose': '玫瑰',
            'sunflower': '向日葵'
        }
        print(f"模型加载成功！支持的类别：{self.classes}")

    def predict(self, file):
        # 读取和预处理图片
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((100, 100))  # 调整大小为模型输入尺寸
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)
        img_array = img_array / 255.0  # 归一化

        # 进行预测
        pred = self.model.predict(img_array)
        predicted_class_idx = np.argmax(pred[0])  # 获取预测类别索引
        confidence = float(pred[0][predicted_class_idx])  # 获取置信度

        # 获取预测的类别名
        predicted_class = self.classes[predicted_class_idx]
        
        print(f"预测类别索引: {predicted_class_idx}")
        print(f"预测类别: {predicted_class}")
        print(f"置信度: {confidence:.2f}")

        return {
            'class_name': predicted_class,
            'chinese_name': self.class_names[predicted_class],
            'confidence': confidence,
            'probabilities': {cls: float(prob) for cls, prob in zip(self.classes, pred[0])}
        }