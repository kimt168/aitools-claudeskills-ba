# Skill: Ma trận CRUD (CRUD Matrix)

## Mô tả
Skill này hỗ trợ BA tạo ma trận CRUD (Create-Read-Update-Delete), mô tả quyền thao tác của từng chức năng/người dùng trên các thực thể dữ liệu.

## Tên kỹ thuật
- **Skill ID:** `crud-matrix`
- **Phiên bản:** 1.0.0
- **File chính:** `generate_crud_matrix.py`

---

## Kích hoạt
Skill được kích hoạt khi người dùng:
- Yêu cầu "tạo CRUD matrix" hoặc "ma trận CRUD"
- Upload ERD và function-breakdown, yêu cầu tạo CRUD
- Gọi từ orchestrator trong giai đoạn thiết kế chi tiết

## Đầu vào (Input)
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `erd_text` | string | Có | Nội dung ERD (danh sách thực thể) |
| `function_breakdown_text` | string | Có | Function breakdown (danh sách chức năng) |
| `roles` | list[str] | Không | Danh sách vai trò (mặc định: Admin, User, Manager) |
| `output_path` | string | Không | Đường dẫn file output |

## Xử lý
1. **Đọc thực thể từ ERD:**
   - Lấy danh sách thực thể
   - Hiểu ý nghĩa mỗi thực thể

2. **Đọc chức năng từ Function Breakdown:**
   - Lấy danh sách chức năng
   - Hiểu mỗi chức năng làm gì

3. **Xác định CRUD cho mỗi cặp (chức năng, thực thể):**
   - Chức năng này có tạo mới thực thể không? → C
   - Có xem/đọc không? → R
   - Có sửa không? → U
   - Có xóa không? → D

4. **Xác định CRUD theo vai trò:**
   - Role nào được làm gì trên thực thể nào

5. **Tạo luồng dữ liệu theo CRUD**

6. **Xuất kết quả theo template CRUD**

## Đầu ra (Output)
File markdown với cấu trúc:
1. Ma trận CRUD - Chức năng và Thực thể
2. Ma trận CRUD - Vai trò và Thực thể
3. Ma trận CRUD chi tiết theo Use Case
4. Luồng dữ liệu theo CRUD
5. Quy tắc CRUD

## Xử lý lỗi
| Lỗi | Hành động |
|-----|-----------|
| Thiếu ERD hoặc Function Breakdown | Yêu cầu cung cấp đủ input |
| Thực thể không rõ nghĩa | Đánh dấu cần review |
| Xung đột CRUD (cùng chức năng vừa C vừa D) | Cảnh báo |

## Công cụ sử dụng
- **LLM:** Claude API để phân tích và điền CRUD
- **Template:** Jinja2 template (`crud-matrix-template.md`)
- **Output:** Markdown

## Tích hợp trong pipeline
```
function-breakdown.md + erd-report.md
    ↓
[crud-matrix] ← Skill này
crud-matrix.md (ma trận quyền)
```

## Ví dụ
**User:** "Tạo CRUD matrix cho hệ thống quản lý thư viện"

**Skill:** Nhận diện chức năng (quản lý sách, quản lý độc giả, mượn/trả) và thực thể (Book, Member, BorrowRecord), điền ma trận CRUD, xuất crud-matrix.md

---

**Người tạo:** kimt168
**Ngày cập nhật:** 18/05/2026
**Phiên bản:** 1.0.0
