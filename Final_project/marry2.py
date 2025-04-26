import cv2
import pytesseract
import pandas as pd


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# I.Đọc và tiền xử lý hình ảnh
# 1. đọc ảnh
image_path = r'D:\Test_Lab\Open_cv\photos\sample3.jpg'
image = cv2.imread(image_path)
if image is None:
    print("Error: Không thể đọc hình ảnh.")
    exit()

# 2.Chuyển đổi sang ảnh xám:
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# II.Cắt các vùng cố định và trích xuất văn bản
height, width = gray.shape
crop_coords = [
    (0, 0, int(width * 0.3), int(height * 0.25)),
        (int(width * 0.3), 0, int(width * 0.75), int(height * 0.3)),
        (int(width * 0.75), 0, width, int(height * 0.3)),
        #nam
        (int(width * 0.08), int(height * 0.33), int(width * 0.5), int(height * 0.41)),
        (int(width * 0.08), int(height * 0.41), int(width * 0.5), int(height * 0.52)),
        (int(width * 0.08), int(height * 0.52), int(width * 0.5), int(height * 0.57)),

        #nữ
        (int(width * 0.5), int(height * 0.33), int(width * 0.9), int(height * 0.41)),
        (int(width * 0.5), int(height * 0.41), int(width * 0.9), int(height * 0.52)),
        (int(width * 0.5), int(height * 0.52), int(width * 0.9), int(height * 0.57)),

        (int(width * 0.1), int(height * 0.58), int(width * 0.4), int(height * 0.73)),
        (int(width * 0.5), int(height * 0.58), int(width * 0.9), int(height * 0.73)),

         (int(width * 0.1), int(height * 0.73), int(width * 0.4), height),
        (int(width * 0.5), int(height * 0.73), int(width * 0.9), height)
      

        # nếu muốn cắt thêm thì chứ thêm tọa độ x1 y1 x2 y2
    
]

text_results = []  
#Lặp qua từng vùng và trích xuất văn bản:
for x1, y1, x2, y2 in crop_coords:
    cropped_image = gray[y1:y2, x1:x2]
    text = pytesseract.image_to_string(cropped_image, lang='vie').strip()
    if text:
        text_results.append(text)  
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  

# III. Tìm các vùng chữ bằng findContours
# 1 Làm mịn:
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 2 Dùng Adaptive Threshold để nhị phân hóa ảnh:
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# 3 Tìm các vùng chữ bằng find coutours:
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 30 and h > 10:
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, lang='vie').strip()
        if text:
            text_results.append(text)  
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) 

# IV. Lưu danh sách văn bản vào CSV:
df = pd.DataFrame(text_results, columns=["Extracted_Text"])
df.to_csv("giấy đăng ký kết hôn.csv", index=False, encoding="utf-8")


cv2.imshow('Processed Image with Rectangles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()