"""
ERD Generator - Entity Relationship Diagram
Thiết kế mô hình dữ liệu từ requirements và function breakdown.

Usage:
    python generate_erd.py <input_requirements.md> [--function-breakdown <fb.md>] [--output <output.md>]
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
class ThuocTinh:
    """Một thuộc tính của thực thể."""
    ten: str
    kieu_du_lieu: str
    do_dai: str = ""
    rang_buoc: str = ""  # PK, FK, Unique, Not Null, ...
    mo_ta: str = ""


@dataclass
class ThucThe:
    """Một thực thể trong ERD."""
    ten_tieng_viet: str
    ten_tieng_anh: str
    mo_ta: str
    thuoc_tinh: list[ThuocTinh] = field(default_factory=list)
    so_ban_ghi_du_kien: int = 1000


@dataclass
class MoiQuanHe:
    """Một quan hệ giữa hai thực thể."""
    thuc_the_nguon: str
    cardinality: str  # 1-1, 1-N, N-N
    thuc_the_dich: str
    mo_ta: str = ""


@dataclass
class ERDReport:
    """Báo cáo ERD."""
    ten_du_an: str
    thuc_the: list[ThucThe] = field(default_factory=list)
    moi_quan_he: list[MoiQuanHe] = field(default_factory=list)
    quy_tac: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Xuất ra markdown theo template."""
        lines = []
        lines.append(f"# Thiết kế ERD - {self.ten_du_an}\n")
        lines.append("---\n")

        # Section 1: Danh sách thực thể
        lines.append("## 1. Danh sách thực thể\n")
        lines.append("| STT | Tên thực thể | Tên tiếng Anh | Mô tả | Số bản ghi dự kiến |")
        lines.append("|-----|--------------|---------------|-------|-------------------|")
        for i, te in enumerate(self.thuc_the, 1):
            lines.append(
                f"| {i} | {te.ten_tieng_viet} | {te.ten_tieng_anh} | "
                f"{te.mo_ta} | ~{te.so_ban_ghi_du_kien} |"
            )
        lines.append("")

        # Section 2: Mô tả chi tiết thực thể
        lines.append("## 2. Mô tả chi tiết thực thể\n")
        for te in self.thuc_the:
            lines.append(f"### 2.{self.thuc_the.index(te) + 1}. {te.ten_tieng_anh} ({te.ten_tieng_viet})\n")
            lines.append("| Thuộc tính | Kiểu dữ liệu | Độ dài | Ràng buộc | Mô tả |")
            lines.append("|------------|--------------|--------|-----------|-------|")
            for tt in te.thuoc_tinh:
                lines.append(
                    f"| {tt.ten} | {tt.kieu_du_lieu} | {tt.do_dai} | {tt.rang_buoc} | {tt.mo_ta} |"
                )
            lines.append("")

        # Section 3: Sơ đồ ERD
        lines.append("## 3. Sơ đồ ERD\n")
        lines.append("```")
        for te in self.thuc_the:
            lines.append(f"┌─────────────┐")
            lines.append(f"│ {te.ten_tieng_anh:11s} │")
            lines.append(f"├─────────────┤")
            for tt in te.thuoc_tinh[:5]:  # Hiển thị tối đa 5 thuộc tính
                pk_fk = ""
                if "PK" in tt.rang_buoc:
                    pk_fk = "PK"
                elif "FK" in tt.rang_buoc:
                    pk_fk = "FK"
                lines.append(f"│ {pk_fk:3s} {tt.ten:20s} │")
            lines.append(f"└─────────────┘")
        lines.append("```")
        lines.append("")

        # Section 4: Mối quan hệ
        lines.append("## 4. Mối quan hệ giữa các thực thể\n")
        lines.append("| Quan hệ | Thực thể nguồn | Cardinality | Thực thể đích | Mô tả |")
        lines.append("|---------|----------------|-------------|---------------|-------|")
        for i, mqh in enumerate(self.moi_quan_he, 1):
            lines.append(
                f"| R{i} | {mqh.thuc_the_nguon} | {mqh.cardinality} | "
                f"{mqh.thuc_the_dich} | {mqh.mo_ta} |"
            )
        lines.append("")

        # Section 5: Quy tắc nghiệp vụ
        lines.append("## 5. Quy tắc nghiệp vụ liên quan đến dữ liệu\n")
        if self.quy_tac:
            for qt in self.quy_tac:
                lines.append(f"- {qt}")
        else:
            lines.append("- Một User chỉ có thể có một Role")
            lines.append("- Entity code phải là duy nhất")
            lines.append("- Khi xóa User, các bản ghi liên quan được giữ lại (soft delete)")
        lines.append("")

        lines.append("---\n")
        lines.append(f"**Người thiết kế:** AI Agent\n")
        lines.append(f"**Ngày tạo:** {datetime.now().strftime('%d/%m/%Y')}\n")
        lines.append(f"**Phiên bản:** 1.0\n")

        return "\n".join(lines)


def extract_entities_from_text(text: str) -> list[ThucThe]:
    """Nhận diện thực thể từ văn bản requirements."""
    # Các thực thể thường gặp trong hệ thống
    common_entities = {
        "người dùng": ("User", "Thông tin người dùng hệ thống", 100),
        "user": ("User", "Thông tin người dùng hệ thống", 100),
        "tài khoản": ("Account", "Tài khoản đăng nhập", 100),
        "vai trò": ("Role", "Vai trò, quyền trong hệ thống", 10),
        "role": ("Role", "Vai trò, quyền trong hệ thống", 10),
        "quyền": ("Permission", "Quyền truy cập chức năng", 20),
        "đơn hàng": ("Order", "Đơn hàng giao dịch", 5000),
        "sản phẩm": ("Product", "Sản phẩm, hàng hóa", 1000),
        "khách hàng": ("Customer", "Thông tin khách hàng", 500),
        "nhân viên": ("Staff", "Thông tin nhân viên", 100),
        "báo cáo": ("Report", "Báo cáo, thống kê", 500),
        "lịch sử": ("History", "Lịch sử hoạt động", 10000),
        "log": ("SystemLog", "Nhật ký hệ thống", 50000),
    }

    entities = []
    text_lower = text.lower()

    for keyword, (ten_anh, mo_ta, so_luong) in common_entities.items():
        if keyword in text_lower:
            # Tạo tên tiếng Việt từ keyword
            ten_viet = keyword.capitalize()
            te = ThucThe(
                ten_tieng_viet=ten_viet,
                ten_tieng_anh=ten_anh,
                mo_ta=mo_ta,
                so_ban_ghi_du_kien=so_luong,
            )

            # Thêm thuộc tính cơ bản
            te.thuoc_tinh = [
                ThuocTinh("id", "INT", "-", "PK, Auto Increment", "Mã định danh"),
                ThuocTinh("code", "VARCHAR", "20", "Unique", "Mã code"),
                ThuocTinh("name", "NVARCHAR", "200", "Not Null", "Tên"),
                ThuocTinh("description", "NVARCHAR", "500", "-", "Mô tả"),
                ThuocTinh("status", "VARCHAR", "20", "Default: 'active'", "Trạng thái"),
                ThuocTinh("created_at", "DATETIME", "-", "Default: now()", "Ngày tạo"),
                ThuocTinh("updated_at", "DATETIME", "-", "-", "Ngày cập nhật"),
            ]

            entities.append(te)

    # Luôn thêm User và Role nếu chưa có
    if not any(te.ten_tieng_anh == "User" for te in entities):
        user = ThucThe("Người dùng", "User", "Thông tin người dùng", 50)
        user.thuoc_tinh = [
            ThuocTinh("user_id", "INT", "-", "PK, Auto Increment", "Mã người dùng"),
            ThuocTinh("username", "VARCHAR", "50", "Unique, Not Null", "Tên đăng nhập"),
            ThuocTinh("password_hash", "VARCHAR", "255", "Not Null", "Mật khẩu mã hóa"),
            ThuocTinh("full_name", "NVARCHAR", "100", "Not Null", "Họ tên"),
            ThuocTinh("email", "VARCHAR", "100", "Unique", "Email"),
            ThuocTinh("role_id", "INT", "-", "FK", "Mã vai trò"),
            ThuocTinh("is_active", "BOOLEAN", "-", "Default: true", "Trạng thái"),
            ThuocTinh("created_at", "DATETIME", "-", "Default: now()", "Ngày tạo"),
        ]
        entities.insert(0, user)

    if not any(te.ten_tieng_anh == "Role" for te in entities):
        role = ThucThe("Vai trò", "Role", "Vai trò trong hệ thống", 5)
        role.thuoc_tinh = [
            ThuocTinh("role_id", "INT", "-", "PK, Auto Increment", "Mã vai trò"),
            ThuocTinh("role_name", "NVARCHAR", "50", "Unique, Not Null", "Tên vai trò"),
            ThuocTinh("description", "NVARCHAR", "255", "-", "Mô tả"),
            ThuocTinh("permissions", "TEXT", "-", "-", "Danh sách quyền (JSON)"),
        ]
        entities.insert(1, role)

    return entities


def extract_relationships(entities: list[ThucThe]) -> list[MoiQuanHe]:
    """Xác định mối quan hệ giữa các thực thể."""
    relationships = []

    # User - Role (N:1)
    if any(te.ten_tieng_anh == "User" for te in entities) and \
       any(te.ten_tieng_anh == "Role" for te in entities):
        relationships.append(MoiQuanHe(
            thuc_the_nguon="User",
            cardinality="N:1",
            thuc_the_dich="Role",
            mo_ta="Một Role có nhiều User, một User có một Role"
        ))

    # User - các thực thể khác (1:N)
    for te in entities:
        if te.ten_tieng_anh not in ["User", "Role"]:
            relationships.append(MoiQuanHe(
                thuc_the_nguon="User",
                cardinality="1:N",
                thuc_the_dich=te.ten_tieng_anh,
                mo_ta=f"Một User tạo nhiều {te.ten_tieng_viet}"
            ))

    return relationships


def generate_erd(
    input_text: str,
    function_breakdown_text: Optional[str] = None,
    ten_du_an: Optional[str] = None
) -> ERDReport:
    """
    Tạo ERD từ requirements.

    Args:
        input_text: Nội dung requirements
        function_breakdown_text: Function breakdown (để hiểu thêm về chức năng)
        ten_du_an: Tên dự án

    Returns:
        ERDReport object
    """
    # Trích xuất tên dự án
    if not ten_du_an:
        match = re.search(r"#\s*([^\n]+)", input_text)
        ten_du_an = match.group(1).strip() if match else "Hệ thống mới"

    # Nhận diện thực thể
    entities = extract_entities_from_text(input_text)

    # Xác định quan hệ
    relationships = extract_relationships(entities)

    # Quy tắc nghiệp vụ
    quy_tac = [
        "Một User chỉ có thể có một Role",
        "Code của mỗi thực thể phải là duy nhất",
        "Khi xóa User, các bản ghi liên quan vẫn được giữ lại",
        "Các thực thể có trường created_at và updated_at để theo dõi lịch sử",
        "Soft delete được áp dụng cho các thực thể nghiệp vụ chính",
    ]

    return ERDReport(
        ten_du_an=ten_du_an,
        thuc_the=entities,
        moi_quan_he=relationships,
        quy_tac=quy_tac
    )


def convert_file(
    input_path: str,
    output_path: Optional[str] = None,
    function_breakdown_path: Optional[str] = None,
    project_name: Optional[str] = None
) -> str:
    """
    Đọc requirements từ file và tạo ERD.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File không tồn tại: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    fb_content = None
    if function_breakdown_path and os.path.exists(function_breakdown_path):
        with open(function_breakdown_path, "r", encoding="utf-8") as f:
            fb_content = f.read()

    report = generate_erd(content, fb_content, project_name)
    markdown = report.to_markdown()

    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(input_path),
            "erd-report.md"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Đã tạo ERD Report: {output_path}")
    print(f"Số thực thể: {len(report.thuc_the)}")
    print(f"Số quan hệ: {len(report.moi_quan_he)}")

    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Sinh ERD từ requirements"
    )
    parser.add_argument(
        "input",
        help="Đường dẫn file requirements (.md)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Đường dẫn file output (mặc định: erd-report.md)"
    )
    parser.add_argument(
        "-fb", "--function-breakdown",
        help="Đường dẫn file function breakdown (.md)"
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
            function_breakdown_path=args.function_breakdown,
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
