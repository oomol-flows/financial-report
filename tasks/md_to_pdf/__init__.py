#region generated meta
import typing
class Inputs(typing.TypedDict):
    md_content: str | None
    md_file_path: str | None
    output_filename: str
    save_path: str | None
    title: str | None
    author: str | None
    css_style: str | None
    generate_toc: bool
    toc_title: str | None
    style_theme: typing.Literal["default", "minimal", "professional"]
class Outputs(typing.TypedDict):
    pdf_path: str
    status: str
    file_size: float
#endregion

import os
import markdown
from weasyprint import HTML, CSS

# Import styles module - handle both relative and absolute imports
try:
    from .styles import get_style_manager, get_theme_styles
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from styles import get_style_manager, get_theme_styles

def main(params: Inputs, _context) -> Outputs:
    """
    Convert Markdown content to PDF format

    Args:
        params: Input parameters containing markdown content/file and options
        context: OOMOL context object

    Returns:
        Output dictionary with PDF path, status and file size
    """
    try:
        # Get markdown content
        md_content = ""
        if params.get("md_content"):
            md_content = params["md_content"]
        elif params.get("md_file_path"):
            if not os.path.exists(params["md_file_path"]):
                raise ValueError(f"Markdown file not found: {params['md_file_path']}")
            with open(params["md_file_path"], 'r', encoding='utf-8') as f:
                md_content = f.read()
        else:
            raise ValueError("Either md_content or md_file_path must be provided")

        if not md_content.strip():
            raise ValueError("Markdown content cannot be empty")

        # Configure markdown extensions
        extensions = [
            'codehilite',
            'tables',
            'toc',
            'fenced_code',
            'nl2br'
        ]

        extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': True,
            },
            'toc': {
                'permalink': True,
                'permalink_title': 'Link to this heading',
                'baselevel': 1,
                'toc_depth': 6,
                'anchorlink': True,
                'title': params.get('toc_title', 'Table of Contents')
            }
        }

        # Convert markdown to HTML
        md = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs
        )
        html_content = md.convert(md_content)

        # Generate table of contents if requested
        toc_html = ""
        if params.get('generate_toc', True):
            if hasattr(md, 'toc') and md.toc:
                toc_title = params.get('toc_title', 'Table of Contents')
                toc_html = f"""
                <div class="toc-container">
                    <h1 class="toc-title">{toc_title}</h1>
                    <div class="toc">
                        {md.toc}
                    </div>
                </div>
                <div class="page-break"></div>
                """

        # Generate CSS styles using the modular system
        style_theme = params.get('style_theme', 'default')

        # Get the appropriate styles based on theme
        if style_theme == 'default':
            style_manager = get_style_manager()
            default_css = style_manager.get_combined_styles()
        else:
            theme_styles = get_theme_styles(style_theme)
            if theme_styles:
                style_manager = get_style_manager()
                # Use theme styles with fallback to default for missing components
                combined_styles = []
                for component in ['base', 'toc', 'headings', 'content', 'code', 'tables']:
                    if component in theme_styles:
                        combined_styles.append(theme_styles[component])
                    else:
                        combined_styles.append(style_manager.get_style(component))
                default_css = '\n'.join(combined_styles)
            else:
                # Fallback to default theme if theme not found
                style_manager = get_style_manager()
                default_css = style_manager.get_combined_styles()

        # Combine with custom CSS
        final_css = default_css
        if params.get("css_style"):
            final_css += "\n" + params["css_style"]

        # Create complete HTML document
        title = params.get("title", "Document")
        author = params.get("author", "")

        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="author" content="{author}">
        </head>
        <body>
            {toc_html}
            {html_content}
        </body>
        </html>
        """

        # Determine output path
        output_filename = params.get("output_filename", "document")
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'

        if params.get("save_path"):
            pdf_path = params["save_path"]
            if not pdf_path.endswith('.pdf'):
                pdf_path = os.path.join(pdf_path, output_filename)
        else:
            # Save to oomol-storage if no specific path provided
            storage_path = "/oomol-driver/oomol-storage"
            os.makedirs(storage_path, exist_ok=True)
            pdf_path = os.path.join(storage_path, output_filename)

        # Ensure directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Convert HTML to PDF
        try:
            html_doc = HTML(string=full_html)
            css_doc = CSS(string=final_css)
            html_doc.write_pdf(pdf_path, stylesheets=[css_doc])
        except Exception as pdf_error:
            # Fallback: try without CSS
            try:
                html_doc = HTML(string=full_html)
                html_doc.write_pdf(pdf_path)
            except Exception as fallback_error:
                raise ValueError(f"PDF generation failed: {pdf_error}; Fallback also failed: {fallback_error}")

        # Get file size
        file_size = os.path.getsize(pdf_path)

        return {
            "pdf_path": pdf_path,
            "status": f"Successfully converted Markdown to PDF: {pdf_path}",
            "file_size": file_size
        }

    except Exception as e:
        error_msg = f"Error converting Markdown to PDF: {str(e)}"
        # Still return a valid response structure even on error
        return {
            "pdf_path": "",
            "status": error_msg,
            "file_size": 0
        }