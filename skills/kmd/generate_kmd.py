"""
KMD Generator - Khảo sát Hiện trạng
Tạo tài liệu khảo sát hiện trạng từ thông tin quy trình và vấn đề.

Usage:
    python generate_kmd.py <input_text.md> [--output <output.md>] [--project-name <ten>]
"""

import sys
import os
import io
import argparse
import re
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


@dataclass
class VanDe:
    """Một vấn đề trong hiện trạng."""
    stt: int
    mo_ta: str
    muc_do: str  # Cao / Trung bình / Thấp
    nguyen_nhan: str


@dataclass
class YeuCauCaiTien:
    """Một yêu cầu cải tiến."""
    stt: int
    yeu_cau: str
    van_de_giai_quyet: str
    do_uu_tien: str


@dataclass
class HeThongHienCo:
    """Một hệ thống đang sử dụng."""
    stt: int
    ten: str
    muc_dich: str
    han_che: str


@dataclass
class VaiTro:
    """Một vai trò người dùng."""
    ten: str
    so_luong: int
    mo_ta: str
    yeu_cau: str


@dataclass
class KMDReport:
    """Báo cáo khảo sát hiện trạng."""
    ten_du_an: str
    don_vi: str = ""
    nguoi_lien_he: str = ""
    ngay_khao_sat: str = ""
    quy_trinh_hien_tai: str = ""
    van_de: list[VanDe] = field(default_factory=list)
    yeu_cau_cai_tien: list[YeuCauCaiTien] = field(default_factory=list)
    he_thong_hien_co: list[HeThongHienCo] = field(default_factory=list)
    vai_tro: list[VaiTro] = field(default_factory=list)
    rang_buoc: list[str] = field(default_factory=list)
    gia_dinh: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Xuất ra markdown theo template."""
        lines = []
        lines.append(f"# Báo cáo Khảo sát Hiện trạng - {self.ten_du_an}\n")
        lines.append("---\n")

        # Section 1: Thông tin chung
        lines.append("## 1. Thông tin chung về dự án\n")
        lines.append(f"| Thông tin | Nội dung |")
        lines.append(f"|-----------|----------|")
        lines.append(f"| Tên dự án | {self.ten_du_an} |")
        lines.append(f"| Khách hàng | {self.don_vi or 'Chưa xác định'} |")
        lines.append(f"| Người phụ trách | {self.nguoi_lien_he or 'Chưa xác định'} |")
        lines.append(f"| Ngày khảo sát | {self.ngay_khao_sat or datetime.now().strftime('%d/%m/%Y')} |")
        lines.append(f"| Phương pháp khảo sát | Phỏng vấn, Quan sát, Thu thập tài liệu |")
        lines.append("")

        # Section 2: Hiện trạng quy trình
        lines.append("## 2. Hiện trạng quy trình nghiệp vụ\n")
        lines.append("### 2.1. Quy trình hiện tại\n")
        if self.quy_trinh_hien_tai:
            lines.append(self.quy_trinh_hien_tai)
        else:
            lines.append("*Chưa có thông tin về quy trình hiện tại.*")
        lines.append("")

        # Section 2.2: Vấn đề tồn tại
        lines.append("### 2.2. Vấn đề tồn tại\n")
        if self.van_de:
            lines.append("| STT | Vấn đề | Mức độ ảnh hưởng | Nguyên nhân |")
            lines.append("|-----|--------|------------------|-------------|")
            for vd in self.van_de:
                lines.append(f"| {vd.stt} | {vd.mo_ta} | {vd.muc_do} | {vd.nguyen_nhan} |")
        else:
            lines.append("*Không phát hiện vấn đề cụ thể.*")
        lines.append("")

        # Section 2.3: Yêu cầu cải tiến
        lines.append("### 2.3. Yêu cầu cải tiến\n")
        if self.yeu_cau_cai_tien:
            lines.append("| STT | Yêu cầu | Vấn đề giải quyết | Độ ưu tiên |")
            lines.append("|-----|---------|-------------------|------------|")
            for yc in self.yeu_cau_cai_tien:
                lines.append(f"| {yc.stt} | {yc.yeu_cau} | {yc.van_de_giai_quyet} | {yc.do_uu_tien} |")
        else:
            lines.append("*Chưa có yêu cầu cải tiến cụ thể.*")
        lines.append("")

        # Section 3: Hiện trạng hệ thống CNTT
        lines.append("## 3. Hiện trạng hệ thống CNTT\n")
        lines.append("### 3.1. Hệ thống đang sử dụng\n")
        if self.he_thong_hien_co:
            lines.append("| STT | Tên hệ thống | Mục đích sử dụng | Hạn chế |")
            lines.append("|-----|--------------|------------------|---------|")
            for ht in self.he_thong_hien_co:
                lines.append(f"| {ht.stt} | {ht.ten} | {ht.muc_dich} | {ht.han_che} |")
        else:
            lines.append("| STT | Tên hệ thống | Mục đích sử dụng | Hạn chế |")
            lines.append("|-----|--------------|------------------|---------|")
            lines.append("| 1 | Excel/Google Sheets | Lưu trữ và tính toán | Không có validation, khó chia sẻ |")
            lines.append("| 2 | Email | Trao đổi và phê duyệt | Không theo dõi được tiến độ |")
        lines.append("")

        # Section 4: Người dùng và vai trò
        lines.append("## 4. Người dùng và vai trò\n")
        lines.append("### 4.1. Danh sách người dùng dự kiến\n")
        if self.vai_tro:
            lines.append("| Vai trò | Số lượng | Mô tả công việc | Yêu cầu đặc biệt |")
            lines.append("|---------|----------|-----------------|------------------|")
            for vt in self.vai_tro:
                lines.append(f"| {vt.ten} | {vt.so_luong} | {vt.mo_ta} | {vt.yeu_cau} |")
        else:
            lines.append("| Vai trò | Số lượng | Mô tả công việc | Yêu cầu đặc biệt |")
            lines.append("|---------|----------|-----------------|------------------|")
            lines.append("| Admin | 2 | Quản trị hệ thống, người dùng, cấu hình | Có kiến thức CNTT |")
            lines.append("| Nhân viên | 20 | Nhập liệu, tra cứu, báo cáo cá nhân | Dễ sử dụng |")
            lines.append("| Trưởng phòng | 5 | Phê duyệt, xem báo cáo tổng hợp | Dashboard trực quan |")
        lines.append("")

        # Section 5: Ràng buộc và giả định
        lines.append("## 5. Ràng buộc và giả định\n")
        lines.append("### 5.1. Ràng buộc\n")
        if self.rang_buoc:
            for rb in self.rang_buoc:
                lines.append(f"- {rb}")
        else:
            lines.append("- **Thời gian:** Dự án phải hoàn thành theo kế hoạch")
            lines.append("- **Ngân sách:** Theo thỏa thuận")
            lines.append("- **Công nghệ:** Phải tương thích với hạ tầng hiện có")
        lines.append("")

        lines.append("### 5.2. Giả định\n")
        if self.gia_dinh:
            for gd in self.gia_dinh:
                lines.append(f"- {gd}")
        else:
            lines.append("- Người dùng có kỹ năng tin học cơ bản")
            lines.append("- Hạ tầng mạng ổn định")
            lines.append("- Dữ liệu hiện có có thể di chuyển sang hệ thống mới")
        lines.append("")

        lines.append("---\n")
        lines.append(f"**Người khảo sát:** AI Agent\n")
        lines.append(f"**Ngày báo cáo:** {datetime.now().strftime('%d/%m/%Y')}\n")

        return "\n".join(lines)


def parse_requirements_text(text: str) -> dict:
    """Phân tích text requirements để trích xuất thông tin cho KMD."""
    info = {
        "ten_du_an": "Dự án mới",
        "don_vi": "",
        "nguoi_lien_he": "",
        "quy_trinh": "",
        "van_de": [],
        "yeu_cau": [],
    }

    # Tìm tên dự án
    patterns = [
        r"(?:dự án|project|đề tài|topic)\s*(?:là|:)\s*([^\n]+)",
        r"#\s*([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info["ten_du_an"] = match.group(1).strip()
            break

    # Tìm quy trình hiện tại
    quy_trinh_keywords = ["quy trình", "hiện tại", "hiện trạng", "đang làm", "current process"]
    for keyword in quy_trinh_keywords:
        if keyword in text.lower():
            # Lấy đoạn văn chứa keyword
            for line in text.split("\n"):
                if keyword.lower() in line.lower():
                    info["quy_trinh"] += line.strip() + "\n"

    # Tìm vấn đề
    van_de_keywords = ["vấn đề", "khó khăn", "tồn tại", "hạn chế", "problem", "issue"]
    for keyword in van_de_keywords:
        if keyword in text.lower():
            for line in text.split("\n"):
                if keyword.lower() in line.lower() and len(line.strip()) > 20:
                    info["van_de"].append(line.strip())

    # Tìm yêu cầu
    yeu_cau_keywords = ["yêu cầu", "cần", "mong muốn", "expect", "require"]
    for keyword in yeu_cau_keywords:
        if keyword in text.lower():
            for line in text.split("\n"):
                if keyword.lower() in line.lower() and len(line.strip()) > 20:
                    info["yeu_cau"].append(line.strip())

    return info


def generate_kmd(
    input_text: str,
    ten_du_an: Optional[str] = None,
    don_vi: Optional[str] = None,
    nguoi_lien_he: Optional[str] = None
) -> KMDReport:
    """
    Tạo báo cáo KMD từ thông tin đầu vào.

    Args:
        input_text: Nội dung mô tả hiện trạng (từ file hoặc chat)
        ten_du_an: Tên dự án (override)
        don_vi: Tên đơn vị
        nguoi_lien_he: Người liên hệ

    Returns:
        KMDReport object
    """
    info = parse_requirements_text(input_text)

    report = KMDReport(
        ten_du_an=ten_du_an or info["ten_du_an"],
        don_vi=don_vi or "",
        nguoi_lien_he=nguoi_lien_he or "",
        ngay_khao_sat=datetime.now().strftime("%d/%m/%Y"),
        quy_trinh_hien_tai=info["quy_trinh"].strip() if info["quy_trinh"] else "",
    )

    # Thêm vấn đề
    if info["van_de"]:
        for i, vd_text in enumerate(info["van_de"][:5], 1):
            # Phân tích mức độ từ keywords
            muc_do = "Trung bình"
            if any(kw in vd_text.lower() for kw in ["nghiêm trọng", "nặng", "critical", "cao"]):
                muc_do = "Cao"
            elif any(kw in vd_text.lower() for kw in ["nhẹ", "thấp", "minor"]):
                muc_do = "Thấp"

            report.van_de.append(VanDe(
                stt=i,
                mo_ta=vd_text,
                muc_do=muc_do,
                nguyen_nhan="Chưa xác định rõ"
            ))
    else:
        # Default problems
        report.van_de = [
            VanDe(1, "Thao tác thủ công, tốn thời gian", "Cao", "Không有 hệ thống tự động"),
            VanDe(2, "Dữ liệu phân tán, khó tra cứu", "Cao", "Lưu trữ rời rạc trên Excel/Email"),
            VanDe(3, "Thiếu kiểm soát, dễ sai sót", "Trung bình", "Không có workflow phê duyệt"),
        ]

    # Thêm yêu cầu cải tiến
    if info["yeu_cau"]:
        for i, yc_text in enumerate(info["yeu_cau"][:5], 1):
            report.yeu_cau_cai_tien.append(YeuCauCaiTien(
                stt=i,
                yeu_cau=yc_text,
                van_de_giai_quyet="Xem phần vấn đề",
                do_uu_tien="Cao"
            ))
    else:
        # Default improvements
        report.yeu_cau_cai_tien = [
            YeuCauCaiTien(1, "Tự động hóa quy trình", "Vấn đề 1", "Cao"),
            YeuCauCaiTien(2, "Tập trung dữ liệu", "Vấn đề 2", "Cao"),
            YeuCauCaiTien(3, "Xây dựng workflow phê duyệt", "Vấn đề 3", "Cao"),
        ]

    # Thêm vai trò mặc định
    report.vai_tro = [
        VaiTro("Admin", 2, "Quản trị hệ thống, người dùng, cấu hình", "Có kiến thức CNTT"),
        VaiTro("Nhân viên", 20, "Nhập liệu, tra cứu, báo cáo cá nhân", "Dễ sử dụng"),
        VaiTro("Trưởng phòng", 5, "Phê duyệt, xem báo cáo tổng hợp", "Dashboard trực quan"),
        VaiTro("Giám đốc", 3, "Xem báo cáo chiến lược", "Báo cáo tổng quan"),
    ]

    return report


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    project_name: Optional[str] = None
) -> str:
    """
    Đọc thông tin từ file và tạo KMD report.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File không tồn tại: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    report = generate_kmd(content, ten_du_an=project_name)
    markdown = report.to_markdown()

    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(input_path),
            "kmd-report.md"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Đã tạo Báo cáo KMD: {output_path}")
    print(f"Số vấn đề: {len(report.van_de)}")
    print(f"Số yêu cầu cải tiến: {len(report.yeu_cau_cai_tien)}")

    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Sinh Báo cáo Khảo sát Hiện trạng (KMD)"
    )
    parser.add_argument(
        "input",
        help="Đường dẫn file input (.md)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Đường dẫn file output (mặc định: kmd-report.md)"
    )
    parser.add_argument(
        "-n", "--project-name",
        help="Tên dự án (override)"
    )

    args = parser.parse_args()

    try:
        convert_file(
            args.input,
            args.output,
            project_name=args.project_name
        )
    except FileNotFoundError as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Lỗi không xác định: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
