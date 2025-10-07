# Hướng dẫn Xây dựng Ứng dụng Code2Video

Chào bạn,

Tài liệu này sẽ hướng dẫn bạn cách tự xây dựng ứng dụng `Code2Video` từ mã nguồn. Quá trình này đã được tự động hóa hoàn toàn, bạn chỉ cần làm theo các bước đơn giản dưới đây.

## Yêu cầu Bắt buộc

Trước khi bắt đầu, máy tính của bạn **BẮT BUỘC** phải có 2 chương trình sau:

### 1. Python
- **Cách kiểm tra:** Mở Command Prompt (gõ `cmd` vào menu Start) và chạy lệnh:
  ```
  python --version
  ```
- Nếu lệnh này hiển thị một phiên bản (ví dụ: `Python 3.10.8`), bạn đã sẵn sàng.
- Nếu không, vui lòng tải và cài đặt Python từ trang chủ [python.org](https://www.python.org/downloads/). **Quan trọng:** Trong quá trình cài đặt, hãy nhớ đánh dấu vào ô "Add Python to PATH".

### 2. LaTeX (Rất quan trọng!)
Manim cần LaTeX để hiển thị văn bản và công thức toán học. Nếu không có LaTeX, ứng dụng sẽ báo lỗi khi bạn cố gắng tạo video có chứa chữ.

- **Lựa chọn cho Windows:** Chúng tôi đề nghị bạn cài đặt **MiKTeX**.
- **Cách cài đặt:**
    1. Truy cập trang tải về của MiKTeX: [https://miktex.org/download](https://miktex.org/download)
    2. Tải xuống trình cài đặt (Installer) và chạy nó.
    3. **QUAN TRỌNG:** Trong quá trình cài đặt, khi được hỏi "Install missing packages on-the-fly", hãy chọn **"Yes"** hoặc **"Always"**. Điều này cho phép MiKTeX tự động tải các phông chữ và gói cần thiết khi Manim cần đến chúng.

---

## Các bước Xây dựng

Sau khi đã cài đặt đủ Python và LaTeX, bạn chỉ cần làm theo các bước sau:

1.  **Giải nén:** Giải nén toàn bộ dự án này vào một thư mục bất kỳ trên máy tính của bạn.

2.  **Chạy kịch bản xây dựng:**
    - Mở thư mục bạn vừa giải nén.
    - Tìm tệp `build.bat` và **nhấp đúp chuột** vào nó để chạy.

3.  **Chờ đợi:**
    - Một cửa sổ dòng lệnh màu đen sẽ xuất hiện và bắt đầu quá trình xây dựng tự động.
    - Lần đầu tiên chạy, quá trình này có thể mất vài phút.
    - Vui lòng **không tắt cửa sổ** này cho đến khi bạn thấy thông báo **"THANH CONG!"**.

## Kết quả

Sau khi quá trình hoàn tất, bạn sẽ tìm thấy một thư mục mới tên là `Code2Video` bên trong thư mục `dist`.

- **Đường dẫn:** `dist\Code2Video`

Để chạy ứng dụng:
1.  Mở thư mục `dist\Code2Video`.
2.  Tìm và **nhấp đúp chuột vào tệp `Code2Video.exe`**.

Một giao diện web sẽ tự động mở ra trong trình duyệt của bạn.

---
Chúc bạn thành công!