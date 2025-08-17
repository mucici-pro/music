import os
import hashlib
from datetime import datetime

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return None

def generate_copyright_file(music_file):
    filename = os.path.basename(music_file)
    name_only = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1].lower()

    file_hash = calculate_sha256(music_file)
    if not file_hash:
        return False
    
    output_file = os.path.join(os.path.dirname(music_file), f"{name_only}.txt")
    
    file_type = "WAV" if extension == ".wav" else "MP3" if extension == ".mp3" else extension[1:].upper()
    
    creation_date = datetime.now().strftime("%Y-%m-%d")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"作品标题：{name_only}\n")
        f.write("作者：慕词词\n")
        f.write(f"创作完成日期：{creation_date}\n")
        f.write("哈希算法：SHA-256\n")
        f.write(f"{file_type}哈希值：{file_hash}\n")
        f.write("版权声明：此文件用于证明本音乐版权归属。\n\n")
        f.write("注：如果标题有附加内容，则是为了方便记忆，实际发行的标题未必相同。\n")
    
    print(f"已生成版权声明: {output_file}")
    return True

def process_music_directory(directory):
    valid_extensions = ['.wav', '.mp3', '.flac', '.aiff', '.ogg', '.m4a']

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in valid_extensions:
            print(f"处理音乐文件: {filename}")
            generate_copyright_file(file_path)

if __name__ == "__main__":
    # 设置音乐目录路径
    music_dir = "music"

    # 确保目录存在
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        print(f"已创建音乐目录: {music_dir}")
        print("请将音乐文件放入此目录后重新运行程序")
    else:
        print(f"开始处理目录: {music_dir}")
        process_music_directory(music_dir)
        print("\n处理完成！请检查生成的版权声明文件，并更新作者名称和创作日期")