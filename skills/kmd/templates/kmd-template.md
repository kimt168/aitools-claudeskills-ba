# Template: Khảo sát Hiện trạng (KMD - Khao Sat Hien Trang)

## Mô tả
Tài liệu khảo sát hiện trạng hệ thống, quy trình nghiệp vụ hiện tại trước khi xây dựng hệ thống mới. Giúp hiểu rõ bối cảnh, vấn đề hiện tại và yêu cầu cải tiến.

---

## 1. Thông tin chung về dự án

| Thông tin | Nội dung |
|-----------|----------|
| Tên dự án | [Tên dự án] |
| Khách hàng | [Tên đơn vị/Phòng ban] |
| Người phụ trách | [Tên người liên hệ] |
| Ngày khảo sát | [DD/MM/YYYY] |
| Phương pháp khảo sát | Phỏng vấn, Quan sát, Thu thập tài liệu |

---

## 2. Hiện trạng quy trình nghiệp vụ

### 2.1. Quy trình hiện tại
*(Mô tả quy trình đang được thực hiện)*

```
[Bước 1] → [Bước 2] → [Bước 3] → [Bước 4] → [Kết thúc]
```

**Mô tả chi tiết:**
- **Bước 1:** [Ai làm gì, dùng công cụ gì]
- **Bước 2:** [Ai làm gì, dùng công cụ gì]
- **Bước 3:** [Ai làm gì, dùng công cụ gì]
- **Bước 4:** [Ai làm gì, dùng công cụ gì]

### 2.2. Vấn đề tồn tại
| STT | Vấn đề | Mức độ ảnh hưởng | Nguyên nhân |
|-----|--------|------------------|-------------|
| 1 | Thao tác thủ công, tốn thời gian | Cao | Không có hệ thống tự động |
| 2 | Dữ liệu phân tán, khó tra cứu | Cao | Lưu trữ rời rạc trên Excel/Email |
| 3 | Thiếu kiểm soát, dễ sai sót | Trung bình | Không có workflow phê duyệt |
| 4 | Báo cáo chậm, không real-time | Trung bình | Tổng hợp thủ công |
| 5 | Khó theo dõi tiến độ | Thấp | Không có dashboard |

### 2.3. Yêu cầu cải tiến
| STT | Yêu cầu | Vấn đề giải quyết | Độ ưu tiên |
|-----|---------|-------------------|------------|
| 1 | Tự động hóa quy trình | Vấn đề 1 | Cao |
| 2 | Tập trung dữ liệu | Vấn đề 2 | Cao |
| 3 | Xây dựng workflow phê duyệt | Vấn đề 3 | Cao |
| 4 | Báo cáo tự động, real-time | Vấn đề 4 | Trung bình |
| 5 | Dashboard theo dõi | Vấn đề 5 | Trung bình |

---

## 3. Hiện trạng hệ thống CNTT

### 3.1. Hệ thống đang sử dụng
| STT | Tên hệ thống | Mục đích sử dụng | Hạn chế |
|-----|--------------|------------------|---------|
| 1 | Excel/Google Sheets | Lưu trữ và tính toán | Không có validation, khó chia sẻ |
| 2 | Email | Trao đổi và phê duyệt | Không theo dõi được tiến độ |
| 3 | [Hệ thống cũ] | [Mục đích] | [Hạn chế] |

### 3.2. Hạ tầng hiện có
- **Máy chủ:** [Mô tả]
- **Mạng:** [Mô tả]
- **Bảo mật:** [Mô tả]
- **Thiết bị đầu cuối:** [Mô tả]

---

## 4. Người dùng và vai trò

### 4.1. Danh sách người dùng dự kiến
| Vai trò | Số lượng | Mô tả công việc | Yêu cầu đặc biệt |
|---------|----------|-----------------|------------------|
| Admin | 2 | Quản trị hệ thống, người dùng, cấu hình | Có kiến thức CNTT |
| Nhân viên | 20 | Nhập liệu, tra cứu, báo cáo cá nhân | Dễ sử dụng |
| Trưởng phòng | 5 | Phê duyệt, xem báo cáo tổng hợp | Dashboard trực quan |
| Ban giám đốc | 3 | Xem báo cáo chiến lược | Báo cáo tổng quan, xuất file |

### 4.2. Phân quyền dự kiến
| Chức năng | Admin | Nhân viên | Trưởng phòng | GĐ |
|-----------|-------|-----------|--------------|-----|
| Nhập liệu | ✓ | ✓ | | |
| Phê duyệt | | | ✓ | |
| Xem báo cáo | ✓ | ✓ (cá nhân) | ✓ (phòng) | ✓ (toàn cty) |
| Quản trị | ✓ | | | |

---

## 5. Ràng buộc và giả định

### 5.1. Ràng buộc
- **Thời gian:** Dự án phải hoàn thành trước [ngày]
- **Ngân sách:** Tối đa [số tiền]
- **Công nghệ:** Phải tương thích với [hệ thống hiện có]
- **Pháp lý:** Tuân thủ [quy định, tiêu chuẩn]

### 5.2. Giả định
- Người dùng có kỹ năng tin học cơ bản
- Hạ tầng mạng ổn định
- Dữ liệu hiện có có thể di chuyển sang hệ thống mới

---

## 6. Tài liệu tham khảo
- [Tài liệu quy trình hiện tại]
- [Biểu mẫu đang sử dụng]
- [Quy định liên quan]

---

**Người khảo sát:** [Tên]
**Người phê duyệt:** [Tên]
**Ngày phê duyệt:** [DD/MM/YYYY]
