import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt


def train_model():
    # 使用正确的绝对路径
    base_dir = os.path.join('C:\\', 'Microsoft VS Code', 'codes', 'huahui', 'data')
    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'val')
    
    # 检查并打印目录
    print(f"检查数据目录...")
    print(f"训练数据目录: {os.path.abspath(train_dir)}")
    print(f"验证数据目录: {os.path.abspath(val_dir)}")
    
    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"训练数据目录不存在: {train_dir}")
    if not os.path.exists(val_dir):
        raise FileNotFoundError(f"验证数据目录不存在: {val_dir}")
    
    # ...existing code...
    
    # 数据生成器
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True
    )
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # 创建数据生成器
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical',
        classes=['daisy', 'rose', 'sunflower']  # 显式指定类别顺序
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(100, 100),
        batch_size=32,
        class_mode='categorical',
        classes=['daisy', 'rose', 'sunflower']  # 保持与训练数据相同的顺序
    )
    
    print("类别映射:", train_generator.class_indices)
    
    # 构建模型
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(100, 100, 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(train_generator.class_indices), activation='softmax')
    ])
    
    # 编译模型
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # 回调函数
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        ),
        ModelCheckpoint(
            'best_model.keras',
            monitor='val_accuracy',
            save_best_only=True
        )
    ]
    
    # 训练模型
    print("\n开始训练模型...")
    history = model.fit(
        train_generator,
        epochs=10,
        validation_data=val_generator,
        callbacks=callbacks
    )
    
    # 保存模型
    save_path = os.path.join('C:\\', 'Microsoft VS Code', 'codes', 'huahui', 'flower_model.keras')
    
    # 确保保存目录存在
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    # 保存模型
    try:
        model.save(save_path)
        print(f"\n模型已保存到: {save_path}")
    except Exception as e:
        print(f"保存模型时出错: {str(e)}")
        raise
    
    return history
   

if __name__ == '__main__':
    try:
        history = train_model()
        plot_training_history(history)
        print("训练完成！")
    except Exception as e:
        print(f"训练过程中出错: {str(e)}")

import matplotlib.pyplot as plt

def plot_training_history(history):
    plt.figure(figsize=(12, 4))
    
    # 绘制准确率
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='训练准确率')
    plt.plot(history.history['val_accuracy'], label='验证准确率')
    plt.title('模型准确率')
    plt.xlabel('轮次')
    plt.ylabel('准确率')
    plt.legend()
    
    # 绘制损失
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='训练损失')
    plt.plot(history.history['val_loss'], label='验证损失')
    plt.title('模型损失')
    plt.xlabel('轮次')
    plt.ylabel('损失')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    try:
        history = train_model()
        plot_training_history(history)
        print("训练完成！")
    except Exception as e:
        print(f"训练过程中出错: {str(e)}")