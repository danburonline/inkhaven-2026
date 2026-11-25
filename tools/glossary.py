"""Glossary terms for consciousness.ink.

Each definition is grounded in Daniel Burger's own published posts on the site
(or, for HMU/CMU, in his HMU constitution).

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
        sources=['0-the-start', '1-causa-finalis', '2-hybrid-mind-uploading', '3-solving-death', '5-transcending-biology', '8-collective-mind', '12-distributed-unification'],
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
        sources=['0-the-start', '12-distributed-unification'],
    ),
    dict(
        slug='mechanistic-gradual-brain-replacement',
        name='Mechanistic gradual brain replacement (MGBR)',
        also=['MGBR'],
        pattern=r'mechanistic gradual|\bMGBR\b',
        sameAs=[],
        text=(
            'Named in 3/30 as the core of hybrid mind uploading, and as step one towards solving death, after '
            'functional brain isolation. 0/30 says that a different piece of brain can take over a function, '
            'but that a different substrate taking over is still open and is the reason for the replacement '
            'work. 3/30 says whether a world-line truly went on via a replacement has to be shown physically.'
        ),
        short='The core of hybrid mind uploading; whether a different substrate can take over, and whether a world-line went on via replacement, still has to be shown.',
        sources=['0-the-start', '3-solving-death', '11-morphological-independence'],
    ),
    dict(
        slug='serial-lesion-effect',
        name='Serial lesion effect',
        also=['SLE'],
        pattern=r'serial lesion',
        sameAs=[],
        text=(
            'Cited in 0/30, together with Barrett\'s (2013) gradual reorganisation principle: a different '
            'piece of brain can take over a function. What neither of them gives you, the post says, is a '
            'different substrate taking over, which is still open.'
        ),
        short='A different piece of brain can take over a function; it does not show that a different substrate can.',
        sources=['0-the-start', '9-multiple-realisability'],
    ),
    dict(
        slug='gradual-reorganisation-principle',
        name='Gradual reorganisation principle',
        also=['gradual reorganization principle', 'GRP'],
        pattern=r'gradual reorgani[sz]ation principle',
        sameAs=[],
        text=(
            'Barrett\'s (2013) principle, cited in 0/30 together with the serial lesion effect: a different '
            'piece of brain can take over a function. What neither of them gives you, the post says, is a '
            'different substrate taking over, which is still open.'
        ),
        short='Barrett (2013): a different piece of brain can take over a function; it does not show that a different substrate can.',
        sources=['0-the-start', '9-multiple-realisability'],
    ),
    dict(
        slug='solving-death',
        name='Solving death',
        also=['solve death'],
        pattern=r'solv(?:e|ing) death|death (?:is )?solved',
        sameAs=[],
        text=(
            'The goal that no one has to end, which is different from halting the natural process of dying. '
            'Reversing ageing halts the dying but does not solve death, since you can still get hit by a bus. '
            'The goal says "no one has to end", never "no one is allowed to end", because only a continuation '
            'worth having counts. In the Ontology it is one of the three hard goals the mission has to achieve; '
            'functional brain isolation is step zero towards it, and gradual replacement comes after. Solved '
            'means the remaining risk keeps falling fast enough that all the yearly risks add up to a finite total.'
        ),
        short='The goal that no one has to end; halting ageing stops dying but does not solve death.',
        sources=['3-solving-death', '5-transcending-biology', '11-morphological-independence'],
    ),
    dict(
        slug='functional-brain-isolation',
        name='Functional brain isolation',
        also=['functionally isolated brain', 'brain isolation'],
        pattern=r'functional(?:ly)? (?:brain )?isolat|isolat\w* (?:the )?brains?',
        sameAs=['https://en.wikipedia.org/wiki/Isolated_brain'],
        text=(
            'Taking a living brain out of its body and keeping it alive outside of it for as long as possible, '
            'the work of Eightsix: early success in rodents, work towards a large animal brain, and ultimately '
            'humans. In this series it is step zero on the route to solving death, before gradual replacement.'
        ),
        short='Keeping a living brain alive outside its body for as long as possible; step zero towards solving death.',
        sources=['3-solving-death', '11-morphological-independence', '13-brain-centredness'],
    ),
    dict(
        slug='deprivation-view',
        name='Deprivation view of death',
        also=['deprivation account', 'deprivationism'],
        pattern=r'deprivation (?:view|account)',
        sameAs=[],
        text=(
            'Nagel\'s view, used in 3/30 as the central reason why death is bad: death is the irreversible end '
            'of a conscious process world-line, so everything that would have come after does not happen for '
            'the someone that this world-line is, and if that would have been worth having, missing out on it '
            'is bad for that someone.'
        ),
        short='Nagel: death is bad for the one who dies because it deprives them of what would have been worth having.',
        sources=['3-solving-death'],
    ),
    dict(
        slug='adaptive-preferences',
        name='Adaptive preferences',
        also=['sour grapes', 'adaptive preference formation'],
        pattern=r'adaptive preferences?|sour grapes',
        sameAs=[],
        text=(
            'Elster\'s term, also called "sour grapes", used in 3/30 for making your peace with death because, '
            'for basically all of human history, there was nothing anybody could do about it. The post says '
            'that the wish to solve death can be explained away, but so can everybody else\'s acceptance, and '
            'that explaining away doesn\'t decide anything.'
        ),
        short='Elster\'s "sour grapes", used in 3/30: acceptance of death can be explained away just as easily as the wish to solve it.',
        sources=['3-solving-death'],
    ),
    dict(
        slug='genetic-fallacy',
        name='Genetic fallacy',
        also=[],
        pattern=r'genetic fallacy',
        sameAs=['https://en.wikipedia.org/wiki/Genetic_fallacy'],
        text=(
            'Used in 3/30 for treating the causes of wanting to solve death (an upbringing, a teenage bookshelf) '
            'as if they showed that the goal itself is bad. The post distinguishes a cause (what made you want it) '
            'from a reason (what makes it worth wanting): those stories tell you how he ended up with death as his '
            'main topic, but they don\'t tell you at all if the goal itself is any good, and they also can\'t tell '
            'you that it\'s bad.'
        ),
        short='Used in 3/30: the causes of a wish don\'t tell you if the goal is any good, and they also can\'t tell you that it\'s bad.',
        sources=['3-solving-death'],
    ),
    dict(
        slug='death',
        name='Death',
        also=['irreversible end'],
        pattern=r'irreversible end of a conscious process world-line|irreversible destruction of the physical and dynamic processes',
        sameAs=[],
        text=(
            'The irreversible end of a conscious process world-line; seen from the engineering side, the '
            'irreversible destruction of the physical and dynamic processes of consciousness. "Irreversible" is '
            'meant strictly: the end that cannot be undone by anything that physics allows. Medicine keeps '
            'pushing the point where a stop turns into an end further out, so solving death is never about '
            'bringing somebody back from an end, only about never letting a stop turn into one.'
        ),
        short='The irreversible end of a conscious process world-line, irreversible by anything physics allows.',
        sources=['3-solving-death', '8-collective-mind'],
    ),
    dict(
        slug='amortality',
        name='Amortality',
        also=['amortal', 'stop dying'],
        pattern=r'\bamortal',
        sameAs=[],
        text=(
            'What you get when the dying is halted (ageing, failing organs): no clock in you runs out by itself '
            'anymore. It is step zero, not solving death, since a risk that just stays where it is, like being '
            'hit by a bus, still gets everybody in the end, only later.'
        ),
        short='Dying halted, so no internal clock runs out; step zero, not yet solving death.',
        sources=['3-solving-death'],
    ),
    dict(
        slug='immortality',
        name='Immortality',
        also=['immortal'],
        pattern=r'\bimmortality\b',
        sameAs=['https://en.wikipedia.org/wiki/Immortality'],
        text=(
            'The state in which death cannot occur at all anymore. In the order "stop dying and achieve '
            'amortality, then solve death and seek immortality", it is something one can seek once death is '
            'solved, and not part of the goal.'
        ),
        short='Death cannot occur at all; sought after solving death, not part of the goal.',
        sources=['3-solving-death'],
    ),
    dict(
        slug='understand-consciousness',
        name='Understand consciousness',
        also=['understanding consciousness'],
        pattern=r'understand(?:ing)? consciousness',
        sameAs=[],
        text=(
            'The second of the three goals of the Ontology. "Understand" comes in three levels: measuring it, '
            'modelling it and explaining it. The goal counts as reached at the second level, a model that can tell '
            'you before a replacement step if the experience will change; the third is the horizon, and it may never '
            'be reachable by science. It is ordered second because it is what is needed to check that death really '
            'got solved: hybrid mind uploading can sidestep a theory of consciousness when building the thing that '
            'carries the process, but it cannot sidestep measuring.'
        ),
        short='The Ontology\'s second goal: reached at a model that can predict whether experience will change, not only at a full theory.',
        sources=['4-measurements-models-theories', '5-transcending-biology'],
    ),
    dict(
        slug='measurement-theory',
        name='Measurement theory',
        also=['measurement theories'],
        pattern=r'measurement theor',
        sameAs=[],
        text=(
            'The most modest of the three: it only tells you what kind of data count at all (reports, behaviour, '
            'neural markers, and so on) and how to read that data as experience; it doesn\'t say why. In this series, '
            'measurement comes first, before a full theory, with the two correcting each other in turns, because what '
            'you think consciousness is already shapes what you accept as a measurement of it.'
        ),
        short='What data count as a measurement of experience, and how to read them; it does not say what consciousness is.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='model-of-consciousness',
        name='Model of consciousness',
        also=['models of consciousness'],
        pattern=r'models? of consciousness',
        sameAs=[],
        text=(
            'With a model you can already predict which experience goes with which physical state. In this series it '
            'is the second of three levels of "understand" (measure, model, explain), and the level at which the goal '
            'counts as reached: a model that allows us to measure, predict and steer experience across a replacement '
            'step, and that can tell you before a step you cannot undo whether the experience will change.'
        ),
        short='A model that predicts which experience goes with which physical state, and whether experience will change before a replacement step.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='theory-of-consciousness',
        name='Theory of consciousness',
        also=['theories of consciousness'],
        pattern=r'theor(?:y|ies) of consciousness',
        sameAs=[],
        text=(
            'A theory would say what consciousness is and why there is any of it in the first place. 4/30 treats this '
            'as the third level of "understand", the horizon, and worries that it may belong with questions science '
            'cannot settle, so that a theory of consciousness may always be poetry in Bohr\'s sense. Hybrid mind '
            'uploading does not let its success depend on any single theory of consciousness being the only true one; '
            'rival theories become predictions that a measurement can test.'
        ),
        short='An account of what consciousness is and why there is any of it; the horizon of the second goal, which may stay out of reach of science.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='goal-vs-outcome',
        name='Goal vs outcome',
        also=['goals and outcomes'],
        pattern=r'goals? and outcomes?|difference between goals and outcomes|a goal and no outcome',
        sameAs=[],
        text=(
            'A goal is something that we strive for and could fail at; an outcome is what follows either way, as long '
            'as we work on the mission. Understanding consciousness is a goal, at least up to the level of '
            'measurement, and not a mere outcome, because without a way to tell that experience is still there, and '
            'that it\'s still this experience, we could never know if the mission succeeded. 5/30 applies the distinction to '
            'transcending humanity: the capability could become possible while nobody goes beyond a limit, or while the '
            'minds that do are all replacements. The goal is that we get there as the ones that we are.'
        ),
        short='A goal is something one could fail at; an outcome follows either way from working on the mission.',
        sources=['4-measurements-models-theories', '5-transcending-biology'],
    ),
    dict(
        slug='consciousness-engineering',
        name='Consciousness engineering',
        also=[],
        pattern=r'consciousness engineering',
        sameAs=[],
        text=(
            'Engineering with matter that we try to couple and integrate with the biological brain, so that experience '
            'extends across both parts ("bridging" phenomenal consciousness), with the aim of ultimately letting it '
            'host synthetic consciousness. 4/30 uses this name both for that work and for the Frontiers Research Topic '
            'Daniel co-organised, and contrasts it with consciousness science: an engineering mindset rather than a '
            'science mindset, though the measurement problem of consciousness may be solved from this work.'
        ),
        short='Engineering that couples with the living brain so experience can extend across both parts and eventually host synthetic consciousness.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='biomimetic-neuromorphics',
        name='Biomimetic neuromorphics',
        also=[],
        pattern=r'biomimetic neuromorphics',
        sameAs=[],
        text=(
            'The slot that whole brain emulation has in classical mind uploading, but in hybrid mind uploading. 4/30 '
            'expects measurement theories, and maybe even models of consciousness, to emerge from this work, and treats '
            'a good model of consciousness here as useful enough to say that we understand consciousness.'
        ),
        short='In hybrid mind uploading, the counterpart to the slot that whole brain emulation has in classical mind uploading.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='sidestepping',
        name='Sidestepping',
        also=['sidestep'],
        pattern=r'sidestep',
        sameAs=[],
        text=(
            'What hybrid mind uploading does with a theory of consciousness: it does not need a theory in order to make '
            'the work succeed, or to have confidence in it, but it does not ignore theories either. Ignoring them '
            'completely would be insanity, as you\'d end up assuming one anyway. Sidestepping means hybrid mind '
            'uploading doesn\'t let its success depend on any single theory of consciousness being the only true one; '
            'it assumes a few things openly (the process world-line is one, held as a hypothesis), and rival theories '
            'become predictions that a measurement can test.'
        ),
        short='Not ignoring theories of consciousness, but not letting success depend on any one of them being the only true one.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='adversarial-collaboration',
        name='Adversarial collaboration',
        also=['adversarial collaborations'],
        pattern=r'adversarial collaborations?',
        sameAs=[],
        text=(
            'Named in 4/30 as one of the first signs of a rigorisation of the consciousness sciences: theories with '
            'conflicting predictions get tested against each other.'
        ),
        short='Theories with conflicting predictions tested against each other; cited as a sign of rigorisation in consciousness science.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='inventing-temperature',
        name='Inventing Temperature',
        also=['calibration circle'],
        pattern=r'inventing temperature|calibrate a thermometer',
        sameAs=[],
        text=(
            'Hasok Chang\'s example, used in 4/30: thermometers and fixed scales (Fahrenheit, 1724) were around long '
            'before a kinetic theory explained what temperature is (1850s–1870s). You can\'t calibrate a thermometer '
            'without knowing what temperature really is, and you can\'t know what temperature is without a thermometer, '
            'so every round of measuring corrected the concept, and also the other way around. This is the picture for '
            'how a measurement theory and a theory of consciousness correct each other in turns.'
        ),
        short='Chang\'s temperature example: measurement and concept correct each other in turns, because neither comes first on its own.',
        sources=['4-measurements-models-theories'],
    ),
    dict(
        slug='transcend-humanity',
        name='Transcend humanity',
        also=['transcending humanity', 'human transcendence'],
        pattern=r'transcend(?:ing)? humanity|human transcendence',
        sameAs=[],
        text=(
            'The third and last of the three goals of the Ontology, and the transformative one, where the thing that '
            'changes is us. Until 5/30 it was called "human transcendence". It means going beyond the limits that '
            'human biology sets for us, and only those: the limits that physics sets stay where they are. What gets '
            'left behind is the species, the kind we were born into with the limits of its biology, not the person who '
            'goes beyond them, not the people who would rather stay, and not being humane. It has to stay you, and it '
            'does not have to stay human. In terms of the process world-line, it is what lets that same world-line '
            'outgrow the limits that it was born with. It comes last because it needs both the engineered carrier that '
            'solving death brings and more understanding of consciousness than solving death does.'
        ),
        short='The Ontology\'s third goal: the same world-line going beyond the limits of biology, while the limits of physics stay.',
        sources=['4-measurements-models-theories', '5-transcending-biology'],
    ),
    dict(
        slug='limits-of-biology',
        name='Limits of biology',
        also=['limits that human biology sets'],
        pattern=r'limits? of (?:human )?biology|limits? that (?:human )?biology sets',
        sameAs=[],
        text=(
            'The limits that come from the thing that carries us, which came with the biology that we were born into. '
            'Death is the one that everybody knows. 5/30 names others: what we can experience (vision is roughly one '
            'octave of the electromagnetic spectrum), what we can keep (memory compresses what it stores and rebuilds '
            'what it recalls), how much a mind can hold, where a mind can exist, and being one mind, closed off from '
            'every other one. A telescope, a notebook or a spacesuit go around a limit and leave it where it was, in the '
            'thing that carries the experience. They are distinct from the limits that physics sets, which stay where '
            'they are, and from the adumbrations of perception, which hold for any mind.'
        ),
        short='Limits from the biological carrier we were born with, death among them; distinct from the limits of physics, which stay.',
        sources=['2-hybrid-mind-uploading', '5-transcending-biology'],
    ),
    dict(
        slug='adumbrations',
        name='Adumbrations',
        also=['Abschattung'],
        pattern=r'adumbration|abschattung',
        sameAs=[],
        text=(
            'Husserl\'s term (Ideas I, \u00a7\u00a741\u201344), as read in 5/30: walking around a table, I only ever see it from '
            'one side at a time, so the table is always "more" than what is given right now, whereas the seeing itself '
            'is immanent and does not come in sides. The table is not a thing-in-itself behind its appearances; its '
            'transcendence lies in how it is given, which is never completely. Husserl says this holds for any mind that '
            'perceives a thing, even for God, so transcending humanity does not try to get rid of it. What can change is '
            'how much of that "more" a mind gets to.'
        ),
        short='Husserl: a thing is only ever given from one side at a time, for any mind; the third goal does not try to remove that.',
        sources=['5-transcending-biology'],
    ),
    dict(
        slug='transhumanism',
        name='Transhumanism',
        also=['posthuman'],
        pattern=r'transhumanis[mt]',
        sameAs=['https://en.wikipedia.org/wiki/Transhumanism', 'https://www.wikidata.org/wiki/Q194100'],
        text=(
            'The position that it is possible and desirable to use technology in order to go beyond the limits of human '
            'biology, up to a point where the result may be called posthuman, in the transhumanist sense of a being with '
            'capacities far beyond ours (not the "posthumanism" of the humanities). Julian Huxley made the word known in '
            'the 1950s, with "man remaining man, but transcending himself", meant for the species as a whole. 5/30 starts '
            'with the single someone instead and drops the "remaining man". The goal is not called transhumanism because '
            'an -ism is something that you hold, and a goal is something that you reach, or don\'t.'
        ),
        short='Using technology to go beyond the limits of human biology; an -ism one holds, where the third goal is something one reaches.',
        sources=['5-transcending-biology'],
    ),
    dict(
        slug='steerable-phenomenology',
        name='Steerable phenomenology',
        also=['steerable substrate', 'built substrate'],
        pattern=r'steerable',
        sameAs=[],
        text=(
            'A carrier that gets built, rather than born, can be built differently: a built substrate is a steerable '
            'one. With every gradual replacement step there is a bit of the carrier that does not have to repeat every '
            'limit of the tissue that it replaced, and where there is freedom like this the substrate becomes steerable, '
            'and with it, bit by bit, the phenomenology. Earlier described as the thing that the transhumanist has long '
            'dreamt of without once having thought it.'
        ),
        short='A built carrier need not repeat every limit of the tissue it replaced, so substrate and phenomenology become steerable.',
        sources=['5-transcending-biology'],
    ),
    dict(
        slug='lossless-q-storage',
        name='Lossless Q-storage',
        also=['forward arrow of personal time'],
        pattern=r'lossless q-storage',
        sameAs=[],
        text=(
            'From an unpublished working document of January 2026, "Synthetic Substrates and the Destruction of the '
            'Forward Arrow of Personal Time", which leans on Lyre\'s neurophenomenal structuralism. The "Q" stands for '
            'what an experience is like. The thesis is that the losses of memory are a contingent limit of biological '
            'storage, not a principled one: a substrate that stored an experience whole would give a memory as rich as the '
            'experience and the same at every recall, a personal time one can traverse. There is no guarantee that it can '
            'be built, and it involves no time travel, since only the playback changes and the substrate still runs '
            'forward. In the Ontology it sits under augmented cognition.'
        ),
        short='A hypothesised substrate that stores an experience whole, so memory is as rich as the experience; an open engineering question.',
        sources=['5-transcending-biology', '8-collective-mind'],
    ),
    dict(
        slug='world-line-fidelity',
        name='World-line fidelity',
        also=['continuity over similarity'],
        pattern=r'world-line fidelity',
        sameAs=[],
        text=(
            '5/30 states the Ontology\'s rule: the process world-line never breaks, and nothing gets traded against it, '
            'enhancement included. A great deal may change, but there cannot be a moment at which one stops and another '
            'takes over. At every step it has to be still you, the "continuer", not a promise that you stay the way you '
            'are, or about where you end up. That the world-line really goes on through such changes is a hypothesis.'
        ),
        short='The world-line never breaks, and nothing is traded against it, enhancement included; at every step it has to be still you.',
        sources=['5-transcending-biology'],
    ),
    dict(
        slug='substrate-independence',
        name='Substrate independence',
        also=['substrate-independence'],
        pattern=r'substrate[- ]independen',
        sameAs=[],
        text=(
            'The first of the three outcomes of the Ontology, listed as a state: mind no longer tied to biological '
            'substrate. It pairs with the goal of solving death: gradual replacement brings a carrier that is no longer '
            'the biology that we were born with. It is an outcome, not a goal, as it comes along with the work, and it '
            'was never meant as a guarantee, since how far it can go is decided by physics. 6/30 rejects the reading in '
            'which the substrate simply does not matter and keeps only the two words: what it means by them is the '
            're-creation of the brain\'s constraints in another material, which it calls physical substrate independence.'
        ),
        short='The first outcome of the Ontology: mind no longer tied to biological substrate, read as re-creating the brain\'s constraints in another material.',
        sources=['5-transcending-biology', '6-substrate-independence'],
    ),
    dict(
        slug='computational-substrate-independence',
        name='Computational substrate independence',
        also=[],
        pattern=r'computational substrate independence',
        sameAs=[],
        text=(
            'What Bostrom and classical mind uploading mean by substrate independence: a mind depends only on the '
            'computation, so whatever runs it will do. Bostrom wrote "substrate-independence" into his 2003 simulation '
            'argument, introducing it as "a common assumption in the philosophy of mind". 6/30 recounts how, in May '
            '2026, the series filed it under the commitments that fix the answers in advance.'
        ),
        short='A mind depends only on the computation, so whatever runs it will do; the assumption of classical mind uploading.',
        sources=['6-substrate-independence'],
    ),
    dict(
        slug='physical-substrate-independence',
        name='Physical substrate independence',
        also=[],
        pattern=r'physical substrate independence|substrate independence, in the physical sense',
        sameAs=[],
        text=(
            'What the series means by substrate independence: a mind depends on what its carrier physically does, so '
            'whatever does the same will do, be it biological or not. What it is supposed to become independent of is '
            'biology, and physics it never leaves. It claims less than the computational version, as a material that '
            'does the same physics also runs the same computation along the way, but not the other way round. Whether '
            'any material other than living cells can do the job is a question for experiments.'
        ),
        short='A mind depends on what its carrier physically does, so whatever does the same will do; independent of biology, never of physics.',
        sources=['6-substrate-independence'],
    ),
    dict(
        slug='multiple-realisability',
        name='Multiple realisability',
        also=['multiple realizability', 'weak multiple realisability'],
        pattern=r'multiple reali[sz]ab',
        sameAs=['https://en.wikipedia.org/wiki/Multiple_realizability', 'https://www.wikidata.org/wiki/Q1414884'],
        text=(
            'Putnam\'s argument in "Psychological Predicates" (1967): pain cannot be one particular state of the brain, '
            'as an octopus presumably feels pain with a brain built very differently, so pain has to be a functional '
            'state that many kinds of matter can realise. 6/30 starts instead from an observation within humans: we have '
            'somewhat the same kind of experience although our brains all differ, and slow-growing gliomas show living '
            'neural tissue taking over from living neural tissue. In that bio-to-bio sense (weak multiple '
            'realisability) it is evidenced; whether a different kind of substrate can take over is still open.'
        ),
        short='Many kinds of matter can realise the same mental state; evidenced bio-to-bio, open for a different kind of substrate.',
        sources=['6-substrate-independence', '9-multiple-realisability'],
    ),
    dict(
        slug='medium-independence',
        name='Medium independence',
        also=[],
        pattern=r'medium independen',
        sameAs=[],
        text=(
            'Gualtiero Piccinini\'s term: a computation does not care what its vehicles are made of, as long as they '
            'have the right degrees of freedom. He contrasts it with multiple realisability, via the mousetrap, which '
            'can be built in many ways but still has to catch actual mice. 6/30: classical mind uploading turned out to '
            'need medium independence for minds, while the series needs at most multiple realisability, as in the '
            'heart-lung machine, whose "lung" is a bundle of plastic fibres.'
        ),
        short='Piccinini: a computation does not care what its vehicles are made of; unlike a mousetrap, which still has to catch mice.',
        sources=['6-substrate-independence', '11-morphological-independence'],
    ),
    dict(
        slug='augmented-cognition',
        name='Augmented cognition',
        also=['augmentation'],
        pattern=r'augmented cognition',
        sameAs=[],
        text=(
            'The second outcome of the Ontology. 7/30 uses it neither in DARPA\'s sense (a programme from the early '
            '2000s about computers that adapt to the measured cognitive state of their user) nor in Engelbart\'s (1962) '
            'sense of better tools around a person, but for expanding the normal baseline of human cognition, and of '
            'conscious experience, which the name does not say. It is the bet that if a mind sits on a carrier that we '
            'built, the phenomenal space itself becomes steerable, not only the tools around it. Whatever takes what '
            'somebody can experience or do outside the range that they had before is called augmentation. In the '
            'Ontology\'s order it comes late, after preservation.'
        ),
        short='The second outcome: expanding the baseline of human cognition and conscious experience on a built, steerable carrier; it comes late.',
        sources=['7-augmented-cognition'],
    ),
    dict(
        slug='baseline-first',
        name='Baseline first',
        also=['the same baseline'],
        pattern=r'same baseline|baseline first|baseline to compare',
        sameAs=[],
        text=(
            '7/30: not to start from an augmented state as step one. First the same constraints, then changes to '
            'them, one at a time, and never both at once, with augmentation last. The baseline means the person\'s '
            'own, so how they experienced things and what they could do before, and no norm of what a human should '
            'be. It only shows what changed: that it is still the same someone hangs on the process having gone on, '
            'not on anybody\'s report. The baseline does not have to be better; it only has to come first.'
        ),
        short='First the same constraints, then changes one at a time, augmentation last; the baseline is the person\'s own.',
        sources=['7-augmented-cognition'],
    ),
    dict(
        slug='comparison-and-verification-problem',
        name='Comparison and verification problem',
        also=[],
        pattern=r'comparison and verification problem',
        sameAs=[],
        text=(
            '7/30\'s main objection to classical mind uploading and whole brain emulation: scanned, emulated and '
            'switched on, the substrate, the body, the surroundings and probably the capacities all change in one step. '
            'Whoever comes out has no before of their own to compare to, and from in there a loss looks exactly like a '
            'difference. An emulation saying that it is fine shows nothing, as it would say that either way.'
        ),
        short='When everything changes in one step, there is no before to compare to, and a loss looks exactly like a difference.',
        sources=['7-augmented-cognition'],
    ),
    dict(
        slug='transformative-experience',
        name='Transformative experience',
        also=[],
        pattern=r'transformative experiences?',
        sameAs=[],
        text=(
            'L. A. Paul\'s name for experiences, such as becoming a vampire or having a child, that one cannot judge '
            'from the outside beforehand. 7/30 uses it for the second reason to keep the baseline first: deciding for a '
            'new sense from the outside is like ordering from a menu in a language one does not speak, where the dish '
            'then also changes what one likes to eat. So if there is a sane place to decide such things from, it is a '
            'stable one, one step at a time.'
        ),
        short='L. A. Paul: experiences one cannot judge beforehand; so augmentation is best decided from a stable baseline.',
        sources=['7-augmented-cognition'],
    ),
    dict(
        slug='experience-machine',
        name='Experience machine',
        also=[],
        pattern=r'experience machine',
        sameAs=['https://en.wikipedia.org/wiki/Experience_machine', 'https://www.wikidata.org/wiki/Q5421060'],
        text=(
            'Robert Nozick\'s thought experiment. 7/30 links it to what people outside the field most often say about '
            '"being embodied in a computer simulation": that they would feel trapped. Most of them do not want new '
            'colours, but to stick around in their familiar environment, with their own place and their friends.'
        ),
        short='Nozick\'s thought experiment; in 7/30, why people say they would feel trapped in a computer simulation.',
        sources=['7-augmented-cognition'],
    ),
    dict(
        slug='collective-mind',
        name='Collective mind',
        also=['hivemind'],
        pattern=r'collective minds?|hive ?minds?|hivemindism',
        sameAs=[],
        text=(
            'The third and last outcome of the Ontology (8/30). As soon as synthetic consciousness has been achieved via '
            'hybrid mind uploading, there is technically the possibility to merge into one giant collective mind, with one '
            'process world-line instead of "society", and phenomenally conscious as a whole, not only smart as a whole the '
            'way a society or the internet can be. Most transhumanists assume that they stay single individuals. 8/30 '
            'expects it to start occasionally, to show something instead of telling it, until coming apart again is the '
            'exception. Whether one would then still be around as oneself is left open.'
        ),
        short='The third outcome: a merge into one giant, phenomenally conscious mind with one process world-line, instead of staying individuals.',
        sources=['8-collective-mind', '12-distributed-unification'],
    ),
    dict(
        slug='neurophenomenal-structuralism',
        name='Neurophenomenal structuralism',
        also=['Q-structure'],
        pattern=r'neurophenomenal structuralism|Q-structure',
        sameAs=[],
        text=(
            'Holger Lyre\'s view, which 8/30 takes seriously: what an experience is like is fixed by its position in a '
            'structure of relations to all other experiences (the Q-structure), and how that position gets activated, by '
            'the eyes or by a memory, should not matter. That it obviously does matter, as a remembered sunset is pale '
            'next to the one in front of you, is what the January 2026 essay explains with ecphoric reconstruction.'
        ),
        short='Lyre: what an experience is like is fixed by its position in a structure of relations to all other experiences.',
        sources=['8-collective-mind'],
    ),
    dict(
        slug='ecphoric-reconstruction',
        name='Ecphoric reconstruction',
        also=[],
        pattern=r'ecphoric',
        sameAs=[],
        text=(
            'The name 8/30 uses for how a biological brain remembers: it keeps a compressed, lossy version of an '
            'experience (its engram) and rebuilds the rest from priors at recall. So remembering lands somewhere near the '
            'original position in the structure of experiences and never exactly on it. Take that bottleneck away on a '
            'substrate built without the compression constraint, and a memory would be the full experience again '
            '(lossless Q-storage), if that can be built at all.'
        ),
        short='A brain keeps a lossy version of an experience and rebuilds the rest from priors, so a memory never lands exactly on the original.',
        sources=['8-collective-mind'],
    ),
    dict(
        slug='q-time-and-p-time',
        name='Q-time and P-time',
        also=['substrate time'],
        pattern=r'\bQ-time\b|\bP-time\b',
        sameAs=[],
        text=(
            'Two layers of time from the unpublished January 2026 essay. Q-time is personal, phenomenal time; P-time is '
            'substrate time, the physical time in which the substrate keeps moving forward like everything else. With a '
            'past that can be re-entered at full resolution, personal time turns from something one gets pushed through '
            'into something one can walk around in, like a DVD that can be rewound while the player does not get a day '
            'younger. The destruction of the forward arrow only ever happens in Q-time, and no dualism is implied: both '
            'stay within physics.'
        ),
        short='Personal, phenomenal time versus substrate time; only Q-time loses its forward arrow, and both stay within physics.',
        sources=['8-collective-mind'],
    ),
    dict(
        slug='branching-identity',
        name='Branching identity',
        also=['directed acyclic graph of selves'],
        pattern=r'branching identity|directed acyclic graph',
        sameAs=[],
        text=(
            'If one can go back into a past experiential state, one can also decide differently from there and see where '
            'it goes, so the history of what one has experienced stops being a simple line and turns into a graph with '
            'branches (a directed acyclic graph, a picture borrowed from Toby Ord). In 8/30 this is the intrapersonal, '
            'Q-time kind of hivemind: one substrate, one ongoing process, many of "me", and in P-time still exactly one person.'
        ),
        short='Re-entering past experiences turns a personal history into a graph with branches: many of "me", one person in P-time.',
        sources=['8-collective-mind'],
    ),
    dict(
        slug='distributed-unification',
        name='Distributed unification',
        also=['many nodes, one mind'],
        pattern=r'distributed unification',
        sameAs=[],
        text=(
            'An operational requirement of the Ontology: many nodes, one mind. A brain that gets replaced piece by piece is '
            'for a long time a mix of old tissue and new parts, and that mix has to be one mind the whole time and not two. '
            'If that can be done between the parts of one brain, 8/30 sees nothing in the method that would care whose '
            'skull the parts came from, which is why collective mind is an outcome and not a goal. 12/30 calls it the fourth '
            'and last operational requirement, with the Ontology\'s two lines "small node count unified" (the weak form) '
            'and "large-scale, graceful degradation" (the strong one), and notes that every brain is already distributed, yet unified.'
        ),
        short='Many nodes, one mind: during replacement, old tissue and new parts have to be one mind the whole time.',
        sources=['8-collective-mind', '12-distributed-unification'],
    ),
    dict(
        slug='show-dont-tell',
        name='Show, don\'t tell',
        also=[],
        pattern=r'show, don.t tell',
        sameAs=[],
        text=(
            'How someone multiplies 17 × 24 in their head can at best be described, and even a much better description '
            'fails to carry over what it is like (Feynman and Tukey both "counted", in different ways, and only found out '
            'by trying). 8/30 connects this with Wittgenstein: what can be shown cannot be said, and the beetle in the box. '
            'Whatever turns experience into signals and back is still telling, only with more channels; the moment '
            'something really gets shown, there is a bit less of "two heads" than before.'
        ),
        short='Words cannot carry over what an experience is like; really showing it means one shared phenomenal space.',
        sources=['8-collective-mind'],
    ),
    dict(
        slug='strong-multiple-realisability',
        name='Strong multiple realisability',
        also=['de novo tissue'],
        pattern=r'strong(?:ly)? multipl[ey] reali[sz]ab|weakly or strongly|strong form of multiple',
        sameAs=[],
        text=(
            'The strong form of the Ontology\'s first requirement (9/30). Weak multiple realisability holds if engrams or '
            'functions get shifted around from living tissue to living tissue inside one brain, which the serial lesion '
            'effect and slowly growing low-grade gliomas show to some degree. The strong form holds if de novo tissue, '
            'tissue that was never part of that brain and maybe is not even biological, can also store and implement the '
            'same functions. If only living de novo tissue can, hybrid mind uploading has to go towards extreme biology.'
        ),
        short='De novo tissue, never part of that brain and maybe not biological, can store and implement the same functions.',
        sources=['9-multiple-realisability'],
    ),
    dict(
        slug='operational-and-axiomatic-requirements',
        name='Operational and axiomatic requirements',
        also=['requirement'],
        pattern=r'operational and axiomatic|axiomatic requirement',
        sameAs=[],
        text=(
            'A requirement is something that has to be true about brains for hybrid mind uploading to have a chance at '
            'all. The Ontology has four of each kind. The operational ones (multiple realisability, continuer migration, '
            'morphological independence, distributed unification) are things a brain turns out to be able to do or not, '
            'so an experiment can come back with a no, and each has a weak and a strong form. The axiomatic ones '
            '(brain-centredness, methodological physicalism, non-organicism, scale separation) have to be granted before '
            'any of those experiments means anything, so each is taken in its least committal form.'
        ),
        short='Four operational requirements an experiment can answer, in weak and strong forms; four axiomatic ones granted in advance.',
        sources=['9-multiple-realisability', '12-distributed-unification', '13-brain-centredness'],
    ),
    dict(
        slug='lesion-momentum',
        name='Lesion momentum',
        also=[],
        pattern=r'lesion momentum',
        sameAs=[],
        text=(
            'The clinic\'s word for how fast a lesion grows, the variable that the gradual reorganisation principle hangs '
            'on. In rats ten days between two stages is too fast for a frontal cortex and twenty is enough; in people with '
            'low-grade gliomas about 4 mm a year is slow enough for speech and movement. In between there is apparently '
            'nothing, and 9/30 wants it as an actual measurement, a speed limit more accurate than "slower than a stroke".'
        ),
        short='How fast a lesion grows; the speed limit of gradual reorganisation, so far known only as "slower than a stroke".',
        sources=['9-multiple-realisability'],
    ),
    dict(
        slug='grandmothers-face-problem',
        name='Grandmother\'s face problem',
        also=[],
        pattern=r'grandmother.s face',
        sameAs=[],
        text=(
            'Slow lesions spare what is measurable from the outside, such as speech and motor function, which are '
            'retrieved all day long. But what about engrams that you are not aware of having until you recall them, such '
            'as the rarely retrieved memory of your grandmother\'s face? The only test for an engram is to retrieve it, '
            'and retrieving is an intervention that rehearses the trace and opens it up to change, so there is no '
            'baseline for the unmeasured ones, and forgetting does not feel like anything.'
        ),
        short='Rarely recalled engrams may be lost during slow reorganisation, and testing for them changes them.',
        sources=['9-multiple-realisability'],
    ),
    dict(
        slug='continuer-migration',
        name='Continuer migration',
        also=['continuer'],
        pattern=r'continuer migration',
        sameAs=[],
        text=(
            'The second requirement of the Ontology (10/30). It is about how the move has to go so that it is still you '
            'who arrives, and its one particular word, the continuer, brings the entire philosophy of personal identity '
            'along. 10/30 sets the thought experiments aside: whether psychological or physical continuity carries you '
            'through, what matters is the continuity of the human brain, kept running so that no accident or disease '
            'robs you of it.'
        ),
        short='How the move has to go so that it is still you who arrives; in 10/30, the continuity of the human brain.',
        sources=['10-continuer-migration', '12-distributed-unification'],
    ),
    dict(
        slug='morphological-independence',
        name='Morphological independence',
        also=[],
        pattern=r'morphological independence',
        sameAs=[],
        text=(
            'The third operational requirement of the Ontology (11/30): a mind tolerates local change and it tolerates '
            'major refactorisations, and size is the simplest refactorisation. Who says that a mechanistic neuron is '
            'literally the same size as the biological neuron that it replaces? On the coarse-grained view of 11/30, a '
            'delay is a length divided by a speed, so how big a replacement piece gets is decided by how slow its carriers '
            'are, with noise as the floor. Which parts of the NCC are like mass and which like radius is open.'
        ),
        short='A mind tolerates local change and major refactorisations, size included; delays can be kept over another length.',
        sources=['11-morphological-independence'],
    ),
    dict(
        slug='computational-irreducibility',
        name='Computational irreducibility',
        also=[],
        pattern=r'computational(?:ly)? irreducib|reducibility question',
        sameAs=['https://en.wikipedia.org/wiki/Computational_irreducibility'],
        text=(
            'Wolfram\'s term for processes whose outcome cannot be had any faster than by letting them run. 11/30 asks '
            'which parts of what the biological brain physically does can be shortcut into something else in a different '
            'substrate while still doing or harnessing physics: another route through physics to the same place, like a '
            'car train through a tunnel, not a simulation, like moving the car on a GPS map.'
        ),
        short='Wolfram: processes whose outcome cannot be had faster than by running them; in 11/30, which brain physics can be shortcut.',
        sources=['11-morphological-independence'],
    ),
    dict(
        slug='neural-correlate-of-consciousness',
        name='Neural correlate of consciousness',
        also=['NCC'],
        pattern=r'neural correlates? of consciousness|\bNCCs?\b',
        sameAs=['https://en.wikipedia.org/wiki/Neural_correlates_of_consciousness'],
        text=(
            '11/30 asks whether the NCC is physically bound to its size. Like the Sun swapped for a black hole of the same '
            'mass, which would keep the Earth on its orbit with a radius of about 3 km instead of 700000 km, some '
            'properties may have to be there in full (candidates: the delays and what is connected to what) and others '
            'may shrink (the lengths, given a slow enough carrier).'
        ),
        short='In 11/30, which of its properties are like mass, all of it needed, and which like radius, free to shrink.',
        sources=['11-morphological-independence'],
    ),
    dict(
        slug='barrow-scale',
        name='Barrow scale',
        proper='Barrow',
        also=[],
        pattern=r'barrow.s scale|barrow scale',
        sameAs=[],
        text=(
            'Barrow ranked civilisations by how small they can build, from things of their own size via genes, molecules '
            'and atoms to nuclei, particles and space-time itself, as the inward counterpart of Kardashev\'s scale of how '
            'much energy they use. 11/30 asks how far a brain could go down it, and guesses that a smaller and lighter '
            'carrier might be what allows solving death at larger scales.'
        ),
        short='Civilisations ranked by how small they can build; 11/30 asks how far down it a replaced brain could go.',
        sources=['11-morphological-independence'],
    ),
    dict(
        slug='epoche',
        name='Epoché',
        also=["Husserl's bracket"],
        pattern=r'epoch[eé]\b|husserl.s bracket',
        sameAs=['https://en.wikipedia.org/wiki/Epoch%C3%A9'],
        text=(
            'Husserl\'s bracket: no claims about brains or the world yet, only what\'s given to you as a conscious observer. '
            'In 12/30 it shows that whatever you experience comes together with the rest, as parts of one stream. It only '
            'gives how it seems, though, which can\'t tell how the thing is made, and it has to come off the moment somebody '
            'takes a scalpel to a brain.'
        ),
        short='Husserl\'s bracket: only what is given to a conscious observer, no claims about brains or the world yet.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='living-present',
        name='Living present',
        also=['synthesis of inner time'],
        pattern=r'living present|synthesis of inner time',
        sameAs=[],
        text=(
            'Husserl\'s name for the width of the now: the just-past is still held in it and the about-to-come is already '
            'expected. 12/30 takes this synthesis of inner time as the most basic form of a unity that consciousness does, '
            'and notes that pulling the parts of a brain apart sooner or later turns "how far apart" into "how wide is the now".'
        ),
        short='The now has a width: the just-past is still held in it and the about-to-come is already expected.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='binding-problem',
        name='Binding problem',
        also=['phenomenal binding problem'],
        pattern=r'binding problem',
        sameAs=['https://en.wikipedia.org/wiki/Binding_problem'],
        text=(
            'Why a pack of membrane-bound neurons isn\'t a "micro-experiential zombie", mind-dust with nobody home. David '
            'Pearce states it as a problem for physics and answers it with quantum coherence. 12/30 takes the problem as '
            'stated without following him there.'
        ),
        short='Why billions of separate neurons make one experience and not mind-dust with nobody home.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='microconsciousness',
        name='Microconsciousness',
        also=['microconsciousnesses'],
        pattern=r'microconsciousness',
        sameAs=[],
        text=(
            'Semir Zeki\'s conclusion from colour being perceived about 80 ms before motion: visual consciousness consists of '
            'many microconsciousnesses spread over space and time. In 12/30 it is part of the case that the unity Husserl '
            'describes is manufactured, out of parts that are centimetres and tens of milliseconds apart.'
        ),
        short='Zeki: visual consciousness as many microconsciousnesses spread over space and time.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='integrated-information-theory',
        name='Integrated information theory (IIT)',
        also=['IIT'],
        pattern=r'integrated information theory|\bIIT\b',
        sameAs=['https://en.wikipedia.org/wiki/Integrated_information_theory'],
        text=(
            'In 12/30, the one theory with an explicit criterion for when two things are one. Tononi and Koch expect one '
            'mind to fall apart into two quite abruptly as the corpus callosum is weakened step by step, and the opposite '
            'for a strong enough link between two brains. A part that\'s only simulated doesn\'t count for them, because a '
            'simulation has no causal power of its own.'
        ),
        short='Tononi and Koch\'s theory, with an explicit criterion for when two things are one mind.',
        sources=['8-collective-mind', '12-distributed-unification'],
    ),
    dict(
        slug='virtual-long-range-axons',
        name='Virtual long-range axons',
        also=['virtual axon'],
        pattern=r'virtual (?:long-range )?axons?',
        sameAs=[],
        text=(
            'The links that carry signals between the parts of a distributed brain, a term from the synconetics essay '
            '"Death is an Engineering Challenge". 12/30 points to work that already goes in this direction, such as living '
            'axon tracts grown in a hydrogel column and a neuromorphic chip that reconnected two cut-apart cultures, and '
            'notes that a virtual axon is only adequate where all that crosses is spikes and their timing.'
        ),
        short='Links that carry the signals between the parts of a distributed brain, adequate where only spikes and timing cross.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='ephaptic-coupling',
        name='Ephaptic coupling',
        also=[],
        pattern=r'ephaptic',
        sameAs=['https://en.wikipedia.org/wiki/Ephaptic_coupling'],
        text=(
            'Neurons influencing each other through the electric field rather than through synapses. In 12/30 it is a '
            'reason why a cut brain cannot always be bridged by virtual axons: in slices of hippocampus, slow waves keep '
            'running across a complete cut with nothing but the field carrying them over.'
        ),
        short='Neurons influencing each other through the electric field; a reason virtual axons are not always enough.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='china-brain',
        name='China brain',
        proper='China',
        also=['China brain thought experiment'],
        pattern=r'china brain',
        sameAs=['https://en.wikipedia.org/wiki/China_brain'],
        text=(
            'Ned Block\'s thought experiment in which people with two-way radios each "play" one neuron. 12/30 runs a '
            'modified version twice: in version one, China carries the mail across one cut tract, so the synapses on the '
            'other side still get actual spikes at the right times; in version two, China does the sums for a part that '
            'was taken out.'
        ),
        short='Block\'s nation of radio operators playing neurons; 12/30 separates carrying the signals from doing the sums.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='braid',
        name='Braid',
        also=['process braid'],
        pattern=r'\bbraids?\b',
        sameAs=[],
        text=(
            'Proposed in 12/30 as an alternative picture to the process world-line, which seems to imply that the process '
            'is in one place at each moment. In a braid every node is a strand, held together by the signals on their way '
            'between them, and it stays one braid although no single strand runs through all of it. Three rules keep it '
            'from coming apart: join before leave, no spares, no fission.'
        ),
        short='Every node a strand, held together by the signals between them; one braid although no strand runs through all of it.',
        sources=['12-distributed-unification'],
    ),
    dict(
        slug='galantai-scale',
        name="Galántai's scale",
        proper='Galántai',
        also=[],
        pattern=r'gal[aá]ntai',
        sameAs=[],
        text=(
            'Zoltan Galántai\'s ranking of civilisations by the size of the disaster that they can\'t survive, from a local '
            'one upwards. 11/30 finds it closest to a scale for solving death; in 12/30 you climb it by spreading out '
            'further, at the price of being slower to react as one mind.'
        ),
        short='Civilisations ranked by the size of the disaster they can survive; climbed by spreading out.',
        sources=['11-morphological-independence', '12-distributed-unification'],
    ),
    dict(
        slug='brain-centredness',
        name='Brain-centredness',
        also=['brain-centred'],
        pattern=r'brain-centred',
        sameAs=[],
        text=(
            'The first of the four axiomatic requirements in the Ontology (13/30). It is pragmatic and least metaphysical: '
            'if the brain is destroyed, you are gone, even if the rest of the body is kept alive, which is what brain death '
            'is. It shows that the brain is necessary, not that it is enough; how much else is needed, from intracranial '
            'pressure to the whole body, is left to be found out empirically, hence brain-centred and not brain-only.'
        ),
        short='The first axiomatic requirement: no brain, no you, whatever else is kept; necessary, not shown to be enough.',
        sources=['13-brain-centredness'],
    ),
    dict(
        slug='extended-mind',
        name='Extended mind',
        also=['extended mind hypothesis'],
        pattern=r'extended mind',
        sameAs=['https://en.wikipedia.org/wiki/Extended_mind_thesis'],
        text=(
            'Andy Clark and David Chalmers\'s hypothesis that a mind can reach beyond the skull: Otto, who has Alzheimer\'s, '
            'keeps everything in a notebook, and the notebook is a part of his mind as memory is a part of yours. In 13/30, '
            'if the notebook counts, then so does a phone or a spouse, and the definition of a mind becomes blurry.'
        ),
        short='Clark and Chalmers: Otto\'s notebook as part of his mind; in 13/30 a sign that the word "mind" gets blurry.',
        sources=['13-brain-centredness'],
    ),
    dict(
        slug='islands-of-awareness',
        name='Islands of awareness',
        also=[],
        pattern=r'islands of awareness',
        sameAs=[],
        text=(
            'Tim Bayne, Anil Seth and Marcello Massimini\'s term (2020) for experience in a brain, or a piece of one, that is '
            'cut off from every input and has no way of expressing anything, e.g. in isolated brains or organoids. 13/30 '
            'takes it to its limit: a whole human brain that develops in isolation and was never connected to anything.'
        ),
        short='Experience in a brain cut off from all input and output; 13/30 imagines a whole brain grown that way.',
        sources=['13-brain-centredness'],
    ),
    dict(
        slug='floating-man',
        name='Floating man',
        also=["Avicenna's floating man"],
        pattern=r'floating man',
        sameAs=['https://en.wikipedia.org/wiki/Floating_man'],
        text=(
            'Avicenna\'s thought experiment from a thousand years ago: a man created in mid-air with no sensation at all is '
            'still aware of himself. 13/30 notes that he is created fully formed, as an adult, unlike a brain that never got '
            'the chance to form anything.'
        ),
        short="Avicenna's man created in mid-air without sensation, still aware of himself.",
        sources=['13-brain-centredness'],
    ),
    dict(
        slug='brain-death',
        name='Brain death',
        also=['death by neurologic criteria'],
        pattern=r'brain death|neurologic criteria',
        sameAs=['https://en.wikipedia.org/wiki/Brain_death'],
        text=(
            'Death by neurologic criteria. In 13/30 it is the reason that brain-centredness is no thought experiment: such a '
            'body can be kept on a ventilator for days in order for its organs to be donated, and the "core object" of '
            'your phenomenality is gone.'
        ),
        short='Death by neurologic criteria: the body can be kept going, the you is gone.',
        sources=['13-brain-centredness'],
    ),
]

# Things a post may mention that are not glossary terms but have a clear
# external identity. Used only in JSON-LD 'mentions'.
MENTIONS = [
    dict(name='Artificial consciousness', pattern=r'artificial consciousness',
         sameAs=['https://en.wikipedia.org/wiki/Artificial_consciousness', 'https://www.wikidata.org/wiki/Q2993663']),
]
