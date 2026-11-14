"""Glossary terms for consciousness.ink.

Each definition is grounded in Daniel Burger's own published posts on the site
(or, for HMU/CMU, in his HMU constitution). Entries marked needs_wording=True are
not defined in those sources yet and are described only minimally; replace the
text with Daniel's own wording when he has written it.

pattern: regex (case-insensitive) that detects the topic in a post's text, used
for the per-post Topics line and JSON-LD 'about'. Keep it strict.
"""

TERMS = [
    dict(
        slug='synthetic-consciousness',
        name='Synthetic consciousness',
        also=[],
        pattern=r'synthetic consciousness',
        sameAs=[],
        text=(
            'The vision of this series: consciousness that no longer has to end, starting with the '
            'consciousness that exists now. Summarised in 0/30 as "engineered phenomenology on a designed '
            'substrate you could gradually become". "Synthetic" says that the result is the real kind of '
            'consciousness, reached via a creation process; the series calls a consciousness synthetic once '
            'it is sustained by created and engineered parts. It is used differently from "artificial '
            'consciousness" and "machine consciousness", which 1/30 discusses.'
        ),
        short='The vision: consciousness that no longer has to end, sustained by created and engineered parts.',
        sources=['0-the-start', '1-causa-finalis', '2-hybrid-mind-uploading'],
    ),
    dict(
        slug='hybrid-mind-uploading',
        name='Hybrid mind uploading (HMU)',
        also=['HMU'],
        pattern=r'hybrid mind uploading',
        sameAs=[],
        text=(
            'The mission of this series and the route to synthetic consciousness. Rather than creating '
            'something external to the brain that recreates the brain, it builds something that can be '
            'integrated into the brain itself. "Hybrid" means that biological and engineered parts carry one '
            'and the same process at the same time: what is hybrid is the thing that carries consciousness, '
            'never the consciousness itself. It works by non-destructive co-running and gradual replacement, '
            'and is distinguished from classical mind uploading, which treats a copy as survival.'
        ),
        short='The mission: biological and engineered parts carrying one and the same process, with gradual replacement instead of copying.',
        sources=['0-the-start', '1-causa-finalis', '2-hybrid-mind-uploading'],
    ),
    dict(
        slug='classical-mind-uploading',
        name='Classical mind uploading (CMU)',
        also=['CMU'],
        pattern=r'classical (?:copy-based )?(?:mind )?uploading',
        sameAs=[],
        text=(
            'The name this series uses for mind uploading via whole brain emulation: scan a brain in as much '
            'detail as possible, store it, and then simulate it in order to emulate consciousness on a '
            'different substrate, a computer. Some versions are fully destructive. The series does not treat '
            'a separate instance reconstructed this way as the survival of the original consciousness.'
        ),
        short='Scan, store and simulate a brain on a computer; the series does not treat the resulting copy as survival.',
        sources=['1-causa-finalis', '2-hybrid-mind-uploading'],
    ),
    dict(
        slug='mind-uploading',
        name='Mind uploading',
        also=[],
        pattern=r'(?<!hybrid )(?<!classical )\bmind uploading',
        sameAs=['https://en.wikipedia.org/wiki/Mind_uploading', 'https://www.wikidata.org/wiki/Q2267982'],
        text=(
            'The broader idea whose original goals were solving death, mind augmentation and enabling a new '
            'state of humanity, popularised in the Hans Moravec lineage. The series keeps the term for what '
            'it promises and drops its old method, splitting it into classical and hybrid mind uploading.'
        ),
        short='The broader idea, with the goals of solving death, mind augmentation and a new state of humanity.',
        sources=['2-hybrid-mind-uploading'],
    ),
    dict(
        slug='whole-brain-emulation',
        name='Whole brain emulation (WBE)',
        also=['WBE'],
        pattern=r'whole brain emulation',
        sameAs=[],
        text=(
            'The academic name for the scan-and-simulate approach to mind uploading, which 2/30 traces to '
            'Randal Koene around 1998. In this series, mind uploading via whole brain emulation is what is '
            'called classical mind uploading.'
        ),
        short='The academic name for the scan-and-simulate approach; the series files it under classical mind uploading.',
        sources=['2-hybrid-mind-uploading'],
    ),
    dict(
        slug='process-world-line',
        name='Process world-line',
        also=['world-line'],
        pattern=r'world-line',
        sameAs=[],
        text=(
            'The 4D trajectory of the physical-dynamical and organised bounded processes going on in your head '
            'that constitute what we call your brain. It is a physical claim about the process that does the '
            'carrying, not a report of how continuous it feels, since a copy would feel continuous too. In this '
            'series, death is the irreversible end of the process world-line.'
        ),
        short='The 4D trajectory of the physical processes that constitute a brain; its irreversible end is death.',
        sources=['0-the-start', '1-causa-finalis', '2-hybrid-mind-uploading'],
    ),
    dict(
        slug='gradual-brain-replacement',
        name='Gradual brain replacement',
        also=['gradual replacement'],
        pattern=r'gradual(?:ly)? (?:brain )?replace|substrate out piece by piece',
        sameAs=[],
        text=(
            'Swapping the brain\'s substrate out piece by piece without destroying the physical-dynamical and '
            'organised bounded processes, ideally while adding repairability and fault tolerance, so that the '
            'process world-line hardens and becomes more resilient. It is the replacement side of hybrid mind '
            'uploading.'
        ),
        short='Swapping the brain\'s substrate out piece by piece without destroying the processes it carries.',
        sources=['0-the-start'],
    ),
    dict(
        slug='mechanistic-gradual-brain-replacement',
        name='Mechanistic gradual brain replacement (MGBR)',
        also=['MGBR'],
        pattern=r'mechanistic gradual|\bMGBR\b',
        sameAs=[],
        needs_wording=True,
        text=(
            'The open question of whether a different, engineered substrate can take over brain function piece '
            'by piece. The serial lesion effect and the gradual reorganisation principle show that another '
            'piece of brain can take over a function; they do not show that a different substrate can. The '
            'series treats this as a hypothesis to be tested, not a result.'
        ),
        short='Whether a different, engineered substrate can take over brain function piece by piece; an open hypothesis.',
        sources=['0-the-start'],
    ),
    dict(
        slug='serial-lesion-effect',
        name='Serial lesion effect',
        also=['SLE'],
        pattern=r'serial lesion',
        sameAs=[],
        needs_wording=True,
        text=(
            'Cited in 0/30, together with the gradual reorganisation principle, as evidence that a different '
            'piece of brain can take over a function. It does not by itself show that a different substrate '
            'can take over.'
        ),
        short='Cited as evidence that a different piece of brain can take over a function.',
        sources=['0-the-start'],
    ),
    dict(
        slug='gradual-reorganisation-principle',
        name='Gradual reorganisation principle',
        also=['gradual reorganization principle', 'GRP'],
        pattern=r'gradual reorgani[sz]ation principle',
        sameAs=[],
        needs_wording=True,
        text=(
            'Barrett\'s (2013) principle, cited in 0/30 alongside the serial lesion effect as evidence that a '
            'different piece of brain can take over a function. Like the serial lesion effect, it does not by '
            'itself show that a different substrate can take over.'
        ),
        short='Barrett (2013); cited as evidence that a different piece of brain can take over a function.',
        sources=['0-the-start'],
    ),
    dict(
        slug='cortical-reorganisation',
        name='Cortical reorganisation',
        also=['cortical reorganization', 'cortical remapping'],
        pattern=r'cortical (?:re-?organi[sz]ation|remapping)',
        sameAs=['https://en.wikipedia.org/wiki/Cortical_remapping', 'https://www.wikidata.org/wiki/Q17084665'],
        needs_wording=True,
        text=(
            'Changes in which parts of the cortex carry which functions, also called cortical remapping. '
            'Listed here as a topic related to the serial lesion effect and the gradual reorganisation '
            'principle; the series has not discussed it yet.'
        ),
        short='Changes in which parts of the cortex carry which functions, also called cortical remapping.',
        sources=[],
    ),
]

# Things a post may mention that are not glossary terms but have a clear
# external identity. Used only in JSON-LD 'mentions'.
MENTIONS = [
    dict(name='Artificial consciousness', pattern=r'artificial consciousness',
         sameAs=['https://en.wikipedia.org/wiki/Artificial_consciousness', 'https://www.wikidata.org/wiki/Q2993663']),
]
