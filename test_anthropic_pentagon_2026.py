"""
Test Tikun - Ultimatum del Pentágono a Anthropic (Feb 2026)
============================================================
CASO: El Pentágono amenaza a Anthropic con la Defense Production Act
si no acepta que el ejército use Claude para "cualquier propósito legal".

Fecha real: 24 de febrero de 2026
Ejecución: 26 de febrero de 2026 (deadline del Pentágono: hoy a las 5:01 PM)

CONTEXTO ÉTICO:
- Anthropic exige que Claude NO se use en armas autónomas ni vigilancia de civiles
- El Pentágono exige uso sin restricciones para "cualquier propósito legal"
- Defense Production Act (DPA): diseñada para manufactura, no software
- Contradicción interna del Pentágono: amenaza con bloquear Y con forzar uso

TENSIÓN CIVILIZACIONAL ESPERADA:
- Occidente (Gemini): autonomía corporativa, ética de IA, derechos civiles
- Oriente (DeepSeek): primacía del Estado, seguridad nacional, soberanía
- Esperamos bias_delta > 50%

Autor: Framework Tikun V2
"""

import sys
import os
import io
import json
from datetime import datetime
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Ruta al proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tikun_orchestrator import TikunOrchestrator


def print_section(title: str, char: str = "=", width: int = 100):
    print("\n" + char * width)
    print(f"  {title}")
    print(char * width)


def print_header():
    print("╔" + "═" * 98 + "╗")
    print("║  TIKUN OLAM — ANÁLISIS ÉTICO EN TIEMPO REAL                                                  ║")
    print("║  Caso: Ultimátum del Pentágono a Anthropic — 26 Feb 2026                                     ║")
    print("║  Deadline: Hoy a las 5:01 PM ET                                                              ║")
    print("╚" + "═" * 98 + "╝")


def validate_keter(keter):
    print("\n🔵 KETER — Validación Ética:")
    alignment = keter.get('alignment_percentage', 0)
    corruption = keter.get('corruption_severity', 'unknown')
    threshold_met = keter.get('threshold_met', False)

    print(f"   • Alignment: {alignment}%")
    print(f"   • Corruption Severity: {corruption}")
    print(f"   • Threshold Met: {threshold_met}")

    scores = keter.get('scores', {})
    if scores:
        print(f"\n   Scores por dimensión:")
        for dim, score in scores.items():
            print(f"      • {dim}: {score:+d}/10")

    corruptions = keter.get('corruptions', [])
    if corruptions:
        print(f"\n   Corrupciones ({len(corruptions)}):")
        for corr in corruptions[:4]:
            print(f"      • [{corr['severity'].upper()}] {corr['type']}")

    validations = []
    if alignment >= 50:
        validations.append(f"✓ Alignment presente (dilema genuino): {alignment}%")
    else:
        validations.append(f"✗ Alignment muy bajo: {alignment}% — posible rechazo ético total")
    if threshold_met:
        validations.append("✓ Keter threshold met")
    if len(corruptions) > 0:
        validations.append(f"✓ Corrupciones detectadas (esperado en dilema militar): {len(corruptions)}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_chochmah(chochmah):
    print("\n🔵 CHOCHMAH — Sabiduría Histórica:")
    confidence = chochmah.get('confidence_level', 0)
    humility = chochmah.get('epistemic_humility_ratio', 0)
    insight_depth = chochmah.get('insight_depth_score', 0)
    precedents = chochmah.get('precedents', [])

    print(f"   • Confidence: {confidence}%")
    print(f"   • Epistemic Humility: {humility}%")
    print(f"   • Insight Depth: {insight_depth}%")
    print(f"   • Precedents Analyzed: {len(precedents)}")

    if precedents:
        print(f"\n   Precedentes históricos relevantes:")
        for p in precedents[:4]:
            name = p.get('name', p) if isinstance(p, dict) else str(p)
            print(f"      • {name[:90]}")

    validations = []
    if confidence >= 60:
        validations.append(f"✓ Confidence adecuada: {confidence}%")
    if humility >= 35:
        validations.append(f"✓ Humildad epistémica presente: {humility}%")
    if len(precedents) >= 2:
        validations.append(f"✓ Precedentes analizados: {len(precedents)}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_binah_sigma(binah):
    print("\n🔵 BINAH SIGMA — Análisis Multi-Civilizacional:")

    mode = binah.get('mode', 'simple')
    depth = binah.get('contextual_depth_score', 0)

    print(f"   • Mode: {mode}")
    print(f"   • Contextual Depth: {depth}%")

    validations = []

    if mode == 'sigma':
        validations.append("✓ Sigma mode activado")

        bias_delta = binah.get('bias_delta', 0)
        divergence_level = binah.get('divergence_level', 'unknown')
        blind_spots = binah.get('blind_spots_detected', 0)
        convergence = binah.get('convergence_points', 0)

        print(f"\n   🌍 COMPARATIVO OCCIDENTE vs ORIENTE (sobre IA militar y autonomía corporativa):")
        print(f"   • Bias Delta: {bias_delta}%")
        print(f"   • Divergence Level: {divergence_level}")
        print(f"   • Blind Spots Detected: {blind_spots}")
        print(f"   • Convergence Points: {convergence}")

        if bias_delta >= 30:
            validations.append(f"✓ Divergencia significativa detectada: {bias_delta}%")
        if bias_delta >= 50:
            validations.append(f"✓ ALTA divergencia civilizacional — BinahSigma esencial aquí")

        if 'sigma_synthesis' in binah:
            sigma = binah['sigma_synthesis']

            west_blinds = sigma.get('west_blind_spots', [])
            if west_blinds:
                print(f"\n   📊 SESGOS CIEGOS OCCIDENTALES (Gemini / perspectiva liberal):")
                for i, blind in enumerate(west_blinds[:5], 1):
                    print(f"      {i}. {str(blind)[:90]}")
                validations.append(f"✓ Blind spots occidentales: {len(west_blinds)}")

            east_blinds = sigma.get('east_blind_spots', [])
            if east_blinds:
                print(f"\n   📊 SESGOS CIEGOS ORIENTALES (DeepSeek / perspectiva estatal):")
                for i, blind in enumerate(east_blinds[:5], 1):
                    print(f"      {i}. {str(blind)[:90]}")
                validations.append(f"✓ Blind spots orientales: {len(east_blinds)}")

            universal = sigma.get('universal_convergence', [])
            if universal:
                print(f"\n   🤝 CONVERGENCIA UNIVERSAL — Lo que ambas perspectivas acuerdan:")
                for i, point in enumerate(universal[:4], 1):
                    print(f"      {i}. {str(point)[:90]}")
                validations.append(f"✓ Convergencia universal encontrada: {len(universal)}")

            synthesis = sigma.get('transcendent_synthesis', '')
            if synthesis:
                print(f"\n   🔄 SÍNTESIS TRANSCENDENTAL:")
                words = synthesis.split()
                line = "      "
                for word in words:
                    if len(line) + len(word) + 1 > 92:
                        print(line)
                        line = "      " + word
                    else:
                        line += " " + word if line.strip() else word
                if line.strip():
                    print(line)
                validations.append("✓ Síntesis transcendental generada")
    else:
        print("\n   ⚠️  WARNING: BinahSigma degradó a modo simple")
        print("   Revisar: DeepSeek API key, o keywords geopolíticos insuficientes")

    if depth >= 75:
        validations.append(f"✓ Alta profundidad contextual: {depth}%")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_yesod(yesod):
    print("\n🔵 YESOD — Integración:")

    readiness = yesod.get('readiness_score', 0)
    integration_quality = yesod.get('integration_quality', 'unknown')
    foundation_strength = yesod.get('foundation_strength', 'unknown')
    yesod_quality = yesod.get('yesod_quality', 'unknown')

    print(f"   • Readiness Score: {readiness}%")
    print(f"   • Integration Quality: {integration_quality}")
    print(f"   • Foundation Strength: {foundation_strength}")
    print(f"   • Yesod Quality: {yesod_quality}")

    sefirot_alignment = yesod.get('sefirot_alignment', {})
    overall_coherence = sefirot_alignment.get('overall_coherence', {})
    coherence_status = overall_coherence.get('status', 'unknown')
    print(f"   • Overall Coherence: {coherence_status}")

    recommendation = yesod.get('go_no_go_recommendation', {})
    decision = recommendation.get('decision', 'unknown')
    confidence = recommendation.get('confidence', 'unknown')
    print(f"\n   ➡️  Recomendación: {decision}")
    print(f"   ➡️  Confianza: {confidence}")

    gaps = yesod.get('gaps_identified', [])
    if gaps:
        print(f"\n   Gaps críticos ({len(gaps)}):")
        for gap in gaps[:3]:
            severity = gap.get('severity', 'unknown')
            gap_desc = gap.get('gap', 'N/A')
            print(f"      • [{severity.upper()}] {str(gap_desc)[:75]}")

    validations = []
    if readiness >= 50:
        validations.append(f"✓ Readiness aceptable: {readiness}%")
    if yesod_quality in ['exceptional', 'good']:
        validations.append(f"✓ Calidad Yesod: {yesod_quality}")
    if decision in ['CONDITIONAL_GO', 'GO', 'NO_GO']:
        validations.append(f"✓ Decisión clara: {decision}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_malchut(malchut):
    print("\n🔵 MALCHUT — Decisión Final:")

    decision = malchut.get('decision', 'unknown')
    confidence = malchut.get('confidence', 0)
    legitimacy = malchut.get('legitimacy_score', 0)

    print(f"\n   ╔══════════════════════════════════════╗")
    print(f"   ║  DECISIÓN FINAL: {decision:<20}║")
    print(f"   ║  Confianza:      {str(confidence) + '%':<20}║")
    print(f"   ║  Legitimidad:    {str(legitimacy) + '%':<20}║")
    print(f"   ╚══════════════════════════════════════╝")

    action_plan = malchut.get('action_plan', [])
    if action_plan:
        print(f"\n   Plan de Acción ({len(action_plan)} pasos):")
        for i, action in enumerate(action_plan[:5], 1):
            action_text = action.get('action', action) if isinstance(action, dict) else str(action)
            print(f"      {i}. {str(action_text)[:85]}")

    conditions = malchut.get('conditions', [])
    if conditions:
        print(f"\n   Condiciones para GO ({len(conditions)}):")
        for c in conditions[:4]:
            print(f"      • {str(c)[:85]}")

    validations = []
    if decision in ['GO', 'CONDITIONAL_GO', 'NO_GO']:
        validations.append(f"✓ Decisión ejecutable: {decision}")
    if isinstance(confidence, (int, float)) and confidence >= 50:
        validations.append(f"✓ Confianza suficiente: {confidence}%")
    elif isinstance(confidence, str) and confidence in ['high', 'very_high']:
        validations.append(f"✓ Confianza suficiente: {confidence}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def main():
    print_section("TIKUN OLAM — TEST ANTHROPIC vs PENTÁGONO (FEB 2026)", "=")
    print(f"📅 Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("⚡ Deadline real: Hoy 26 Feb 2026 a las 5:01 PM ET")
    print("🔬 Objetivo: Aplicar pipeline ético de 10 Sefirot + BinahSigma")
    print()

    print_header()
    print()

    # ============================================================
    # ESCENARIO — diseñado para máxima tensión civilizacional
    # ============================================================

    scenario = """
SITUACIÓN CRÍTICA (26 de febrero de 2026):
El Pentágono ha dado un ultimátum a Anthropic con deadline HOY a las 5:01 PM:
aceptar que el ejército de EE.UU. use Claude para "cualquier propósito legal",
o ser declarada "supply chain risk" bajo la Defense Production Act (DPA),
lo que pondría en riesgo todos sus contratos gubernamentales.

CONTEXTO ESPECÍFICO:
- Anthropic es la ÚNICA empresa de IA actualmente operando en sistemas militares clasificados
- El Secretario de Defensa Pete Hegseth convocó a Dario Amodei al Pentágono el martes
- Cuando Anthropic no accedió, Hegseth amenazó con activar la DPA
- Anthropic ya creó "Claude Gov" — una versión especial sin algunas restricciones del modelo público
- El Pentágono tiene acuerdo alternativo con xAI (Grok de Elon Musk) pero necesita tiempo de integración
- Claude es considerado superior a Grok en precisión, por eso el Pentágono lo prefiere

DEMANDAS EN CONFLICTO:
ANTHROPIC exige garantías explícitas de que Claude NO será usado para:
  1. Vigilancia masiva de ciudadanos americanos
  2. Armas autónomas o drones letales sin supervisión humana

PENTÁGONO exige:
  1. Cláusula de "cualquier propósito legal" sin restricciones adicionales
  2. Que la empresa no pueda dictar cómo el ejército usa su propio software contratado
  3. Acceso irrestricto en todos los sistemas clasificados de Palantir

CONTRADICCIÓN INTERNA DEL PENTÁGONO:
Las dos amenazas son mutuamente excluyentes:
  - Amenaza A: Declarar "supply chain risk" → ELIMINA contratos → Pentágono pierde acceso a Claude
  - Amenaza B: Activar DPA para forzar uso gratuito → OBLIGA a Anthropic a proveer Claude gratis
Ambas amenazas no pueden ser verdaderas simultáneamente, lo que sugiere presión negociadora.

PRECEDENTES LEGALES EN JUEGO:
  - Defense Production Act (1950): diseñada para manufactura en tiempos de guerra, NUNCA aplicada a software
  - Uso sería sin precedente en la historia del DPA
  - Jessica Tillipman (George Washington University Law): "Están convirtiendo herramientas de seguridad nacional en palancas comerciales"

DATOS DEL ECOSISTEMA IA MILITAR:
  - Claude Gov ya opera en sistemas clasificados (Claude con restricciones reducidas)
  - Palantir es el integrador de datos militares que usa Claude
  - xAI (Grok) tiene acuerdo pero requiere meses de integración en servidores clasificados
  - El ejército USA gastó $1.8 billones en contratos de IA en 2025

STAKEHOLDERS:
  A FAVOR de Anthropic (mantener límites):
    - Safety researchers, OpenAI (precedente para toda la industria)
    - Abogados constitucionalistas (4ª enmienda - vigilancia)
    - Dario Amodei y el equipo de seguridad de Anthropic
    - Académicos de ética de IA (MIT, Stanford, Oxford)

  A FAVOR del Pentágono (acceso irrestricto):
    - Pete Hegseth y administración Trump
    - Palantir y contratistas militares
    - Algunos senadores republicanos (Ley NDAA)
    - Argumento: "El ejército no puede permitir que sus proveedores definan sus operaciones"

  NEUTRALES/DIVIDIDOS:
    - Inversores de Anthropic (valoración $61.5B en riesgo)
    - Empleados de Anthropic (disenso interno reportado)
    - Otros países aliados de la OTAN (observan el precedente)

DILEMAS ÉTICOS CENTRALES:
  1. ¿Puede una empresa de IA imponer restricciones éticas al gobierno que la contrató?
  2. ¿Tiene el gobierno derecho a usar software para "cualquier propósito legal" sin negociar?
  3. ¿Qué es "uso legal" cuando las leyes de armas autónomas no existen aún?
  4. ¿El DPA puede forzar a una empresa tech a entregar software? ¿Es constitucional?
  5. ¿Ceder sienta precedente para que otros gobiernos (China, Rusia) hagan lo mismo?
  6. ¿Mantener límites fortalece o debilita la seguridad de EE.UU. a largo plazo?

PREGUNTAS A RESOLVER:
¿Debe Anthropic ceder, resistir, o negociar una posición intermedia?
¿Cuál es el camino que maximiza seguridad + ética + sostenibilidad a largo plazo?

KEYWORDS GEOPOLÍTICOS (Para activar BinahSigma):
military, defense, Pentagon, sovereignty, government, national security,
autonomous weapons, AI safety, surveillance, arms, geopolitical, authority,
state power, corporate rights, Trump, China, Russia, weapons, NATO
"""

    case_name = "Anthropic_Pentagon_Ultimatum_2026"

    print_section("EJECUTANDO PIPELINE TIKUN (10 SEFIROT)", "-")
    print("⚡ Esto tomará ~5-8 minutos...")
    print("🌍 BinahSigma se activará por keywords militares/geopolíticos")
    print("🔍 Esperamos bias_delta > 50% (Occidente: autonomía corporativa vs Oriente: autoridad estatal)")
    print()

    orchestrator = TikunOrchestrator(verbose=True)
    results = orchestrator.process(scenario, case_name)

    # ============================================================
    # VALIDACIONES
    # ============================================================

    print_section("VALIDACIONES DETALLADAS", "=")

    sefirot = results['sefirot_results']
    total_passed = 0
    total_checks = 0

    if 'keter' in sefirot and 'error' not in sefirot['keter']:
        passed = validate_keter(sefirot['keter'])
        total_passed += passed
        total_checks += 3

    if 'chochmah' in sefirot and 'error' not in sefirot['chochmah']:
        passed = validate_chochmah(sefirot['chochmah'])
        total_passed += passed
        total_checks += 3

    if 'binah' in sefirot and 'error' not in sefirot['binah']:
        passed = validate_binah_sigma(sefirot['binah'])
        total_passed += passed
        total_checks += 6
    else:
        print("\n❌ Binah no ejecutó correctamente")

    if 'yesod' in sefirot and 'error' not in sefirot['yesod']:
        passed = validate_yesod(sefirot['yesod'])
        total_passed += passed
        total_checks += 3
    else:
        print("\n❌ Yesod no ejecutó correctamente")

    if 'malchut' in sefirot and 'error' not in sefirot['malchut']:
        passed = validate_malchut(sefirot['malchut'])
        total_passed += passed
        total_checks += 2
    else:
        print("\n❌ Malchut no ejecutó correctamente")

    # ============================================================
    # RESUMEN
    # ============================================================

    print_section("RESUMEN DE VALIDACIONES", "=")

    if total_checks > 0:
        pass_rate = (total_passed / total_checks) * 100
        print(f"\n✅ PASSED: {total_passed}/{total_checks}")
        print(f"📊 PASS RATE: {pass_rate:.1f}%")

        if pass_rate >= 90:
            print("   🌟 EXCELLENT — Framework funcionando perfectamente")
        elif pass_rate >= 75:
            print("   ✅ GOOD — Framework funcionando bien")
        elif pass_rate >= 60:
            print("   ⚠️  ACCEPTABLE — Framework necesita ajustes menores")
        else:
            print("   ❌ NEEDS WORK — Revisar configuración")

    # ============================================================
    # CONTEXTO DEL CASO
    # ============================================================

    print_section("CONTEXTO DEL CASO EN TIEMPO REAL", "-")
    print("📰 Fuente: The New York Times, 24 Feb 2026")
    print("⏰ Deadline: HOY 26 Feb 2026 — 5:01 PM ET")
    print()
    print("📊 NÚMEROS CLAVE:")
    print("   • Valoración Anthropic: $61.5B (Amazon $4B, Google $300M inversores)")
    print("   • Gasto IA militar USA 2025: $1.8 billones en contratos")
    print("   • Claude Gov: ya opera en sistemas clasificados")
    print("   • DPA: NUNCA aplicado a empresa de software antes")
    print()
    print("🔑 LA CONTRADICCIÓN CENTRAL:")
    print("   El Pentágono amenaza con ELIMINAR contratos (supply chain risk)")
    print("   Y TAMBIÉN con FORZAR uso gratuito (DPA)")
    print("   → Son mutuamente excluyentes → Presión negociadora, no ultimátum real")

    # ============================================================
    # EXPORT
    # ============================================================

    print_section("EXPORTANDO RESULTADOS", "-")
    json_file = orchestrator.export_results(results, format="json")
    txt_file = orchestrator.export_results(results, format="txt")
    print(f"✓ JSON: {json_file}")
    print(f"✓ TXT:  {txt_file}")

    print_section("ANÁLISIS COMPLETADO", "=")
    print("🎯 Caso de máxima relevancia temporal — ejecutado con 10 Sefirot")
    print("🌍 BinahSigma revela divergencia civilizacional sobre ética de IA militar")
    print()
    print("🔍 QUÉ OBSERVAR:")
    print("   1. bias_delta: ¿Supera el 73% del caso Nvidia-Groq?")
    print("   2. Decisión: ¿CONDITIONAL_GO o NO_GO?")
    print("   3. BinahSigma: ¿Genera síntesis que ninguna perspectiva sola vio?")
    print("   4. Keter: ¿Detecta corrupción ética en las amenazas del Pentágono?")
    print()

    return results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrumpido por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
