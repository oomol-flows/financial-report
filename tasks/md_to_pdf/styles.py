"""
PDF styling module for markdown to PDF conversion
Provides CSS styles and theme management for PDF generation
"""

from typing import Dict, Optional


class PDFStyles:
    """Manages CSS styles for PDF generation"""

    def __init__(self):
        self._styles = {}
        self._load_default_styles()

    def _load_default_styles(self):
        """Load all default style components"""
        self._styles = {
            'base': self._get_base_styles(),
            'toc': self._get_toc_styles(),
            'headings': self._get_heading_styles(),
            'content': self._get_content_styles(),
            'code': self._get_code_styles(),
            'tables': self._get_table_styles(),
        }

    def _get_base_styles(self) -> str:
        """Base page and body styles"""
        return """
        @page {
            margin: 2cm;
            @bottom-center {
                content: counter(page);
            }
        }

        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: none;
        }
        """

    def _get_toc_styles(self) -> str:
        """Table of Contents styles"""
        return """
        /* Table of Contents Styles */
        .toc-container {
            page-break-after: always;
            margin-bottom: 2em;
        }

        .toc-title {
            font-size: 2em;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
            margin-bottom: 1em;
            bookmark-level: 1;
        }

        .toc {
            margin-left: 0;
        }

        .toc ul {
            list-style-type: none;
            padding-left: 0;
            margin: 0.5em 0;
        }

        .toc li {
            margin: 0.3em 0;
            padding-left: 1em;
        }

        .toc li ul {
            padding-left: 1.5em;
        }

        .toc a {
            color: #3498db;
            text-decoration: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.3em 0.5em;
            border-radius: 3px;
            transition: all 0.2s ease;
        }

        .toc a:hover {
            color: #2980b9;
            background-color: #ecf0f1;
            text-decoration: none;
            transform: translateX(5px);
        }

        .toc a:after {
            content: target-counter(attr(href), page);
            color: #7f8c8d;
            font-size: 0.9em;
            margin-left: auto;
            padding-left: 1em;
        }

        .toc-simple .toc a:after {
            display: none;
        }

        .page-break {
            page-break-after: always;
        }

        /* Enhanced TOC Navigation */
        .toc-detailed .toc a {
            border-left: 3px solid transparent;
        }

        .toc-detailed .toc a:hover {
            border-left-color: #3498db;
        }

        .toc .toc-level-1 > a {
            font-weight: bold;
            font-size: 1.1em;
        }

        .toc .toc-level-2 > a {
            font-weight: 500;
        }

        .toc .toc-level-3 > a,
        .toc .toc-level-4 > a,
        .toc .toc-level-5 > a,
        .toc .toc-level-6 > a {
            font-weight: normal;
            opacity: 0.9;
        }
        """

    def _get_heading_styles(self) -> str:
        """Heading styles with PDF bookmarks"""
        return """
        /* Heading Styles with PDF Bookmarks */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
        }

        h1 {
            font-size: 2.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.3em;
            bookmark-level: 1;
        }

        h2 {
            font-size: 2em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.3em;
            bookmark-level: 2;
        }

        h3 {
            font-size: 1.5em;
            bookmark-level: 3;
        }

        h4 {
            font-size: 1.2em;
            bookmark-level: 4;
        }

        h5 {
            font-size: 1.1em;
            bookmark-level: 5;
        }

        h6 {
            font-size: 1em;
            bookmark-level: 6;
        }
        """

    def _get_content_styles(self) -> str:
        """General content styles"""
        return """
        /* Content Styles */
        p {
            margin: 1em 0;
        }

        blockquote {
            border-left: 4px solid #bdc3c7;
            margin: 1em 0;
            padding: 0 1em;
            color: #7f8c8d;
        }

        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }

        li {
            margin: 0.5em 0;
        }

        a {
            color: #3498db;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .highlight {
            background-color: #f8f9fa;
            padding: 0.1em;
            border-radius: 3px;
        }
        """

    def _get_code_styles(self) -> str:
        """Code block and inline code styles"""
        return """
        /* Code Styles */
        code {
            background-color: #f8f9fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'DejaVu Sans Mono', 'Courier New', monospace;
            font-size: 0.9em;
        }

        pre {
            background-color: #f8f9fa;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }

        pre code {
            background-color: transparent;
            padding: 0;
        }
        """

    def _get_table_styles(self) -> str:
        """Table styles"""
        return """
        /* Table Styles */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }

        th, td {
            border: 1px solid #bdc3c7;
            padding: 0.5em;
            text-align: left;
        }

        th {
            background-color: #ecf0f1;
            font-weight: bold;
        }
        """

    def get_style(self, style_name: str) -> str:
        """Get a specific style component"""
        return self._styles.get(style_name, "")

    def get_combined_styles(self,
                          include_styles: Optional[list] = None,
                          exclude_styles: Optional[list] = None,
                          custom_css: str = "") -> str:
        """
        Get combined CSS styles

        Args:
            include_styles: List of style names to include (default: all)
            exclude_styles: List of style names to exclude
            custom_css: Additional custom CSS to append

        Returns:
            Combined CSS string
        """
        if include_styles is None:
            include_styles = list(self._styles.keys())

        if exclude_styles is None:
            exclude_styles = []

        # Filter styles
        styles_to_include = [
            name for name in include_styles
            if name in self._styles and name not in exclude_styles
        ]

        # Combine styles
        combined = "\n".join([
            self._styles[name] for name in styles_to_include
        ])

        # Add custom CSS
        if custom_css:
            combined += "\n" + custom_css

        return combined

    def create_theme(self, theme_name: str, style_overrides: Dict[str, str]):
        """Create a custom theme with style overrides"""
        _ = theme_name  # Theme name reserved for future use
        theme_styles = self._styles.copy()
        theme_styles.update(style_overrides)
        return theme_styles


class PDFThemes:
    """Predefined PDF themes"""

    @staticmethod
    def get_minimal_theme() -> Dict[str, str]:
        """Minimal theme with reduced styling"""
        return {
            'base': """
            @page {
                margin: 1.5cm;
                @bottom-center {
                    content: counter(page);
                }
            }

            body {
                font-family: 'DejaVu Sans', Arial, sans-serif;
                line-height: 1.5;
                color: #000;
                max-width: none;
            }
            """,
            'headings': """
            h1, h2, h3, h4, h5, h6 {
                color: #000;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                bookmark-level: var(--heading-level);
            }

            h1 { font-size: 2em; bookmark-level: 1; }
            h2 { font-size: 1.5em; bookmark-level: 2; }
            h3 { font-size: 1.2em; bookmark-level: 3; }
            h4 { font-size: 1em; bookmark-level: 4; }
            """
        }

    @staticmethod
    def get_professional_theme() -> Dict[str, str]:
        """Professional theme with enhanced styling"""
        return {
            'base': """
            @page {
                margin: 2.5cm;
                @top-right {
                    content: string(chapter);
                }
                @bottom-center {
                    content: "Page " counter(page) " of " counter(pages);
                }
            }

            body {
                font-family: 'DejaVu Serif', 'Times New Roman', serif;
                line-height: 1.6;
                color: #2c3e50;
                max-width: none;
            }
            """,
            'headings': """
            h1 {
                font-size: 2.5em;
                color: #1a252f;
                border-bottom: 4px solid #3498db;
                padding-bottom: 0.3em;
                margin-top: 3em;
                string-set: chapter content();
                bookmark-level: 1;
            }

            h2 {
                font-size: 2em;
                color: #34495e;
                border-bottom: 2px solid #7fb3d3;
                padding-bottom: 0.2em;
                bookmark-level: 2;
            }
            """
        }


def get_style_manager() -> PDFStyles:
    """Get the default PDF styles manager"""
    return PDFStyles()


def get_theme_styles(theme_name: str) -> Optional[Dict[str, str]]:
    """Get predefined theme styles"""
    themes = {
        'minimal': PDFThemes.get_minimal_theme(),
        'professional': PDFThemes.get_professional_theme(),
    }
    return themes.get(theme_name)