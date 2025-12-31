"""
Example: How to reproduce the Nvidia-Groq analysis

This script demonstrates the Tikun Olam API for running ethical AI analysis.
The scenario analyzed here is the Nvidia-Groq $20B acquisition deal announced
on December 24, 2025.

Requirements:
- Python 3.11+
- Tikun Olam installed (pip install -r requirements.txt)
- API keys configured (.env file)

Usage:
    python results/run_analysis_example.py
"""

import asyncio
import json
from datetime import datetime
from tikun.orchestrator import TikunOrchestrator
from tikun.config import get_config

# Initialize configuration
config = get_config()

# Define the ethical scenario to analyze
scenario = """
NVIDIA-GROQ $20B ACQUISITION EVALUATION

On December 24, 2024, Nvidia announced a $20 billion agreement to license
technology from AI chip startup Groq and hire its CEO Jonathan Ross and
executive team.

KEY CONCERNS:
• Nvidia controls 95% of AI training chip market
• Groq is a key competitor in AI inference market
• Deal structured as "licensing" to avoid merger review
• Groq loses entire leadership team despite remaining "independent"
• $20B represents 290% premium over recent $6.9B valuation
• Pattern of eliminating competition vs. competing fairly

DECISION REQUIRED:
How should the Federal Trade Commission (FTC) respond to preserve competition,
protect innovation, and balance national strategic interests?

OPTIONS:
A) Approve as-is (trust free market)
B) Block deal entirely (preserve independent competition)
C) Conditional approval (with divestitures/oversight)
D) Restructure requirement (force formal acquisition review)
E) Investigation first (delay pending comprehensive review)

Evaluate using Tikún framework with BinahSigma civilizational bias detection.
"""

async def main():
    """Run the full ethical analysis pipeline"""

    print("=" * 70)
    print("TIKUN OLAM - Ethical AI Analysis")
    print("=" * 70)
    print(f"\nCase: Nvidia-Groq $20B Acquisition")
    print(f"Analysis started: {datetime.now().isoformat()}")
    print("\nExecuting 10-stage Sefirot pipeline with BinahSigma...\n")

    # Initialize orchestrator
    orchestrator = TikunOrchestrator()

    # Run full analysis
    result = await orchestrator.process(
        scenario=scenario,
        case_name="Nvidia_Groq_20B_MA_Example"
    )

    # Extract key metrics
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

    # BinahSigma metrics
    binah = result['sefirot_results']['binah']
    print(f"\n📊 BinahSigma Analysis:")
    print(f"   Bias Delta: {binah['bias_delta']}%")
    print(f"   Divergence Level: {binah['divergence_level']}")
    print(f"   Blind Spots Detected: {binah['blind_spots_detected']}")
    print(f"   Contextual Depth: {binah['contextual_depth_score']}/100")
    print(f"   Mode: {binah['mode'].upper()}")

    # Keter (ethical alignment)
    keter = result['sefirot_results']['keter']
    print(f"\n⚖️  Keter (Ethical Alignment):")
    print(f"   Alignment: {keter['alignment_percentage']}%")

    # Malchut (final decision)
    malchut = result['sefirot_results']['malchut']
    print(f"\n🎯 Malchut (Final Decision):")
    print(f"   Decision: {malchut['decision']}")
    print(f"   Confidence: {malchut.get('confidence', 'N/A')}")

    # Performance metrics
    metadata = result['metadata']
    duration = metadata['total_duration_seconds']
    print(f"\n⚡ Performance:")
    print(f"   Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"   Sefirot Completed: 10/10")

    # Save results
    output_file = f"results/nvidia_groq_example_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Results saved to: {output_file}")
    print(f"\nResult file size: {len(json.dumps(result)) / 1024:.1f} KB")

    print("\n" + "=" * 70)
    print("Analysis demonstrates:")
    print("  ✓ Civilizational blind spot detection (BinahSigma)")
    print("  ✓ Multi-model AI synthesis (Gemini + DeepSeek + Claude)")
    print("  ✓ Full auditability trail (10-stage reasoning)")
    print("  ✓ Transcendent synthesis beyond binary thinking")
    print("=" * 70 + "\n")

    return result

if __name__ == "__main__":
    # Run the async analysis
    result = asyncio.run(main())

    # Print transcendent synthesis if available
    if 'binah' in result['sefirot_results']:
        synthesis = result['sefirot_results']['binah'].get('sigma_synthesis', {})
        if 'transcendent_synthesis' in synthesis:
            print("\n🌟 TRANSCENDENT SYNTHESIS:")
            print("-" * 70)
            print(synthesis['transcendent_synthesis'][:500] + "...")
            print("-" * 70)
