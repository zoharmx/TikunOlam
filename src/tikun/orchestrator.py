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

# Datadog observability
try:
    from ddtrace import tracer
    from monitoring.datadog_config import (
        emit_pipeline_start,
        emit_pipeline_complete,
        emit_pipeline_error,
        emit_metric
    )
    DATADOG_AVAILABLE = True
except ImportError:
    DATADOG_AVAILABLE = False
    tracer = None


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
            self.logger.info("Initializing Sefirot...")
            import time
            start = time.time()

            self.logger.info("Initializing Keter...")
            self.keter = Keter(self.config, self.verbose)
            self.logger.info(f"Keter initialized in {time.time() - start:.2f}s")

            self.logger.info("Initializing Chochmah...")
            t = time.time()
            self.chochmah = Chochmah(self.config, self.verbose)
            self.logger.info(f"Chochmah initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Binah...")
            t = time.time()
            self.binah = Binah(self.config, self.verbose)
            self.logger.info(f"Binah initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Chesed...")
            t = time.time()
            self.chesed = Chesed(self.config, self.verbose)
            self.logger.info(f"Chesed initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Gevurah...")
            t = time.time()
            self.gevurah = Gevurah(self.config, self.verbose)
            self.logger.info(f"Gevurah initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Tiferet...")
            t = time.time()
            self.tiferet = Tiferet(self.config, self.verbose)
            self.logger.info(f"Tiferet initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Netzach...")
            t = time.time()
            self.netzach = Netzach(self.config, self.verbose)
            self.logger.info(f"Netzach initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Hod...")
            t = time.time()
            self.hod = Hod(self.config, self.verbose)
            self.logger.info(f"Hod initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Yesod...")
            t = time.time()
            self.yesod = Yesod(self.config, self.verbose)
            self.logger.info(f"Yesod initialized in {time.time() - t:.2f}s")

            self.logger.info("Initializing Malchut...")
            t = time.time()
            self.malchut = Malchut(self.config, self.verbose)
            self.logger.info(f"Malchut initialized in {time.time() - t:.2f}s")

            self.logger.info(f"All Sefirot initialized successfully in {time.time() - start:.2f}s")

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

        # Create Datadog span for entire pipeline
        pipeline_span = None
        if DATADOG_AVAILABLE and tracer:
            pipeline_span = tracer.trace(
                "tikun.full_pipeline",
                service="tikun-orchestrator",
                resource="full_pipeline"
            )
            pipeline_span.set_tag('case_name', case_name)
            pipeline_span.set_tag('scenario_length', len(scenario))

            # Emit pipeline start metric
            emit_pipeline_start(case_name)

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

            # Get final decision for metrics
            final_decision = results['sefirot_results']['malchut'].get('decision', 'UNKNOWN')

            # Emit Datadog metrics for pipeline completion
            if DATADOG_AVAILABLE:
                duration_ms = duration * 1000

                # Emit pipeline completion
                emit_pipeline_complete(
                    case_name,
                    duration_ms,
                    final_decision
                )

                # Emit average alignment score
                keter_result = results['sefirot_results'].get('keter', {})
                alignment = keter_result.get('alignment_percentage', 0)
                emit_metric('pipeline.average_alignment', alignment, tags=[f'case:{case_name}'])

                # Add tags to pipeline span
                if pipeline_span:
                    pipeline_span.set_tag('final_decision', final_decision)
                    pipeline_span.set_tag('alignment_score', alignment)
                    pipeline_span.set_tag('duration_ms', duration_ms)
                    pipeline_span.set_tag('status', 'success')

            self.logger.info(
                f"Tikun analysis complete",
                case_name=case_name,
                duration=duration,
                final_decision=final_decision
            )

            # Auto-export if requested
            if auto_export:
                self.export_results(results, format="json")
                self.export_results(results, format="txt")

            return results

        except Exception as e:
            # Emit error metrics
            if DATADOG_AVAILABLE:
                emit_pipeline_error(case_name, e)

                if pipeline_span:
                    pipeline_span.set_tag('error', True)
                    pipeline_span.set_tag('error.message', str(e))
                    pipeline_span.set_tag('error.type', type(e).__name__)
                    pipeline_span.set_tag('status', 'failed')

            self.logger.error(
                f"Pipeline execution failed",
                case_name=case_name,
                error=str(e),
                exc_info=True
            )
            raise

        finally:
            # Finish pipeline span
            if pipeline_span:
                pipeline_span.finish()

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

    def get_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured summary of results for API response.

        Args:
            results: Results dictionary

        Returns:
            Structured summary dictionary
        """
        sefirot = results.get('sefirot_results', {})

        # Extract final decision from Malchut
        malchut = sefirot.get('malchut', {})
        final_decision = malchut.get('decision', 'UNKNOWN')

        # Extract overall alignment from Keter
        keter = sefirot.get('keter', {})
        overall_alignment = float(keter.get('alignment_percentage', 0))

        # Extract key risks from Gevurah (top 5)
        gevurah = sefirot.get('gevurah', {})
        risks = gevurah.get('risks', [])
        key_risks = []
        for risk in risks[:5]:
            if isinstance(risk, dict):
                desc = risk.get('description', '')
                if desc:
                    key_risks.append(desc)
            elif isinstance(risk, str):
                key_risks.append(risk)

        # If no risks extracted, add a generic message
        if not key_risks:
            key_risks = ["No significant risks identified"]

        # Extract key opportunities from Chesed (top 5)
        chesed = sefirot.get('chesed', {})
        opportunities = chesed.get('opportunities', [])
        key_opportunities = []
        for opp in opportunities[:5]:
            if isinstance(opp, dict):
                desc = opp.get('description', '')
                if desc:
                    key_opportunities.append(desc)
            elif isinstance(opp, str):
                key_opportunities.append(opp)

        # If no opportunities extracted, add a generic message
        if not key_opportunities:
            key_opportunities = ["Analysis complete. See detailed results."]

        # Generate recommendation from Yesod or Malchut
        yesod = sefirot.get('yesod', {})
        recommendation = yesod.get('recommendation', '')
        if not recommendation:
            recommendation = malchut.get('rationale', 'Analysis complete. Review detailed Sefirot results for comprehensive insights.')

        return {
            "final_decision": final_decision,
            "overall_alignment": overall_alignment,
            "key_risks": key_risks,
            "key_opportunities": key_opportunities,
            "recommendation": recommendation
        }
