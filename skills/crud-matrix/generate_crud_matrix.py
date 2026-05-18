"""
CRUD Matrix Generator
Tạo ma trận CRUD từ ERD và Function Breakdown.

Usage:
    python generate_crud_matrix.py --erd <erd.md> --function-breakdown <fb.md> [--output <output.md>]
"""

import sys
import os
import io
import argparse
import re
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


@dataclass
class CRUDCell:
    """Một ô trong ma trận CRUD."""
    chuc_nang: str
    thuc_the: str
    c: bool = False
    r: bool = False
    u: bool = False
    d: bool = False

    def to_string(self) -> str:
        s = ""
        if self.c: s += "C"
        if self.r: s += "R"
        if self.u: s += "U"
        if self.d: s += "D"
        return s or "-"


@dataclass
class CRUDMatrix:
    """Ma trận CRUD."""
    ten_du_an: str
    chuc_nangs: list[str] = field(default_factory=list)
    thuc_the: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    cells: list[list[CRUDCell]] = field(default_factory=list)
    role_cells: list[list[str]] = field(default_factory=list)  # Role x Entity

    def to_markdown(self) -> str:
        """Xuất ra markdown."""
        lines = []
        lines.append(f"# Ma trận CRUD - {self.ten_du_an}\n")
        lines.append("---\n")

        # Section 1: CRUD Matrix - Chức năng x Thực thể
        lines.append("## 1. Ma trận CRUD - Chức năng và Thực thể\n")
        header = "| Chức năng | " + " | ".join(self.thuc_the) + " |"
        separator = "|" + "---|" * (len(self.thuc_the) + 1)
        lines.append(header)
        lines.append(separator)

        for i, cn in enumerate(self.chuc_nangs):
            row = [self.cells[i][j].to_string() for j in range(len(self.thuc_the))]
            lines.append(f"| {cn} | " + " | ".join(row) + " |")
        lines.append("")

        # Section 2: CRUD Matrix - Vai trò x Thực thể
        lines.append("## 2. Ma trận CRUD - Vai trò và Thực thể\n")
        header = "| Vai trò | " + " | ".join(self.thuc_the) + " |"
        separator = "|" + "---|" * (len(self.thuc_the) + 1)
        lines.append(header)
        lines.append(separator)

        for i, role in enumerate(self.roles):
            row = self.role_cells[i]
            lines.append(f"| {role} | " + " | ".join(row) + " |")
        lines.append("")

        # Section 3: Quy tắc CRUD
        lines.append("## 3. Quy tắc CRUD\n")
        lines.append("| STT | Quy tắc | Giải thích |")
        lines.append("|-----|---------|------------|")
        lines.append("| 1 | Nhân viên chỉ CRUD được dữ liệu do mình tạo | Kiểm soát theo created_by |")
        lines.append("| 2 | Trưởng phòng có thể CRUD tất cả dữ liệu trong phòng | Kiểm soát theo department_id |")
        lines.append("| 3 | Admin có full CRUD trên mọi thực thể | Ngoại lệ |")
        lines.append("| 4 | Xóa thực thể cha → các thực thể con bị xóa theo | Quan hệ 1-N cascade |")
        lines.append("| 5 | Thực thể sau khi xóa không cho phép sửa (soft delete) | Giữ lịch sử |")
        lines.append("")

        lines.append("---\n")
        lines.append(f"**Người tạo:** AI Agent\n")
        lines.append(f"**Ngày tạo:** {datetime.now().strftime('%d/%m/%Y')}\n")
        lines.append(f"**Phiên bản:** 1.0\n")

        return "\n".join(lines)


def extract_entities_from_erd(text: str) -> list[str]:
    """Trích xuất danh sách thực thể từ ERD markdown."""
    entities = []
    # Tìm trong bảng danh sách thực thể
    in_table = False
    for line in text.split("\n"):
        if "Tên thực thể" in line or "Tên tiếng Anh" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                # Lấy tên tiếng Anh (cột 2)
                entity_name = parts[1]
                if entity_name and entity_name not in ["STT", "---"]:
                    entities.append(entity_name)
        elif in_table and not line.startswith("|"):
            in_table = False

    # Nếu không tìm thấy, dùng default
    if not entities:
        entities = ["User", "Role", "EntityA", "EntityB", "Report"]

    return entities


def extract_functions_from_fb(text: str) -> list[str]:
    """Trích xuất danh sách chức năng từ Function Breakdown markdown."""
    functions = []
    # Tìm trong bảng mô tả chức năng
    in_table = False
    for line in text.split("\n"):
        if "Tên chức năng" in line or "Mã | Tên" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                func_name = parts[1]
                if func_name and func_name not in ["---", "Mã"]:
                    # Lấy thêm mã nếu có
                    if len(parts) >= 1 and parts[0] not in ["---"]:
                        func_name = f"{parts[0]} {func_name}"
                    functions.append(func_name)
        elif in_table and not line.startswith("|"):
            in_table = False

    # Nếu không tìm thấy, dùng default
    if not functions:
        functions = [
            "1.1 Quản lý EntityA",
            "1.2 Quản lý EntityB",
            "2.1 Báo cáo tổng hợp",
            "3.1 Quản lý người dùng",
            "3.2 Quản lý vai trò",
        ]

    return functions


def determine_crud(chuc_nang: str, thuc_the: str) -> str:
    """Xác định CRUD cho một cặp (chức năng, thực thể)."""
    cn_lower = chuc_nang.lower()
    te_lower = thuc_the.lower()

    # Pattern matching dựa trên tên chức năng
    if any(kw in cn_lower for kw in ["tạo", "new", "create", "add", "thêm"]):
        if te_lower in cn_lower or te_lower.replace("_", " ") in cn_lower:
            return "C"
    if any(kw in cn_lower for kw in ["xem", "danh sách", "list", "read", "view", "tìm", "search", "báo cáo"]):
        if te_lower in cn_lower or te_lower.replace("_", " ") in cn_lower:
            return "R"
    if any(kw in cn_lower for kw in ["sửa", "chỉnh", "update", "duyệt", "approve", "cập nhật"]):
        if te_lower in cn_lower or te_lower.replace("_", " ") in cn_lower:
            return "U"
    if any(kw in cn_lower for kw in ["xóa", "delete", "remove", "xoá"]):
        if te_lower in cn_lower or te_lower.replace("_", " ") in cn_lower:
            return "D"

    # Default rules based on function type
    if "quản lý" in cn_lower:
        if te_lower in cn_lower:
            return "CRUD"
    if "quản trị" in cn_lower:
        return "CRUD"
    if "báo cáo" in cn_lower or "report" in cn_lower:
        if thuc_the.lower() == "report":
            return "R"

    return ""


def generate_crud_matrix(
    erd_text: str,
    fb_text: str,
    ten_du_an: Optional[str] = None
) -> CRUDMatrix:
    """
    Tạo ma trận CRUD từ ERD và Function Breakdown.
    """
    entities = extract_entities_from_erd(erd_text)
    functions = extract_functions_from_fb(fb_text)
    roles = ["Admin", "Nhân viên", "Trưởng phòng", "Giám đốc"]

    if not ten_du_an:
        ten_du_an = "Hệ thống"

    # Tạo ma trận CRUD
    cells = []
    for func in functions:
        row = []
        for entity in entities:
            crud = determine_crud(func, entity)
            cell = CRUDCell(
                chuc_nang=func,
                thuc_the=entity,
                c="C" in crud,
                r="R" in crud,
                u="U" in crud,
                d="D" in crud,
            )
            row.append(cell)
        cells.append(row)

    # Tạo ma trận Role x Entity
    role_cells = []
    for role in roles:
        row = []
        for entity in entities:
            if role == "Admin":
                row.append("CRUD")
            elif role == "Nhân viên":
                if entity.lower() == "user":
                    row.append("R")
                else:
                    row.append("CRU")
            elif role == "Trưởng phòng":
                row.append("CRUD")
            elif role == "Giám đốc":
                if entity.lower() == "report":
                    row.append("RUD")
                else:
                    row.append("R")
        role_cells.append(row)

    return CRUDMatrix(
        ten_du_an=ten_du_an,
        chuc_nangs=functions,
        thuc_the=entities,
        roles=roles,
        cells=cells,
        role_cells=role_cells,
    )


def convert_file(
    erd_path: str,
    fb_path: str,
    output_path: Optional[str] = None,
    project_name: Optional[str] = None
) -> str:
    """
    Đọc ERD và Function Breakdown, tạo CRUD Matrix.
    """
    # Đọc ERD
    if not os.path.exists(erd_path):
        raise FileNotFoundError(f"File ERD không tồn tại: {erd_path}")
    with open(erd_path, "r", encoding="utf-8") as f:
        erd_content = f.read()

    # Đọc Function Breakdown
    if not os.path.exists(fb_path):
        raise FileNotFoundError(f"File Function Breakdown không tồn tại: {fb_path}")
    with open(fb_path, "r", encoding="utf-8") as f:
        fb_content = f.read()

    matrix = generate_crud_matrix(erd_content, fb_content, project_name)
    markdown = matrix.to_markdown()

    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(erd_path),
            "crud-matrix.md"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Đã tạo CRUD Matrix: {output_path}")
    print(f"Số chức năng: {len(matrix.chuc_nangs)}")
    print(f"Số thực thể: {len(matrix.thuc_the)}")
    print(f"Số vai trò: {len(matrix.roles)}")

    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Sinh Ma trận CRUD từ ERD và Function Breakdown"
    )
    parser.add_argument(
        "-erd", "--erd",
        required=True,
        help="Đường dẫn file ERD (.md)"
    )
    parser.add_argument(
        "-fb", "--function-breakdown",
        required=True,
        help="Đường dẫn file Function Breakdown (.md)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Đường dẫn file output (mặc định: crud-matrix.md)"
    )
    parser.add_argument(
        "-n", "--project-name",
        help="Tên dự án (override)"
    )

    args = parser.parse_args()

    try:
        convert_file(
            args.erd,
            args.function_breakdown,
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
