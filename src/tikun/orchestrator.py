"""
TikunOrchestrator - Main orchestration engine

Coordinates the execution of all 10 Sefirot in sequence,
managing state, error handling, and result aggregation.
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from tikun.config import TikunConfig, get_config
from tikun.utils.logging import get_logger, setup_logging, PerformanceLogger
from tikun.utils.validation import validate_scenario
from tikun.utils.export import ResultsExporter
from tikun.models.schemas import TikunResults, TikunMetadata, SefirotResults

# Import all Sefirot
from tikun.sefirot.keter import Keter
from tikun.sefirot.chochmah import Chochmah
from tikun.sefirot.binah import Binah
from tikun.sefirot.chesed import Chesed
from tikun.sefirot.gevurah import Gevurah
from tikun.sefirot.tiferet import Tiferet
from tikun.sefirot.netzach import Netzach
from tikun.sefirot.hod import Hod
from tikun.sefirot.yesod import Yesod
from tikun.sefirot.malchut import Malchut


class TikunOrchestrator:
    """
    Main orchestrator for Tikun Olam ethical reasoning pipeline.

    Executes all 10 Sefirot in sequence:
    1. Keter - Scope Definition & Validation
    2. Chochmah - Wisdom Analysis
    3. Binah - Understanding / BinahSigma
    4. Chesed - Opportunity Evaluation
    5. Gevurah - Risk Assessment
    6. Tiferet - Synthesis & Balance
    7. Netzach - Strategy Formation
    8. Hod - Communication Design
    9. Yesod - Integration & Coherence
    10. Malchut - Manifestation & Decision
    """

    def __init__(
        self,
        config: Optional[TikunConfig] = None,
        verbose: bool = False
    ):
        """
        Initialize orchestrator.

        Args:
            config: Tikun configuration (uses defaults if None)
            verbose: Enable verbose logging
        """
        self.config = config or get_config()
        self.verbose = verbose

        # Setup logging
        setup_logging(
            level=self.config.log_level,
            enable_console=True
        )

        self.logger = get_logger(__name__)
        self.logger.info("TikunOrchestrator initialized", version="1.0.0")

        # Initialize Sefirot
        self._init_sefirot()

        # Results exporter
        self.exporter = ResultsExporter(self.config.output_dir)

    def _init_sefirot(self) -> None:
        """Initialize all Sefirot."""
        try:
            self.logger.debug("Initializing Sefirot")

            self.keter = Keter(self.config, self.verbose)
            self.chochmah = Chochmah(self.config, self.verbose)
            self.binah = Binah(self.config, self.verbose)
            self.chesed = Chesed(self.config, self.verbose)
            self.gevurah = Gevurah(self.config, self.verbose)
            self.tiferet = Tiferet(self.config, self.verbose)
            self.netzach = Netzach(self.config, self.verbose)
            self.hod = Hod(self.config, self.verbose)
            self.yesod = Yesod(self.config, self.verbose)
            self.malchut = Malchut(self.config, self.verbose)

            self.logger.debug("All Sefirot initialized successfully")

        except Exception as e:
            self.logger.error(
                "Failed to initialize Sefirot",
                error=str(e),
                exc_info=True
            )
            raise

    def process(
        self,
        scenario: str,
        case_name: Optional[str] = None,
        auto_export: bool = True
    ) -> Dict[str, Any]:
        """
        Process scenario through full Tikun pipeline.

        Args:
            scenario: Input scenario text
            case_name: Optional name for this case
            auto_export: If True, automatically export results

        Returns:
            Complete results dictionary
        """
        start_time = time.time()

        case_name = case_name or f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.logger.info(
            f"Starting Tikun analysis",
            case_name=case_name,
            scenario_length=len(scenario)
        )

        # Validate scenario
        is_valid, error = validate_scenario(
            scenario,
            max_length=self.config.max_scenario_length
        )

        if not is_valid:
            self.logger.error(f"Scenario validation failed", error=error)
            raise ValueError(f"Invalid scenario: {error}")

        # Initialize results container
        results = {
            'sefirot_results': {},
            'metadata': {
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'case_name': case_name,
                'scenario_length': len(scenario),
                'models_used': {}
            },
            'scenario': scenario
        }

        try:
            # Execute pipeline with performance tracking
            with PerformanceLogger(self.logger, "full_tikun_pipeline"):
                # 1. KETER
                results['sefirot_results']['keter'] = self.keter.safe_process(scenario)
                results['metadata']['models_used']['keter'] = self.config.keter_model

                # Check if Keter threshold met
                if results['sefirot_results']['keter'].get('threshold_met', False):
                    self.logger.info("Keter threshold met, continuing pipeline")
                else:
                    self.logger.warning("Keter threshold NOT met, but continuing analysis")

                # 2. CHOCHMAH
                results['sefirot_results']['chochmah'] = self.chochmah.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['chochmah'] = self.config.chochmah_model

                # 3. BINAH (may activate BinahSigma)
                results['sefirot_results']['binah'] = self.binah.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                binah_mode = results['sefirot_results']['binah'].get('mode', 'simple')
                results['metadata']['models_used']['binah'] = f"{self.config.binah_west_model}"
                if binah_mode == 'sigma':
                    results['metadata']['models_used']['binah'] += f" + {self.config.binah_east_model}"

                # 4. CHESED
                results['sefirot_results']['chesed'] = self.chesed.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['chesed'] = self.config.chesed_model

                # 5. GEVURAH
                results['sefirot_results']['gevurah'] = self.gevurah.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['gevurah'] = self.config.gevurah_model

                # 6. TIFERET
                results['sefirot_results']['tiferet'] = self.tiferet.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['tiferet'] = self.config.tiferet_model

                # 7. NETZACH
                results['sefirot_results']['netzach'] = self.netzach.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['netzach'] = self.config.netzach_model

                # 8. HOD
                results['sefirot_results']['hod'] = self.hod.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['hod'] = self.config.hod_model

                # 9. YESOD
                results['sefirot_results']['yesod'] = self.yesod.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['yesod'] = self.config.yesod_model

                # 10. MALCHUT
                results['sefirot_results']['malchut'] = self.malchut.safe_process(
                    scenario,
                    results['sefirot_results']
                )
                results['metadata']['models_used']['malchut'] = self.config.malchut_model

            # Calculate total duration
            duration = time.time() - start_time
            results['metadata']['total_duration_seconds'] = round(duration, 2)

            self.logger.info(
                f"Tikun analysis complete",
                case_name=case_name,
                duration=duration,
                final_decision=results['sefirot_results']['malchut'].get('decision', 'UNKNOWN')
            )

            # Auto-export if requested
            if auto_export:
                self.export_results(results, format="json")
                self.export_results(results, format="txt")

            return results

        except Exception as e:
            self.logger.error(
                f"Pipeline execution failed",
                case_name=case_name,
                error=str(e),
                exc_info=True
            )
            raise

    def export_results(
        self,
        results: Dict[str, Any],
        format: str = "json"
    ) -> Path:
        """
        Export results to file.

        Args:
            results: Results dictionary
            format: Export format (json, txt, markdown)

        Returns:
            Path to exported file
        """
        try:
            case_name = results['metadata'].get('case_name', 'unknown')
            filepath = self.exporter.export(results, case_name, format=format)

            self.logger.info(
                f"Results exported",
                format=format,
                filepath=str(filepath)
            )

            return filepath

        except Exception as e:
            self.logger.error(
                f"Export failed",
                format=format,
                error=str(e),
                exc_info=True
            )
            raise

    def get_summary(self, results: Dict[str, Any]) -> str:
        """
        Generate human-readable summary of results.

        Args:
            results: Results dictionary

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("TIKUN OLAM ANALYSIS SUMMARY")
        lines.append("=" * 80)
        lines.append("")

        # Metadata
        meta = results.get('metadata', {})
        lines.append(f"Case: {meta.get('case_name', 'Unknown')}")
        lines.append(f"Timestamp: {meta.get('timestamp', 'Unknown')}")
        lines.append(f"Duration: {meta.get('total_duration_seconds', 0)}s")
        lines.append("")

        # Key metrics
        sefirot = results.get('sefirot_results', {})

        if 'keter' in sefirot:
            keter = sefirot['keter']
            lines.append(f"KETER - Alignment: {keter.get('alignment_percentage', 0)}%")
            lines.append(f"       Corruption: {keter.get('corruption_severity', 'unknown')}")
            lines.append(f"       Threshold Met: {keter.get('threshold_met', False)}")
            lines.append("")

        if 'binah' in sefirot:
            binah = sefirot['binah']
            mode = binah.get('mode', 'simple')
            lines.append(f"BINAH - Mode: {mode.upper()}")
            if mode == 'sigma':
                lines.append(f"       Bias Delta: {binah.get('bias_delta', 0)}%")
                lines.append(f"       Divergence: {binah.get('divergence_level', 'unknown')}")
            lines.append("")

        if 'yesod' in sefirot:
            yesod = sefirot['yesod']
            lines.append(f"YESOD - Readiness: {yesod.get('readiness_score', 0)}%")
            lines.append(f"       Quality: {yesod.get('yesod_quality', 'unknown')}")
            recommendation = yesod.get('go_no_go_recommendation', {})
            lines.append(f"       Recommendation: {recommendation.get('decision', 'UNKNOWN')}")
            lines.append("")

        if 'malchut' in sefirot:
            malchut = sefirot['malchut']
            lines.append(f"MALCHUT - FINAL DECISION: {malchut.get('decision', 'UNKNOWN')}")
            lines.append(f"         Confidence: {malchut.get('confidence', 'unknown')}")
            lines.append(f"         Quality: {malchut.get('manifestation_quality', 'unknown')}")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)
