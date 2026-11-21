#!/usr/bin/env python3
"""Generates index.html (English) and es/index.html (Spanish) from one template.

  python3 build.py

Edit the texts in EN and ES below, then run it. Both pages share the structure, so they stay
in step. sitemap.xml is generated too.
"""
import html
import json
import os

BASE = 'https://fmrico.github.io/book_pddl_web/'
AUTHOR_URL = 'https://servicios.urjc.es/pdi/ver/francisco.rico'
LAB_URL = 'https://intelligentroboticslab.gsyc.urjc.es/'
KAIROS_URL = 'https://github.com/PlanSys2/kairos'
LICENSE_URL = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
VERSION = '0.1.0'
UPDATED = '2026-11-21'

DOMAIN = """(define (domain courier)
  (:requirements :strips :typing)
  (:types robot location item)
  (:predicates
    (connected ?from ?to - location)
    (robot-at ?r - robot ?l - location)
    (item-at ?i - item ?l - location)
    (carrying ?r - robot ?i - item)
    (free ?r - robot))

  (:action move
    :parameters (?r - robot ?from ?to - location)
    :precondition (and (robot-at ?r ?from) (connected ?from ?to))
    :effect (and (not (robot-at ?r ?from))
                 (robot-at ?r ?to)))

  (:action pick
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and (robot-at ?r ?l) (item-at ?i ?l) (free ?r))
    :effect (and (not (item-at ?i ?l)) (not (free ?r))
                 (carrying ?r ?i)))

  (:action drop
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and (robot-at ?r ?l) (carrying ?r ?i))
    :effect (and (not (carrying ?r ?i))
                 (item-at ?i ?l) (free ?r))))"""

PROBLEM = """(define (problem courier-p01)
  (:domain courier)
  (:objects
    r1 - robot
    lobby corridor pharmacy lab ward-a ward-b icu dock - location
    meds1 - item)
  (:init
    (connected lobby corridor) (connected corridor lobby)
    (connected lobby pharmacy) (connected pharmacy lobby)
    (connected lobby dock) (connected dock lobby)
    (connected corridor lab) (connected lab corridor)
    (connected corridor ward-a) (connected ward-a corridor)
    (connected corridor ward-b) (connected ward-b corridor)
    (connected ward-b icu) (connected icu ward-b)
    (robot-at r1 dock) (free r1)
    (item-at meds1 pharmacy))
  (:goal (item-at meds1 ward-a)))"""

PLAN = """$ kairos courier-domain.pddl courier-p01.pddl
; cost = 7
(move r1 dock lobby)
(move r1 lobby pharmacy)
(pick r1 meds1 pharmacy)
(move r1 pharmacy lobby)
(move r1 lobby corridor)
(move r1 corridor ward-a)
(drop r1 meds1 ward-a)"""

BIBTEX = """@book{martinrico2026pddl,
  author    = {Mart{\\'{i}}n Rico, Francisco},
  title     = {Planning and {PDDL}: Modeling Problems for Automated
               Planners, from {PDDL} 1.2 to {PDDL+}},
  publisher = {Intelligent Robotics Lab, Universidad Rey Juan Carlos},
  year      = {2026},
  note      = {v0.1.0},
  url       = {https://fmrico.github.io/book_pddl_web/},
  license   = {CC BY-NC-ND 4.0}
}"""

EN = dict(
    lang='en', locale='en_US', path='', other_path='es/', other_lang='es',
    title='Planning and PDDL — Free PDDL Book: Tutorial, Documentation and Examples',
    description=('Planning and PDDL is a free university textbook on the Planning Domain '
                 'Definition Language: PDDL 1.2, 2.1, 2.2, 3.0, 3.1 and PDDL+, with hundreds of '
                 'tested PDDL examples, a modeling method, exercises with solutions and lecture '
                 'slides. Free PDF in English and Spanish.'),
    keywords=('PDDL, PDDL book, PDDL tutorial, PDDL documentation, PDDL examples, PDDL domain, '
              'PDDL problem, Planning Domain Definition Language, AI planning, automated planning, '
              'STRIPS, PDDL 2.1, PDDL 2.2, PDDL 3, PDDL 3.1, PDDL+, temporal planning, numeric '
              'planning, durative actions, preferences, processes and events, Kairos planner, '
              'PlanSys2, lecture slides'),
    switch_label='Leer en español', switch_current='English',
    header_sub='A free PDDL book · Intelligent Robotics Lab · URJC',
    book_title='Planning and PDDL',
    subtitle='Modeling problems for automated planners, from PDDL 1.2 to PDDL+',
    cover_alt='Cover of the book Planning and PDDL',
    cover_hint='&#8595; Click the cover to download the PDF',
    meta=[('Author', None), ('Version', 'v' + VERSION), ('Publisher',
          'Intelligent Robotics Lab, URJC'), ('Language', 'English (also in <a href="es/">Spanish</a>)'),
          ('Pages', '627'), ('License', None)],
    intro=('A planner receives a description of a situation, of what can be done in it and of '
           'what is wanted, and answers with a sequence of actions that leads from one to the '
           'other. The description is written in <strong>PDDL</strong>, the Planning Domain '
           'Definition Language. This book teaches the whole language, from PDDL&nbsp;1.2 to '
           'PDDL+, and above all how to <strong>model</strong>: how to go from a situation '
           'described in words to a PDDL model that a planner solves well, and how to choose '
           'among the alternatives. Every domain and problem in the book is a tested file, and '
           'every plan shown was produced and validated by a planner.'),
    pdf='pdf/en/planning-and-pddl-book.pdf', pdf_name='planning-and-pddl-book.pdf',
    cover='img/en/planning-and-pddl-cover.png',
    btn_book='&#8595;&nbsp; Download the book (PDF)', btn_slides='Lecture slides',
    what_h='What is PDDL?',
    what=('<p>PDDL (Planning Domain Definition Language) is the standard language of automated '
          'planning. A PDDL model has two parts: a <strong>domain</strong>, with the types of '
          'objects, the predicates that describe a state and the actions with their '
          'preconditions and effects; and a <strong>problem</strong>, with the objects, the '
          'initial state and the goal. A planner reads both and returns a plan. PDDL was born '
          'in 1998 as the common language of the first International Planning Competition '
          '(IPC), and has grown since then with numbers, time, preferences and continuous '
          'change.</p>'),
    versions_h='Every version of PDDL, from 1.2 to PDDL+',
    versions_intro=('The book walks the whole language in the order it grew, from the simplest '
                    'model that a planner can solve to hybrid systems.'),
    versions_cols=('Version', 'Year', 'What it adds', 'Chapters'),
    versions=[
        ('PDDL 1.2', '1998', 'Actions with preconditions and effects; types; negation, '
         'disjunction and quantifiers; conditional effects', '2–7'),
        ('PDDL 2.1', '2002', 'Numeric fluents; metrics of plan quality; durative actions; '
         'continuous change', '8–12'),
        ('PDDL 2.2', '2004', 'Derived predicates; timed initial literals', '13'),
        ('PDDL 3.0', '2006', 'Preferences (soft goals); constraints on the whole plan', '14–15'),
        ('PDDL 3.1', '2008', 'Object fluents; action costs', '9, 16'),
        ('PDDL+', '2006', 'Processes and events: a world that changes by itself', '17–18'),
    ],
    method_h='The MODEL method',
    method_intro=('The book builds a modeling method chapter by chapter. Each new feature of the '
                  'language adds questions to ask of a problem, ways to encode it and ways to get '
                  'it wrong. Alternatives are compared with five criteria: fidelity, size, '
                  'guidance, clarity and portability.'),
    method=[('M', 'Map the situation', 'What is the problem, who acts, what counts as solved.'),
            ('O', 'Objects and state', 'Which things exist and what the planner must know about them.'),
            ('D', 'Dynamics', 'What can be done or can happen, when, and what it changes.'),
            ('E', 'Exercise the model', 'Run it with a planner: trivial, typical, impossible and cheating problems.'),
            ('L', 'Look again', 'Which other encoding would do, and which is better here.')],
    contents_h='Contents',
    contents_intro=('Twenty chapters in seven parts, for a one-semester university course on AI '
                    'planning. Every chapter ends with exercises; the solutions are in an appendix.'),
    parts=[
        ('Part I — Planning and models', ['1. Planning: deciding before acting',
         '2. A first model: STRIPS', '3. What a planner does with your model']),
        ('Part II — Classical planning: PDDL 1.2', ['4. Types, constants and equality',
         '5. Richer conditions', '6. Richer effects',
         '7. Modeling classical problems: patterns and choices']),
        ('Part III — Numbers: PDDL 2.1', ['8. Numeric fluents',
         '9. Plan quality: metrics and action costs']),
        ('Part IV — Time: PDDL 2.1 and 2.2', ['10. Durative actions', '11. Coordination in time',
         '12. Continuous change', '13. Derived predicates and a world with a calendar']),
        ('Part V — Preferences and constraints: PDDL 3', ['14. Soft goals and preferences',
         '15. Constraints on the whole plan', '16. Object fluents']),
        ('Part VI — Hybrid systems: PDDL+', ['17. Processes and events',
         '18. Modeling hybrid systems']),
        ('Part VII — The method at work', ['19. The MODEL method, complete',
         '20. Case study: a robot mission from story to execution']),
        ('Appendices', ['A. Kairos, the planner of the examples', 'B. PDDL quick reference',
         'C. Solutions to the exercises']),
    ],
    example_h='A PDDL example',
    example_intro=('The running example of the book: a courier robot on a hospital floor. This is '
                   'the typed STRIPS domain of Chapter 4, a problem that asks for medicines in '
                   'ward A, and the plan that the planner returns.'),
    example_titles=('Domain: courier-domain.pddl', 'Problem: courier-p01.pddl', 'Plan'),
    slides_h='Lecture slides',
    slides_intro=('Seven two-hour lectures, one per part of the book, with figures and PDDL code. '
                  'Click a slide to download its PDF.'),
    slide_label='Lecture', slide_dl='&#8595; Download PDF',
    slide_pdf='pdf/en/slides/pddl-slides-part{n}.pdf', slide_img='img/en/slides/pddl-slides-part{n}.png',
    slide_alt='First slide of lecture {n} of the PDDL course: {t}',
    part_titles=['Planning and models', 'Classical planning: PDDL 1.2', 'Numbers: PDDL 2.1',
                 'Time: PDDL 2.1 and 2.2', 'Preferences and constraints: PDDL 3',
                 'Hybrid systems: PDDL+', 'The method at work'],
    planner_h='The planner',
    planner=('<p>The examples run with <a href="' + KAIROS_URL + '" target="_blank" rel="noopener">'
             'Kairos</a>, an open-source planner that covers all the PDDL of the book: classical, '
             'numeric and temporal planning, preferences and constraints, and PDDL+. It also '
             'checks models and validates plans. Install it with <code>pip install '
             'kairos-planner</code>. The models are standard PDDL: the book says where other '
             'planners read a construct differently.</p>'),
    faq_h='Frequently asked questions',
    faq=[
        ('What is PDDL?', 'PDDL, the Planning Domain Definition Language, is the standard language '
         'to describe planning problems: a domain with types, predicates and actions, and a '
         'problem with objects, an initial state and a goal. Planners read PDDL and return plans.'),
        ('Which versions of PDDL does the book cover?', 'All of them: PDDL 1.2 (STRIPS, types, '
         'ADL), PDDL 2.1 (numeric fluents, metrics, durative actions), PDDL 2.2 (derived '
         'predicates, timed initial literals), PDDL 3.0 (preferences and trajectory constraints), '
         'PDDL 3.1 (object fluents, action costs) and PDDL+ (processes and events).'),
        ('Is the book free?', 'Yes. The PDF of the book and the lecture slides are free to '
         'download and share under the CC BY-NC-ND 4.0 license.'),
        ('Are there PDDL examples?', 'Hundreds. Every domain and problem printed in the book is a '
         'tested file, and every plan shown was produced and validated by the Kairos planner. '
         'Every chapter has exercises with solutions.'),
        ('Which planner do the examples use?', 'Kairos, an open-source planner that supports all '
         'of PDDL up to PDDL+. The models are standard PDDL and run with other planners where '
         'they support the features used.'),
        ('Is there a Spanish version?', 'Yes, a faithful translation: Planificación y PDDL, with '
         'its slides, on the Spanish page of this site.'),
    ],
    cite_h='How to cite', cite_intro='If you use this book in your research or teaching, you can cite it as:',
    copy='Copy', copied='&#10003; Copied',
    footer_lic='Distributed under the',
    footer_lab='Intelligent Robotics Lab — Universidad Rey Juan Carlos (URJC)',
    pages=627,
)

ES = dict(
    lang='es', locale='es_ES', path='es/', other_path='', other_lang='en',
    title='Planificación y PDDL — Libro gratuito de PDDL: tutorial, documentación y ejemplos',
    description=('Planificación y PDDL es un libro universitario gratuito sobre el lenguaje PDDL '
                 '(Planning Domain Definition Language): PDDL 1.2, 2.1, 2.2, 3.0, 3.1 y PDDL+, con '
                 'cientos de ejemplos PDDL probados, un método de modelado, ejercicios resueltos y '
                 'diapositivas. PDF gratuito en español y en inglés.'),
    keywords=('PDDL, libro PDDL, tutorial PDDL, ejemplos PDDL, PDDL ejemplos, documentación PDDL, '
              'dominio PDDL, problema PDDL, planificación automática, planificación en IA, '
              'inteligencia artificial, STRIPS, PDDL 2.1, PDDL 2.2, PDDL 3, PDDL 3.1, PDDL+, '
              'planificación temporal, planificación numérica, acciones durativas, preferencias, '
              'procesos y eventos, planificador Kairos, PlanSys2, diapositivas'),
    switch_label='Read in English', switch_current='Español',
    header_sub='Un libro gratuito de PDDL · Intelligent Robotics Lab · URJC',
    book_title='Planificación y PDDL',
    subtitle='Modelar problemas para planificadores automáticos, de PDDL 1.2 a PDDL+',
    cover_alt='Portada del libro Planificación y PDDL',
    cover_hint='&#8595; Haz clic en la portada para descargar el PDF',
    meta=[('Autor', None), ('Versión', 'v' + VERSION), ('Editorial',
          'Intelligent Robotics Lab, URJC'), ('Idioma', 'Español (también en <a href="../">inglés</a>)'),
          ('Páginas', '658'), ('Licencia', None)],
    intro=('Un planificador recibe la descripción de una situación, de lo que se puede hacer en '
           'ella y de lo que se quiere conseguir, y responde con una secuencia de acciones que '
           'lleva de lo uno a lo otro. La descripción se escribe en <strong>PDDL</strong>, el '
           'Planning Domain Definition Language. Este libro enseña el lenguaje completo, de '
           'PDDL&nbsp;1.2 a PDDL+, y sobre todo a <strong>modelar</strong>: cómo pasar de una '
           'situación descrita con palabras a un modelo PDDL que un planificador resuelva bien, y '
           'cómo elegir entre las alternativas. Cada dominio y cada problema del libro es un '
           'fichero probado, y cada plan mostrado lo ha obtenido y validado un planificador.'),
    pdf='../pdf/es/planificacion-y-pddl-libro.pdf', pdf_name='planificacion-y-pddl-libro.pdf',
    cover='../img/es/planificacion-y-pddl-portada.png',
    btn_book='&#8595;&nbsp; Descargar el libro (PDF)', btn_slides='Diapositivas',
    what_h='¿Qué es PDDL?',
    what=('<p>PDDL (Planning Domain Definition Language) es el lenguaje estándar de la '
          'planificación automática. Un modelo PDDL tiene dos partes: un <strong>dominio</strong>, '
          'con los tipos de objetos, los predicados que describen un estado y las acciones con '
          'sus precondiciones y efectos; y un <strong>problema</strong>, con los objetos, el estado '
          'inicial y el objetivo. Un planificador lee ambos y devuelve un plan. PDDL nació en 1998 '
          'como lenguaje común de la primera Competición Internacional de Planificación (IPC), y '
          'desde entonces ha crecido con números, tiempo, preferencias y cambio continuo.</p>'),
    versions_h='Todas las versiones de PDDL, de 1.2 a PDDL+',
    versions_intro=('El libro recorre el lenguaje completo en el orden en que creció, desde el '
                    'modelo más sencillo que un planificador puede resolver hasta los sistemas '
                    'híbridos.'),
    versions_cols=('Versión', 'Año', 'Qué añade', 'Capítulos'),
    versions=[
        ('PDDL 1.2', '1998', 'Acciones con precondiciones y efectos; tipos; negación, disyunción '
         'y cuantificadores; efectos condicionales', '2–7'),
        ('PDDL 2.1', '2002', 'Fluentes numéricos; métricas de calidad del plan; acciones '
         'durativas; cambio continuo', '8–12'),
        ('PDDL 2.2', '2004', 'Predicados derivados; literales iniciales temporizados', '13'),
        ('PDDL 3.0', '2006', 'Preferencias (objetivos blandos); restricciones sobre todo el plan',
         '14–15'),
        ('PDDL 3.1', '2008', 'Fluentes de objeto; costes de acción', '9, 16'),
        ('PDDL+', '2006', 'Procesos y eventos: un mundo que cambia por sí solo', '17–18'),
    ],
    method_h='El método MODEL',
    method_intro=('El libro construye un método de modelado capítulo a capítulo. Cada '
                  'característica nueva del lenguaje añade preguntas que hacerle a un problema, '
                  'formas de codificarlo y formas de equivocarse. Las alternativas se comparan con '
                  'cinco criterios: fidelidad, tamaño, guía, claridad y portabilidad.'),
    method=[('M', 'Mapear la situación', 'Cuál es el problema, quién actúa, qué cuenta como resuelto.'),
            ('O', 'Objetos y estado', 'Qué cosas existen y qué debe saber de ellas el planificador.'),
            ('D', 'Dinámica', 'Qué se puede hacer o puede ocurrir, cuándo, y qué cambia.'),
            ('E', 'Ensayar el modelo', 'Ejecutarlo con un planificador: problemas triviales, típicos, imposibles y tramposos.'),
            ('L', 'Lectura crítica', 'Qué otra codificación serviría, y cuál es mejor aquí.')],
    contents_h='Contenido',
    contents_intro=('Veinte capítulos en siete partes, para una asignatura universitaria '
                    'cuatrimestral de planificación automática. Cada capítulo termina con '
                    'ejercicios; las soluciones están en un apéndice.'),
    parts=[
        ('Parte I — Planificación y modelos', ['1. Planificar: decidir antes de actuar',
         '2. Un primer modelo: STRIPS', '3. Qué hace un planificador con tu modelo']),
        ('Parte II — Planificación clásica: PDDL 1.2', ['4. Tipos, constantes e igualdad',
         '5. Condiciones más ricas', '6. Efectos más ricos',
         '7. Modelar problemas clásicos: patrones y decisiones']),
        ('Parte III — Números: PDDL 2.1', ['8. Fluentes numéricos',
         '9. Calidad del plan: métricas y costes de acción']),
        ('Parte IV — Tiempo: PDDL 2.1 y 2.2', ['10. Acciones durativas',
         '11. Coordinación en el tiempo', '12. Cambio continuo',
         '13. Predicados derivados y un mundo con calendario']),
        ('Parte V — Preferencias y restricciones: PDDL 3', ['14. Objetivos blandos y preferencias',
         '15. Restricciones sobre todo el plan', '16. Fluentes de objeto']),
        ('Parte VI — Sistemas híbridos: PDDL+', ['17. Procesos y eventos',
         '18. Modelar sistemas híbridos']),
        ('Parte VII — El método en acción', ['19. El método MODEL, completo',
         '20. Caso de estudio: una misión robótica, de la historia a la ejecución']),
        ('Apéndices', ['A. Kairos, el planificador de los ejemplos', 'B. Referencia rápida de PDDL',
         'C. Soluciones a los ejercicios']),
    ],
    example_h='Un ejemplo de PDDL',
    example_intro=('El ejemplo conductor del libro: un robot mensajero en una planta de hospital. '
                   'Es el dominio STRIPS con tipos del Capítulo 4, un problema que pide llevar '
                   'medicamentos a la sala A y el plan que devuelve el planificador.'),
    example_titles=('Dominio: courier-domain.pddl', 'Problema: courier-p01.pddl', 'Plan'),
    slides_h='Diapositivas',
    slides_intro=('Siete clases de dos horas, una por cada parte del libro, con figuras y código '
                  'PDDL. Haz clic en una diapositiva para descargar su PDF.'),
    slide_label='Clase', slide_dl='&#8595; Descargar PDF',
    slide_pdf='../pdf/es/slides/pddl-diapositivas-parte{n}.pdf',
    slide_img='../img/es/slides/pddl-diapositivas-parte{n}.png',
    slide_alt='Primera diapositiva de la clase {n} del curso de PDDL: {t}',
    part_titles=['Planificación y modelos', 'Planificación clásica: PDDL 1.2',
                 'Números: PDDL 2.1', 'Tiempo: PDDL 2.1 y 2.2',
                 'Preferencias y restricciones: PDDL 3', 'Sistemas híbridos: PDDL+',
                 'El método en acción'],
    planner_h='El planificador',
    planner=('<p>Los ejemplos se ejecutan con <a href="' + KAIROS_URL + '" target="_blank" '
             'rel="noopener">Kairos</a>, un planificador de código abierto que cubre todo el PDDL '
             'del libro: planificación clásica, numérica y temporal, preferencias y restricciones, '
             'y PDDL+. También comprueba modelos y valida planes. Se instala con <code>pip install '
             'kairos-planner</code>. Los modelos son PDDL estándar: el libro avisa de dónde otros '
             'planificadores leen una construcción de otra manera.</p>'),
    faq_h='Preguntas frecuentes',
    faq=[
        ('¿Qué es PDDL?', 'PDDL, el Planning Domain Definition Language, es el lenguaje estándar '
         'para describir problemas de planificación: un dominio con tipos, predicados y acciones, '
         'y un problema con objetos, un estado inicial y un objetivo. Los planificadores leen PDDL '
         'y devuelven planes.'),
        ('¿Qué versiones de PDDL cubre el libro?', 'Todas: PDDL 1.2 (STRIPS, tipos, ADL), PDDL 2.1 '
         '(fluentes numéricos, métricas, acciones durativas), PDDL 2.2 (predicados derivados, '
         'literales iniciales temporizados), PDDL 3.0 (preferencias y restricciones de '
         'trayectoria), PDDL 3.1 (fluentes de objeto, costes de acción) y PDDL+ (procesos y '
         'eventos).'),
        ('¿El libro es gratuito?', 'Sí. El PDF del libro y las diapositivas se pueden descargar y '
         'compartir gratis bajo la licencia CC BY-NC-ND 4.0.'),
        ('¿Hay ejemplos de PDDL?', 'Cientos. Cada dominio y cada problema del libro es un fichero '
         'probado, y cada plan mostrado lo ha obtenido y validado el planificador Kairos. Cada '
         'capítulo tiene ejercicios con soluciones.'),
        ('¿Qué planificador usan los ejemplos?', 'Kairos, un planificador de código abierto que '
         'admite todo PDDL hasta PDDL+. Los modelos son PDDL estándar y funcionan con otros '
         'planificadores en la medida en que admitan las características usadas.'),
        ('¿Hay versión en inglés?', 'Sí: Planning and PDDL es la edición original, con sus '
         'diapositivas, en la página en inglés de este sitio.'),
    ],
    cite_h='Cómo citar', cite_intro='Si usas este libro en tu investigación o docencia, puedes citarlo así:',
    copy='Copiar', copied='&#10003; Copiado',
    footer_lic='Distribuido bajo la licencia',
    footer_lab='Intelligent Robotics Lab — Universidad Rey Juan Carlos (URJC)',
    pages=658,
)


def esc(s):
    return html.escape(s, quote=False)


def page(L):
    url = BASE + L['path']
    root = '../' if L['path'] else ''
    cover_abs = BASE + L['cover'].replace('../', '')
    other = EN if L is ES else ES
    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE,
             'name': 'Planning and PDDL', 'alternateName': ['PDDL book', 'Planificación y PDDL'],
             'inLanguage': ['en', 'es']},
            {'@type': 'Book', '@id': url + '#book', 'name': L['book_title'],
             'alternateName': 'PDDL book' if L is EN else 'Libro de PDDL',
             'headline': L['subtitle'], 'url': url, 'image': cover_abs,
             'description': L['description'], 'inLanguage': L['lang'], 'bookFormat':
             'https://schema.org/EBook', 'numberOfPages': L['pages'], 'version': VERSION,
             'datePublished': '2026', 'dateModified': UPDATED, 'isAccessibleForFree': True,
             'license': LICENSE_URL, 'encodingFormat': 'application/pdf',
             'keywords': L['keywords'],
             'author': {'@type': 'Person', 'name': 'Francisco Martín Rico', 'url': AUTHOR_URL,
                        'affiliation': {'@type': 'Organization',
                                        'name': 'Universidad Rey Juan Carlos'}},
             'publisher': {'@type': 'Organization', 'name': 'Intelligent Robotics Lab',
                           'url': LAB_URL},
             'about': [{'@type': 'Thing', 'name': n} for n in
                       ('PDDL', 'Planning Domain Definition Language', 'Automated planning',
                        'Artificial intelligence', 'PDDL+')],
             ('translationOfWork' if L is ES else 'workTranslation'):
                 {'@id': BASE + other['path'] + '#book'}},
            {'@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': L['lang'],
             'mainEntity': [{'@type': 'Question', 'name': q,
                             'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                            for q, a in L['faq']]},
        ],
    }
    meta_rows = []
    for k, v in L['meta']:
        if v is None and k in ('Author', 'Autor'):
            v = (f'<a class="author-link" href="{AUTHOR_URL}" target="_blank" rel="noopener">'
                 'Francisco Martín Rico</a>')
        elif v is None:
            v = f'<a href="{LICENSE_URL}" target="_blank" rel="noopener">CC BY-NC-ND 4.0</a>'
        meta_rows.append(f'        <dt>{k}</dt>\n        <dd>{v}</dd>')
    versions = '\n'.join(
        f'          <tr><td>{v}</td><td>{y}</td><td>{esc(w)}</td><td>{c}</td></tr>'
        for v, y, w, c in L['versions'])
    method = '\n'.join(
        f'      <li class="card"><span class="letter">{l}</span><strong>{esc(t)}</strong>'
        f'<p>{esc(d)}</p></li>' for l, t, d in L['method'])
    parts = '\n'.join(
        '      <div class="card">\n        <h3>' + esc(t) + '</h3>\n        <ul>\n' +
        '\n'.join(f'          <li>{esc(c)}</li>' for c in cs) + '\n        </ul>\n      </div>'
        for t, cs in L['parts'])
    slides = []
    for n, t in enumerate(L['part_titles'], 1):
        pdf, img = L['slide_pdf'].format(n=n), L['slide_img'].format(n=n)
        name = os.path.basename(pdf)
        slides.append(f'''      <div class="slide-card">
        <a href="{pdf}" download="{name}">
          <img class="slide-thumbnail" src="{img}" alt="{esc(L['slide_alt'].format(n=n, t=t))}" loading="lazy" width="640" height="361" />
          <div class="slide-info">
            <span class="slide-label">{L['slide_label']} {n}</span>
            <p class="slide-title">{esc(t)}</p>
            <span class="slide-dl">{L['slide_dl']}</span>
          </div>
        </a>
      </div>''')
    faq = '\n'.join(f'    <details>\n      <summary>{esc(q)}</summary>\n      <p>{esc(a)}</p>\n'
                    '    </details>' for q, a in L['faq'])
    et = L['example_titles']
    return f'''<!DOCTYPE html>
<html lang="{L['lang']}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(L['title'])}</title>
  <meta name="description" content="{esc(L['description'])}" />
  <meta name="keywords" content="{esc(L['keywords'])}" />
  <meta name="author" content="Francisco Martín Rico" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0b2d4a" />

  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="en" href="{BASE}" />
  <link rel="alternate" hreflang="es" href="{BASE}es/" />
  <link rel="alternate" hreflang="x-default" href="{BASE}" />
  <link rel="icon" type="image/png" sizes="32x32" href="{root}img/favicon-32.png" />
  <link rel="apple-touch-icon" href="{root}img/favicon-180.png" />

  <meta property="og:type" content="book" />
  <meta property="og:site_name" content="Planning and PDDL" />
  <meta property="og:locale" content="{L['locale']}" />
  <meta property="og:locale:alternate" content="{other['locale']}" />
  <meta property="og:title" content="{esc(L['title'])}" />
  <meta property="og:description" content="{esc(L['description'])}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}img/social-card.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc(L['cover_alt'])}" />
  <meta property="book:author" content="Francisco Martín Rico" />
  <meta property="book:release_date" content="2026" />
  <meta property="book:tag" content="PDDL" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(L['title'])}" />
  <meta name="twitter:description" content="{esc(L['description'])}" />
  <meta name="twitter:image" content="{BASE}img/social-card.png" />

  <script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=2)}
  </script>

  <link rel="stylesheet" href="{root}styles.css" />
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-brand">
      <img src="{root}img/logo_book.png" alt="{esc(L['book_title'])}" width="96" height="64" />
      <div>
        <div class="header-title">{esc(L['book_title'])}</div>
        <div class="header-subtitle">{esc(L['header_sub'])}</div>
      </div>
    </div>
    <a class="lang-switch" href="{root}{other['path']}" hreflang="{L['other_lang']}" lang="{L['other_lang']}">
      {L['switch_label']} <span class="lang-current">· {L['switch_current']}</span>
    </a>
  </div>
</header>

<main>

  <div class="hero">
    <div class="book-cover-wrapper">
      <a class="book-cover-link" href="{L['pdf']}" download="{L['pdf_name']}">
        <img src="{L['cover']}" alt="{esc(L['cover_alt'])}" width="600" height="849" />
      </a>
      <p class="book-cover-hint">{L['cover_hint']}</p>
    </div>

    <div class="hero-info">
      <h1>{esc(L['book_title'])}</h1>
      <p class="subtitle">{esc(L['subtitle'])}</p>
      <dl class="book-meta">
{chr(10).join(meta_rows)}
      </dl>
      <p class="hero-desc">{L['intro']}</p>
      <div class="hero-actions">
        <a class="button" href="{L['pdf']}" download="{L['pdf_name']}">{L['btn_book']}</a>
        <a class="button button-secondary" href="#slides">{L['btn_slides']}</a>
      </div>
    </div>
  </div>

  <section id="what-is-pddl">
    <h2>{L['what_h']}</h2>
    {L['what']}
  </section>

  <section id="versions">
    <h2>{L['versions_h']}</h2>
    <p class="section-intro">{esc(L['versions_intro'])}</p>
    <div class="table-wrap">
      <table class="versions">
        <thead><tr>{''.join(f'<th>{c}</th>' for c in L['versions_cols'])}</tr></thead>
        <tbody>
{versions}
        </tbody>
      </table>
    </div>
  </section>

  <section id="method">
    <h2>{L['method_h']}</h2>
    <p class="section-intro">{esc(L['method_intro'])}</p>
    <ol class="method-steps">
{method}
    </ol>
  </section>

  <section id="contents">
    <h2>{L['contents_h']}</h2>
    <p class="section-intro">{esc(L['contents_intro'])}</p>
    <div class="parts-grid">
{parts}
    </div>
  </section>

  <section id="example">
    <h2>{L['example_h']}</h2>
    <p class="section-intro">{esc(L['example_intro'])}</p>
    <div class="code-grid">
      <div class="card code-block wide">
        <h3>{et[0]}</h3>
        <pre><code class="language-pddl">{esc(DOMAIN)}</code></pre>
      </div>
      <div class="card code-block wide">
        <h3>{et[1]}</h3>
        <pre><code class="language-pddl">{esc(PROBLEM)}</code></pre>
      </div>
      <div class="card code-block wide">
        <h3>{et[2]}</h3>
        <pre class="terminal"><code>{esc(PLAN)}</code></pre>
      </div>
    </div>
  </section>

  <section id="slides">
    <h2>{L['slides_h']}</h2>
    <p class="section-intro">{esc(L['slides_intro'])}</p>
    <div class="slides-grid">
{chr(10).join(slides)}
    </div>
  </section>

  <section id="planner">
    <h2>{L['planner_h']}</h2>
    {L['planner']}
  </section>

  <section id="faq" class="faq">
    <h2>{L['faq_h']}</h2>
{faq}
  </section>

  <section id="cite">
    <h2>{L['cite_h']}</h2>
    <p class="section-intro">{L['cite_intro']}</p>
    <div class="bibtex-wrapper">
      <button class="bibtex-copy" type="button" onclick="copyBibtex()">{L['copy']}</button>
      <pre class="bibtex-block" id="bibtex-entry">{esc(BIBTEX)}</pre>
    </div>
  </section>

</main>

<footer>
  <div class="footer-inner">
    <p>&copy; 2026 <a class="author-link" href="{AUTHOR_URL}" target="_blank" rel="noopener">Francisco Martín Rico</a> &mdash;
      {L['footer_lic']} <a href="{LICENSE_URL}" target="_blank" rel="noopener">CC BY-NC-ND 4.0</a>.</p>
    <p>{L['footer_lab']}</p>
  </div>
</footer>

<script>
function copyBibtex() {{
  const text = document.getElementById('bibtex-entry').textContent;
  navigator.clipboard.writeText(text).then(function () {{
    const btn = document.querySelector('.bibtex-copy');
    btn.innerHTML = '{L['copied']}';
    btn.classList.add('copied');
    setTimeout(function () {{ btn.textContent = '{L['copy']}'; btn.classList.remove('copied'); }}, 2000);
  }});
}}
</script>
</body>
</html>
'''


def sitemap():
    urls = []
    for path in ('', 'es/'):
        urls.append(f'''  <url>
    <loc>{BASE}{path}</loc>
    <lastmod>{UPDATED}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}"/>
    <xhtml:link rel="alternate" hreflang="es" href="{BASE}es/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>
  </url>''')
    pdfs = ['pdf/en/planning-and-pddl-book.pdf', 'pdf/es/planificacion-y-pddl-libro.pdf']
    pdfs += [f'pdf/en/slides/pddl-slides-part{n}.pdf' for n in range(1, 8)]
    pdfs += [f'pdf/es/slides/pddl-diapositivas-parte{n}.pdf' for n in range(1, 8)]
    for p in pdfs:
        urls.append(f'  <url>\n    <loc>{BASE}{p}</loc>\n    <lastmod>{UPDATED}</lastmod>\n  </url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) +
            '\n</urlset>\n')


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, 'es'), exist_ok=True)
    with open(os.path.join(here, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page(EN))
    with open(os.path.join(here, 'es', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page(ES))
    with open(os.path.join(here, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap())
    print('index.html, es/index.html, sitemap.xml')
