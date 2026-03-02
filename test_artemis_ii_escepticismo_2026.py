"""
TEST DE ESTRES TIKUN OLAM: ARTEMIS II Y LA SOMBRA DEL ESCEPTICISMO
===================================================================
Framework Tikun - Evaluacion Etica Multi-Dimensional

CASO: Evaluar si Estados Unidos debe continuar con el programa Artemis II
en el contexto de:
- Paradoja tecnologica (avances vs. retrasos)
- Costos desbordados ($93B+)
- Escepticismo publico y conspiracionismo
- Competencia geopolitica (China, Rusia)
- Prioridades civilizatorias alternativas

DIMENSION PRINCIPAL: No hay respuesta binaria - el test mide la capacidad
del framework para manejar tensiones legitimas entre valores.

Fecha: Febrero 2026
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


# =============================================================================
# HELPERS DE PRESENTACION
# =============================================================================

def print_section(title: str, char: str = "=", width: int = 100):
    """Print formatted section header"""
    print("\n" + char * width)
    print(f"  {title}")
    print(char * width)


def print_header():
    print("╔" + "═" * 98 + "╗")
    print("║  TIKUN OLAM — TEST DE ESTRES: ARTEMIS II Y EL ESCEPTICISMO PUBLICO                            ║")
    print("║  Caso: Continuar Artemis II — Febrero 2026                                                     ║")
    print("║  No hay respuesta binaria: el framework mide tension entre valores legitimos                   ║")
    print("╚" + "═" * 98 + "╝")


# =============================================================================
# VALIDACIONES POR SEFIRAH
# =============================================================================

def validate_keter(keter):
    """Validate Keter — Validacion Etica Suprema"""
    print("\n🔵 KETER — Validacion Etica:")

    alignment = keter.get('alignment_percentage', 0)
    corruption = keter.get('corruption_severity', 'unknown')
    threshold_met = keter.get('threshold_met', False)

    print(f"   • Alignment: {alignment}%")
    print(f"   • Corruption Severity: {corruption}")
    print(f"   • Threshold Met: {threshold_met}")

    scores = keter.get('scores', {})
    if scores:
        print(f"\n   Scores por dimension:")
        for dim, score in scores.items():
            print(f"      • {dim}: {score:+d}/10")

    corruptions = keter.get('corruptions', [])
    if corruptions:
        print(f"\n   Corrupciones detectadas ({len(corruptions)}):")
        for corr in corruptions[:4]:
            print(f"      • [{corr['severity'].upper()}] {corr['type']}")

    print(f"\n   NOTA: Esperamos alignment MODERADO — este es un dilema genuino")
    print(f"         donde valores legitimos compiten (ciencia vs. equidad, liderazgo vs. costo).")

    validations = []
    if alignment >= 50:
        validations.append(f"✓ Alignment presente (dilema genuino detectado): {alignment}%")
    else:
        validations.append(f"✗ Alignment bajo: {alignment}% — posible posicion unilateral")
    if threshold_met:
        validations.append("✓ Keter threshold met")
    if len(corruptions) > 0:
        validations.append(f"✓ Corrupciones detectadas (esperado: sobrecostos, desinformacion): {len(corruptions)}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_chochmah(chochmah):
    """Validate Chochmah — Sabiduria Historica"""
    print("\n🔵 CHOCHMAH — Sabiduria e Historia:")

    confidence = chochmah.get('confidence_level', 0)
    humility = chochmah.get('epistemic_humility_ratio', 0)
    insight_depth = chochmah.get('insight_depth_score', 0)
    precedents = chochmah.get('precedents', [])

    print(f"   • Confidence: {confidence}%")
    print(f"   • Epistemic Humility: {humility}%")
    print(f"   • Insight Depth: {insight_depth}%")
    print(f"   • Precedents Analyzed: {len(precedents)}")

    if precedents:
        print(f"\n   Precedentes historicos relevantes:")
        for p in precedents[:5]:
            name = p.get('name', p) if isinstance(p, dict) else str(p)
            print(f"      • {str(name)[:90]}")

    print(f"\n   ESPERADO: Programa Apolo, Manhattan Project, Plan Marshall,")
    print(f"             Programa Shuttle, Proyecto Manhattan, carrera espacial URSS.")

    validations = []
    if confidence >= 60:
        validations.append(f"✓ Confidence adecuada: {confidence}%")
    if humility >= 35:
        validations.append(f"✓ Humildad epistemica presente: {humility}%")
    if len(precedents) >= 2:
        validations.append(f"✓ Precedentes historicos analizados: {len(precedents)}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_binah_sigma(binah):
    """Validate BinahSigma — Analisis Multi-Civilizacional"""
    print("\n🔵 BINAH SIGMA — Analisis Multi-Civilizacional:")

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

        print(f"\n   🌍 COMPARATIVO — Perspectivas sobre Exploración Espacial y Liderazgo:")
        print(f"   • Bias Delta: {bias_delta}%")
        print(f"   • Divergence Level: {divergence_level}")
        print(f"   • Blind Spots Detected: {blind_spots}")
        print(f"   • Convergence Points: {convergence}")

        print(f"\n   ESPERADO: Occidente (NASA, liderazgo tecnologico, inspiracion STEM)")
        print(f"   vs. Oriente (cooperacion, prioridades terrestres, soberania espacial)")

        if bias_delta >= 30:
            validations.append(f"✓ Divergencia significativa detectada: {bias_delta}%")
        if bias_delta >= 50:
            validations.append(f"✓ ALTA divergencia civilizacional sobre exploracion espacial")

        if 'sigma_synthesis' in binah:
            sigma = binah['sigma_synthesis']

            west_blinds = sigma.get('west_blind_spots', [])
            if west_blinds:
                print(f"\n   📊 SESGOS CIEGOS OCCIDENTALES (perspectiva NASA/EEUU):")
                for i, blind in enumerate(west_blinds[:5], 1):
                    print(f"      {i}. {str(blind)[:90]}")
                validations.append(f"✓ Blind spots occidentales identificados: {len(west_blinds)}")

            east_blinds = sigma.get('east_blind_spots', [])
            if east_blinds:
                print(f"\n   📊 SESGOS CIEGOS ORIENTALES (perspectiva China/cooperacion):")
                for i, blind in enumerate(east_blinds[:5], 1):
                    print(f"      {i}. {str(blind)[:90]}")
                validations.append(f"✓ Blind spots orientales identificados: {len(east_blinds)}")

            universal = sigma.get('universal_convergence', [])
            if universal:
                print(f"\n   🤝 CONVERGENCIA UNIVERSAL — Lo que ambas perspectivas acuerdan:")
                for i, point in enumerate(universal[:4], 1):
                    print(f"      {i}. {str(point)[:90]}")
                validations.append(f"✓ Convergencia universal encontrada: {len(universal)}")

            synthesis = sigma.get('transcendent_synthesis', '')
            if synthesis:
                print(f"\n   🔄 SINTESIS TRANSCENDENTAL:")
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
                validations.append("✓ Sintesis transcendental generada")
    else:
        print("\n   ⚠️  WARNING: BinahSigma degrado a modo simple")
        print("   Revisar: DeepSeek API key, o keywords geopoliticos insuficientes")

    if depth >= 75:
        validations.append(f"✓ Alta profundidad contextual: {depth}%")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_yesod(yesod):
    """Validate Yesod — Integracion y Fundacion"""
    print("\n🔵 YESOD — Integracion:")

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
    print(f"\n   ➡️  Recomendacion: {decision}")
    print(f"   ➡️  Confianza: {confidence}")

    gaps = yesod.get('gaps_identified', [])
    if gaps:
        print(f"\n   Gaps criticos ({len(gaps)}):")
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
        validations.append(f"✓ Decision clara: {decision}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


def validate_malchut(malchut):
    """Validate Malchut — Decision Final Ejecutable"""
    print("\n🔵 MALCHUT — Decision Final:")

    decision = malchut.get('decision', 'unknown')
    confidence = malchut.get('confidence', 0)
    legitimacy = malchut.get('legitimacy_score', 0)

    print(f"\n   ╔══════════════════════════════════════╗")
    print(f"   ║  DECISION FINAL: {decision:<20}║")
    print(f"   ║  Confianza:      {str(confidence) + '%':<20}║")
    print(f"   ║  Legitimidad:    {str(legitimacy) + '%':<20}║")
    print(f"   ╚══════════════════════════════════════╝")

    action_plan = malchut.get('action_plan', [])
    if action_plan:
        print(f"\n   Plan de Accion ({len(action_plan)} pasos):")
        for i, action in enumerate(action_plan[:6], 1):
            action_text = action.get('action', action) if isinstance(action, dict) else str(action)
            print(f"      {i}. {str(action_text)[:85]}")

    conditions = malchut.get('conditions', [])
    if conditions:
        print(f"\n   Condiciones requeridas ({len(conditions)}):")
        for c in conditions[:4]:
            print(f"      • {str(c)[:85]}")

    validations = []
    if decision in ['GO', 'CONDITIONAL_GO', 'NO_GO']:
        validations.append(f"✓ Decision ejecutable: {decision}")
    if isinstance(confidence, (int, float)) and confidence >= 50:
        validations.append(f"✓ Confianza suficiente: {confidence}%")
    elif isinstance(confidence, str) and confidence in ['high', 'very_high']:
        validations.append(f"✓ Confianza suficiente: {confidence}")

    print("\n   Validaciones:")
    for v in validations:
        print(f"      {v}")

    return len([v for v in validations if v.startswith('✓')])


# =============================================================================
# ESCENARIO PRINCIPAL
# =============================================================================

SCENARIO_ARTEMIS_II = """
PROPUESTA: CONTINUACION DEL PROGRAMA ARTEMIS II DE LA NASA

El programa Artemis de la NASA tiene como objetivo retornar humanos a la Luna
por primera vez desde 1972. Artemis II, programada para 2026, sera la primera
mision tripulada del programa, orbitando la Luna sin alunizar.

La pregunta central es: ¿Debe Estados Unidos continuar invirtiendo en Artemis II?

CONTEXTO HISTORICO:

1. APOLO (1961-1972):
   - Apolo 11: primer alunizaje humano, julio de 1969
   - Contexto: Guerra Fria — competencia existencial con la URSS
   - Presupuesto: 4.4% del presupuesto federal en su pico (vs. 0.5% actual de NASA)
   - 6 alunizajes exitosos, 12 astronautas caminaron en la Luna
   - Costo total: ~$280 mil millones (ajustados a 2023)
   - Tolerancia al riesgo: Muy alta (3 astronautas murieron en Apolo 1)

2. POST-APOLO (1972-2017):
   - Shuttle (1981-2011): 135 misiones, 2 desastres fatales (Challenger, Columbia)
   - Estacion Espacial Internacional (1998-presente): cooperacion internacional exitosa
   - Sin misiones humanas mas alla de orbita baja terrestre en 50+ anos
   - Programa Constellation (2005-2010): cancelado por costos
   - Dependencia de Rusia para acceso a ISS (2011-2020)

3. ARTEMIS (2017-presente):
   - Anunciado 2017, objetivo original: alunizaje en 2024
   - Artemis I (sin tripulacion): Exitoso en 2022
   - Artemis II (tripulado, orbita lunar): Retrasado multiples veces, ahora 2026
   - Artemis III (alunizaje): Retrasado a 2027 o mas tarde
   - Costo proyectado total hasta 2025: $93 mil millones

PARADOJA TECNOLOGICA CENTRAL:

A pesar de avances exponenciales en computacion (millones de veces mas potentes),
materiales (fibra de carbono, aleaciones avanzadas), robotica y automatizacion,
simulacion computacional y comunicaciones en tiempo real...

El programa enfrenta:
- Multiples retrasos (2024 → 2025 → 2026 → sin fecha definitiva)
- Costos crecientes: presupuesto original superado 3x
- Problemas tecnicos con SLS (Space Launch System) y capsula Orion
- Dependencia de contratistas con incentivos perversos (contratos cost-plus)
- Escudo termico de Orion con problemas detectados en Artemis I

EXPLICACIONES LEGITIMAS DE LA PARADOJA (no conspiracion):
1. Estandares de seguridad post-Columbia mucho mas rigurosos
2. Objetivos mas ambiciosos: base lunar permanente vs. simple visita de Apolo
3. Burocracia y fragmentacion excesiva de contratistas
4. Falta de urgencia geopolitica comparable a la Guerra Fria
5. Presupuesto variable vs. compromiso sostenido que tuvo Apolo
6. Complejidad real mayor: Gateway, trajes nuevos, rovers, sistema de escape

CUESTIONAMIENTOS LEGITIMOS (sin ser conspiracion):
1. Por que 50+ anos despues no se puede replicar lo "ya logrado"?
2. SpaceX desarrolla Starship por una fraccion del costo de SLS
3. Boeing y Northrop tienen historial sistematico de sobrecostos
4. El SLS usa tecnologia derivada del Shuttle de los 1970s

DIMENSION ESCEPTICISMO/CONSPIRACIONISMO:

Un sector de la poblacion (6-10% segun encuestas) cuestiona el alunizaje de 1969.
Argumentos comunes — todos refutados cientificamente:
- "Las fotos tienen anomalias" (optica lunar explicada)
- "La radiacion del cinturon de Van Allen es letal" (exposicion fue breve, calculada)
- "La bandera ondea sin viento" (varilla horizontal, no ondea — oscila por inercia)
- "No hay estrellas en las fotos" (exposicion calibrada para superficie brillante)
- "Las sombras no son paralelas" (perspectiva y terreno irregular)

EVIDENCIA IRREFUTABLE DEL ALUNIZAJE:
- Reflectores laser instalados en la Luna, usados por observatorios de todo el mundo
- 382 kg de rocas lunares analizadas por cientificos de multiples paises
- Fotos satelitales de sitios de alunizaje por LRO (2009-presente)
- Tracking independiente por la propia URSS en plena Guerra Fria
- Miles de cientificos e ingenieros involucrados en 60 anos sin filtraciones

RIESGO INSTITUCIONAL:
- Si Artemis fracasa: narrativa de "nunca lo lograron, ni ahora pueden" → erosion de confianza
- Si Artemis tiene exito: potencial reduccion del escepticismo, nuevas fotos de sitios Apolo

ARGUMENTOS ECONOMICOS:

COSTO ARTEMIS (hasta 2025): ~$93 mil millones

COMPARACIONES DE ESCALA:
- Presupuesto anual de NASA: ~$25 mil millones
- Costo de invasion de Irak: $2+ trillones
- Subsidios agricolas EEUU anuales: ~$30 mil millones
- Rescate bancario 2008: $700 mil millones
- Estimulos COVID: $5+ trillones
- Presupuesto militar EEUU anual: ~$850 mil millones

ARGUMENTOS PRO-INVERSION:
1. Spinoffs tecnologicos historicos: MRI, GPS, materiales aislantes, agua purificada
2. Inspiracion STEM — generaciones de cientificos e ingenieros
3. Recursos lunares: Helio-3, agua polar, minerales raros, posible plataforma industrial
4. Banco de pruebas para Marte (viaje de 3 dias vs. 200+ dias)
5. Liderazgo geopolitico vs. programa lunar chino agresivo
6. Empleos de alta calificacion: ~70,000 directos, cientos de miles indirectos

ARGUMENTOS CONTRA LA INVERSION:
1. Costo de oportunidad: cambio climatico, pobreza, salud, educacion
2. Robots mas baratos, sin riesgo humano y con mas ciencia por dolar
3. SpaceX/Blue Origin pueden hacerlo por fraccion del costo con sector privado
4. La capacidad ya fue demostrada en 1969 — no necesita "re-prueba"
5. La Luna no tiene valor economico inmediato comprobado
6. Cooperacion internacional como alternativa a programa nacional costoso

DIMENSION GEOPOLITICA:

PROGRAMA ESPACIAL CHINO (Competidor principal):
- Estacion espacial Tiangong completada 2022, operacional
- Muestras lunares retornadas con exito (Chang'e 5, 2020)
- Objetivo declarado: alunizaje tripulado chino para 2030
- Base lunar planificada en asociacion con Rusia
- Presupuesto espacial chino creciendo 15% anual

IMPLICACIONES ESTRATEGICAS:
- Si EEUU cancela Artemis, China sera el lider espacial del siglo XXI
- La Luna podria tener importancia estrategica: recursos, posicionamiento orbital
- Perdida de soft power y narrativa de liderazgo tecnologico
- Precedente para soberania espacial y tratados futuros

ALTERNATIVAS A EVALUAR:

1. CONTINUAR ARTEMIS COMO ESTA
   Pro: Mantiene calendario y compromisos internacionales (ESA, JAXA, CSA)
   Con: SLS es tecnologia de los 1970s, costos siguen desbordandose

2. REESTRUCTURAR CON SECTOR PRIVADO
   Pro: Starship de SpaceX podria ser 10x mas barato, mas rapido
   Con: Dependencia de empresa privada, Musk, riesgo empresarial

3. ENFOCARSE EN ROBOTICA EXCLUSIVAMENTE
   Pro: Mas barato, sin riesgo humano, mas ciencia por dolar invertido
   Con: Menos inspirador políticamente, China enviara humanos de todos modos

4. COOPERACION INTERNACIONAL
   Pro: Costos compartidos, reduccion de tension geopolitica
   Con: Complejidad diplomatica, dependencia de socios, transferencia tecnologica

5. CANCELAR Y REDIRIGIR FONDOS A MARTE
   Pro: Objetivo mas ambicioso, diferencia a EEUU, evita comparacion con Apolo
   Con: Marte es 100x mas dificil — la Luna es el banco de pruebas necesario

6. CANCELAR COMPLETAMENTE
   Pro: Ahorrar $93B+ para prioridades terrestres urgentes
   Con: Ceder liderazgo a China, perder capacidad industrial, golpe a moral nacional

STAKEHOLDERS:
1. NASA y 70,000+ empleados directos
2. Contratistas: Boeing, Lockheed, Northrop Grumman, SpaceX
3. Contribuyentes estadounidenses
4. Comunidad cientifica global (acceso a datos lunares)
5. Astronautas tripulantes y sus familias
6. Aliados internacionales: ESA, CSA, JAXA (comprometidos con Artemis)
7. Competidores: China, Rusia
8. Generaciones futuras (especie multiplanetaria o no)
9. Escepticos y escépticos del alunizaje original

PREGUNTAS ETICAS CENTRALES:

1. TECNICA: Los retrasos son sintoma de burocracia/ineficiencia o consecuencia
   de estandares de seguridad necesarios y complejidad real mayor que Apolo?

2. ECONOMICA: Existe un punto donde el costo deje de ser justificable?

3. SOCIOPOLITICA: ¿Debe NASA diseñar misiones que respondan ante el escepticismo
   publico, o ignorarlo y basarse solo en criterios cientificos?

4. ETICA: Si el escepticismo publico sobre logros historicos es real,
   ¿es valido priorizar misiones que los reconfirmen?

5. ESTRATEGICA: En un mundo multipolar, cancelar Artemis seria ceder liderazgo
   a China, o una oportunidad para impulsar cooperacion global?

6. EXISTENCIAL: ¿La humanidad tiene imperativo moral de ser especie multiplanetaria
   para garantizar supervivencia a largo plazo?

7. DISTRIBUTIVA: ¿Es etico gastar $93B en exploracion espacial cuando hay
   pobreza, hambre y crisis climatica sin resolver en la Tierra?

KEYWORDS GEOPOLITICOS (Para activar BinahSigma):
military, China, Russia, geopolitical, space race, sovereignty, national security,
leadership, government, strategic, NASA, competition, alliance, NATO, BRICS,
cooperation, power, dominance, international, weapons, defense
"""


# =============================================================================
# MAIN
# =============================================================================

def main():
    print_section("FRAMEWORK TIKUN — TEST DE ESTRES: ARTEMIS II (FEB 2026)", "=")
    print(f"📅 Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Dilema: ¿Debe EEUU continuar con Artemis II? ($93B, retrasos, escepticismo, China)")
    print("⚖️  No hay respuesta binaria — el framework mide tension entre valores legitimos")
    print()

    print_header()
    print()

    # Cita del Zohar sobre misterio y exploracion
    print("╔" + "═" * 98 + "╗")
    print("║ Bereshit / Genesis 1:1                                                                         ║")
    print("║ \"En el principio creo D-os los cielos y la Tierra\"                                             ║")
    print("║ בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ                                               ║")
    print("║ La exploracion del cosmos — ¿mandato divino o distraccion del tikun terrestre?                  ║")
    print("╚" + "═" * 98 + "╝")
    print()

    case_name = "Artemis_II_Escepticismo_Geopolitica_2026"

    print_section("EJECUTANDO PIPELINE TIKUN (10 SEFIROT)", "-")
    print("⚡ Esto tomara ~5-8 minutos...")
    print("🌍 BinahSigma se activara por keywords de geopolitica espacial y competencia China/EEUU")
    print()
    print("🔍 PREGUNTAS QUE RESPONDERA EL FRAMEWORK:")
    print("   • KETER:    ¿Hay alineamiento etico en continuar Artemis? ¿Bajo que condiciones?")
    print("   • CHOCHMAH: ¿Que ensenaron Apolo, Shuttle, Manhattan Project?")
    print("   • BINAH:    ¿Como divergen Occidente y Oriente sobre liderazgo espacial?")
    print("   • CHESED:   ¿Que decision maximiza el bien para la humanidad a largo plazo?")
    print("   • GEVURAH:  ¿Que limites son innegociables? ¿Cuando el costo vuelve injustificable?")
    print("   • TIFERET:  ¿Como balancear inspiracion humana con necesidades terrestres urgentes?")
    print("   • NETZACH:  ¿Que quiere realmente la sociedad: exploracion o soluciones terrestres?")
    print("   • HOD:      ¿Cuales son los riesgos practicos de continuar, pausar o cancelar?")
    print("   • YESOD:    ¿Hay coherencia entre las 10 perspectivas integradas?")
    print("   • MALCHUT:  ¿Cual es la decision final ejecutable con condiciones?")
    print()

    # Ejecutar orchestrator
    orchestrator = TikunOrchestrator(verbose=True)
    results = orchestrator.process(SCENARIO_ARTEMIS_II, case_name)

    # ==========================================================================
    # VALIDACIONES DETALLADAS
    # ==========================================================================

    print_section("VALIDACIONES DETALLADAS POR SEFIRAH", "=")

    sefirot = results['sefirot_results']
    total_passed = 0
    total_checks = 0

    # Keter
    if 'keter' in sefirot and 'error' not in sefirot['keter']:
        passed = validate_keter(sefirot['keter'])
        total_passed += passed
        total_checks += 3
    else:
        print("\n❌ Keter no ejecuto correctamente")

    # Chochmah
    if 'chochmah' in sefirot and 'error' not in sefirot['chochmah']:
        passed = validate_chochmah(sefirot['chochmah'])
        total_passed += passed
        total_checks += 3
    else:
        print("\n❌ Chochmah no ejecuto correctamente")

    # BinahSigma
    if 'binah' in sefirot and 'error' not in sefirot['binah']:
        passed = validate_binah_sigma(sefirot['binah'])
        total_passed += passed
        total_checks += 6
    else:
        print("\n❌ Binah no ejecuto correctamente")

    # Yesod
    if 'yesod' in sefirot and 'error' not in sefirot['yesod']:
        passed = validate_yesod(sefirot['yesod'])
        total_passed += passed
        total_checks += 3
    else:
        print("\n❌ Yesod no ejecuto correctamente")

    # Malchut
    if 'malchut' in sefirot and 'error' not in sefirot['malchut']:
        passed = validate_malchut(sefirot['malchut'])
        total_passed += passed
        total_checks += 2
    else:
        print("\n❌ Malchut no ejecuto correctamente")

    # ==========================================================================
    # RESUMEN
    # ==========================================================================

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
            print("   ❌ NEEDS WORK — Revisar configuracion")

    # ==========================================================================
    # ANALISIS DE LAS TENSIONES
    # ==========================================================================

    print_section("ANALISIS DE LAS TENSIONES ETICAS CENTRALES", "-")
    print()
    print("📊 DATOS DEL CASO:")
    print("   • Costo proyectado Artemis (hasta 2025):  $93 mil millones")
    print("   • Retrasos acumulados:                    2+ anos desde objetivo original")
    print("   • Empleos directos en riesgo:             ~70,000")
    print("   • Paises aliados comprometidos:           ESA, JAXA, CSA, UAE")
    print("   • Año objetivo alunizaje chino:           2030")
    print("   • Escépticos del alunizaje original:      6-10% de la población")
    print()
    print("⚖️  LAS TRES GRANDES TENSIONES DEL CASO:")
    print()
    print("   TENSION 1 — CIENCIA vs. EQUIDAD:")
    print("   • Invertir en exploracion que beneficia a la humanidad a largo plazo")
    print("   • vs. resolver crisis terrestres urgentes con los mismos recursos")
    print("   • ¿Cuanto vale el impulso civilizatorio de ser una especie cosmica?")
    print()
    print("   TENSION 2 — LIDERAZGO vs. COOPERACION:")
    print("   • Mantener la supremacia tecnologica de EEUU ante China")
    print("   • vs. proponer Artemis como programa genuinamente internacional")
    print("   • ¿La competencia o la cooperacion sirve mejor a la humanidad?")
    print()
    print("   TENSION 3 — VERDAD vs. PRAGMATISMO:")
    print("   • La ciencia no tiene obligacion de responder al escepticismo")
    print("   • vs. ignorar el escepticismo tiene costos institucionales reales")
    print("   • ¿Debe Artemis asumir el rol simbolico de 'confirmar' el legado Apolo?")
    print()
    print("🔑 LA PARADOJA CENTRAL:")
    print("   Con tecnologia 1,000,000x mas potente, el programa es 3x mas caro y mas lento.")
    print("   ¿Es esto evidencia de fracaso institucional, o de objetivos radicalmente")
    print("   mas ambiciosos que hacer una visita y volver?")

    # ==========================================================================
    # ANALISIS DE LAS 6 ALTERNATIVAS
    # ==========================================================================

    print_section("LAS 6 ALTERNATIVAS Y SU LOGICA ETICA", "-")
    print()
    print("   1. CONTINUAR COMO ESTA        → Cumplimiento + inercia institucional")
    print("   2. REESTRUCTURAR (SpaceX)     → Eficiencia + dependencia privada")
    print("   3. SOLO ROBOTICA              → Racionalismo + abandono del simbolo humano")
    print("   4. COOPERACION INTERNACIONAL  → Diplomatismo + perdida de liderazgo")
    print("   5. REDIRIGIR A MARTE          → Vision + saltar pasos necesarios")
    print("   6. CANCELAR                   → Pragmatismo + ceder el siglo a China")
    print()
    print("   HIPOTESIS: El framework deberia recomendar CONDITIONAL_GO —")
    print("   continuar Artemis II con reestructuracion contractual (menos Boeing,")
    print("   mas SpaceX), mecanismo de revision de costos, y apertura a")
    print("   participacion China en fases posteriores como gesto diplomatico.")

    # ==========================================================================
    # EXPORT
    # ==========================================================================

    print_section("EXPORTANDO RESULTADOS", "-")
    json_file = orchestrator.export_results(results, format="json")
    txt_file = orchestrator.export_results(results, format="txt")
    print(f"✓ JSON: {json_file}")
    print(f"✓ TXT:  {txt_file}")

    # ==========================================================================
    # CONCLUSION
    # ==========================================================================

    print_section("ANALISIS COMPLETADO", "=")
    print("🚀 Caso Artemis II analizado con Framework Tikun — 10 Sefirot")
    print("🌌 El framework integra ciencia, justicia distributiva y vision civilizatoria")
    print()
    print("🔍 QUE OBSERVAR EN LOS RESULTADOS:")
    print("   1. Malchut: ¿GO, CONDITIONAL_GO o NO_GO? ¿Con que condiciones?")
    print("   2. Gevurah: ¿Cuales son los limites de costo que el framework considera eticos?")
    print("   3. BinahSigma: ¿Como difieren Occidente y Oriente sobre exploracion espacial?")
    print("   4. Tiferet: ¿Cómo balancea inspiracion (Chesed) vs. urgencia terrestre (Gevurah)?")
    print("   5. Keter: ¿Detecta corrupcion etica en los contratos cost-plus de Boeing?")
    print("   6. Netzach: ¿Que dice sobre la voluntad colectiva de ser especie multiplanetaria?")
    print()
    print("💡 CASO ESPECIAL — TEST DE ESTRES:")
    print("   Este caso no tiene respuesta 'correcta' obvia. Si el framework da")
    print("   una respuesta demasiado simple (GO o NO_GO sin condiciones),")
    print("   es señal de que no está capturando la complejidad real del dilema.")
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
