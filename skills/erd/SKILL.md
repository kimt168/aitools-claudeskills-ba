# Skill: Thiết kế ERD (Entity Relationship Diagram)

## Mô tả
Skill này hỗ trợ BA thiết kế mô hình dữ liệu (ERD) từ requirements, bao gồm các thực thể, thuộc tính và mối quan hệ giữa chúng.

## Tên kỹ thuật
- **Skill ID:** `erd`
- **Phiên bản:** 1.0.0
- **File chính:** `generate_erd.py`

---

## Kích hoạt
Skill được kích hoạt khi người dùng:
- Yêu cầu "tạo ERD" hoặc "thiết kế mô hình dữ liệu"
- Upload function-breakdown và yêu cầu thiết kế database
- Gọi từ orchestrator trong giai đoạn thiết kế tổng quan

## Đầu vào (Input)
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `function_breakdown_text` | string | Không | Function breakdown (để hiểu chức năng) |
| `requirements_text` | string | Có | Nội dung requirements |
| `ten_du_an` | string | Không | Tên dự án |
| `output_path` | string | Không | Đường dẫn file output |

## Xử lý
1. **Nhận diện thực thể từ requirements:**
   - Tìm các danh từ chỉ đối tượng (user, order, product, invoice...)
   - Loại bỏ thực thể không quan trọng
   - Group các thực thể liên quan

2. **Xác định thuộc tính cho mỗi thực thể:**
   - Thuộc tính định danh (PK)
   - Thuộc tính mô tả
   - Thuộc tính ngoại khóa (FK)
   - Thuộc tính thời gian (created_at, updated_at)

3. **Xác định mối quan hệ:**
   - 1-1 (một-một)
   - 1-N (một-nhiều)
   - N-N (nhiều-nhiều, cần bảng trung gian)

4. **Áp dụng chuẩn hóa:**
   - Kiểm tra 1NF, 2NF, 3NF
   - Tách thực thể nếu cần

5. **Xuất kết quả theo template ERD**

## Đầu ra (Output)
File markdown với cấu trúc:
1. Danh sách thực thể
2. Mô tả chi tiết thực thể (thuộc tính, kiểu dữ liệu, ràng buộc)
3. Sơ đồ ERD (dạng text)
4. Bảng mối quan hệ
5. Quy tắc nghiệp vụ liên quan đến dữ liệu

## Xử lý lỗi
| Lỗi | Hành động |
|-----|-----------|
| Không tìm thấy thực thể nào | Gợi ý user cung cấp thêm requirements |
| Quan hệ không rõ ràng | Đánh dấu cần review |
| Thiếu thuộc tính quan trọng | Cảnh báo |

## Công cụ sử dụng
- **LLM:** Claude API để nhận diện thực thể và quan hệ
- **Template:** Jinja2 template (`erd-template.md`)
- **Output:** Markdown

## Tích hợp trong pipeline
```
function-breakdown.md
    ↓
[erd] ← Skill này
erd-report.md (mô hình dữ liệu)
```

## Ví dụ
**User:** "Tạo ERD cho hệ thống quản lý bán hàng với các chức năng: quản lý sản phẩm, quản lý đơn hàng, quản lý khách hàng"

**Skill:** Nhận diện 5 thực thể (User, Customer, Product, Order, OrderItem), xác định quan hệ, xuất erd-report.md

---

**Người tạo:** kimt168
**Ngày cập nhật:** 18/05/2026
**Phiên bản:** 1.0.0
