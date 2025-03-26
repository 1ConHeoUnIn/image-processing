import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đường dẫn đến hình ảnh
image_path = r'D:\Test_Lab\Open_cv\photos\sample3.jpg'  # Sử dụng r'' để tránh lỗi escape

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