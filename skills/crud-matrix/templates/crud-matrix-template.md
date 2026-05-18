# Template: CRUD Matrix

## Mô tả
Ma trận CRUD (Create-Read-Update-Delete) mô tả quyền thao tác của từng chức năng/người dùng trên các thực thể dữ liệu. Giúp xác định rõ quyền và luồng dữ liệu trong hệ thống.

---

## 1. Ma trận CRUD - Chức năng và Thực thể

| Chức năng | User | Role | EntityA | EntityB | EntityC |
|-----------|------|------|---------|---------|---------|
| Quản lý người dùng | C R U D | - | - | - | - |
| Quản lý vai trò | - | C R U D | - | - | - |
| Tạo mới EntityA | - | - | C | - | - |
| Xem danh sách EntityA | - | - | R | - | - |
| Chỉnh sửa EntityA | - | - | U | - | - |
| Xóa EntityA | - | - | D | - | - |
| Tạo mới EntityB | - | - | R | C | - |
| Xem danh sách EntityB | - | - | R | R | - |
| Chỉnh sửa EntityB | - | - | - | U | - |
| Xóa EntityB | - | - | - | D | - |
| Báo cáo EntityC | - | - | R | R | R |

**Chú thích:**
- **C (Create):** Tạo mới bản ghi
- **R (Read):** Xem/đọc dữ liệu
- **U (Update):** Cập nhật dữ liệu
- **D (Delete):** Xóa bản ghi
- **-:** Không thao tác

---

## 2. Ma trận CRUD - Vai trò và Thực thể

| Vai trò | User | Role | EntityA | EntityB | EntityC |
|---------|------|------|---------|---------|---------|
| Admin | C R U D | C R U D | C R U D | C R U D | C R U D |
| Nhân viên | R (của mình) | R | C R U D (của mình) | C R U (của mình) | R |
| Trưởng phòng | R | R | C R U D | C R U D | R U |
| Giám đốc | R | R | R | R | R U D |

---

## 3. Ma trận CRUD chi tiết theo Use Case

### 3.1. UC: Quản lý EntityA

| Bước | Thao tác | Thực thể | C | R | U | D | Mô tả |
|------|----------|----------|---|---|---|---|-------|
| 1 | Tìm kiếm EntityA | EntityA | | ✓ | | | Đọc danh sách theo điều kiện |
| 2 | Xem chi tiết EntityA | EntityA | | ✓ | | | Đọc thông tin chi tiết |
| 3 | Tạo mới EntityA | EntityA | ✓ | | | | Thêm bản ghi mới |
| 4 | Chỉnh sửa EntityA | EntityA | | | ✓ | | Cập nhật thông tin |
| 5 | Xóa EntityA | EntityA | | | | ✓ | Xóa (soft/hard) |

### 3.2. UC: Quản lý EntityB

| Bước | Thao tác | Thực thể | C | R | U | D | Mô tả |
|------|----------|----------|---|---|---|---|-------|
| 1 | Chọn EntityA | EntityA | | ✓ | | | Đọc EntityA để chọn |
| 2 | Tạo mới EntityB | EntityB | ✓ | | | | Thêm bản ghi EntityB mới |
| 3 | Cập nhật EntityB | EntityB | | | ✓ | | Chỉnh sửa EntityB |
| 4 | Xóa EntityB | EntityB | | | | ✓ | Xóa EntityB |

---

## 4. Luồng dữ liệu theo CRUD

```
[Người dùng] → [Chức năng] → [Thực thể] → [Thao tác CRUD]

Ví dụ:
Nhân viên → Tạo EntityA → EntityA → Create
         → Xem EntityA  → EntityA → Read
         → Sửa EntityA  → EntityA → Update (của mình)

Trưởng phòng → Duyệt EntityB → EntityB → Update (trạng thái)
           → Xem báo cáo  → EntityC → Read
```

---

## 5. Quy tắc CRUD

| STT | Quy tắc | Giải thích |
|-----|---------|------------|
| 1 | Nhân viên chỉ CRUD được dữ liệu do mình tạo | Kiểm soát theo created_by |
| 2 | Trưởng phòng có thể CRUD tất cả dữ liệu trong phòng | Kiểm soát theo department_id |
| 3 | Admin có full CRUD trên mọi thực thể | Ngoại lệ |
| 4 | Xóa EntityA → các EntityB liên quan bị xóa theo (cascade) | Quan hệ 1-N |
| 5 | EntityA sau khi bị xóa không cho phép sửa (soft delete) | Giữ lịch sử |

---

## 6. Ghi chú
- CRUD matrix giúp xác định permission cần thiết cho từng chức năng
- Dùng để thiết kế API endpoints (POST, GET, PUT, DELETE)
- Cập nhật khi có thay đổi về chức năng hoặc thực thể

---

**Người tạo:** [Tên]
**Ngày tạo:** [DD/MM/YYYY]
**Phiên bản:** 1.0
