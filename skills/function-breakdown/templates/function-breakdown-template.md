# Template: Function Breakdown (Phân rã chức năng)

## Mô tả
Tài liệu này phân rã hệ thống thành các chức năng con theo cấu trúc cây, từ tổng quan đến chi tiết. Giúp xác định phạm vi và cấu trúc hệ thống trước khi đi vào use case chi tiết.

---

## 1. Sơ đồ phân rã chức năng

```
[Hệ thống ABC]
├── [Phân hệ 1: Quản lý nghiệp vụ]
│   ├── [Chức năng 1.1: Quản lý A]
│   │   ├── [Chức năng 1.1.1: Tạo mới A]
│   │   ├── [Chức năng 1.1.2: Chỉnh sửa A]
│   │   ├── [Chức năng 1.1.3: Xóa A]
│   │   └── [Chức năng 1.1.4: Tìm kiếm A]
│   ├── [Chức năng 1.2: Quản lý B]
│   │   ├── [Chức năng 1.2.1: Tạo mới B]
│   │   └── [Chức năng 1.2.2: Phê duyệt B]
│   └── [Chức năng 1.3: Báo cáo]
│       ├── [Chức năng 1.3.1: Báo cáo tổng hợp]
│       └── [Chức năng 1.3.2: Xuất báo cáo]
├── [Phân hệ 2: Quản trị hệ thống]
│   ├── [Chức năng 2.1: Quản lý người dùng]
│   ├── [Chức năng 2.2: Quản lý vai trò]
│   └── [Chức năng 2.3: Cấu hình hệ thống]
└── [Phân hệ 3: Tích hợp]
    ├── [Chức năng 3.1: Kết nối API ngoài]
    └── [Chức năng 3.2: Đồng bộ dữ liệu]
```

---

## 2. Bảng mô tả chức năng

| Mã chức năng | Tên chức năng | Phân hệ | Mô tả ngắn | Độ ưu tiên | Độ phức tạp |
|-------------|---------------|---------|------------|------------|-------------|
| 1.1 | Quản lý A | Nghiệp vụ | Cho phép tạo, sửa, xóa, tìm kiếm A | Cao | Trung bình |
| 1.1.1 | Tạo mới A | Nghiệp vụ | Người dùng nhập thông tin và tạo bản ghi A mới | Cao | Thấp |
| 1.1.2 | Chỉnh sửa A | Nghiệp vụ | Cập nhật thông tin của bản ghi A đã tồn tại | Cao | Thấp |
| 1.1.3 | Xóa A | Nghiệp vụ | Xóa bản ghi A (soft delete/hard delete) | Trung bình | Thấp |
| 1.1.4 | Tìm kiếm A | Nghiệp vụ | Tìm kiếm A theo nhiều tiêu chí | Cao | Trung bình |
| 1.2 | Quản lý B | Nghiệp vụ | Quản lý quy trình B | Cao | Cao |
| 1.2.1 | Tạo mới B | Nghiệp vụ | Khởi tạo quy trình B | Cao | Trung bình |
| 1.2.2 | Phê duyệt B | Nghiệp vụ | Duyệt quy trình B | Cao | Cao |
| 1.3 | Báo cáo | Nghiệp vụ | Tạo và xuất báo cáo | Trung bình | Trung bình |
| 2.1 | Quản lý người dùng | Quản trị | CRUD người dùng hệ thống | Cao | Thấp |
| 2.2 | Quản lý vai trò | Quản trị | Định nghĩa và gán vai trò | Cao | Trung bình |
| 2.3 | Cấu hình hệ thống | Quản trị | Thiết lập tham số hệ thống | Thấp | Thấp |
| 3.1 | Kết nối API ngoài | Tích hợp | Gọi API từ hệ thống bên thứ 3 | Trung bình | Cao |
| 3.2 | Đồng bộ dữ liệu | Tích hợp | Đồng bộ dữ liệu với hệ thống ngoài | Trung bình | Cao |

---

## 3. Ma trận chức năng - Tác nhân

| Chức năng | Admin | User | Manager | System |
|-----------|-------|------|---------|--------|
| 1.1.1 Tạo mới A | ✓ | ✓ | ✓ | |
| 1.1.2 Chỉnh sửa A | ✓ | ✓ (của mình) | ✓ | |
| 1.1.3 Xóa A | ✓ | ✓ (của mình) | ✓ | |
| 1.1.4 Tìm kiếm A | ✓ | ✓ | ✓ | |
| 1.2.1 Tạo mới B | | ✓ | ✓ | |
| 1.2.2 Phê duyệt B | | | ✓ | |
| 1.3.1 Báo cáo tổng hợp | ✓ | | ✓ | |
| 1.3.2 Xuất báo cáo | ✓ | | ✓ | |
| 2.1 Quản lý người dùng | ✓ | | | |
| 2.2 Quản lý vai trò | ✓ | | | |
| 2.3 Cấu hình hệ thống | ✓ | | | |
| 3.1 Kết nối API ngoài | | | | ✓ |
| 3.2 Đồng bộ dữ liệu | | | | ✓ |

---

## 4. Phân loại chức năng

### 4.1. Chức năng nghiệp vụ (Business Functions)
- Quản lý A, B
- Báo cáo, thống kê
- Quy trình nghiệp vụ

### 4.2. Chức năng quản trị (Admin Functions)
- Quản lý người dùng, vai trò
- Cấu hình hệ thống
- Audit logs

### 4.3. Chức năng tích hợp (Integration Functions)
- API gateway
- Data sync
- Webhook handling

---

## 5. Ghi chú
- Độ ưu tiên: Cao / Trung bình / Thấp
- Độ phức tạp: Cao / Trung bình / Thấp
- Cập nhật khi có thay đổi về phạm vi

---

**Người tạo:** [Tên BA]
**Ngày tạo:** [DD/MM/YYYY]
**Phiên bản:** 1.0
