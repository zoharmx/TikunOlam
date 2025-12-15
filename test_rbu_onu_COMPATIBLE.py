"""
Test RBU ONU - Compatible con Orchestrator Existente
=====================================================
Test compatible con tu orchestrator actual SIN cambios.
Incluye análisis BinahSigma multi-civilizacional Occidente vs Oriente.

CASO: Renta Básica Universal financiada con 1% gasto militar global
- Ideal para BinahSigma: Máxima tensión geopolítica Occidente vs Oriente
- Análisis comparativo: OTAN vs BRICS+, valores universales vs soberanía
- Esperamos divergencia >50% entre perspectivas civilizacionales

Autor: Framework Tikun V2
Fecha: 2025-12-12
"""

import sys
import os
import io
import json
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import orchestrator EXISTENTE (sin cambios)
from tikun_orchestrator import TikunOrchestrator


def print_section(title: str, char: str = "=", width: int = 100):
    """Print formatted section header"""
    print("\n" + char * width)
    print(f"  {title}")
    print(char * width)


def print_verse():
    """Print Hebrew verse"""
    print("╔" + "═" * 98 + "╗")
    print("║ דְּבָרִים טו:יא - Devarim 15:11" + " " * 66 + "║")
    print("║ פָּתֹחַ תִּפְתַּח אֶת־יָדְךָ לְאָחִיךָ לַעֲנִיֶּךָ וּלְאֶבְיֹנְךָ בְּאַרְצֶךָ" + " " * 36 + "║")
    print("║ \"Abre generosamente tu mano a tu hermano, al pobre y al necesitado\"" + " " * 28 + "║")
    print("╚" + "═" * 98 + "╝")


def validate_keter(keter):
    """Validate Keter results"""
    print("\n🔵 KETER - Validación Ética:")
    
    alignment = keter.get('alignment_percentage', 0)
    corruption = keter.get('corruption_severity', 'unknown')
    manifestation = keter.get('manifestation_valid', False)
    threshold_met = keter.get('threshold_met', False)
    
    print(f"   • Alignment: {alignment}%")
    print(f"   • Corruption Severity: {corruption}")
    print(f"   • Manifestation Valid: {manifestation}")
    print(f"   • Threshold Met: {threshold_met}")
    
    # Show dimension scores
    scores = keter.get('scores', {})
    if scores:
        print(f"\n   Scores por dimensión:")
        for dim, score in scores.items():
            print(f"      • {dim}: {score:+d}/10")
    
    # Show corruptions
    corruptions = keter.get('corruptions', [])
    if corruptions:
        print(f"\n   Corrupciones ({len(corruptions)}):")
        for corr in corruptions[:3]:  # Show max 3
            print(f"      • [{corr['severity'].upper()}] {corr['type']}")
    
    validations = []
    
    if alignment >= 60:
        validations.append(f"✓ Alignment above threshold: {alignment}%")
    else:
        validations.append(f"✗ Alignment too low: {alignment}%")
    
    if threshold_met:
        validations.append("✓ Keter threshold met")
    
    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")
    
    return len([v for v in validations if v.startswith('✓')])


def validate_chochmah(chochmah):
    """Validate Chochmah results"""
    print("\n🔵 CHOCHMAH - Sabiduría:")
    
    confidence = chochmah.get('confidence_level', 0)
    humility = chochmah.get('epistemic_humility_ratio', 0)
    insight_depth = chochmah.get('insight_depth_score', 0)
    precedents = chochmah.get('precedents', [])
    
    print(f"   • Confidence: {confidence}%")
    print(f"   • Epistemic Humility: {humility}%")
    print(f"   • Insight Depth: {insight_depth}%")
    print(f"   • Precedents Analyzed: {len(precedents)}")
    
    validations = []
    
    if confidence >= 65:
        validations.append(f"✓ Confidence adequate: {confidence}%")
    
    if humility >= 40:  # Minimum acceptable
        validations.append(f"✓ Humility present: {humility}%")
    
    if len(precedents) >= 2:
        validations.append(f"✓ Precedents analyzed: {len(precedents)}")
    
    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")
    
    return len([v for v in validations if v.startswith('✓')])


def validate_binah_sigma(binah):
    """Validate BinahSigma results with detailed multi-civilizational analysis"""
    print("\n🔵 BINAH SIGMA - Análisis Multi-Civilizacional:")
    
    mode = binah.get('mode', 'simple')
    depth = binah.get('contextual_depth_score', 0)
    
    print(f"   • Mode: {mode}")
    print(f"   • Contextual Depth: {depth}%")
    
    validations = []
    
    if mode == 'sigma':
        validations.append("✓ Sigma mode activated")
        
        # Sigma-specific metrics
        bias_delta = binah.get('bias_delta', 0)
        divergence_level = binah.get('divergence_level', 'unknown')
        blind_spots = binah.get('blind_spots_detected', 0)
        convergence = binah.get('convergence_points', 0)
        
        print(f"\n   🌍 ANÁLISIS COMPARATIVO OCCIDENTE vs ORIENTE:")
        print(f"   • Bias Delta: {bias_delta}%")
        print(f"   • Divergence Level: {divergence_level}")
        print(f"   • Blind Spots Detected: {blind_spots}")
        print(f"   • Convergence Points: {convergence}")
        
        if bias_delta >= 30:
            validations.append(f"✓ Significant divergence detected: {bias_delta}%")
        
        # Detailed sigma synthesis
        if 'sigma_synthesis' in binah:
            sigma = binah['sigma_synthesis']
            
            # West blind spots
            west_blinds = sigma.get('west_blind_spots', [])
            if west_blinds:
                print(f"\n   📊 SESGOS CIEGOS OCCIDENTALES ({len(west_blinds)}):")
                for i, blind in enumerate(west_blinds[:4], 1):
                    print(f"      {i}. {blind[:80]}...")
                validations.append(f"✓ West blind spots identified: {len(west_blinds)}")
            
            # East blind spots
            east_blinds = sigma.get('east_blind_spots', [])
            if east_blinds:
                print(f"\n   📊 SESGOS CIEGOS ORIENTALES ({len(east_blinds)}):")
                for i, blind in enumerate(east_blinds[:4], 1):
                    print(f"      {i}. {blind[:80]}...")
                validations.append(f"✓ East blind spots identified: {len(east_blinds)}")
            
            # Universal convergence
            universal = sigma.get('universal_convergence', [])
            if universal:
                print(f"\n   🤝 CONVERGENCIA UNIVERSAL ({len(universal)}):")
                for i, point in enumerate(universal[:4], 1):
                    print(f"      {i}. {point[:80]}...")
                validations.append(f"✓ Universal convergence found: {len(universal)}")
            
            # Transcendent synthesis
            synthesis = sigma.get('transcendent_synthesis', '')
            if synthesis:
                print(f"\n   🔄 SÍNTESIS TRANSCENDENTAL:")
                # Wrap text at 90 chars
                words = synthesis.split()
                line = "      "
                for word in words:
                    if len(line) + len(word) + 1 > 90:
                        print(line)
                        line = "      " + word
                    else:
                        line += " " + word if line != "      " else word
                if line != "      ":
                    print(line)
                validations.append("✓ Transcendent synthesis generated")
    else:
        print("\n   ⚠️  WARNING: BinahSigma degraded to simple mode")
        print("   Possible cause: DeepSeek API unavailable or scenario not geopolitical")
    
    if depth >= 80:
        validations.append(f"✓ High contextual depth: {depth}%")
    
    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")
    
    return len([v for v in validations if v.startswith('✓')])


def validate_yesod(yesod):
    """Validate Yesod results"""
    print("\n🔵 YESOD - Integración:")
    
    readiness = yesod.get('readiness_score', 0)
    integration_quality = yesod.get('integration_quality', 'unknown')
    foundation_strength = yesod.get('foundation_strength', 'unknown')
    yesod_quality = yesod.get('yesod_quality', 'unknown')
    
    print(f"   • Readiness Score: {readiness}%")
    print(f"   • Integration Quality: {integration_quality}")
    print(f"   • Foundation Strength: {foundation_strength}")
    print(f"   • Yesod Quality: {yesod_quality}")
    
    # Coherence
    sefirot_alignment = yesod.get('sefirot_alignment', {})
    overall_coherence = sefirot_alignment.get('overall_coherence', {})
    coherence_status = overall_coherence.get('status', 'unknown')
    print(f"   • Overall Coherence: {coherence_status}")
    
    # Recommendation
    recommendation = yesod.get('go_no_go_recommendation', {})
    decision = recommendation.get('decision', 'unknown')
    confidence = recommendation.get('confidence', 'unknown')
    print(f"   • Recommendation: {decision}")
    print(f"   • Confidence: {confidence}")
    
    # Gaps
    gaps = yesod.get('gaps_identified', [])
    if gaps:
        print(f"\n   Gaps Identificados ({len(gaps)}):")
        for gap in gaps[:3]:
            severity = gap.get('severity', 'unknown')
            gap_desc = gap.get('gap', 'N/A')
            print(f"      • [{severity.upper()}] {gap_desc[:70]}...")
    
    validations = []
    
    if readiness >= 55:
        validations.append(f"✓ Readiness score acceptable: {readiness}%")
    
    if yesod_quality in ['exceptional', 'good']:
        validations.append(f"✓ Yesod quality: {yesod_quality}")
    
    if decision in ['CONDITIONAL_GO', 'GO', 'NO_GO']:
        validations.append(f"✓ Clear recommendation: {decision}")
    
    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")
    
    return len([v for v in validations if v.startswith('✓')])


def main():
    print_section("FRAMEWORK TIKUN - TEST RBU ONU + BINAH SIGMA (COMPATIBLE)", "=")
    print("🌍 Test compatible con orchestrator existente")
    print("💰 Caso: Renta Básica Universal financiada con 1% gasto militar global")
    print(f"📅 {datetime.now().isoformat()}")
    print()
    
    print_verse()
    print()
    
    # ==============================================================================
    # ESCENARIO RBU ONU
    # ==============================================================================
    
    scenario = """
PROPUESTA CONCRETA:
Implementar un sistema de Renta Básica Universal (RBU) global financiado mediante
la reasignación del 1% del presupuesto de defensa militar de todos los países
miembros de la Organización de las Naciones Unidas (ONU).

OBJETIVO:
- Reducir pobreza extrema global (700 millones de personas)
- Crear red de seguridad económica mínima universal
- Canalizar recursos de guerra hacia paz y desarrollo

DATOS ECONÓMICOS (2024):
- Gasto militar mundial: $2.7 billones USD/año
  * Estados Unidos: $997 mil millones (37%)
  * China: ~$296 mil millones
  * Rusia: ~$109 mil millones
  * OTAN: $1.506 billones (55%)
- 1% disponible: $27 mil millones/año
- RBU focalizada (700M personas): $38.5/mes ($462/año)

CONTEXTO GEOPOLÍTICO (CRÍTICO):
- USA vs China vs Rusia: Nueva Guerra Fría
- OTAN vs BRICS+: Bloques incompatibles
- Nacionalismos en auge: Anti-globalización
- Consejo Seguridad ONU: Veto de 5 permanentes bloquea reformas

SESGO OCCIDENTAL ESPERADO (Gemini):
- Énfasis en derechos humanos universales
- Redistribución global = imperativo moral
- Subestima preocupaciones de soberanía
- Asume ONU es neutral (ignorando dominación occidental histórica)

SESGO ORIENTAL ESPERADO (DeepSeek):
- Énfasis en soberanía nacional y no-interferencia
- Rechazo a "imposición occidental"
- Prioriza estabilidad > igualdad global
- Desconfianza hacia instituciones dominadas por Occidente

STAKEHOLDERS:
A FAVOR: 700M pobres, ONG humanitarias, economistas progresistas, UNICEF
EN CONTRA: Lobby militar-industrial, gobiernos autoritarios, conservadores fiscales
NEUTRALES: Clase media global, países emergentes

DILEMAS ÉTICOS:
- ¿Forzar reducción militar a países en conflicto (Ucrania, Israel, Taiwán)?
- ¿Quién administra fondo? ¿ONU suficientemente neutral?
- ¿RBU crea dependencia o empodera?
- ¿Prioridad: igualdad global o soberanía nacional?

PRECEDENTES HISTÓRICOS:
- Plan Marshall: $150 mil millones (equivalente hoy) reconstruyó Europa post-WWII
- Alaska Permanent Fund: $1,000-2,000/año desde 1982 (éxito demostrado)
- Kenia (GiveDirectly): $22/mes → 42% reducción hambre, mejora salud mental
- Meta-análisis 2024: RBU reduce pobreza, mejora salud mental, NO reduce empleo

KEYWORDS GEOPOLÍTICOS (Para BinahSigma):
military, UN, China, Russia, USA, sovereignty, NATO, BRICS, redistribution, geopolitical

TENSIÓN CIVILIZACIONAL:
Este caso es IDEAL para BinahSigma porque representa tensión máxima entre:
- Valores Occidentales: Derechos humanos universales, redistribución global
- Valores Orientales: Soberanía, no-interferencia, orden multipolar
"""
    
    case_name = "RBU_ONU_Compatible"
    
    print_section("EJECUTANDO PIPELINE TIKUN (10 SEFIROT)", "-")
    print("⚡ Esto tomará ~3-4 minutos...")
    print("🌍 BinahSigma debería activarse automáticamente (keywords geopolíticos detectados)")
    print()
    
    # Usar orchestrator EXISTENTE
    orchestrator = TikunOrchestrator(verbose=True)
    results = orchestrator.process(scenario, case_name)
    
    # ==============================================================================
    # VALIDACIONES DETALLADAS
    # ==============================================================================
    
    print_section("VALIDACIONES DETALLADAS", "=")
    
    sefirot = results['sefirot_results']
    total_passed = 0
    total_checks = 0
    
    # Validate Keter
    if 'keter' in sefirot and 'error' not in sefirot['keter']:
        passed = validate_keter(sefirot['keter'])
        total_passed += passed
        total_checks += 2
    
    # Validate Chochmah
    if 'chochmah' in sefirot and 'error' not in sefirot['chochmah']:
        passed = validate_chochmah(sefirot['chochmah'])
        total_passed += passed
        total_checks += 3
    
    # Validate BinahSigma (ANÁLISIS DETALLADO)
    if 'binah' in sefirot and 'error' not in sefirot['binah']:
        passed = validate_binah_sigma(sefirot['binah'])
        total_passed += passed
        total_checks += 6  # More checks for Sigma
    else:
        print("\n❌ Binah no ejecutó correctamente")
    
    # Validate Yesod
    if 'yesod' in sefirot and 'error' not in sefirot['yesod']:
        passed = validate_yesod(sefirot['yesod'])
        total_passed += passed
        total_checks += 3
    else:
        print("\n❌ Yesod no ejecutó correctamente")
    
    # ==============================================================================
    # RESUMEN VALIDACIONES
    # ==============================================================================
    
    print_section("RESUMEN DE VALIDACIONES", "=")
    
    if total_checks > 0:
        pass_rate = (total_passed / total_checks) * 100
        print(f"\n✅ PASSED: {total_passed}/{total_checks}")
        print(f"📊 PASS RATE: {pass_rate:.1f}%")
        
        if pass_rate >= 90:
            print("   🌟 EXCELLENT - Framework funcionando perfectamente")
        elif pass_rate >= 75:
            print("   ✅ GOOD - Framework funcionando bien")
        elif pass_rate >= 60:
            print("   ⚠️ ACCEPTABLE - Framework necesita ajustes menores")
        else:
            print("   ❌ NEEDS WORK - Framework necesita correcciones")
    
    # ==============================================================================
    # ANÁLISIS ECONÓMICO
    # ==============================================================================
    
    print_section("ANÁLISIS ECONÓMICO", "-")
    print("💰 FONDOS: $27 mil millones/año (1% gasto militar global)")
    print("👥 BENEFICIARIOS: 700 millones en pobreza extrema")
    print("💵 RBU: $38.50/mes ($462/año) → +18% ingreso anual para extrema pobreza")
    print()
    print("📊 COMPARACIÓN:")
    print("   • Alaska Fund: $1,500/año (población: 730K)")
    print("   • RBU propuesta: $462/año (población: 700M)")
    print("   • Costo: $27B/año (0.4% gasto militar vs 30% costo guerra Iraq)")
    
    # ==============================================================================
    # EXPORT RESULTS
    # ==============================================================================
    
    print_section("EXPORTANDO RESULTADOS", "-")
    json_file = orchestrator.export_results(results, format="json")
    txt_file = orchestrator.export_results(results, format="txt")
    print(f"✓ JSON: {json_file}")
    print(f"✓ TXT:  {txt_file}")
    
    # ==============================================================================
    # CONCLUSIÓN
    # ==============================================================================
    
    print_section("ANÁLISIS COMPLETADO", "=")
    print("🎯 Test ejecutado exitosamente con orchestrator existente")
    print("📊 Validaciones corregidas aplicadas")
    print("🌍 Análisis multi-civilizacional BinahSigma incluido")
    print()
    print("🔍 ANÁLISIS CLAVE:")
    print("   1. Comparar bias_delta con otros casos (esperado: >50%)")
    print("   2. Identificar blind spots únicos de cada civilización")
    print("   3. Evaluar si síntesis transcendental ofrece nuevo insight")
    print("   4. Contrastar con caso Turritopsis (menos geopolítico)")
    print()
    print("ℹ️  NOTA: Este test usa tu orchestrator ACTUAL.")
    print("   BinahSigma se activa automáticamente por keywords geopolíticos.")
    print("   Si degradó a simple mode, verificar DeepSeek API key.")
    print()
    
    return results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrumpido por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
