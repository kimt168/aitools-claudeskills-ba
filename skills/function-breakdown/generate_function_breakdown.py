"""
Function Breakdown Generator
Phân rã hệ thống thành các chức năng con theo cấu trúc cây.

Usage:
    python generate_function_breakdown.py <input_requirements.md> [--output <output.md>] [--project-name <ten>]
"""

import sys
import os
import io
import argparse
import json
import re
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


class DoUuTien(Enum):
    CAO = "Cao"
    TRUNG_BINH = "Trung bình"
    THAP = "Thap"


class DoPhucTap(Enum):
    CAO = "Cao"
    TRUNG_BINH = "Trung bình"
    THAP = "Thap"


@dataclass
class ChucNang:
    """Một chức năng trong hệ thống."""
    ma: str  # 1.1, 1.1.1, ...
    ten: str
    mo_ta: str
    do_uu_tien: DoUuTien = DoUuTien.TRUNG_BINH
    do_phuc_tap: DoPhucTap = DoPhucTap.TRUNG_BINH
    tac_nhan: list[str] = field(default_factory=list)


@dataclass
class PhanHe:
    """Một phân hệ chứa các chức năng."""
    ten: str
    mo_ta: str
    chuc_nangs: list[ChucNang] = field(default_factory=list)


@dataclass
class FunctionBreakdown:
    """Kết quả phân rã chức năng."""
    ten_du_an: str
    phan_he: list[PhanHe] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Xuất ra markdown theo template."""
        lines = []
        lines.append(f"# Phân rã chức năng - {self.ten_du_an}\n")
        lines.append("---\n")

        # Section 1: Cây phân rã
        lines.append("## 1. Sơ đồ phân rã chức năng\n")
        lines.append("```")
        lines.append(f"[{self.ten_du_an}]")
        for i, ph in enumerate(self.phan_he, 1):
            lines.append(f"├── [Phân hệ {i}: {ph.ten}]")
            for j, cn in enumerate(ph.chuc_nangs, 1):
                prefix = "│   " if j < len(ph.chuc_nangs) else "    "
                lines.append(f"│   ├── [Chức năng {i}.{j}: {cn.ten}]")
                # Sub-functions (level 3)
                if cn.mo_ta:
                    lines.append(f"│   │   └── {cn.mo_ta}")
        lines.append("```\n")

        # Section 2: Bảng mô tả chức năng
        lines.append("## 2. Bảng mô tả chức năng\n")
        lines.append("| Mã | Tên chức năng | Phân hệ | Mô tả | Độ ưu tiên | Độ phức tạp |")
        lines.append("|-----|---------------|---------|-------|------------|-------------|")
        for i, ph in enumerate(self.phan_he, 1):
            for j, cn in enumerate(ph.chuc_nangs, 1):
                lines.append(
                    f"| {i}.{j} | {cn.ten} | {ph.ten} | {cn.mo_ta[:50]}... | "
                    f"{cn.do_uu_tien.value} | {cn.do_phuc_tap.value} |"
                )
        lines.append("")

        # Section 3: Ma trận chức năng - tác nhân
        lines.append("## 3. Ma trận chức năng - Tác nhân\n")
        # Thu thập tất cả actors
        all_actors = set()
        for ph in self.phan_he:
            for cn in ph.chuc_nangs:
                all_actors.update(cn.tac_nhan)
        all_actors = sorted(all_actors) if all_actors else ["Admin", "User"]

        header = "| Chức năng | " + " | ".join(all_actors) + " |"
        separator = "|" + "---|" * (len(all_actors) + 1)
        lines.append(header)
        lines.append(separator)

        for i, ph in enumerate(self.phan_he, 1):
            for j, cn in enumerate(ph.chuc_nangs, 1):
                marks = []
                for actor in all_actors:
                    if actor in cn.tac_nhan:
                        marks.append("✓")
                    else:
                        marks.append("")
                lines.append(f"| {i}.{j} {cn.ten} | " + " | ".join(marks) + " |")
        lines.append("")

        # Section 4: Phân loại
        lines.append("## 4. Phân loại chức năng\n")
        lines.append("### 4.1. Chức năng nghiệp vụ")
        for i, ph in enumerate(self.phan_he[:2], 1):  # Giả sử 2 phân hệ đầu là nghiệp vụ
            lines.append(f"- **Phân hệ {i} ({ph.ten}):** {len(ph.chuc_nangs)} chức năng")
        lines.append("")

        lines.append("### 4.2. Chức năng quản trị")
        if len(self.phan_he) > 2:
            ph = self.phan_he[2]
            lines.append(f"- **Phân hệ quản trị:** {len(ph.chuc_nangs)} chức năng")
        lines.append("")

        lines.append("### 4.3. Chức năng tích hợp")
        if len(self.phan_he) > 3:
            ph = self.phan_he[3]
            lines.append(f"- **Phân hệ tích hợp:** {len(ph.chuc_nangs)} chức năng")
        lines.append("")

        lines.append("---\n")
        lines.append(f"**Người tạo:** AI Agent\n")
        lines.append(f"**Ngày tạo:** {self._get_date()}\n")
        lines.append(f"**Phiên bản:** 1.0\n")

        return "\n".join(lines)

    def _get_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y")

    def to_dict(self) -> dict:
        """Serialize to dictionary for LLM context."""
        return {
            "ten_du_an": self.ten_du_an,
            "phan_he": [
                {
                    "ten": ph.ten,
                    "mo_ta": ph.mo_ta,
                    "chuc_nangs": [
                        {
                            "ma": cn.ma,
                            "ten": cn.ten,
                            "mo_ta": cn.mo_ta,
                            "do_uu_tien": cn.do_uu_tien.value,
                            "do_phuc_tap": cn.do_phuc_tap.value,
                            "tac_nhan": cn.tac_nhan,
                        }
                        for cn in ph.chuc_nangs
                    ]
                }
                for ph in self.phan_he
            ]
        }


def extract_project_name(text: str) -> str:
    """Trích xuất tên dự án từ requirements."""
    # Tìm trong các mẫu thường gặp
    patterns = [
        r"(?:tên|name|tiêu đề|title)\s*(?:là|:)\s*([^\n]+)",
        r"#\s*([^\n]+)",
        r"##\s*([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return "Hệ thống mới"


def analyze_requirements(text: str) -> FunctionBreakdown:
    """
    Phân tích requirements và tạo Function Breakdown.
    Sử dụng pattern matching và heuristics để nhận diện phân hệ và chức năng.
    """
    ten_du_an = extract_project_name(text)

    # Các keywords để nhận diện phân hệ
    phan_he_keywords = {
        "Quản lý nghiệp vụ": ["quản lý", "nghiệp vụ", "chức năng chính", "core", "business"],
        "Quản trị hệ thống": ["quản trị", "admin", "cấu hình", "setting", "configuration"],
        "Báo cáo & Thống kê": ["báo cáo", "thống kê", "report", "dashboard", "analytics"],
        "Tích hợp & API": ["tích hợp", "api", "kết nối", "sync", "integration"],
    }

    # Các keywords để nhận diện chức năng
    chuc_nang_keywords = {
        "Tạo mới": ["tạo", "thêm", "new", "create", "add"],
        "Chỉnh sửa": ["sửa", "chỉnh sửa", "cập nhật", "update", "edit"],
        "Xóa": ["xóa", "delete", "remove"],
        "Tìm kiếm": ["tìm", "tìm kiếm", "search", "query"],
        "Xem danh sách": ["danh sách", "list", "xem", "view"],
        "Xuất file": ["xuất", "export", "in", "download"],
        "Phê duyệt": ["duyệt", "phê duyệt", "approve", "approval"],
    }

    # Phân tích văn bản để tìm các thực thể chính (danh từ)
    lines = text.strip().split("\n")
    entities = []
    current_section = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Tìm các danh từ chỉ đối tượng quản lý
        for keyword in ["quản lý", "quản trị"]:
            if keyword in line.lower():
                # Trích xuất đối tượng được quản lý
                match = re.search(rf"{keyword}\s+([^\n,.;]+)", line, re.IGNORECASE)
                if match:
                    entity = match.group(1).strip()
                    if entity and entity not in entities:
                        entities.append(entity)

    # Tạo phân hệ dựa trên entities tìm được
    phan_he_list = []

    # Phân hệ 1: Quản lý nghiệp vụ (chứa các entities chính)
    nghiep_vu = PhanHe(
        ten="Quản lý nghiệp vụ",
        mo_ta="Các chức năng nghiệp vụ chính của hệ thống"
    )

    for i, entity in enumerate(entities[:5], 1):  # Giới hạn 5 entities chính
        cn = ChucNang(
            ma=f"1.{i}",
            ten=f"Quản lý {entity}",
            mo_ta=f"Quản lý thông tin {entity}: tạo, sửa, xóa, tìm kiếm",
            do_uu_tien=DoUuTien.CAO,
            do_phuc_tap=DoPhucTap.TRUNG_BINH,
            tac_nhan=["Admin", "User"]
        )
        nghiep_vu.chuc_nangs.append(cn)

    # Nếu không tìm thấy entity, tạo mặc định
    if not entities:
        default_entities = ["Đối tượng A", "Đối tượng B", "Đối tượng C"]
        for i, entity in enumerate(default_entities, 1):
            cn = ChucNang(
                ma=f"1.{i}",
                ten=f"Quản lý {entity}",
                mo_ta=f"Quản lý thông tin {entity}",
                do_uu_tien=DoUuTien.CAO,
                do_phuc_tap=DoPhucTap.TRUNG_BINH,
                tac_nhan=["Admin", "User"]
            )
            nghiep_vu.chuc_nangs.append(cn)

    phan_he_list.append(nghiep_vu)

    # Phân hệ 2: Báo cáo & Thống kê
    bao_cao = PhanHe(
        ten="Báo cáo & Thống kê",
        mo_ta="Các chức năng báo cáo, thống kê, dashboard"
    )
    bao_cao.chuc_nangs.append(ChucNang(
        ma="2.1",
        ten="Báo cáo tổng hợp",
        mo_ta="Xem báo cáo tổng hợp theo nhiều tiêu chí",
        do_uu_tien=DoUuTien.TRUNG_BINH,
        do_phuc_tap=DoPhucTap.TRUNG_BINH,
        tac_nhan=["Admin", "Manager"]
    ))
    bao_cao.chuc_nangs.append(ChucNang(
        ma="2.2",
        ten="Xuất báo cáo",
        mo_ta="Xuất báo cáo ra file Excel/PDF",
        do_uu_tien=DoUuTien.TRUNG_BINH,
        do_phuc_tap=DoPhucTap.THAP,
        tac_nhan=["Admin", "Manager"]
    ))
    phan_he_list.append(bao_cao)

    # Phân hệ 3: Quản trị hệ thống
    quan_tri = PhanHe(
        ten="Quản trị hệ thống",
        mo_ta="Các chức năng quản trị, cấu hình hệ thống"
    )
    quan_tri.chuc_nangs.append(ChucNang(
        ma="3.1",
        ten="Quản lý người dùng",
        mo_ta="Thêm, sửa, xóa, phân quyền người dùng",
        do_uu_tien=DoUuTien.CAO,
        do_phuc_tap=DoPhucTap.TRUNG_BINH,
        tac_nhan=["Admin"]
    ))
    quan_tri.chuc_nangs.append(ChucNang(
        ma="3.2",
        ten="Quản lý vai trò",
        mo_ta="Định nghĩa và phân quyền vai trò",
        do_uu_tien=DoUuTien.CAO,
        do_phuc_tap=DoPhucTap.TRUNG_BINH,
        tac_nhan=["Admin"]
    ))
    quan_tri.chuc_nangs.append(ChucNang(
        ma="3.3",
        ten="Cấu hình hệ thống",
        mo_ta="Thiết lập tham số, cấu hình hệ thống",
        do_uu_tien=DoUuTien.TRUNG_BINH,
        do_phuc_tap=DoPhucTap.THAP,
        tac_nhan=["Admin"]
    ))
    phan_he_list.append(quan_tri)

    return FunctionBreakdown(ten_du_an=ten_du_an, phan_he=phan_he_list)


def generate_from_llm(text: str, ten_du_an: str) -> FunctionBreakdown:
    """
    Generate Function Breakdown sử dụng LLM (Claude API).
    Đây là phiên bản nâng cao, dùng khi cần phân tích sâu hơn.
    """
    # Placeholder - sẽ implement khi có API key
    print("Lưu ý: Chức năng LLM cần API key. Sử dụng phiên bản cơ bản.")
    return analyze_requirements(text)


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    project_name: Optional[str] = None
) -> str:
    """
    Đọc requirements từ file và tạo Function Breakdown.

    Args:
        input_path: Đường dẫn file requirements (.md)
        output_path: Đường dẫn file output (mặc định: function-breakdown.md)
        project_name: Tên dự án (override)

    Returns:
        Nội dung markdown của Function Breakdown
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File không tồn tại: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Phân tích
    if project_name:
        fb = FunctionBreakdown(ten_du_an=project_name)
        fb = analyze_requirements(content)
        fb.ten_du_an = project_name
    else:
        fb = analyze_requirements(content)

    markdown = fb.to_markdown()

    # Lưu file
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(input_path),
            "function-breakdown.md"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Đã tạo Function Breakdown: {output_path}")
    print(f"Tổng số phân hệ: {len(fb.phan_he)}")
    tong_chuc_nang = sum(len(ph.chuc_nangs) for ph in fb.phan_he)
    print(f"Tổng số chức năng: {tong_chuc_nang}")

    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Sinh Function Breakdown từ requirements"
    )
    parser.add_argument(
        "input",
        help="Đường dẫn file requirements (.md)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Đường dẫn file output (mặc định: function-breakdown.md)"
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
