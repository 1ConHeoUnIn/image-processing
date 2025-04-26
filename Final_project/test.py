import cv2
import pytesseract
import pandas as pd

# Thiết lập đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đọc ảnh
image_path = r'D:\Test_Lab\Open_cv\photos\sample1.jpg'
image = cv2.imread(image_path)
if image is None:
    print("Error: Không thể đọc hình ảnh.")
    exit()

# Chuyển đổi sang ảnh xám và cải thiện chất lượng
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Tìm các vùng văn bản bằng contour detection
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
data = []

# Hàm vẽ hình chữ nhật quanh vùng chữ
def draw_rectangle(image, x1, y1, x2, y2):
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Xử lý từng vùng chữ tìm thấy
for i, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 30 and h > 10:  # Loại bỏ vùng quá nhỏ
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, lang='vie').strip()
        data.append([i+1, x, y, w, h, text])
        draw_rectangle(image, x, y, x+w, y+h)

# Xuất kết quả ra file CSV
df = pd.DataFrame(data, columns=["ID", "X", "Y", "Width", "Height", "Text"])
df.to_csv("output.csv", index=False, encoding="utf-8")

# Hiển thị hình ảnh với các vùng chữ được đánh dấu
cv2.imshow('Detected Text Areas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()