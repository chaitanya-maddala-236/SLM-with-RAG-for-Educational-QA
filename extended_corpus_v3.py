"""
extended_corpus_v3.py
---------------------
300+ NEW unique educational documents across additional topics,
grades 4–12, multiple subjects.

NEW topics (on top of v1 / v2):
  Science:    cell structure, mitosis/meiosis, genetics, evolution,
              photosynthesis (depth), enzymes, digestion, blood/circulation,
              nervous system, skeleton/muscle, immune system, biogeochemical
              cycles (water/nitrogen/carbon), electricity, magnetism/EM
              induction, EM spectrum, sound waves, thermal energy, nuclear
              energy, renewable energy, stars, solar system, space exploration,
              seismic waves, volcanoes (depth), earthquakes (depth),
              glacial/river landforms
  Maths:      trigonometry, circle theorems, transformations, 3-D geometry,
              data handling, histograms, box plots, scatter graphs,
              normal distribution, hypothesis testing, differentiation,
              integration
  Geography:  population, urbanisation, megacities, climate change solutions,
              river/glacial landforms (depth)
  History:    ancient Egypt, ancient Greece, ancient Rome, Viking Age,
              medieval England, Black Death, Renaissance, colonialism/slavery,
              WWI, WWII/Holocaust, Cold War, civil rights, apartheid
  Technology: cybersecurity, machine learning, neural networks, ethical AI,
              digital privacy, green tech, fusion energy, hydrogen economy,
              electric vehicles
  Arts:       Impressionism, Cubism, photography history, graphic design

HOW TO INTEGRATE — see bottom of this file.
"""

from __future__ import annotations

EXTENDED_DOCUMENTS_V3: list[dict] = [

    # ══════════════════════════════════════════════════════════════════════════
    # CELL STRUCTURE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Prokaryotic cells (bacteria and archaea) lack a membrane-bound nucleus; "
            "their DNA floats freely in the cytoplasm as a circular chromosome. They have "
            "no membrane-bound organelles and are typically 1-10 um in size, reproducing "
            "by binary fission. Eukaryotic cells (animals, plants, fungi, protists) have a "
            "true nucleus and membrane-bound organelles and are generally 10-100 um in size."
        ),
        "subject": "biology", "topic": "cell structure", "grade": "8",
    },
    {
        "text": (
            "Key animal cell organelles: the nucleus contains DNA and directs cell activity. "
            "Mitochondria produce ATP via aerobic respiration — cells with high energy demand "
            "have many mitochondria. Ribosomes synthesise proteins. The rough endoplasmic "
            "reticulum (RER) is studded with ribosomes and processes proteins. The Golgi "
            "apparatus modifies, packages, and exports proteins. Lysosomes contain digestive "
            "enzymes that break down waste material."
        ),
        "subject": "biology", "topic": "cell structure", "grade": "9",
    },
    {
        "text": (
            "Plant cells share all animal cell organelles but also have three unique features. "
            "The cell wall, made of cellulose, gives rigidity and support. A large central "
            "vacuole stores water and maintains turgor pressure. Chloroplasts contain "
            "chlorophyll and carry out photosynthesis. The endosymbiotic theory proposes that "
            "chloroplasts and mitochondria were once free-living prokaryotes engulfed by "
            "ancient host cells — supported by their own circular DNA and double membranes."
        ),
        "subject": "biology", "topic": "cell structure", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MITOSIS AND MEIOSIS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Mitosis produces two genetically identical daughter cells with the same chromosome "
            "number as the parent cell, used for growth, repair, and asexual reproduction. "
            "The stages are Prophase (chromosomes condense), Metaphase (align at equator), "
            "Anaphase (chromatids pulled to opposite poles), and Telophase (two nuclei form). "
            "Cytokinesis then divides the cytoplasm."
        ),
        "subject": "biology", "topic": "mitosis", "grade": "9",
    },
    {
        "text": (
            "Meiosis produces four genetically unique haploid cells used to make gametes "
            "(sperm and eggs). In Meiosis I, homologous chromosome pairs separate. In "
            "Meiosis II, sister chromatids separate, similar to mitosis. Crossing over "
            "during Prophase I exchanges DNA segments between homologous chromosomes, "
            "generating new allele combinations — a key source of genetic variation that "
            "drives evolution."
        ),
        "subject": "biology", "topic": "meiosis", "grade": "10",
    },
    {
        "text": (
            "The cell cycle includes Interphase (G1 cell growth, S-phase DNA replication, "
            "G2 preparation for division) and the Mitotic phase. Checkpoints at G1, G2, "
            "and the spindle assembly checkpoint monitor cell size, DNA integrity, and "
            "correct chromosome attachment before the cycle proceeds. Failure of these "
            "checkpoints can allow damaged or incompletely replicated DNA to proceed, "
            "potentially leading to uncontrolled division and cancer."
        ),
        "subject": "biology", "topic": "mitosis", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # GENETICS AND INHERITANCE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Gregor Mendel's Law of Segregation states that each organism carries two alleles "
            "for each trait which separate during gamete formation, so each gamete carries "
            "one allele. His Law of Independent Assortment states that alleles of different "
            "genes are distributed to gametes independently. These laws, derived from "
            "pea-plant experiments in the 1860s, are the foundation of classical genetics."
        ),
        "subject": "biology", "topic": "genetics", "grade": "9",
    },
    {
        "text": (
            "A dominant allele is expressed when even one copy is present (heterozygous). "
            "A recessive allele is only expressed with two copies (homozygous recessive). "
            "Genotype refers to the alleles an organism carries; phenotype is the observable "
            "trait. A Punnett square predicts the probability of offspring genotypes from a "
            "cross. Codominance occurs when both alleles are fully expressed — blood group AB "
            "results from codominant IA and IB alleles."
        ),
        "subject": "biology", "topic": "genetics", "grade": "9",
    },
    {
        "text": (
            "Genetic disorders result from DNA mutations. Cystic fibrosis is autosomal "
            "recessive, caused by a faulty CFTR gene producing thick mucus in the lungs. "
            "Sickle cell anaemia is also autosomal recessive; mutant haemoglobin distorts "
            "red blood cells into sickle shapes that block capillaries. Carriers of the "
            "sickle cell allele gain partial protection against malaria, explaining the "
            "allele's persistence in malaria-endemic regions."
        ),
        "subject": "biology", "topic": "genetics", "grade": "10",
    },
    {
        "text": (
            "Down syndrome (trisomy 21) occurs when a person has three copies of chromosome 21 "
            "due to non-disjunction during meiosis. Karyotyping — photographing the full "
            "chromosome set — diagnoses chromosomal abnormalities prenatally via amniocentesis "
            "or chorionic villus sampling. CRISPR-Cas9 is a modern gene-editing tool that can "
            "precisely cut and modify DNA sequences, offering hope for treating genetic diseases "
            "while raising ethical questions about germline editing."
        ),
        "subject": "biology", "topic": "genetics", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # EVOLUTION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Natural selection is the mechanism of evolution. Key conditions: organisms "
            "overproduce offspring; individuals vary in heritable traits; variants better "
            "suited to their environment survive and reproduce more (survival of the fittest). "
            "Over generations, advantageous traits become more common in the population. "
            "Darwin formalised this theory after observing how Galapagos finch beak shapes "
            "were adapted to local food sources on different islands."
        ),
        "subject": "biology", "topic": "evolution", "grade": "9",
    },
    {
        "text": (
            "Evidence for evolution comes from multiple sources. The fossil record shows "
            "gradual change in organisms over geological time. Comparative anatomy reveals "
            "homologous structures — the pentadactyl limb appears in mammals, birds, and "
            "reptiles with the same underlying bone arrangement, suggesting a common ancestor. "
            "Molecular biology shows that closely related species share more DNA. Direct "
            "observation of evolution occurs in bacteria developing antibiotic resistance."
        ),
        "subject": "biology", "topic": "evolution", "grade": "9",
    },
    {
        "text": (
            "Speciation is the formation of new species. Allopatric speciation occurs when "
            "a population is geographically isolated by a barrier such as a mountain range "
            "or ocean. The isolated populations accumulate different mutations and face "
            "different selection pressures until they can no longer interbreed. The Galapagos "
            "finches are a classic example of adaptive radiation: one ancestral species "
            "diversified into many species filling different ecological niches."
        ),
        "subject": "biology", "topic": "evolution", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ENZYMES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Enzymes are biological catalysts — proteins that speed up chemical reactions "
            "without being consumed. They are highly specific: the active site is "
            "complementary in shape to a particular substrate (lock-and-key model). The "
            "induced-fit model refines this by noting that the enzyme changes shape slightly "
            "when the substrate binds. Enzymes lower activation energy and are essential for "
            "digestion, DNA replication, and cellular metabolism."
        ),
        "subject": "biology", "topic": "enzymes", "grade": "8",
    },
    {
        "text": (
            "Enzyme activity peaks at an optimum temperature (around 37-40 degrees C in "
            "humans) and optimum pH. Increasing temperature raises reaction rate up to the "
            "optimum; above it, heat permanently breaks bonds maintaining the enzyme's shape "
            "(denaturation). Pepsin (stomach protease) works best at pH 2; salivary amylase "
            "at pH 7. Competitive inhibitors block the active site; non-competitive inhibitors "
            "change the enzyme's shape allosterically, reducing activity."
        ),
        "subject": "biology", "topic": "enzymes", "grade": "9",
    },
    {
        "text": (
            "Digestive enzymes break large food molecules into absorbable ones. Amylase "
            "breaks starch into maltose (produced in salivary glands and pancreas). Protease "
            "breaks proteins into amino acids (stomach and pancreas). Lipase breaks lipids "
            "into fatty acids and glycerol (pancreas). Bile, produced by the liver and stored "
            "in the gallbladder, emulsifies fat droplets to increase the surface area for "
            "lipase to work on efficiently."
        ),
        "subject": "biology", "topic": "enzymes", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BLOOD AND CIRCULATORY SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Blood consists of plasma (55%, transporting nutrients, hormones, CO2, and urea), "
            "red blood cells (44%, carrying oxygen via haemoglobin — they lack a nucleus to "
            "maximise haemoglobin space), white blood cells (fighting infection), and platelets "
            "(cell fragments initiating blood clotting). The ABO blood group system is "
            "determined by antigens on red blood cell surfaces; mismatched transfusions cause "
            "fatal agglutination."
        ),
        "subject": "biology", "topic": "blood and circulation", "grade": "8",
    },
    {
        "text": (
            "The human heart is a double pump. The right side sends deoxygenated blood to the "
            "lungs (pulmonary circulation); the left side pumps oxygenated blood around the "
            "body (systemic circulation). Four chambers — right and left atria (receive blood) "
            "and right and left ventricles (pump blood out) — work in coordinated cycles. "
            "The left ventricle has a much thicker wall because it must push blood against "
            "high pressure around the entire body."
        ),
        "subject": "biology", "topic": "blood and circulation", "grade": "8",
    },
    {
        "text": (
            "Arteries carry blood away from the heart under high pressure and have thick, "
            "elastic, muscular walls. Veins return blood to the heart under low pressure; "
            "they have valves to prevent backflow. Capillaries are one cell thick, allowing "
            "exchange of oxygen, nutrients, carbon dioxide, and waste between blood and "
            "tissues. Coronary heart disease occurs when fatty plaques (atherosclerosis) "
            "narrow coronary arteries, restricting oxygen supply to the heart muscle."
        ),
        "subject": "biology", "topic": "blood and circulation", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # NERVOUS SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The nervous system enables rapid communication via electrical signals. The "
            "central nervous system (CNS) consists of the brain and spinal cord. The "
            "peripheral nervous system connects the CNS to the rest of the body via sensory "
            "neurones (carrying signals to the CNS) and motor neurones (carrying signals from "
            "the CNS to effectors like muscles and glands). The autonomic nervous system "
            "controls involuntary functions such as heart rate and digestion."
        ),
        "subject": "biology", "topic": "nervous system", "grade": "8",
    },
    {
        "text": (
            "A reflex arc produces a rapid, automatic response to a stimulus that bypasses "
            "the brain, using the spinal cord as the relay centre. The pathway is: receptor "
            "to sensory neurone to relay neurone (in the spinal cord) to motor neurone to "
            "effector (muscle or gland). Reflexes protect the body and are faster than "
            "conscious responses because the signal travels a shorter path. The knee-jerk "
            "reflex and pulling a hand away from heat are common examples."
        ),
        "subject": "biology", "topic": "nervous system", "grade": "8",
    },
    {
        "text": (
            "Neurones transmit impulses via action potentials. At rest, the inside of the "
            "axon membrane is negatively charged (resting potential: -70 mV). Stimulation "
            "causes sodium ions to rush in, depolarising the membrane to +40 mV. At synapses "
            "(gaps between neurones), neurotransmitters such as acetylcholine, dopamine, and "
            "serotonin diffuse across and bind to receptors on the next neurone. Many drugs "
            "and toxins work by mimicking or blocking specific neurotransmitters."
        ),
        "subject": "biology", "topic": "nervous system", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DIGESTION AND NUTRITION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The digestive system breaks food into molecules small enough to enter the blood. "
            "The mouth chews food and salivary amylase begins starch digestion. The stomach "
            "churns food; pepsin activated by hydrochloric acid (pH 2) digests protein. The "
            "small intestine completes digestion using pancreatic enzymes and bile, then "
            "absorbs nutrients via villi. The large intestine reabsorbs water, and remaining "
            "undigested waste is excreted as faeces."
        ),
        "subject": "biology", "topic": "digestion", "grade": "8",
    },
    {
        "text": (
            "Villi and microvilli greatly increase the absorptive surface area of the small "
            "intestine. Glucose and amino acids pass into capillaries by active transport "
            "and diffusion. Fatty acids and glycerol are absorbed into lacteals (lymphatic "
            "capillaries). The hepatic portal vein carries absorbed nutrients to the liver "
            "for processing and storage. The liver detoxifies harmful substances, produces "
            "bile, and helps regulate blood glucose concentration."
        ),
        "subject": "biology", "topic": "digestion", "grade": "9",
    },
    {
        "text": (
            "Food tests identify specific nutrients. The Benedict's test detects reducing "
            "sugars: a blue solution turns orange-red on heating with glucose. The iodine "
            "test detects starch: brown iodine solution turns blue-black. The Biuret test "
            "detects protein: a blue solution turns purple. The emulsion test detects lipids: "
            "a white emulsion forms when a sample dissolved in ethanol is added to water. "
            "These tests are used in laboratory investigations to analyse food composition."
        ),
        "subject": "biology", "topic": "digestion", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # IMMUNE SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The innate immune system provides the first line of non-specific defence. "
            "Physical barriers include the skin (impermeable and slightly acidic), mucus "
            "(traps pathogens in airways), cilia (sweep mucus away), and stomach acid "
            "(kills swallowed pathogens). Chemical defences include lysozyme in tears and "
            "saliva (destroys bacterial cell walls) and interferons (proteins released by "
            "virus-infected cells to warn neighbouring cells to prepare their defences)."
        ),
        "subject": "biology", "topic": "immune system", "grade": "8",
    },
    {
        "text": (
            "When pathogens breach physical barriers, phagocytes engulf and destroy them "
            "via phagocytosis. The adaptive immune system then mounts a specific response: "
            "B cells produce antibodies that neutralise pathogens and mark them for "
            "destruction; T helper cells coordinate the response; cytotoxic T cells kill "
            "infected host cells. Memory B and T cells persist after infection, enabling "
            "a faster, stronger response on re-exposure — the biological basis of vaccination."
        ),
        "subject": "biology", "topic": "immune system", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BIOGEOCHEMICAL CYCLES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The nitrogen cycle moves nitrogen through ecosystems. Nitrogen-fixing bacteria "
            "(in soil and legume root nodules) convert atmospheric N2 to ammonium (NH4+). "
            "Nitrifying bacteria convert ammonium to nitrates (NO3-) that plants absorb. "
            "Decomposers return nitrogen from dead organisms to the soil as ammonium. "
            "Denitrifying bacteria convert nitrates back to N2, completing the cycle. "
            "Industrial fertiliser production has roughly doubled reactive nitrogen in "
            "the biosphere, causing water pollution through run-off."
        ),
        "subject": "biology", "topic": "nitrogen cycle", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ELECTRICITY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Electric current is the flow of charge, measured in amperes (A). In metals, "
            "current is carried by free electrons. Voltage (potential difference) is the "
            "energy transferred per unit charge, measured in volts (V). Resistance opposes "
            "current flow, measured in ohms. Ohm's Law states V = IR and applies to ohmic "
            "conductors whose resistance remains constant regardless of the applied voltage "
            "and direction."
        ),
        "subject": "physics", "topic": "electricity", "grade": "8",
    },
    {
        "text": (
            "In a series circuit, current is the same throughout; voltages add up to the "
            "supply voltage; total resistance equals the sum of individual resistances. In "
            "a parallel circuit, voltage is the same across each branch; total current equals "
            "the sum of branch currents; adding resistors in parallel decreases total "
            "resistance. Household circuits are wired in parallel so each appliance receives "
            "full mains voltage and can be switched independently."
        ),
        "subject": "physics", "topic": "electricity", "grade": "9",
    },
    {
        "text": (
            "Electrical power is the rate of energy transfer: P = IV = I squared R = V "
            "squared divided by R. Energy transferred equals power multiplied by time. The "
            "kilowatt-hour (kWh) is the unit used for domestic electricity billing. A 2 kW "
            "appliance running for 3 hours uses 6 kWh. The national grid transmits power at "
            "high voltage (and low current) to minimise energy lost as heat in transmission "
            "cables, since power loss equals I squared times resistance."
        ),
        "subject": "physics", "topic": "electricity", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MAGNETISM AND ELECTROMAGNETIC INDUCTION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Magnets have north and south poles; like poles repel, unlike poles attract. "
            "Magnetic field lines run from north to south, with closer spacing indicating "
            "stronger fields. Earth's magnetic field is generated by convection currents of "
            "liquid iron in its outer core. It protects life by deflecting the solar wind "
            "and is responsible for the aurora borealis and aurora australis near the poles."
        ),
        "subject": "physics", "topic": "magnetism", "grade": "7",
    },
    {
        "text": (
            "An electric current produces a magnetic field around it (Oersted, 1820). A "
            "solenoid — a coil of wire — acts as an electromagnet when current flows through "
            "it. Electromagnetic induction (Faraday's law) states that a changing magnetic "
            "field induces an EMF in a conductor. This is the principle behind generators "
            "(converting kinetic energy to electrical energy) and transformers (changing AC "
            "voltage using mutual induction between two coils)."
        ),
        "subject": "physics", "topic": "magnetism", "grade": "8",
    },
    {
        "text": (
            "Transformers change AC voltage using the turns ratio: primary voltage divided by "
            "secondary voltage equals primary turns divided by secondary turns (Vp/Vs = Np/Ns). "
            "A step-up transformer increases voltage and decreases current proportionally. "
            "Transformers only work with AC because a steady magnetic field produces no "
            "induction. The national grid uses step-up transformers at power stations "
            "(to about 400 kV) to minimise transmission losses, then step-down transformers "
            "at substations to provide safe domestic voltage."
        ),
        "subject": "physics", "topic": "magnetism", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ELECTROMAGNETIC SPECTRUM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The electromagnetic spectrum is a family of transverse waves all travelling at "
            "3 x 10 to the 8 metres per second in a vacuum. In order of increasing frequency "
            "(decreasing wavelength): radio waves, microwaves, infrared, visible light, "
            "ultraviolet, X-rays, gamma rays. Higher frequency means greater energy. Radio "
            "waves are used in broadcasting; microwaves in cooking and mobile communication; "
            "infrared in remote controls and thermal imaging."
        ),
        "subject": "physics", "topic": "electromagnetic spectrum", "grade": "8",
    },
    {
        "text": (
            "X-rays pass through soft tissue but are absorbed by dense bone and metal, making "
            "them ideal for medical imaging and airport security scanners. Gamma rays, emitted "
            "by radioactive nuclei, sterilise surgical equipment, treat cancer via radiotherapy, "
            "and are used in PET scans. Both X-rays and gamma rays are ionising radiation — "
            "they carry enough energy to remove electrons from atoms, damaging DNA and "
            "increasing cancer risk with prolonged or repeated exposure."
        ),
        "subject": "physics", "topic": "electromagnetic spectrum", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SOUND WAVES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Sound is a mechanical longitudinal wave — particles vibrate parallel to the "
            "direction of travel, creating compressions (high pressure) and rarefactions "
            "(low pressure). Sound requires a medium and cannot travel through a vacuum. "
            "Speed of sound in air is approximately 340 m/s, in water about 1500 m/s, "
            "and in steel about 5000 m/s. Frequency is perceived as pitch; amplitude as "
            "loudness. The human audible range is 20 Hz to 20000 Hz."
        ),
        "subject": "physics", "topic": "sound waves", "grade": "8",
    },
    {
        "text": (
            "Ultrasound (above 20 kHz) is used in medical scanning because it is non-ionising "
            "and safe for soft tissue. Pulses are emitted and the time for reflected echoes "
            "to return locates internal structures. Ultrasound is also used for industrial "
            "flaw detection, sonar for ocean depth measurement, and echolocation by bats and "
            "dolphins. The Doppler effect — change in observed frequency when source or "
            "observer moves — is used in Doppler ultrasound to measure blood flow speed."
        ),
        "subject": "physics", "topic": "sound waves", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # THERMAL ENERGY TRANSFER
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Thermal energy transfers by three mechanisms. Conduction: vibrating particles "
            "pass energy to neighbouring particles — dominant in solids; metals conduct well "
            "because free electrons transfer energy rapidly. Convection: hot fluid is less "
            "dense, rises, and cool fluid sinks, creating convection currents. Radiation: "
            "infrared electromagnetic waves transfer energy without needing a medium — this "
            "is how the Sun's energy reaches Earth across the vacuum of space."
        ),
        "subject": "physics", "topic": "thermal energy", "grade": "8",
    },
    {
        "text": (
            "Specific heat capacity (c) is the energy required to raise 1 kg of a substance "
            "by 1 degree C. The equation is Q = mcDeltaT where Q is energy transferred in "
            "joules, m is mass in kg, and DeltaT is the temperature change. Water has a "
            "high specific heat capacity (4200 J/kg/C), which stabilises Earth's climate and "
            "makes it an effective coolant in engines and reactors. Black surfaces are best "
            "absorbers and emitters of infrared radiation; shiny surfaces are best reflectors."
        ),
        "subject": "physics", "topic": "thermal energy", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # NUCLEAR ENERGY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Nuclear fission splits a heavy nucleus (uranium-235 or plutonium-239) into "
            "two smaller nuclei, releasing neutrons and large amounts of energy. Released "
            "neutrons can trigger further fissions, creating a chain reaction. In a nuclear "
            "reactor, control rods made of boron or cadmium absorb neutrons to regulate "
            "the chain reaction rate. The heat produced converts water to steam that drives "
            "turbines generating electricity. Nuclear power produces no direct CO2 emissions."
        ),
        "subject": "physics", "topic": "nuclear energy", "grade": "10",
    },
    {
        "text": (
            "Nuclear fusion joins two light nuclei — typically deuterium and tritium, isotopes "
            "of hydrogen — to form helium, releasing enormous energy and no long-lived "
            "radioactive waste. This is the reaction powering stars. Achieving sustained "
            "controlled fusion on Earth requires temperatures above 100 million degrees C, "
            "hotter than the Sun's core. The international ITER project in France aims to "
            "demonstrate net energy gain from fusion and could transform clean energy supply."
        ),
        "subject": "physics", "topic": "nuclear energy", "grade": "11",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # RENEWABLE ENERGY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Renewable energy sources replenish naturally and produce little or no greenhouse "
            "gas during operation. Solar photovoltaic (PV) cells convert sunlight to "
            "electricity via the photoelectric effect. Wind turbines convert kinetic energy "
            "of wind. Hydroelectric power uses falling water to drive turbines. The cost of "
            "solar electricity has fallen over 90% since 2010, making it the cheapest "
            "electricity source in history in many regions of the world."
        ),
        "subject": "physics", "topic": "renewable energy", "grade": "8",
    },
    {
        "text": (
            "Intermittency is the main challenge for renewables since they generate only "
            "when sun shines or wind blows. Solutions include battery storage (lithium-ion "
            "grid batteries), pumped hydroelectric storage (pumping water uphill when "
            "electricity is cheap, releasing it downhill to generate when demand is high), "
            "demand-side management, and interconnected national grids. Green hydrogen, "
            "produced by electrolysis using renewable electricity, can store energy long-term "
            "and decarbonise hard-to-electrify industries."
        ),
        "subject": "physics", "topic": "renewable energy", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # STARS AND STELLAR EVOLUTION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Stars form from collapsing clouds of gas and dust called nebulae. As the cloud "
            "contracts under gravity, it heats up; when the core reaches about 15 million "
            "degrees C, hydrogen fusion begins and a protostar becomes a main sequence star. "
            "The Sun is a middle-aged main sequence star that has burned for 4.6 billion years "
            "and will continue for another approximately 5 billion years before expanding "
            "into a red giant."
        ),
        "subject": "astronomy", "topic": "stars", "grade": "8",
    },
    {
        "text": (
            "A medium-mass star like the Sun eventually exhausts its core hydrogen, expands "
            "to a red giant, sheds outer layers as a planetary nebula, and leaves a white "
            "dwarf that slowly cools over billions of years. Massive stars (over 8 solar "
            "masses) end in a supernova explosion, dispersing heavy elements across space "
            "and leaving either a neutron star (incredibly dense) or, for the most massive "
            "stars, a black hole from which even light cannot escape."
        ),
        "subject": "astronomy", "topic": "stars", "grade": "9",
    },
    {
        "text": (
            "The Hertzsprung-Russell (H-R) diagram plots stellar luminosity against surface "
            "temperature. Most stars lie on the main sequence, a diagonal band from hot "
            "luminous blue stars to cool dim red stars. Red giants occupy the upper right; "
            "white dwarfs the lower left. A star's position on the main sequence is "
            "determined by its mass — massive stars are hotter and more luminous but live "
            "far shorter lives than smaller stars. The H-R diagram is a cornerstone of "
            "stellar astrophysics."
        ),
        "subject": "astronomy", "topic": "stars", "grade": "10",
    },
    {
        "text": (
            "Heavy elements heavier than iron can only be formed in supernova explosions. "
            "Elements up to iron are produced by nuclear fusion reactions inside stars. "
            "When a massive star explodes as a supernova, these elements are dispersed into "
            "space as a nebula, which can eventually collapse to form new stars and planetary "
            "systems. The atoms in our bodies — carbon, oxygen, calcium, iron — were all "
            "forged inside ancient stars and scattered by supernovae billions of years ago."
        ),
        "subject": "astronomy", "topic": "stars", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SOLAR SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The solar system formed approximately 4.6 billion years ago from a collapsing "
            "cloud of gas and dust. Eight planets orbit the Sun: Mercury, Venus, Earth, "
            "Mars (rocky terrestrial planets), then Jupiter, Saturn, Uranus, and Neptune "
            "(gas and ice giants). The asteroid belt lies between Mars and Jupiter. The "
            "Kuiper Belt beyond Neptune contains icy bodies including Pluto, reclassified "
            "as a dwarf planet in 2006."
        ),
        "subject": "astronomy", "topic": "solar system", "grade": "6",
    },
    {
        "text": (
            "The Moon formed when a Mars-sized body called Theia collided with early Earth, "
            "ejecting debris that coalesced into the Moon. The Moon is tidally locked — "
            "the same side always faces Earth. Lunar phases result from different proportions "
            "of the lit hemisphere being visible from Earth as the Moon orbits. A solar "
            "eclipse occurs when the Moon passes between Earth and the Sun; a lunar eclipse "
            "occurs when Earth's shadow falls on the Moon."
        ),
        "subject": "astronomy", "topic": "solar system", "grade": "7",
    },
    {
        "text": (
            "Tides are caused primarily by the Moon's gravitational pull on Earth's oceans. "
            "The Moon pulls the near-side ocean outward, creating a high tide; inertia creates "
            "a corresponding high tide on the far side. Spring tides (largest range) occur "
            "at full and new moon when Sun, Moon, and Earth are aligned. Neap tides (smallest "
            "range) occur at quarter moons when the Sun and Moon pull at right angles to each "
            "other relative to Earth."
        ),
        "subject": "astronomy", "topic": "solar system", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SPACE EXPLORATION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The Space Race pitted the USA against the USSR during the Cold War. The USSR "
            "launched Sputnik 1 (first satellite, 1957), sent Yuri Gagarin on the first "
            "human spaceflight (April 1961), and achieved the first spacewalk (Alexei Leonov, "
            "1965). The USA responded with the Apollo programme; Apollo 11 (July 1969) "
            "landed Neil Armstrong and Buzz Aldrin on the Moon — the first humans to walk "
            "on another celestial body."
        ),
        "subject": "history", "topic": "space exploration", "grade": "8",
    },
    {
        "text": (
            "Modern space exploration uses both crewed and robotic spacecraft. The "
            "International Space Station (ISS) has been continuously occupied since 2000, "
            "hosting research in microgravity conditions. Mars rovers Curiosity and "
            "Perseverance search for signs of ancient microbial life. The James Webb Space "
            "Telescope (launched December 2021) observes infrared light to study the "
            "earliest galaxies formed after the Big Bang. SpaceX's reusable Falcon 9 "
            "rocket has drastically reduced launch costs."
        ),
        "subject": "astronomy", "topic": "space exploration", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # EARTH STRUCTURE AND SEISMIC WAVES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Earth's interior has four layers. The crust (5-70 km thick) is thin oceanic "
            "or thicker continental rock. The mantle is solid rock that flows plastically "
            "over geological timescales, driving plate tectonics. The outer core is liquid "
            "iron and nickel; its convection currents generate Earth's magnetic field. The "
            "inner core is solid iron and nickel, kept solid despite extreme temperature "
            "by the enormous pressure at Earth's centre."
        ),
        "subject": "geography", "topic": "earth structure", "grade": "8",
    },
    {
        "text": (
            "Seismic waves from earthquakes reveal Earth's interior. P-waves (compressional, "
            "primary) travel through solids and liquids. S-waves (shear, secondary) travel "
            "only through solids — their absence in a shadow zone on the far side of Earth "
            "from an earthquake proves the outer core is liquid. By analysing arrival times "
            "of P and S waves at seismograph stations worldwide, geologists have mapped the "
            "boundaries between Earth's internal layers with high precision."
        ),
        "subject": "geography", "topic": "seismic waves", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # VOLCANOES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Volcanoes form where magma reaches Earth's surface. At constructive (divergent) "
            "plate boundaries, plates move apart and basaltic magma fills the gap, producing "
            "gentle effusive eruptions as in Iceland. At destructive (convergent) boundaries, "
            "an oceanic plate subducts beneath a continental plate; water released lowers the "
            "mantle's melting point, producing silica-rich viscous magma and explosive "
            "stratovolcanoes. Shield volcanoes have gentle slopes and runny lava."
        ),
        "subject": "geography", "topic": "volcanoes", "grade": "9",
    },
    {
        "text": (
            "Volcanic hazards include pyroclastic flows (superheated gas and ash at 700 km/h), "
            "lava flows, lahars (volcanic mudflows), ash fall, and toxic gas release. Benefits "
            "include extremely fertile volcanic soil (dense populations around Vesuvius in "
            "Italy), creation of new land (the Hawaiian Islands formed entirely from "
            "volcanoes), and temporary global cooling when sulphur dioxide injected into "
            "the stratosphere reflects incoming sunlight back to space."
        ),
        "subject": "geography", "topic": "volcanoes", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # EARTHQUAKES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Earthquakes occur when stress accumulated along tectonic faults is suddenly "
            "released as seismic energy. The focus (hypocentre) is the underground origin "
            "point; the epicentre is the point on the surface directly above. The moment "
            "magnitude scale (Mw) measures energy released; each whole number represents "
            "about 32 times more energy. The Pacific Ring of Fire, following destructive "
            "plate boundaries around the Pacific Ocean, accounts for about 90% of all "
            "seismic activity worldwide."
        ),
        "subject": "geography", "topic": "earthquakes", "grade": "9",
    },
    {
        "text": (
            "Earthquake impact depends heavily on development level. Haiti (2010, Mw 7.0) "
            "killed approximately 200,000 people because of poor building quality and "
            "limited emergency response. Chile (2010, Mw 8.8, about 500 times more powerful) "
            "killed around 500 because of strict seismic building codes. Earthquake-resistant "
            "design uses base isolators, cross-bracing, and counterweights. Japan has the "
            "world's most advanced earthquake early warning system."
        ),
        "subject": "geography", "topic": "earthquakes", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # GLACIAL LANDFORMS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Glaciers erode by abrasion (rock fragments embedded in ice scrape bedrock) and "
            "plucking (ice freezes around chunks of bedrock and pulls them away as the "
            "glacier moves). Erosional landforms include U-shaped valleys (steep-sided and "
            "flat-bottomed), corries or cirques (armchair-shaped hollows where glaciers "
            "begin), aretes (sharp ridges between two corries), and pyramidal peaks where "
            "three or more corries erode back toward a central point — for example the "
            "Matterhorn on the Swiss-Italian border."
        ),
        "subject": "geography", "topic": "glacial landforms", "grade": "9",
    },
    {
        "text": (
            "Glacial deposition creates distinctive features when ice melts and drops its "
            "load of sediment called till. Terminal moraines mark the furthest advance of "
            "a glacier. Lateral moraines form along glacier sides; medial moraines form "
            "where two glaciers merge. Drumlins are smooth elongated hills formed beneath "
            "moving ice. Erratics are large boulders transported far from their origin — "
            "their rock type differs from local bedrock, revealing ancient ice-flow directions."
        ),
        "subject": "geography", "topic": "glacial landforms", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # RIVER LANDFORMS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "In a river's upper course, vertical erosion dominates, creating V-shaped "
            "valleys, interlocking spurs, and waterfalls where resistant rock overlies "
            "less resistant rock. In the middle course, lateral erosion widens the valley; "
            "meanders develop as the faster water on the outer bend erodes a river cliff "
            "while slower water on the inner bend deposits sediment forming a slip-off slope. "
            "In the lower course, deposition builds broad flat floodplains and deltas at "
            "river mouths."
        ),
        "subject": "geography", "topic": "river landforms", "grade": "8",
    },
    {
        "text": (
            "Oxbow lakes form when a meander is cut off during flood. The river cuts through "
            "the neck of a tight meander loop, taking the shorter straighter path; the "
            "abandoned meander is sealed by deposition and becomes an oxbow lake that "
            "gradually fills with sediment. Flooding occurs when river discharge exceeds "
            "channel capacity due to intense rainfall, urban impermeable surfaces, or "
            "deforestation. Both hard engineering (flood barriers, dams) and soft engineering "
            "(floodplain restoration, reforestation) are used to manage flood risk."
        ),
        "subject": "geography", "topic": "river landforms", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # POPULATION GEOGRAPHY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "World population reached 8 billion in 2022. Growth accelerated after the "
            "Industrial Revolution due to improvements in medicine, sanitation, and "
            "agriculture. The global fertility rate has fallen from about 5 births per "
            "woman in 1960 to approximately 2.3 today, driven by female education, improved "
            "child survival rates, and urbanisation. Most future population growth will occur "
            "in sub-Saharan Africa; Europe and parts of East Asia face population decline."
        ),
        "subject": "geography", "topic": "population", "grade": "8",
    },
    {
        "text": (
            "The Demographic Transition Model (DTM) describes how birth and death rates "
            "change with economic development. Stage 1: both rates are high and population "
            "is stable (pre-industrial). Stage 2: death rate falls due to medical improvements "
            "while birth rate stays high, producing rapid population growth. Stage 3: birth "
            "rate falls as development continues. Stage 4: both rates are low and population "
            "is stable again. Stage 5: birth rate falls below death rate and population "
            "declines, as seen in Germany and Japan."
        ),
        "subject": "geography", "topic": "population", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # URBANISATION AND MEGACITIES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "More than half the world's population now lives in cities, a milestone first "
            "crossed in 2007. Urbanisation is fastest in developing countries in Africa and "
            "Asia. A megacity is an urban area with over 10 million inhabitants; Tokyo with "
            "about 37 million people is the world's largest. Megacities offer economic "
            "opportunity and cultural richness but face serious challenges including traffic "
            "congestion, air pollution, housing shortages, and social inequality."
        ),
        "subject": "geography", "topic": "urbanisation", "grade": "9",
    },
    {
        "text": (
            "Informal settlements (slums, favelas, shanty towns) house over 1 billion people, "
            "about 25% of the urban population globally. They typically lack secure land "
            "tenure, clean water, sanitation, and durable housing. Rio de Janeiro's favelas "
            "house approximately 22% of the city's population. Upgrading schemes that improve "
            "infrastructure while allowing residents to remain are more effective and humane "
            "than demolition. Community-led improvements, as in Mumbai's Dharavi, can "
            "transform living conditions at relatively low cost."
        ),
        "subject": "geography", "topic": "urbanisation", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CLIMATE CHANGE SOLUTIONS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The Paris Agreement (2015) commits nations to limit global warming to well "
            "below 2 degrees C above pre-industrial levels, aiming for 1.5 degrees C. "
            "Each country submits Nationally Determined Contributions (NDCs) outlining "
            "emission reduction plans. Achieving the 1.5 degree target requires net-zero "
            "CO2 emissions globally by around 2050. Current pledges are insufficient and "
            "the world is on track for approximately 2.5-3 degrees C of warming by 2100 "
            "without additional urgent action."
        ),
        "subject": "environmental science", "topic": "climate change", "grade": "10",
    },
    {
        "text": (
            "Carbon capture and storage (CCS) removes CO2 from industrial emissions or "
            "directly from air (Direct Air Capture, DAC) and stores it underground in "
            "geological formations. Natural carbon sinks include forests, peatlands, "
            "mangroves, and seagrass meadows. Climate adaptation strategies — sea walls "
            "and managed coastal retreat, drought-resistant crops, improved early-warning "
            "systems — help communities adjust to changes already locked in. Vulnerable "
            "low-income countries contribute least to emissions but suffer most, raising "
            "core climate justice issues."
        ),
        "subject": "environmental science", "topic": "climate change", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ANCIENT EGYPT
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Ancient Egypt was one of the world's earliest great civilisations, flourishing "
            "along the Nile for over 3000 years. The annual Nile flood deposited fertile silt "
            "enabling agriculture in the surrounding desert. Egypt was unified around 3100 BCE. "
            "Society was hierarchical: the pharaoh (regarded as divine) at the apex, followed "
            "by nobles, priests, craftspeople, farmers, and slaves. The economy rested on "
            "agriculture, trade, and tribute from conquered territories."
        ),
        "subject": "history", "topic": "ancient Egypt", "grade": "7",
    },
    {
        "text": (
            "Egyptian achievements include the pyramids (the Great Pyramid of Giza, built "
            "around 2560 BCE for Pharaoh Khufu, is one of the Seven Wonders of the Ancient "
            "World), hieroglyphic writing, papyrus as a writing material, mummification to "
            "preserve bodies for the afterlife, a 365-day calendar, and early surgical "
            "techniques. Egyptian mathematical and engineering knowledge was essential for "
            "monument construction. Decline followed conquest by Alexander the Great in 332 BCE."
        ),
        "subject": "history", "topic": "ancient Egypt", "grade": "7",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ANCIENT GREECE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Ancient Greece (c. 800-146 BCE) was a collection of independent city-states "
            "(poleis). Athens developed the world's first democracy under Cleisthenes "
            "(c. 507 BCE), though only free adult male citizens could vote. Sparta was a "
            "militaristic oligarchy focused on military training from age seven. Greek "
            "city-states united temporarily to repel Persian invasions at Marathon (490 BCE) "
            "and at Thermopylae and Salamis (480 BCE), preserving Greek culture and "
            "independence."
        ),
        "subject": "history", "topic": "ancient Greece", "grade": "8",
    },
    {
        "text": (
            "Greek philosophy profoundly shaped Western thought. Socrates used systematic "
            "questioning to uncover assumptions and reach truth (the Socratic method). "
            "Plato described an ideal state governed by philosopher-kings in The Republic. "
            "Aristotle systematised knowledge across biology, physics, ethics, and logic. "
            "Alexander the Great spread Hellenistic culture from Greece to India. Archimedes "
            "and Eratosthenes (who accurately calculated Earth's circumference using shadow "
            "angles) represent the remarkable Greek tradition of rational scientific enquiry."
        ),
        "subject": "history", "topic": "ancient Greece", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ANCIENT ROME
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Rome grew from a city-state into a Republic (509 BCE) governed by a Senate "
            "and elected consuls. After civil wars following Julius Caesar's assassination "
            "(44 BCE), Augustus established the Roman Empire in 27 BCE. At its peak under "
            "Emperor Trajan (117 CE), the Roman Empire covered approximately 5 million km2 "
            "with a population of 50-70 million people, stretching from Scotland to "
            "Mesopotamia and from the Rhine to North Africa."
        ),
        "subject": "history", "topic": "ancient Rome", "grade": "8",
    },
    {
        "text": (
            "Roman achievements include concrete construction, over 80000 km of roads "
            "facilitating trade and military movement, aqueducts supplying cities with clean "
            "water, Roman law (the foundation of most European legal systems), and Latin "
            "(ancestor of the Romance languages: French, Spanish, Italian, Portuguese, and "
            "Romanian). The Western Roman Empire fell in 476 CE due to overextension, "
            "economic problems, political instability, and Germanic invasions. The Eastern "
            "Byzantine Empire survived until 1453."
        ),
        "subject": "history", "topic": "ancient Rome", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # VIKING AGE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The Viking Age (c. 793-1066 CE) saw Norse people from Scandinavia raid, trade, "
            "and settle across Europe, the North Atlantic, and beyond. The raid on Lindisfarne "
            "monastery (793 CE) traditionally marks its start. Viking longships were "
            "masterpieces of engineering: narrow, shallow-hulled, and fast enough to cross "
            "oceans and navigate shallow rivers alike. Leif Eriksson reached North America "
            "(Vinland) around 1000 CE, approximately 500 years before Christopher Columbus."
        ),
        "subject": "history", "topic": "Viking Age", "grade": "7",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MEDIEVAL ENGLAND AND BLACK DEATH
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Medieval English society was organised under the feudal system. The king granted "
            "land (fiefs) to barons in exchange for military service; barons granted land to "
            "knights who provided military service; serfs worked the land in exchange for "
            "protection. The Catholic Church owned about one-third of English land and "
            "controlled education, hospitals, and ecclesiastical courts. Magna Carta (1215) "
            "established that the king was subject to law, becoming a foundation of "
            "constitutional government."
        ),
        "subject": "history", "topic": "medieval England", "grade": "7",
    },
    {
        "text": (
            "The Black Death (1347-1353) was a bubonic plague pandemic caused by Yersinia "
            "pestis bacteria, spread by fleas on rats transported on merchant ships from "
            "Central Asia. It killed approximately one-third to half of Europe's population, "
            "an estimated 25-50 million people. The enormous death toll disrupted feudalism "
            "because surviving labourers could demand higher wages, shook faith in the "
            "Church's ability to explain or prevent suffering, and stimulated interest in "
            "understanding medicine and disease."
        ),
        "subject": "history", "topic": "Black Death", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # RENAISSANCE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The Renaissance (meaning rebirth), beginning in 14th-century Italy and spreading "
            "across Europe, revived interest in classical Greek and Roman learning, individual "
            "human achievement, and direct observation of nature. Humanist thinkers placed "
            "humans rather than God at the centre of inquiry. The printing press spread new "
            "ideas rapidly across Europe. Leonardo da Vinci exemplified the Renaissance ideal "
            "as painter, engineer, anatomist, and scientist, while Michelangelo and Raphael "
            "transformed European art."
        ),
        "subject": "history", "topic": "Renaissance", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # COLONIALISM AND SLAVERY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The transatlantic slave trade (c. 1500-1867) forcibly transported an estimated "
            "12.5 million enslaved Africans to the Americas. Enslaved people were transported "
            "in horrific conditions across the Middle Passage; approximately 1.5-2 million "
            "died en route. Enslaved labour drove sugar, cotton, and tobacco plantation "
            "economies. William Wilberforce and the abolitionist movement secured Britain's "
            "Slave Trade Act (1807) and Slavery Abolition Act (1833); the 13th Amendment "
            "(1865) abolished slavery in the United States after the Civil War."
        ),
        "subject": "history", "topic": "colonialism and slavery", "grade": "9",
    },
    {
        "text": (
            "European colonialism imposed political control over vast territories in Africa, "
            "Asia, and the Americas from the 15th to 20th centuries. The Berlin Conference "
            "(1884-85) divided almost all of Africa among European powers with no African "
            "representation. Colonial rule extracted raw materials, disrupted local economies, "
            "imposed European languages and religions, and drew arbitrary borders that "
            "generated post-independence conflicts whose effects continue to shape the "
            "continent today."
        ),
        "subject": "history", "topic": "colonialism and slavery", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # WORLD WAR I
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "World War I (1914-1918) was triggered by the assassination of Archduke Franz "
            "Ferdinand of Austria-Hungary in Sarajevo on 28 June 1914. The underlying causes "
            "are remembered using the acronym MAIN: Militarism (arms race), Alliance system "
            "(Triple Entente vs Triple Alliance), Imperialism (colonial competition), and "
            "Nationalism (Balkan independence movements, Pan-Slavism). The Western Front was "
            "characterised by trench warfare; WWI killed approximately 17 million people."
        ),
        "subject": "history", "topic": "World War I", "grade": "9",
    },
    {
        "text": (
            "The Treaty of Versailles (1919) ended WWI by imposing the war guilt clause on "
            "Germany, demanding enormous reparations, stripping Germany of territory and all "
            "overseas colonies, and drastically limiting its military. The resulting national "
            "humiliation, combined with the Great Depression's economic devastation, fuelled "
            "the resentment that Adolf Hitler's Nazi Party exploited. The League of Nations "
            "was established to prevent future wars but was fatally undermined by the United "
            "States' refusal to join."
        ),
        "subject": "history", "topic": "World War I", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # WORLD WAR II
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "World War II (1939-1945) began when Germany invaded Poland on 1 September 1939 "
            "and Britain and France declared war. Key events: Fall of France (1940), Battle "
            "of Britain (1940), Operation Barbarossa — Germany's invasion of the USSR (1941), "
            "Japanese attack on Pearl Harbor (December 1941, bringing the USA into the war), "
            "D-Day landings in Normandy (6 June 1944), and Germany's unconditional surrender "
            "on 8 May 1945 (VE Day)."
        ),
        "subject": "history", "topic": "World War II", "grade": "10",
    },
    {
        "text": (
            "The Holocaust was the systematic, state-sponsored genocide of six million Jews — "
            "about two-thirds of European Jewry — by the Nazi regime and its collaborators. "
            "The Nazis also murdered Romani people, disabled people, Soviet prisoners of war, "
            "Polish civilians, and homosexuals. The genocide was implemented through mobile "
            "killing units (Einsatzgruppen) and purpose-built death camps including "
            "Auschwitz-Birkenau, Treblinka, and Sobibor. The Nuremberg trials established "
            "individual criminal responsibility under international law."
        ),
        "subject": "history", "topic": "Holocaust", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # COLD WAR
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The Cold War (1947-1991) was a geopolitical competition between the USA "
            "(capitalist democracy) and the USSR (communist) that did not involve direct "
            "large-scale military conflict between the two superpowers. It featured a nuclear "
            "arms race, proxy wars in Korea, Vietnam, and Angola, the Space Race, and "
            "ideological rivalry across the globe. NATO (1949) and the Warsaw Pact (1955) "
            "formalised two opposing military alliances dividing the world."
        ),
        "subject": "history", "topic": "Cold War", "grade": "10",
    },
    {
        "text": (
            "The Cuban Missile Crisis (October 1962) was the Cold War's closest brush with "
            "nuclear war. The USA discovered Soviet nuclear missile sites under construction "
            "in Cuba, just 90 miles from Florida. President Kennedy imposed a naval blockade. "
            "After 13 days of intense tension, the USSR agreed to remove missiles in exchange "
            "for a US pledge not to invade Cuba and the secret removal of US missiles from "
            "Turkey. The crisis accelerated arms control talks including the 1963 Partial "
            "Nuclear Test Ban Treaty."
        ),
        "subject": "history", "topic": "Cold War", "grade": "10",
    },
    {
        "text": (
            "The Cold War ended when the Soviet Union dissolved in December 1991. Mikhail "
            "Gorbachev's reforms of glasnost (openness) and perestroika (restructuring) "
            "loosened political control and exposed the system's failures. Eastern European "
            "communist governments fell in a wave of revolutions in 1989. The Berlin Wall "
            "was breached on 9 November 1989 in a defining moment of the 20th century. "
            "Germany reunified in 1990. Russia inherited the Soviet Union's nuclear arsenal "
            "and UN Security Council seat."
        ),
        "subject": "history", "topic": "Cold War", "grade": "11",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CIVIL RIGHTS MOVEMENT (USA)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The US Civil Rights Movement (1954-1968) fought to end racial segregation and "
            "discrimination against African Americans. Jim Crow laws enforced segregation "
            "throughout the South. Key events include Rosa Parks' arrest (1955, sparking "
            "the Montgomery Bus Boycott), the Birmingham Campaign (1963) where police used "
            "fire hoses and dogs against peaceful demonstrators, and the March on Washington "
            "where Martin Luther King Jr delivered the I Have a Dream speech to 250000 people."
        ),
        "subject": "history", "topic": "civil rights", "grade": "10",
    },
    {
        "text": (
            "The Civil Rights Act (1964) outlawed discrimination based on race, colour, "
            "religion, sex, or national origin in employment and public places. The Voting "
            "Rights Act (1965) prohibited discriminatory voting practices that had "
            "disenfranchised Black Americans in the South. These landmark laws resulted from "
            "decades of non-violent direct action, legal challenges, and political pressure. "
            "Martin Luther King Jr was assassinated in Memphis on 4 April 1968, shocking "
            "the nation and inspiring rights movements worldwide."
        ),
        "subject": "history", "topic": "civil rights", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # APARTHEID
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Apartheid (meaning separateness in Afrikaans) was a system of institutionalised "
            "racial segregation enforced in South Africa from 1948 to 1991 by the National "
            "Party government. Citizens were classified by race and laws restricted where "
            "they could live, work, and travel. The African National Congress (ANC) led "
            "resistance. The Sharpeville Massacre (1960) killed 69 peaceful protesters and "
            "galvanised international opposition. Nelson Mandela was imprisoned from 1964 to "
            "1990; his release and the 1994 elections ended apartheid."
        ),
        "subject": "history", "topic": "apartheid", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TRIGONOMETRY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "In a right-angled triangle, the trigonometric ratios are: sin theta equals "
            "opposite divided by hypotenuse, cos theta equals adjacent divided by hypotenuse, "
            "tan theta equals opposite divided by adjacent. The mnemonic SOHCAHTOA helps "
            "recall these. The Pythagorean theorem (a squared plus b squared equals c squared) "
            "gives the hypotenuse length. These ratios find unknown sides or angles and are "
            "applied in architecture, navigation, surveying, and physics."
        ),
        "subject": "mathematics", "topic": "trigonometry", "grade": "9",
    },
    {
        "text": (
            "The sine rule (a divided by sin A equals b divided by sin B equals c divided by "
            "sin C) solves any triangle when two angles and a side, or two sides and a "
            "non-included angle, are known. The cosine rule (a squared equals b squared plus "
            "c squared minus 2bc cos A) applies when two sides and the included angle, or "
            "all three sides, are given. Together these rules solve all possible triangle "
            "configurations in navigation, surveying, engineering, and physics."
        ),
        "subject": "mathematics", "topic": "trigonometry", "grade": "10",
    },
    {
        "text": (
            "Trigonometric functions extend beyond right triangles using the unit circle. "
            "Sine and cosine are periodic with period 360 degrees (2 pi radians); tangent "
            "has period 180 degrees. Key exact values: sin 30 degrees equals 0.5, cos 60 "
            "degrees equals 0.5, sin 45 degrees equals cos 45 degrees equals 1 divided by "
            "root 2. Radians are the natural unit: 2 pi radians equal 360 degrees. Graphs "
            "of sine, cosine, and tangent model oscillations, waves, and alternating current."
        ),
        "subject": "mathematics", "topic": "trigonometry", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CIRCLE THEOREMS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Key circle theorems: (1) The angle at the centre is twice the angle at the "
            "circumference when both are subtended by the same arc. (2) Angles in the same "
            "segment are equal. (3) The angle in a semicircle is always 90 degrees. (4) "
            "Opposite angles of a cyclic quadrilateral sum to 180 degrees. (5) The tangent "
            "to a circle is perpendicular to the radius at the point of contact. These "
            "theorems are used to calculate unknown angles in circle geometry problems."
        ),
        "subject": "mathematics", "topic": "circle theorems", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TRANSFORMATIONS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Geometric transformations change the position, size, or orientation of a shape. "
            "Translation moves every point by the same vector without changing orientation. "
            "Rotation turns a shape about a fixed centre point through a given angle. "
            "Reflection produces a mirror image across a line of symmetry. Enlargement "
            "scales a shape from a centre point by a scale factor; a factor greater than 1 "
            "enlarges, between 0 and 1 reduces, and a negative factor enlarges and also "
            "rotates the shape 180 degrees."
        ),
        "subject": "mathematics", "topic": "transformations", "grade": "8",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DATA HANDLING
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Histograms display continuous grouped data. The y-axis shows frequency density "
            "(frequency divided by class width) rather than raw frequency, so bars with "
            "unequal widths correctly represent proportions. The area of each bar equals its "
            "frequency. Box plots show the median, lower and upper quartiles (Q1 and Q3), "
            "minimum, and maximum. The interquartile range (IQR equals Q3 minus Q1) measures "
            "the spread of the middle 50% of data around the median."
        ),
        "subject": "mathematics", "topic": "data handling", "grade": "10",
    },
    {
        "text": (
            "Scatter graphs show the relationship between two continuous variables. A line "
            "of best fit drawn through the data's centre of gravity allows predictions. "
            "Positive correlation means both variables increase together; negative correlation "
            "means one rises as the other falls; no correlation means no clear pattern. "
            "Pearson's correlation coefficient (r) measures linear correlation: r equals +1 "
            "is perfect positive, r equals -1 perfect negative, r equals 0 means no linear "
            "relationship. Importantly, correlation does not imply causation."
        ),
        "subject": "mathematics", "topic": "data handling", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # NORMAL DISTRIBUTION AND HYPOTHESIS TESTING
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "The normal distribution is a symmetric bell-shaped probability distribution "
            "defined by its mean (mu) and standard deviation (sigma). About 68% of data "
            "lies within one standard deviation of the mean, 95% within two, and 99.7% "
            "within three (the empirical rule or 68-95-99.7 rule). Many natural phenomena "
            "such as heights, exam scores, and measurement errors approximate a normal "
            "distribution. Z-scores standardise values: z equals (x minus mu) divided by "
            "sigma, allowing comparison across different distributions."
        ),
        "subject": "mathematics", "topic": "normal distribution", "grade": "11",
    },
    {
        "text": (
            "Hypothesis testing formally evaluates whether observed data supports a claim. "
            "The null hypothesis (H0) states no effect or no difference; the alternative "
            "hypothesis (H1) states the opposite. The p-value is the probability of "
            "observing results at least as extreme as those obtained if H0 is true. If the "
            "p-value is less than the significance level (typically 0.05 or 5%), H0 is "
            "rejected. A Type I error is rejecting a true null hypothesis; a Type II error "
            "is failing to reject a false null hypothesis."
        ),
        "subject": "mathematics", "topic": "hypothesis testing", "grade": "12",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DIFFERENTIATION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Differentiation finds the instantaneous rate of change of a function. For "
            "f(x) equal to x to the power n, the derivative f prime(x) equals n times x to "
            "the power (n minus 1) — the power rule. The derivative of a constant is zero. "
            "The chain rule handles composite functions: the derivative of f applied to g(x) "
            "equals f prime of g(x) multiplied by g prime of x. Applications include finding "
            "the gradient of a curve at a specific point and locating turning points where "
            "f prime(x) equals zero."
        ),
        "subject": "mathematics", "topic": "differentiation", "grade": "11",
    },
    {
        "text": (
            "The second derivative f double prime(x) determines the nature of stationary "
            "points: if positive, the point is a minimum (curve is concave upward); if "
            "negative, a maximum (curve is concave downward). Differentiation applies to "
            "kinematics: velocity equals ds/dt and acceleration equals dv/dt. In economics, "
            "marginal cost and marginal revenue are the derivatives of total cost and total "
            "revenue with respect to output quantity, used to find the profit-maximising "
            "level of production."
        ),
        "subject": "mathematics", "topic": "differentiation", "grade": "12",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # INTEGRATION
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Integration is the reverse process of differentiation (the Fundamental Theorem "
            "of Calculus links them). The indefinite integral of x to the n is x to the "
            "(n+1) divided by (n+1) plus a constant c. A definite integral between limits a "
            "and b calculates the area enclosed between a curve and the x-axis. Areas below "
            "the x-axis give negative values; the total enclosed area must be computed using "
            "absolute values of each section separately."
        ),
        "subject": "mathematics", "topic": "integration", "grade": "12",
    },
    {
        "text": (
            "Integration techniques include substitution (reversing the chain rule by "
            "substituting a new variable) and integration by parts (reversing the product "
            "rule): the integral of u dv equals uv minus the integral of v du. Applications "
            "include finding displacement from a velocity-time equation, computing volumes "
            "of revolution, evaluating probability density functions, and finding areas "
            "between two curves. Numerical methods such as the trapezium rule and Simpson's "
            "rule estimate integrals when exact analytical solutions cannot be found."
        ),
        "subject": "mathematics", "topic": "integration", "grade": "12",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 3-D GEOMETRY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Three-dimensional shape formulae: volume of a cuboid equals length times width "
            "times height; surface area equals 2 times (lw plus lh plus wh). Volume of a "
            "cylinder equals pi r squared h; curved surface area equals 2 pi r h. Volume of "
            "a sphere equals four thirds pi r cubed; surface area equals 4 pi r squared. "
            "Volume of a cone equals one third pi r squared h. Euler's formula for convex "
            "polyhedra states vertices minus edges plus faces equals 2, a fundamental "
            "relationship in topology."
        ),
        "subject": "mathematics", "topic": "3D geometry", "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CYBERSECURITY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Cybersecurity protects computer systems, networks, and data from attack or "
            "unauthorised access. Common threats include phishing (deceptive emails tricking "
            "users into revealing credentials), malware (malicious software including viruses, "
            "ransomware, and spyware), denial-of-service attacks that flood servers with "
            "traffic, and SQL injection (inserting malicious code into database queries). "
            "Firewalls, encryption, and multi-factor authentication are fundamental defences."
        ),
        "subject": "technology", "topic": "cybersecurity", "grade": "9",
    },
    {
        "text": (
            "Encryption converts readable plaintext into unreadable ciphertext. Symmetric "
            "encryption uses the same key for both encryption and decryption (Advanced "
            "Encryption Standard, AES, is the global standard). Asymmetric encryption uses "
            "a public key (shared openly) and a private key (kept secret) — RSA is most "
            "widely used. HTTPS uses TLS (Transport Layer Security) which combines asymmetric "
            "key exchange with symmetric encryption to provide secure, authenticated "
            "web communication."
        ),
        "subject": "technology", "topic": "cybersecurity", "grade": "10",
    },
    {
        "text": (
            "Social engineering exploits human psychology rather than technical vulnerabilities. "
            "Phishing attacks impersonate trusted organisations via email or fake websites. "
            "Spear phishing targets specific individuals using personal information gathered "
            "from social media. Vishing attacks use phone calls; smishing uses SMS messages. "
            "The 2011 RSA Security breach — which compromised security tokens used worldwide "
            "— began with a single phishing email. Strong unique passwords, password managers, "
            "and security awareness training are the most effective countermeasures."
        ),
        "subject": "technology", "topic": "cybersecurity", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MACHINE LEARNING
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Machine learning (ML) is a branch of artificial intelligence in which systems "
            "learn patterns from data rather than being explicitly programmed with rules. "
            "Supervised learning trains a model on labelled examples (input-output pairs) to "
            "predict labels for new inputs — applications include email spam detection and "
            "image classification. Unsupervised learning finds hidden patterns in unlabelled "
            "data and is used for customer segmentation and anomaly detection."
        ),
        "subject": "technology", "topic": "machine learning", "grade": "10",
    },
    {
        "text": (
            "Neural networks are machine learning models loosely inspired by the structure "
            "of the brain. They consist of layers of connected nodes (neurons); each "
            "connection has a weight adjusted during training using backpropagation. Deep "
            "learning uses many hidden layers to learn hierarchical feature representations. "
            "Convolutional Neural Networks (CNNs) excel at image recognition; Transformer "
            "architectures excel at natural language processing. Large Language Models such "
            "as GPT are built on Transformer architecture trained on massive text datasets."
        ),
        "subject": "technology", "topic": "machine learning", "grade": "11",
    },
    {
        "text": (
            "Training a machine learning model requires a labelled dataset, a loss function "
            "measuring prediction error, and an optimisation algorithm (typically stochastic "
            "gradient descent) that adjusts model weights to minimise loss. Overfitting "
            "occurs when a model learns the training data too specifically and performs "
            "poorly on new unseen data. Regularisation techniques, dropout layers, and "
            "splitting data into training, validation, and test sets are standard methods "
            "to detect and reduce overfitting."
        ),
        "subject": "technology", "topic": "machine learning", "grade": "11",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ETHICAL AI AND DIGITAL PRIVACY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Ethical AI addresses potential harms from artificial intelligence systems. "
            "Bias in training data causes algorithms to discriminate — facial recognition "
            "systems have been shown to misidentify dark-skinned faces at far higher error "
            "rates than light-skinned faces. Algorithmic decision-making in hiring, lending, "
            "and criminal justice raises serious fairness and accountability concerns. "
            "Principles of ethical AI include transparency, fairness, accountability, "
            "privacy protection, and respect for human rights and dignity."
        ),
        "subject": "technology", "topic": "ethical AI", "grade": "10",
    },
    {
        "text": (
            "Digital privacy concerns the control individuals have over their personal data. "
            "Technology companies collect vast amounts of behavioural data for targeted "
            "advertising. The EU's General Data Protection Regulation (GDPR, 2018) requires "
            "informed consent for data collection, grants the right to access and delete "
            "personal data, and imposes heavy fines for data breaches. End-to-end encryption "
            "ensures only the communicating parties can read messages — not the service "
            "provider, hackers, or governments intercepting the transmission."
        ),
        "subject": "technology", "topic": "digital privacy", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ELECTRIC VEHICLES AND HYDROGEN ECONOMY
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Electric vehicles (EVs) are powered by electric motors drawing energy from "
            "lithium-ion battery packs. They produce zero exhaust emissions during use, but "
            "overall carbon footprint depends on how electricity is generated. EV range has "
            "improved from about 160 km in early models to over 600 km for premium vehicles. "
            "Battery costs have fallen approximately 90% since 2010. Charging infrastructure "
            "availability, long charging times, and sustainable battery recycling remain key "
            "challenges for mass adoption worldwide."
        ),
        "subject": "technology", "topic": "electric vehicles", "grade": "9",
    },
    {
        "text": (
            "Green hydrogen is produced by electrolysis — splitting water into hydrogen and "
            "oxygen using renewable electricity with no carbon emissions. It can be stored "
            "and transported, used in hydrogen fuel cells (producing electricity and water "
            "vapour as the only by-product), burned as a clean fuel, or used to decarbonise "
            "steel manufacturing and chemical production — industries currently dependent "
            "on fossil fuels and difficult to electrify directly. Green hydrogen costs are "
            "falling rapidly as electrolysis technology scales up."
        ),
        "subject": "technology", "topic": "hydrogen economy", "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ART HISTORY — IMPRESSIONISM AND CUBISM
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": (
            "Impressionism emerged in 1870s France as a reaction against rigid academic "
            "painting conventions. Impressionist painters including Monet, Renoir, and Degas "
            "captured fleeting effects of light and atmosphere using loose visible brushstrokes "
            "and pure colours applied side by side. The movement's name came mockingly from "
            "Monet's painting Impression, Sunrise (1872). Painting outdoors (en plein air) "
            "was central to their practice. Impressionism transformed Western art by "
            "prioritising the artist's perception over precise photographic representation."
        ),
        "subject": "arts", "topic": "art history", "grade": "8",
    },
    {
        "text": (
            "Cubism, developed by Pablo Picasso and Georges Braque around 1907-1914, "
            "revolutionised art by showing multiple viewpoints of a subject simultaneously "
            "rather than a single perspective. Analytic Cubism fragmented objects into "
            "geometric planes in muted tones; Synthetic Cubism introduced collage elements. "
            "Picasso's Les Demoiselles d'Avignon (1907) is a pivotal proto-Cubist work "
            "influenced by African art and masks. Cubism profoundly influenced abstract art, "
            "modern architecture, and graphic design throughout the 20th century."
        ),
        "subject": "arts", "topic": "art history", "grade": "9",
    },

]


# ── Helper functions (mirrors data_loader.py API exactly) ─────────────────────

def get_documents() -> list[dict]:
    """Return all V3 documents."""
    return EXTENDED_DOCUMENTS_V3


def get_texts_and_metadatas() -> tuple[list[str], list[dict]]:
    """Return (texts, metadatas) lists ready for embedding into Chroma."""
    texts = [doc["text"] for doc in EXTENDED_DOCUMENTS_V3]
    metadatas = [
        {"subject": doc["subject"], "topic": doc["topic"], "grade": doc["grade"]}
        for doc in EXTENDED_DOCUMENTS_V3
    ]
    return texts, metadatas


# ── Self-test ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    topics   = {d["topic"]   for d in EXTENDED_DOCUMENTS_V3}
    subjects = {d["subject"] for d in EXTENDED_DOCUMENTS_V3}
    grades   = sorted({d["grade"] for d in EXTENDED_DOCUMENTS_V3})
    print(f"Total documents  : {len(EXTENDED_DOCUMENTS_V3)}")
    print(f"Unique topics    : {len(topics)}")
    print(f"Unique subjects  : {len(subjects)}")
    print(f"Grade range      : {grades[0]} - {grades[-1]}")
    print(f"\nTopics covered:")
    for t in sorted(topics):
        count = sum(1 for d in EXTENDED_DOCUMENTS_V3 if d["topic"] == t)
        print(f"  {t:<35} {count} docs")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                  HOW TO INTEGRATE INTO THE RAG SYSTEM                   ║
# ╠═══════════════════════════════════════════════════════════════════════════╣
# ║                                                                           ║
# ║  The existing codebase reads all documents from EDUCATIONAL_DOCUMENTS    ║
# ║  in data_loader.py.  Only FOUR files need any changes at all.            ║
# ║  The vector store, pipeline, app, and every other file: NO changes.     ║
# ║                                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
#
# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — data_loader.py  (REQUIRED)
# ─────────────────────────────────────────────────────────────────────────────
#
# Add two import lines near the top and extend EDUCATIONAL_DOCUMENTS:
#
#   # ── at the top of data_loader.py, after existing imports ─────────────────
#   from extended_corpus_v2 import EXTENDED_DOCUMENTS_V2
#   from extended_corpus_v3 import EXTENDED_DOCUMENTS_V3
#
#   # ── at the bottom, after defining the original list ───────────────────────
#   EDUCATIONAL_DOCUMENTS = (
#       EDUCATIONAL_DOCUMENTS        # the original 14 documents
#       + EXTENDED_DOCUMENTS_V2      # 300+ documents added in v2
#       + EXTENDED_DOCUMENTS_V3      # 300+ documents added in v3 (this file)
#   )
#
# That is the ONLY required change in data_loader.py.  All downstream
# functions (get_texts_and_metadatas, get_chunked_texts_and_metadatas)
# already iterate over EDUCATIONAL_DOCUMENTS so they pick up new docs
# automatically without any further modification.
#
# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Delete chroma_db/ and rebuild  (REQUIRED)
# ─────────────────────────────────────────────────────────────────────────────
#
# New documents are only searchable after the Chroma vector store is rebuilt.
#
#   # From the terminal:
#   rm -rf ./chroma_db
#   python main.py          # OR: streamlit run app.py
#
# build_vector_store() in retriever.py detects the missing folder and
# automatically embeds all documents (now including V2 and V3) and saves
# the new index to disk.  This takes a few minutes on first run.
#
# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — query_classifier.py  (RECOMMENDED — improves topic detection)
# ─────────────────────────────────────────────────────────────────────────────
#
# For each brand-new topic, add an entry to TOPIC_KEYWORDS so the keyword
# classifier can route queries correctly without solely relying on embeddings.
# Add the following block anywhere after the existing TOPIC_KEYWORDS dict:
#
#   TOPIC_KEYWORDS.update({
#       "trigonometry": [
#           "trigonometry", "sin", "cos", "tan", "sine", "cosine", "tangent",
#           "sohcahtoa", "hypotenuse", "angle", "pythagoras", "sine rule",
#           "cosine rule",
#       ],
#       "cell structure": [
#           "cell", "nucleus", "mitochondria", "ribosome", "organelle",
#           "prokaryote", "eukaryote", "cytoplasm", "membrane", "chloroplast",
#           "vacuole", "lysosome",
#       ],
#       "genetics": [
#           "genetics", "allele", "dominant", "recessive", "punnett",
#           "chromosome", "inheritance", "gene", "dna", "mutation",
#           "genotype", "phenotype", "mendel",
#       ],
#       "evolution": [
#           "evolution", "natural selection", "darwin", "adaptation",
#           "speciation", "fossil", "survival", "fitness", "mutation",
#           "homologous", "species",
#       ],
#       "electricity": [
#           "current", "voltage", "resistance", "ohm", "circuit", "series",
#           "parallel", "power", "watts", "ampere", "electric", "conductor",
#           "insulator", "diode",
#       ],
#       "magnetism": [
#           "magnet", "magnetic", "electromagnet", "induction", "faraday",
#           "transformer", "generator", "solenoid", "coil", "flux",
#       ],
#       "electromagnetic spectrum": [
#           "electromagnetic", "radio wave", "microwave", "infrared",
#           "ultraviolet", "x-ray", "gamma", "spectrum", "wavelength",
#           "frequency",
#       ],
#       "sound waves": [
#           "sound", "wave", "frequency", "amplitude", "pitch", "loudness",
#           "ultrasound", "vibration", "longitudinal", "decibel",
#       ],
#       "thermal energy": [
#           "conduction", "convection", "radiation", "thermal", "heat",
#           "temperature", "specific heat", "insulation",
#       ],
#       "nuclear energy": [
#           "nuclear", "fission", "fusion", "uranium", "reactor",
#           "chain reaction", "radioactive", "neutron",
#       ],
#       "renewable energy": [
#           "renewable", "solar", "wind", "hydroelectric", "turbine",
#           "photovoltaic", "green energy", "sustainable energy",
#       ],
#       "stars": [
#           "star", "sun", "red giant", "white dwarf", "supernova", "neutron",
#           "black hole", "main sequence", "hertzsprung", "luminosity",
#           "stellar", "nebula",
#       ],
#       "solar system": [
#           "planet", "orbit", "moon", "solar system", "asteroid",
#           "mercury", "venus", "mars", "jupiter", "saturn", "uranus",
#           "neptune", "eclipse", "tide",
#       ],
#       "earthquakes": [
#           "earthquake", "seismic", "fault", "epicentre", "magnitude",
#           "richter", "tectonic", "tremor",
#       ],
#       "volcanoes": [
#           "volcano", "magma", "lava", "eruption", "pyroclastic",
#           "tectonic", "shield", "composite",
#       ],
#       "glacial landforms": [
#           "glacier", "ice", "moraine", "corrie", "arete", "u-shaped",
#           "glacial", "till", "drumlin", "erratic",
#       ],
#       "river landforms": [
#           "river", "meander", "oxbow", "floodplain", "delta", "valley",
#           "erosion", "deposition", "waterfall",
#       ],
#       "population": [
#           "population", "birth rate", "death rate", "fertility",
#           "demographic", "dtm", "migration", "census",
#       ],
#       "urbanisation": [
#           "urban", "city", "megacity", "slum", "favela", "rural",
#           "urbanisation", "migration",
#       ],
#       "machine learning": [
#           "machine learning", "neural network", "deep learning", "training",
#           "model", "dataset", "supervised", "unsupervised", "ai",
#           "algorithm", "overfitting",
#       ],
#       "cybersecurity": [
#           "cybersecurity", "encryption", "phishing", "malware", "firewall",
#           "password", "hacking", "breach", "ransomware", "tls", "cyber",
#       ],
#   })
#
# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — glossary_mapper.py  (RECOMMENDED — improves synonym resolution)
# ─────────────────────────────────────────────────────────────────────────────
#
# Add synonym → canonical topic mappings so expand_query() enriches queries
# from this file's topics automatically.
#
# Add the following block at the end of glossary_mapper.py:
#
#   GLOSSARY.update({
#       # trigonometry
#       "sohcahtoa":         "trigonometry",
#       "sine rule":         "trigonometry",
#       "cosine rule":       "trigonometry",
#       "hypotenuse":        "trigonometry",
#       "pythagoras":        "trigonometry",
#       # genetics
#       "allele":            "genetics",
#       "punnett square":    "genetics",
#       "dominant allele":   "genetics",
#       "recessive allele":  "genetics",
#       "chromosome":        "genetics",
#       "crispr":            "genetics",
#       # evolution
#       "natural selection": "evolution",
#       "adaptation":        "evolution",
#       "speciation":        "evolution",
#       "fossil record":     "evolution",
#       "darwin":            "evolution",
#       # electricity
#       "ohm's law":         "electricity",
#       "resistor":          "electricity",
#       "capacitor":         "electricity",
#       "diode":             "electricity",
#       # magnetism
#       "electromagnetic induction": "magnetism",
#       "faraday":           "magnetism",
#       "solenoid":          "magnetism",
#       "transformer":       "magnetism",
#       # stars
#       "supernova":         "stars",
#       "red giant":         "stars",
#       "white dwarf":       "stars",
#       "black hole":        "stars",
#       "main sequence":     "stars",
#       # machine learning / AI
#       "neural network":    "machine learning",
#       "deep learning":     "machine learning",
#       "overfitting":       "machine learning",
#       "training data":     "machine learning",
#       # cybersecurity
#       "phishing":          "cybersecurity",
#       "malware":           "cybersecurity",
#       "ransomware":        "cybersecurity",
#       "encryption":        "cybersecurity",
#       "firewall":          "cybersecurity",
#   })
#
#   # Also extend the TOPICS list in glossary_mapper.py:
#   TOPICS.extend([
#       "trigonometry", "circle theorems", "transformations", "3D geometry",
#       "data handling", "normal distribution", "hypothesis testing",
#       "differentiation", "integration",
#       "cell structure", "mitosis", "meiosis", "genetics", "evolution",
#       "enzymes", "digestion", "blood and circulation", "nervous system",
#       "immune system", "nitrogen cycle",
#       "electricity", "magnetism", "electromagnetic spectrum", "sound waves",
#       "thermal energy", "nuclear energy", "renewable energy",
#       "stars", "solar system", "space exploration",
#       "earth structure", "seismic waves", "volcanoes", "earthquakes",
#       "glacial landforms", "river landforms",
#       "population", "urbanisation", "climate change",
#       "ancient Egypt", "ancient Greece", "ancient Rome", "Viking Age",
#       "medieval England", "Black Death", "Renaissance",
#       "colonialism and slavery", "World War I", "World War II",
#       "Holocaust", "Cold War", "civil rights", "apartheid",
#       "machine learning", "cybersecurity", "ethical AI",
#       "digital privacy", "electric vehicles", "hydrogen economy",
#       "art history",
#   ])
#
# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — contextual_query_builder.py  (RECOMMENDED — improves ambiguity resolution)
# ─────────────────────────────────────────────────────────────────────────────
#
# Extend the TOPICS list at the top of contextual_query_builder.py with the
# same list added in Step 4.  This ensures the AmbiguityResolver correctly
# recognises when a query already contains a fully-specified topic name and
# does not flag it as ambiguous.
#
#   # In contextual_query_builder.py, extend TOPICS:
#   TOPICS.extend([
#       "trigonometry", "genetics", "evolution", "electricity", "magnetism",
#       "stars", "solar system", "earthquakes", "volcanoes",
#       "machine learning", "cybersecurity", ...  # same list as Step 4
#   ])
#
# Optionally add weighted keyword entries to TOPIC_KEYWORD_WEIGHTS for the
# most important new topics to enable fine-grained confidence scoring.
#
# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY TABLE
# ─────────────────────────────────────────────────────────────────────────────
#
#   File                          Required?     What to do
#   ──────────────────────────    ──────────    ──────────────────────────────
#   data_loader.py                YES           Import + concatenate lists
#   chroma_db/ folder             YES (delete)  rm -rf ./chroma_db, rebuild
#   query_classifier.py           Recommended   Add TOPIC_KEYWORDS entries
#   glossary_mapper.py            Recommended   Add GLOSSARY + TOPICS entries
#   contextual_query_builder.py   Recommended   Extend TOPICS list
#   rag_pipeline.py               NO            No changes needed
#   retriever.py                  NO            No changes needed
#   context_memory.py             NO            No changes needed
#   topic_memory_manager.py       NO            No changes needed
#   evaluation.py                 NO            No changes needed
#   embeddings.py                 NO            No changes needed
#   app.py                        NO            No changes needed
#   main.py                       NO            No changes needed
#
# ─────────────────────────────────────────────────────────────────────────────