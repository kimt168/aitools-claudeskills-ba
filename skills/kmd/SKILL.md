# Skill: Khảo sát Hiện trạng (KMD - Khao Sat Hien Trang)

## Mô tả
Skill này hỗ trợ BA tạo tài liệu khảo sát hiện trạng (KMD), mô tả quy trình nghiệp vụ hiện tại, vấn đề tồn tại, và yêu cầu cải tiến trước khi xây dựng hệ thống mới.

## Tên kỹ thuật
- **Skill ID:** `kmd`
- **Phiên bản:** 1.0.0
- **File chính:** `generate_kmd.py`

---

## Kích hoạt
Skill được kích hoạt khi người dùng:
- Yêu cầu "tạo khảo sát hiện trạng" hoặc "tạo KMD"
- Upload tài liệu quy trình hiện tại và yêu cầu phân tích
- Gọi từ orchestrator trong giai đoạn khảo sát

## Đầu vào (Input)
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `current_process_text` | string | Có | Mô tả quy trình hiện tại |
| `pain_points` | string | Không | Các vấn đề/vướng mắc hiện tại |
| `ten_du_an` | string | Không | Tên dự án |
| `output_path` | string | Không | Đường dẫn file output |

## Xử lý
1. **Phân tích quy trình hiện tại:**
   - Xác định các bước trong quy trình
   - Xác định người thực hiện mỗi bước
   - Xác định công cụ/hệ thống đang dùng

2. **Nhận diện vấn đề:**
   - Phân loại vấn đề theo mức độ (Cao/Trung bình/Thấp)
   - Xác định nguyên nhân gốc rễ
   - Đánh giá tác động

3. **Đề xuất cải tiến:**
   - Map mỗi vấn đề với yêu cầu cải tiến
   - Ưu tiên hóa yêu cầu
   - Xác định phạm vi hệ thống mới

4. **Phân tích người dùng:**
   - Xác định các vai trò
   - Ước lượng số lượng người dùng
   - Phân quyền dự kiến

5. **Xuất kết quả theo template KMD**

## Đầu ra (Output)
File markdown với cấu trúc:
1. Thông tin chung về dự án
2. Hiện trạng quy trình nghiệp vụ
3. Vấn đề tồn tại và yêu cầu cải tiến
4. Hiện trạng hệ thống CNTT
5. Người dùng và vai trò
6. Ràng buộc và giả định

## Xử lý lỗi
| Lỗi | Hành động |
|-----|-----------|
| Không có thông tin quy trình | Yêu cầu user cung cấp |
| Thông tin quá ít | Cảnh báo và đề xuất bổ sung |

## Công cụ sử dụng
- **LLM:** Claude API để phân tích và tổng hợp
- **Template:** Jinja2 template (`kmd-template.md`)
- **Output:** Markdown

## Tích hợp trong pipeline
```
Phỏng vấn BA/Stakeholder
    ↓
[current_process.md]
    ↓ [kmd] ← Skill này
kmd-report.md (khảo sát hiện trạng)
    ↓
function-breakdown.md (phân rã chức năng)
```

## Ví dụ
**User:** "Tạo KMD cho quy trình quản lý đơn hàng hiện tại: Nhân viên nhận đơn qua email, nhập vào Excel, gửi sếp duyệt qua email, lưu file vào folder chung. Vấn đề: chậm, dễ sai, khó theo dõi."

**Skill:** Phân tích quy trình, nhận diện 5 vấn đề chính, đề xuất cải tiến, xuất kmd-report.md

---

**Người tạo:** kimt168
**Ngày cập nhật:** 18/05/2026
**Phiên bản:** 1.0.0
