#region generated meta
import typing
class Inputs(typing.TypedDict):
    report_data: dict
    output_filename: str | None
    company_name: str | None
    save_path: str | None
class Outputs(typing.TypedDict):
    md_content: str
    file_path: str
    status: str
    title: str
#endregion

from oocana import Context
import os
from datetime import datetime

def main(params: Inputs, context: Context) -> Outputs:
    """
    Generate comprehensive MD report from structured financial data

    Args:
        params: Input parameters including report data and configuration
        context: OOMOL context object

    Returns:
        Generated markdown content and file information
    """

    try:
        # Extract data structure
        data = params["report_data"]["data"]
        year = data["year"]
        quarter = data["quarter"]
        reports = data["reports"]

        # Generate report content
        md_content, title = generate_md_report(data, params.get("company_name"))

        # Determine save path
        if params.get("save_path"):
            file_path = params["save_path"]
        else:
            # Default to oomol-storage directory
            storage_dir = "/oomol-driver/oomol-storage"
            os.makedirs(storage_dir, exist_ok=True)

            # Generate filename - handle nullable output_filename
            output_filename = params.get('output_filename')
            if not output_filename:
                # Generate filename from title or use default
                company_name = params.get('company_name', '')
                if company_name:
                    # Sanitize company name for filename
                    import re
                    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', company_name)
                    sanitized_name = sanitized_name.replace(' ', '_')
                    output_filename = f"{sanitized_name}_financial_report"
                else:
                    output_filename = "financial_report"

            filename = f"{output_filename}_{year}Q{quarter}.md"
            file_path = os.path.join(storage_dir, filename)

        # Ensure directory exists
        dir_path = os.path.dirname(file_path)
        if dir_path:  # Only create directory if file_path contains a directory
            os.makedirs(dir_path, exist_ok=True)

        # Write MD file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return {
            "md_content": md_content,
            "file_path": file_path,
            "status": f"Successfully generated MD report with {len(reports)} Q&A items",
            "title": title
        }

    except Exception as e:
        raise ValueError(f"Failed to generate MD report: {str(e)}")

def generate_md_report(data: dict, company_name: str = None) -> tuple[str, str]:
    """Generate structured and standardized markdown report"""

    year = data["year"]
    quarter = data["quarter"]
    reports = data["reports"]

    # Classify content by categories
    classified_content = classify_content(reports)

    md_lines = []

    # Document title
    if company_name:
        title = f"{company_name} 财务分析报告 ({year}Q{quarter})"
        md_lines.append(f"# {title}")
    else:
        title = f"财务分析报告 ({year}Q{quarter})"
        md_lines.append(f"# {title}")

    md_lines.extend(["", "---", ""])

    # Table of contents generation removed - no longer generates TOC

    # First, add financial content directly under main title (no section header)
    section_number = 1
    if "financial" in classified_content and classified_content["financial"]:
        financial_items = classified_content["financial"]

        for item in financial_items:
            question = item.get("question", "").strip()
            answer = item.get("answer", "").strip()

            if question and answer:
                processed_answer = answer.replace("\\n", "\n")
                md_lines.extend([
                    f"## {section_number}. {question}",
                    "",
                    processed_answer,
                    "",
                    "---",
                    ""
                ])
                section_number += 1

        # Add separator after financial content
        md_lines.extend(["", "---", ""])

    # Generate other sections with numbered headings (excluding financial)
    sections = [
        ("business", "业务运营分析"),
        ("analysis", "专项分析"),
        ("management", "管理层分析"),
        ("governance", "公司治理与合规"),
        ("other", "其他信息")
    ]
    for section_key, section_title in sections:
        if section_key in classified_content and classified_content[section_key]:
            md_lines.extend([f"## {section_number}. {section_title}", ""])

            # Add all subsections without limits
            items = classified_content[section_key]

            subsection_number = 1
            for item in items:
                question = item.get("question", "").strip()
                answer = item.get("answer", "").strip()

                if question and answer:
                    processed_answer = answer.replace("\\n", "\n")
                    md_lines.extend([
                        f"### {section_number}.{subsection_number} {question}",
                        "",
                        processed_answer,
                        "",
                        "---",
                        ""
                    ])
                    subsection_number += 1

            section_number += 1

    # Add document footer
    md_lines.extend([
        "",
        "---",
        ""
    ])

    return "\n".join(md_lines), title


def generate_table_of_contents(classified_content: dict) -> str:
    """Generate table of contents based on classified content"""

    toc_lines = ["## 目录", ""]

    # Add financial content items (these appear directly under main title without section numbers)
    toc_number = 1
    if "financial" in classified_content and classified_content["financial"]:
        financial_items = classified_content["financial"]

        for item in financial_items:
            question = item.get("question", "").strip()
            if question:
                # Create anchor link compatible with markdown heading format
                anchor = create_anchor_link(f"{toc_number}. {question}")
                toc_lines.append(f"- [{toc_number}. {question}](#{anchor})")
                toc_number += 1

        toc_lines.append("")

    # Add other sections with numbered headings
    sections = [
        ("business", "业务运营分析"),
        ("analysis", "专项分析"),
        ("management", "管理层分析"),
        ("governance", "公司治理与合规"),
        ("other", "其他信息")
    ]

    section_number = toc_number
    for section_key, section_title in sections:
        if section_key in classified_content and classified_content[section_key]:
            anchor = create_anchor_link(f"{section_number}. {section_title}")
            toc_lines.append(f"- [{section_number}. {section_title}](#{anchor})")

            # Add all subsections without limits
            items = classified_content[section_key]

            subsection_number = 1
            for item in items:
                question = item.get("question", "").strip()
                if question:
                    anchor = create_anchor_link(f"{section_number}.{subsection_number} {question}")
                    toc_lines.append(f"  - [{section_number}.{subsection_number} {question}](#{anchor})")
                    subsection_number += 1

            section_number += 1

    toc_lines.extend(["", "---", ""])
    return "\n".join(toc_lines)


def create_anchor_link(text: str) -> str:
    """Create a URL-safe anchor link from text"""
    import re
    # Convert to lowercase, replace spaces and special chars with hyphens
    anchor = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text.lower())
    # Remove leading/trailing hyphens and multiple consecutive hyphens
    anchor = re.sub(r'^-+|-+$', '', anchor)
    anchor = re.sub(r'-+', '-', anchor)
    return anchor


def classify_content(reports: list) -> dict:
    """Classify Q&A content into different categories"""

    categories = {
        "financial": [],      # 财务相关
        "business": [],       # 业务运营
        "analysis": [],       # 专项分析
        "management": [],     # 管理层
        "governance": [],     # 治理合规
        "other": []          # 其他
    }

    # Keywords for classification
    financial_keywords = ["收入", "利润", "负债", "资产", "现金流", "毛利", "股息", "财务", "盈利", "营收", "EBITDA", "成本", "费用", "税收"]
    business_keywords = ["业务", "运营", "项目", "市场", "产品", "服务", "战略", "投资", "合作", "布局", "发展", "扩张", "竞争"]
    analysis_keywords = ["分析", "操纵", "风险", "评估", "模型", "指标", "比率", "趋势", "预测", "展望"]
    management_keywords = ["管理层", "高管", "董事", "薪酬", "激励", "员工", "人事", "变动", "任命", "离职"]
    governance_keywords = ["治理", "合规", "监管", "审计", "内控", "制度", "规范", "透明度", "责任"]

    for report in reports:
        question = report.get("question", "").strip()
        answer = report.get("answer", "").strip()

        if not question or not answer:
            continue

        # Classify based on keywords in question
        classified = False
        text_to_check = question + " " + answer[:100]  # Check first 100 chars of answer too

        if any(keyword in text_to_check for keyword in financial_keywords):
            categories["financial"].append(report)
            classified = True
        elif any(keyword in text_to_check for keyword in business_keywords):
            categories["business"].append(report)
            classified = True
        elif any(keyword in text_to_check for keyword in analysis_keywords):
            categories["analysis"].append(report)
            classified = True
        elif any(keyword in text_to_check for keyword in management_keywords):
            categories["management"].append(report)
            classified = True
        elif any(keyword in text_to_check for keyword in governance_keywords):
            categories["governance"].append(report)
            classified = True

        if not classified:
            categories["other"].append(report)

    return categories




