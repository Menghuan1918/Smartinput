from langdetect import detect
import pytesseract
from PIL import Image
import subprocess
import io
import pyperclip

# 使用 xclip 从剪贴板获取图像并保存到 BytesIO
command = "xclip -selection clipboard -t image/png -o"
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
image_data = process.communicate()[0]

image_file = io.BytesIO(image_data)
img = Image.open(image_file)

# OCR识别
text = pytesseract.image_to_string(img)
print(text)
# 检测语言
detected_lang = detect(text)
print(f"Fi : {detected_lang}")
# 只接受英文或简体中文
if detected_lang not in ['en', 'zh-cn']:
    detected_lang = 'chi_sim'  # Tesseract 的简体中文识别代码
elif detected_lang == 'zh-cn':
    detected_lang = 'chi_sim'
elif detected_lang == 'en':
    detected_lang = 'eng'

print(f"Detected language: {detected_lang}")

# 再次进行语言特定的 OCR
text = pytesseract.image_to_string(img, lang=detected_lang)

# 删除最后一个字符
text = text[:-1]

# 如果语言是中文，删除所有空格
if detected_lang == 'chi_sim':
    text = text.replace(' ', '')

# 删除空行
lines = text.split('\n')
lines = [line for line in lines if line.strip() != '']
text = '\n'.join(lines)

# 将识别结果复制到剪贴板
pyperclip.copy(text)

print("The text has been copied to the clipboard.")