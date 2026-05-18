# Skill: Đọc file .docx (Read DOCX)

## Mô tả
Skill này cho phép đọc và trích xuất nội dung từ các file Microsoft Word (.docx), chuyển đổi sang định dạng Markdown để AI có thể đọc và xử lý. Hỗ trợ tiếng Việt, bảng biểu, danh sách, và cấu trúc heading.

## Tên kỹ thuật
- **Skill ID:** `read-docx`
- **Phiên bản:** 1.0.0
- **File chính:** `read_docx.py`

---

## Kích hoạt
Skill được kích hoạt khi người dùng:
- Upload file có đuôi `.docx`
- Yêu cầu đọc, tóm tắt, hoặc phân tích nội dung file Word
- Gọi trực tiếp từ orchestrator trong pipeline sinh SRS

## Đầu vào (Input)
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `input_path` | string | Có | Đường dẫn file `.docx` đầu vào |
| `output_path` | string | Không | Đường dẫn file `.md` đầu ra (mặc định: cùng tên với file input) |
| `include_metadata` | bool | Không | Có bao gồm metadata vào đầu file (mặc định: True) |

## Xử lý
1. **Kiểm tra đầu vào:**
   - File có tồn tại không
   - File có đúng định dạng `.docx` không
   - File có bị rỗng không

2. **Đọc và trích xuất nội dung:**
   - Duyệt qua từng element trong document (table, paragraph)
   - Với mỗi paragraph:
     - Phát hiện heading → chuyển thành `# Heading`
     - Phát hiện list item (bullet/numbered) → chuyển thành `- item`
     - Paragraph thường → giữ nguyên

3. **Xử lý bảng biểu:**
   - Chuyển đổi table Word → Markdown table
   - Escape ký tự đặc biệt (`|`, newline)

4. **Trích xuất metadata:**
   - Số đoạn văn (paragraphs)
   - Số bảng (tables)
   - Số heading
   - Kích thước file

5. **Xuất kết quả:**
   - Ghi ra file `.md` hoặc trả về chuỗi
   - Bao gồm metadata header (nếu yêu cầu)

## Đầu ra (Output)
```markdown
---
# Metadata
- Source: ten_file.docx
- Paragraphs: 150
- Tables: 3
- Headings: 12
- File size: 45678 bytes
---

# Tiêu đề chính

## Tiêu đề con

Nội dung đoạn văn...

- Danh sách item 1
- Danh sách item 2

| Cột 1 | Cột 2 | Cột 3 |
| --- | --- | --- |
| Dữ liệu 1 | Dữ liệu 2 | Dữ liệu 3 |
```

## Xử lý lỗi
| Lỗi | Hành động |
|-----|-----------|
| File không tồn tại | Ném `FileNotFoundError` với message rõ ràng |
| File không phải .docx | Ném `ValueError`, gợi ý dùng skill read-pdf |
| File bị mã hóa/bảo vệ | Ném exception, thông báo không thể đọc |
| File rỗng | Trả về markdown rỗng với metadata |
| Encoding lỗi | Dùng `errors="replace"` để thay thế ký tự không đọc được |

## Công cụ sử dụng
- **Python library:** `python-docx>=0.8.11`
- **Encoding:** UTF-8
- **Output format:** Markdown

## Tích hợp trong pipeline SRS
Skill này là bước đầu tiên trong pipeline:

```
requirements.docx
    ↓ [read-docx]
requirements.md (markdown)
    ↓ [requirement-parser]
YeuCauCoCauTruc (structured JSON)
    ↓ [srs-generator]
sections/*.md
    ↓ [srs-merger]
SRS_hoan_chinh.md
```

## Ví dụ sử dụng

### Dòng lệnh
```bash
# Chuyển đổi cơ bản
python read_docx.py "HuongDanTB_HPTN_(26-2-2020).docx"

# Chỉ định output path
python read_docx.py "input.docx" -o "output.md"

# Không bao gồm metadata
python read_docx.py "input.docx" --no-metadata
```

### Trong Python code
```python
from read_docx import convert_file, docx_to_markdown

# Cách 1: Convert và lưu file
markdown = convert_file("requirements.docx", output_path="requirements.md")

# Cách 2: Chỉ lấy nội dung markdown
content = docx_to_markdown("requirements.docx")
print(content)
```

### Trong orchestrator
```python
# Gọi như một skill trong pipeline
result = orchestrator.execute_skill(
    skill_id="read-docx",
    input_data={"input_path": "requirements.docx"}
)
```

## Kiểm thử
```bash
# Test với file thật
python read_docx.py "test_files/simple.docx"
python read_docx.py "test_files/with_tables.docx"
python read_docx.py "test_files/vietnamese_content.docx"

# Test error cases
python read_docx.py "non_existent.docx"  # File không tồn tại
python read_docx.py "file.txt"           # Sai định dạng
```

## Tài liệu tham khảo
- [python-docx documentation](https://python-docx.readthedocs.io/)
- [IEEE 830 SRS Template](../references/srs-structure.md)
