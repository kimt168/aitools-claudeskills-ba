# Skill: Phân rã chức năng (Function Breakdown)

## Mô tả
Skill này hỗ trợ BA phân rã hệ thống thành các chức năng con theo cấu trúc cây, từ tổng quan đến chi tiết. Giúp xác định phạm vi và cấu trúc hệ thống trước khi đi vào use case chi tiết.

## Tên kỹ thuật
- **Skill ID:** `function-breakdown`
- **Phiên bản:** 1.0.0
- **File chính:** `generate_function_breakdown.py`

---

## Kích hoạt
Skill được kích hoạt khi người dùng:
- Yêu cầu "phân rã chức năng" hoặc "function breakdown"
- Upload file requirements và yêu cầu tạo function breakdown
- Gọi từ orchestrator trong giai đoạn phân tích tổng quan

## Đầu vào (Input)
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `requirements_text` | string | Có | Nội dung requirements (từ file .md hoặc chat) |
| `ten_du_an` | string | Không | Tên dự án (mặc định: lấy từ content) |
| `output_path` | string | Không | Đường dẫn file output (mặc định: function-breakdown.md) |

## Xử lý
1. **Phân tích requirements:**
   - Đọc nội dung requirements
   - Xác định các phân hệ chính (dựa trên domain keywords)
   - Xác định các chức năng trong mỗi phân hệ

2. **Phân rã theo cấp độ:**
   - Level 1: Phân hệ (Subsystem)
   - Level 2: Chức năng chính (Main Function)
   - Level 3: Chức năng con (Sub-function)

3. **Gán thuộc tính cho mỗi chức năng:**
   - Độ ưu tiên (Cao/Trung bình/Thấp)
   - Độ phức tạp (Cao/Trung bình/Thấp)
   - Tác nhân liên quan

4. **Tạo ma trận chức năng - tác nhân:**
   - Xác định ai (role nào) được làm gì

5. **Xuất kết quả theo template:**
   - Dùng template `function-breakdown-template.md`
   - Điền thông tin vào các section

## Đầu ra (Output)
File markdown với cấu trúc:
1. Sơ đồ phân rã chức năng (dạng cây)
2. Bảng mô tả chức năng
3. Ma trận chức năng - tác nhân
4. Phân loại chức năng (nghiệp vụ, quản trị, tích hợp)

## Xử lý lỗi
| Lỗi | Hành động |
|-----|-----------|
| Không tìm thấy chức năng nào | Gợi ý user cung cấp thêm thông tin |
| Requirements quá ngắn | Cảnh báo và yêu cầu bổ sung |
| Lỗi template | Fallback sang format đơn giản |

## Công cụ sử dụng
- **LLM:** Claude API để phân tích ngữ nghĩa và grouping
- **Template:** Jinja2 template
- **Output:** Markdown

## Tích hợp trong pipeline
```
requirements.docx
    ↓ [read-docx]
requirements.md
    ↓ [function-breakdown] ← Skill này
function-breakdown.md (tổng quan hệ thống)
    ↓ [requirement-parser]
YeuCauCoCauTruc (chi tiết)
```

## Ví dụ
**User:** "Phân rã chức năng cho hệ thống quản lý thư viện từ file requirements.md"

**Skill:**
1. Đọc requirements.md
2. Nhận diện các phân hệ: Quản lý sách, Quản lý độc giả, Mượn/trả, Báo cáo
3. Phân rã từng phân hệ thành chức năng con
4. Xuất function-breakdown.md

---

**Người tạo:** kimt168
**Ngày cập nhật:** 18/05/2026
**Phiên bản:** 1.0.0
