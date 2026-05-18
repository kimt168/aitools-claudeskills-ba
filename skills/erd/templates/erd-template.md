# Template: ERD (Entity Relationship Diagram)

## Mô tả
Tài liệu mô tả mô hình dữ liệu của hệ thống, bao gồm các thực thể, thuộc tính và mối quan hệ giữa chúng.

---

## 1. Danh sách thực thể

| STT | Tên thực thể | Tên tiếng Anh | Mô tả | Số bản ghi dự kiến |
|-----|--------------|---------------|-------|-------------------|
| 1 | Người dùng | User | Thông tin người dùng hệ thống | ~50 |
| 2 | Vai trò | Role | Các vai trò trong hệ thống | ~5 |
| 3 | [Thực thể A] | [EntityA] | [Mô tả] | ~1000 |
| 4 | [Thực thể B] | [EntityB] | [Mô tả] | ~500 |
| 5 | [Thực thể C] | [EntityC] | [Mô tả] | ~5000 |

---

## 2. Mô tả chi tiết thực thể

### 2.1. User (Người dùng)

| Thuộc tính | Kiểu dữ liệu | Độ dài | Ràng buộc | Mô tả |
|------------|--------------|--------|-----------|-------|
| user_id | INT | - | PK, Auto Increment | Mã người dùng |
| username | VARCHAR | 50 | Unique, Not Null | Tên đăng nhập |
| password_hash | VARCHAR | 255 | Not Null | Mật khẩu mã hóa |
| full_name | NVARCHAR | 100 | Not Null | Họ và tên đầy đủ |
| email | VARCHAR | 100 | Unique, Not Null | Email |
| phone | VARCHAR | 20 | - | Số điện thoại |
| role_id | INT | - | FK | Mã vai trò |
| is_active | BOOLEAN | - | Default: true | Trạng thái hoạt động |
| created_at | DATETIME | - | Default: now() | Ngày tạo |
| updated_at | DATETIME | - | - | Ngày cập nhật |

### 2.2. Role (Vai trò)

| Thuộc tính | Kiểu dữ liệu | Độ dài | Ràng buộc | Mô tả |
|------------|--------------|--------|-----------|-------|
| role_id | INT | - | PK, Auto Increment | Mã vai trò |
| role_name | NVARCHAR | 50 | Unique, Not Null | Tên vai trò |
| description | NVARCHAR | 255 | - | Mô tả |
| permissions | TEXT | - | - | Danh sách quyền (JSON) |

### 2.3. [EntityA]

| Thuộc tính | Kiểu dữ liệu | Độ dài | Ràng buộc | Mô tả |
|------------|--------------|--------|-----------|-------|
| id | INT | - | PK, Auto Increment | Mã [thực thể] |
| code | VARCHAR | 20 | Unique, Not Null | Mã định danh |
| name | NVARCHAR | 200 | Not Null | Tên [thực thể] |
| description | NVARCHAR | 500 | - | Mô tả |
| status | VARCHAR | 20 | Default: 'active' | Trạng thái |
| created_by | INT | - | FK → User.user_id | Người tạo |
| created_at | DATETIME | - | Default: now() | Ngày tạo |
| updated_at | DATETIME | - | - | Ngày cập nhật |

### 2.4. [EntityB]

| Thuộc tính | Kiểu dữ liệu | Độ dài | Ràng buộc | Mô tả |
|------------|--------------|--------|-----------|-------|
| id | INT | - | PK, Auto Increment | Mã [thực thể] |
| entity_a_id | INT | - | FK → EntityA.id | Liên kết đến [A] |
| name | NVARCHAR | 200 | Not Null | Tên |
| quantity | DECIMAL | 10,2 | Default: 0 | Số lượng |
| unit_price | DECIMAL | 15,2 | Not Null | Đơn giá |
| total_amount | DECIMAL | 15,2 | - | Thành tiền |
| notes | NVARCHAR | 500 | - | Ghi chú |
| created_at | DATETIME | - | Default: now() | Ngày tạo |

---

## 3. Mối quan hệ giữa các thực thể

### 3.1. Sơ đồ ERD (dạng text)

```
┌─────────────┐         ┌─────────────┐
│    User     │         │    Role     │
├─────────────┤         ├─────────────┤
│ PK user_id  │◄───────┐│ PK role_id  │
│   username  │        ││   role_name │
│   email     │        ││   permissions│
│ FK role_id  │────────┘└─────────────┘
│   ...       │
└─────────────┘

┌─────────────┐         ┌─────────────┐
│    User     │         │  EntityA    │
├─────────────┤         ├─────────────┤
│ PK user_id  │◄───────┐│ PK id       │
│   ...       │        ││   code      │
└─────────────┘        ││   name      │
                       ││ FK created_by│────────┐
                       ││   ...       │        │
                       └─────────────┘        │
                                              │
                       ┌─────────────┐        │
                       │  EntityB    │        │
                       ├─────────────┤        │
                       │ PK id       │        │
                       │ FK entity_a_id│─────┘ (1-N)
                       │   ...       │
                       └─────────────┘
```

### 3.2. Bảng mối quan hệ

| Quan hệ | Thực thể nguồn | Cardinality | Thực thể đích | Mô tả |
|---------|----------------|-------------|---------------|-------|
| R1 | User | N:1 | Role | Một role có nhiều user, một user có một role |
| R2 | User | 1:N | EntityA | Một user tạo nhiều EntityA |
| R3 | EntityA | 1:N | EntityB | Một EntityA có nhiều EntityB |
| R4 | EntityA | N:N | EntityC | Nhiều-nhiều (cần bảng trung gian) |

### 3.3. Bảng trung gian (nếu có)

**EntityA_EntityC** (cho quan hệ N:N)

| Thuộc tính | Kiểu dữ liệu | Ràng buộc | Mô tả |
|------------|--------------|-----------|-------|
| entity_a_id | INT | PK, FK → EntityA.id | |
| entity_c_id | INT | PK, FK → EntityC.id | |
| created_at | DATETIME | Default: now() | |

---

## 4. Quy tắc nghiệp vụ liên quan đến dữ liệu

| STT | Quy tắc | Thực thể liên quan |
|-----|---------|-------------------|
| 1 | Một user chỉ có thể có một role | User, Role |
| 2 | EntityA.code phải là duy nhất | EntityA |
| 3 | Khi xóa user, các EntityA do user tạo vẫn được giữ lại | User, EntityA |
| 4 | EntityB.total_amount = EntityB.quantity × EntityB.unit_price | EntityB |
| 5 | EntityA.status chỉ có thể là 'active', 'inactive', 'deleted' | EntityA |

---

## 5. Ghi chú
- ERD có thể thay đổi khi phân tích chi tiết use case
- Cập nhật phiên bản khi có thay đổi

---

**Người thiết kế:** [Tên]
**Ngày tạo:** [DD/MM/YYYY]
**Phiên bản:** 1.0
