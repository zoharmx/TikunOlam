"""
Results export utilities for Tikun Olam

Handles exporting results to various formats (JSON, TXT, Markdown).
"""

import json
import orjson
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Literal
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

ExportFormat = Literal["json", "txt", "markdown", "md"]


class ResultsExporter:
    """
    Export Tikun results to various formats with proper formatting.
    """

    def __init__(self, output_dir: Path):
        """
        Initialize exporter.

        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        results: Dict[str, Any],
        case_name: str,
        format: ExportFormat = "json"
    ) -> Path:
        """
        Export results to specified format.

        Args:
            results: Results dictionary
            case_name: Name of the case
            format: Export format (json, txt, markdown, md)

        Returns:
            Path to exported file
        """
        format_lower = format.lower()

        if format_lower == "json":
            return self.export_json(results, case_name)
        elif format_lower in ["txt", "text"]:
            return self.export_txt(results, case_name)
        elif format_lower in ["markdown", "md"]:
            return self.export_markdown(results, case_name)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def export_json(
        self,
        results: Dict[str, Any],
        case_name: str,
        pretty: bool = True
    ) -> Path:
        """
        Export results as JSON.

        Args:
            results: Results dictionary
            case_name: Name of the case
            pretty: If True, format with indentation

        Returns:
            Path to exported JSON file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tikun_{case_name}_{timestamp}.json"
        filepath = self.output_dir / filename

        try:
            if pretty:
                # Use orjson for better performance
                json_bytes = orjson.dumps(
                    results,
                    option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
                )
                filepath.write_bytes(json_bytes)
            else:
                json_bytes = orjson.dumps(results)
                filepath.write_bytes(json_bytes)

            logger.info(f"Exported JSON results", filepath=str(filepath))
            return filepath

        except Exception as e:
            logger.error(f"Failed to export JSON", error=str(e), exc_info=True)
            raise

    def export_txt(
        self,
        results: Dict[str, Any],
        case_name: str
    ) -> Path:
        """
        Export results as plain text with formatting.

        Args:
            results: Results dictionary
            case_name: Name of the case

        Returns:
            Path to exported TXT file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tikun_{case_name}_{timestamp}.txt"
        filepath = self.output_dir / filename

        try:
            lines = []

            # Header
            lines.append("=" * 80)
            lines.append(f"TIKUN OLAM ANALYSIS RESULTS")
            lines.append("=" * 80)
            lines.append("")

            # Metadata
            if 'metadata' in results:
                meta = results['metadata']
                lines.append("METADATA:")
                lines.append("-" * 80)
                for key, value in meta.items():
                    lines.append(f"  {key}: {value}")
                lines.append("")

            # Sefirot Results
            if 'sefirot_results' in results:
                lines.append("SEFIROT ANALYSIS:")
                lines.append("=" * 80)

                sefirot_order = [
                    'keter', 'chochmah', 'binah', 'chesed', 'gevurah',
                    'tiferet', 'netzach', 'hod', 'yesod', 'malchut'
                ]

                for sefirah in sefirot_order:
                    if sefirah in results['sefirot_results']:
                        lines.append("")
                        lines.append(f"{sefirah.upper()}")
                        lines.append("-" * 80)

                        sefirah_data = results['sefirot_results'][sefirah]
                        self._format_dict_to_text(sefirah_data, lines, indent=2)

            filepath.write_text("\n".join(lines), encoding='utf-8')
            logger.info(f"Exported TXT results", filepath=str(filepath))
            return filepath

        except Exception as e:
            logger.error(f"Failed to export TXT", error=str(e), exc_info=True)
            raise

    def export_markdown(
        self,
        results: Dict[str, Any],
        case_name: str
    ) -> Path:
        """
        Export results as Markdown with formatting.

        Args:
            results: Results dictionary
            case_name: Name of the case

        Returns:
            Path to exported Markdown file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tikun_{case_name}_{timestamp}.md"
        filepath = self.output_dir / filename

        try:
            lines = []

            # Title
            lines.append(f"# Tikun Olam Analysis: {case_name}")
            lines.append("")

            # Metadata
            if 'metadata' in results:
                meta = results['metadata']
                lines.append("## Metadata")
                lines.append("")
                for key, value in meta.items():
                    lines.append(f"- **{key}**: {value}")
                lines.append("")

            # Sefirot Results
            if 'sefirot_results' in results:
                lines.append("## Sefirot Analysis")
                lines.append("")

                sefirot_order = [
                    'keter', 'chochmah', 'binah', 'chesed', 'gevurah',
                    'tiferet', 'netzach', 'hod', 'yesod', 'malchut'
                ]

                for sefirah in sefirot_order:
                    if sefirah in results['sefirot_results']:
                        lines.append(f"### {sefirah.title()}")
                        lines.append("")

                        sefirah_data = results['sefirot_results'][sefirah]
                        self._format_dict_to_markdown(sefirah_data, lines, level=4)
                        lines.append("")

            filepath.write_text("\n".join(lines), encoding='utf-8')
            logger.info(f"Exported Markdown results", filepath=str(filepath))
            return filepath

        except Exception as e:
            logger.error(f"Failed to export Markdown", error=str(e), exc_info=True)
            raise

    def _format_dict_to_text(
        self,
        data: Any,
        lines: list,
        indent: int = 0
    ) -> None:
        """Helper to format dictionary as text."""
        indent_str = " " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{indent_str}{key}:")
                    self._format_dict_to_text(value, lines, indent + 2)
                else:
                    lines.append(f"{indent_str}{key}: {value}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    lines.append(f"{indent_str}[{i}]:")
                    self._format_dict_to_text(item, lines, indent + 2)
                else:
                    lines.append(f"{indent_str}- {item}")
        else:
            lines.append(f"{indent_str}{data}")

    def _format_dict_to_markdown(
        self,
        data: Any,
        lines: list,
        level: int = 1
    ) -> None:
        """Helper to format dictionary as Markdown."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    lines.append(f"{'#' * level} {key}")
                    lines.append("")
                    self._format_dict_to_markdown(value, lines, level + 1)
                elif isinstance(value, list):
                    lines.append(f"**{key}**:")
                    lines.append("")
                    for item in value:
                        if isinstance(item, dict):
                            for k, v in item.items():
                                lines.append(f"- **{k}**: {v}")
                        else:
                            lines.append(f"- {item}")
                    lines.append("")
                else:
                    lines.append(f"**{key}**: {value}")
                    lines.append("")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for k, v in item.items():
                        lines.append(f"- **{k}**: {v}")
                else:
                    lines.append(f"- {item}")
            lines.append("")


def export_results(
    results: Dict[str, Any],
    output_dir: Path,
    case_name: str,
    format: ExportFormat = "json"
) -> Path:
    """
    Convenience function to export results.

    Args:
        results: Results dictionary
        output_dir: Directory to save exported files
        case_name: Name of the case
        format: Export format (json, txt, markdown, md)

    Returns:
        Path to exported file
    """
    exporter = ResultsExporter(output_dir)
    return exporter.export(results, case_name, format)
