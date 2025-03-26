import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đường dẫn đến hình ảnh
image_path = r'D:\Test_Lab\Open_cv\photos\sample1.jpg'  # Sử dụng r'' để tránh lỗi escape

# Đọc hình ảnh từ file
image = cv2.imread(image_path)
if image is None:
    print("Error: Không thể đọc hình ảnh. Vui lòng kiểm tra đường dẫn.")
else:
    # Chuyển đổi sang ảnh xám
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    # Kiểm tra kích thước
    height, width = image.shape
    print("width : ", width)
    print("height : ", height)

    # Hàm để vẽ hình chữ nhật
    def draw_rectangle(image, x1, y1, x2, y2):
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2) 

    # Hàm để cắt và trích xuất văn bản từ ảnh
    def extract_text_from_image(image, x1, y1, x2, y2):
        if x1 >= 0 and x2 <= width and y1 >= 0 and y2 <= height:
            # Cắt một phần của ảnh
            cropped_image = image[y1:y2, x1:x2]
            # Trích xuất văn bản từ ảnh đã cắt
            text = pytesseract.image_to_string(cropped_image, lang='vie')
            return text, cropped_image
        else:
            return "Tọa độ không hợp lệ.", None

    # Danh sách các tọa độ cắt
    crop_coords = [
        (0, 0, int(width * 0.3), int(height * 0.25)),
        (int(width * 0.25), 0, int(width * 0.75), int(height * 0.25)),
        (int(width * 0.73), 0, width, int(height * 0.18)),
        (int(width * 0.07), int(height * 0.25), width, int(height * 0.29)),
        (int(width * 0.07), int(height * 0.25), width, int(height * 0.35)),
        (int(width * 0.07), int(height * 0.35), width, int(height * 0.38)),
        (int(width * 0.07), int(height * 0.38), int(width * 0.5), int(height * 0.42)),
        (int(width * 0.5), int(height * 0.38), width, int(height * 0.43)),
        (int(width * 0.07), int(height * 0.43), width, int(height * 0.46)),
        (int(width * 0.07), int(height * 0.46), width, int(height * 0.5)),
        (int(width * 0.07), int(height * 0.5), width, int(height * 0.53)),
        (int(width * 0.07), int(height * 0.53), width, int(height * 0.56)),
        (int(width * 0.07), int(height * 0.56), width, int(height * 0.6)),
        (int(width * 0.07), int(height * 0.6), width, int(height * 0.63)),
        (int(width * 0.07), int(height * 0.63), width, int(height * 0.69)),
        (int(width * 0.02), int(height * 0.7), int(width * 0.3), int(height * 0.77)),
        (int(width * 0.31), int(height * 0.7), int(width * 0.57), int(height * 0.77)),
        (int(width * 0.57), int(height * 0.7), width, int(height * 0.77))
        # nếu muốn cắt thêm thì chứ thêm tọa độ x1 y1 x2 y2
    ]

    # Lặp qua danh sách tọa độ cắt
    for i, (x1, y1, x2, y2) in enumerate(crop_coords):
        draw_rectangle(image, x1, y1, x2, y2)  # Vẽ hình chữ nhật
        text, cropped_image = extract_text_from_image(image, x1, y1, x2, y2)
        #cv2.imshow(f'Cropped {i+1}', cropped_image)
        print(text)

    # Hiển thị hình ảnh gốc
    cv2.imshow('Image', image)

    # Chờ người dùng nhấn phím và đóng cửa sổ
    cv2.waitKey(0)
    cv2.destroyAllWindows()