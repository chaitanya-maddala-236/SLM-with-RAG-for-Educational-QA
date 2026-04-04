"""
extended_corpus_v8.py
-----------------------
Extended educational documents corpus (version 8).
Exports: EXTENDED_DOCUMENTS_V8
"""

EXTENDED_DOCUMENTS_V8 = [   {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Chemical kinetics is the study of how fast chemical reactions occur and what factors influence their '
                'speed. Reaction rate is defined as the change in concentration of a reactant or product per unit '
                'time. Understanding reaction rates is essential for designing industrial processes, developing '
                'medicines, and preserving food safely.',
        'topic': 'kinetics'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Four main factors affect the rate of a chemical reaction: temperature, concentration, surface area, '
                'and the presence of a catalyst. Increasing any of these generally speeds up a reaction by increasing '
                'the frequency or energy of particle collisions. For example, grinding a solid into fine powder '
                'greatly increases its surface area, allowing far more collisions between reacting particles per '
                'second.',
        'topic': 'kinetics'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Collision theory states that for a reaction to occur, particles must collide with both the correct '
                'orientation and energy equal to or greater than the activation energy. Not every collision leads to a '
                'reaction — only those with sufficient energy and proper geometry are successful. Increasing '
                'temperature raises the fraction of particles that exceed the activation energy threshold.',
        'topic': 'kinetics'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A Maxwell-Boltzmann distribution curve shows the spread of kinetic energies among particles in a gas '
                'at a given temperature. The area under the curve to the right of the activation energy represents the '
                'fraction of particles able to react. When temperature increases, the curve flattens and shifts right, '
                'meaning a significantly greater proportion of particles exceed the activation energy.',
        'topic': 'kinetics'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The rate law expresses how reaction rate depends on reactant concentrations: rate = k[A]^m[B]^n. The '
                'exponents m and n are the reaction orders with respect to each reactant and must be determined '
                'experimentally — they cannot be read from the stoichiometric equation. The rate constant k is '
                'specific to a given reaction at a given temperature and increases as temperature rises.',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'A first-order reaction has a rate directly proportional to the concentration of one reactant: rate = '
                'k[A]. The integrated rate law is ln[A] = ln[A]₀ − kt, giving a straight line when ln[A] is plotted '
                'against time. The half-life of a first-order reaction is constant: t½ = 0.693/k, independent of '
                'initial concentration. Radioactive decay is the classic example.',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "A second-order reaction has a rate that depends on the square of one reactant's concentration: rate = "
                'k[A]². The integrated rate law is 1/[A] = 1/[A]₀ + kt, giving a straight line when 1/[A] is plotted '
                'against time. Unlike first-order reactions, the half-life of a second-order reaction increases as the '
                'initial concentration decreases: t½ = 1/(k[A]₀).',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The Arrhenius equation k = Ae^(−Ea/RT) quantitatively relates the rate constant to temperature and '
                'activation energy. Taking the natural log gives ln k = ln A − Ea/RT — plotting ln k versus 1/T gives '
                'a straight line with slope −Ea/R, allowing activation energy to be determined experimentally from '
                'rate constants measured at different temperatures.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'A reaction mechanism is the step-by-step sequence of elementary reactions by which overall reactants '
                'become products. The slowest step is the rate-determining step and controls the overall reaction '
                'rate. Reaction intermediates are produced in one step and consumed in a later step — they appear in '
                'the mechanism but not in the overall balanced equation.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Homogeneous catalysts exist in the same phase as the reactants; heterogeneous catalysts are in a '
                'different phase. Catalytic converters in cars use solid platinum and palladium to convert toxic CO '
                'and NOₓ gases into less harmful CO₂ and N₂. Heterogeneous catalysts work by adsorbing reactant '
                'molecules onto their surface, weakening bonds and providing an alternative low-energy reaction '
                'pathway.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Enzymes are biological catalysts — nearly all are proteins — that speed up reactions by providing an '
                'alternative pathway with lower activation energy. Each enzyme has an active site that binds specific '
                'substrates (lock-and-key model). The Michaelis-Menten equation describes enzyme kinetics: reaction '
                'rate = Vmax[S] / (Km + [S]), where Km is the substrate concentration giving half-maximum rate.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Zero-order reactions have a rate that is independent of reactant concentration: rate = k. The '
                'concentration decreases linearly with time, and the half-life decreases as initial concentration '
                'decreases: t½ = [A]₀/2k. Zero-order kinetics occur when a catalyst is saturated with reactant, such '
                'as in some enzyme-catalysed reactions operating at maximum velocity (Vmax).',
        'topic': 'kinetics'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'Air is a mixture of gases — about 78% nitrogen, 21% oxygen, and 1% argon, with trace amounts of '
                'carbon dioxide and other gases. Gases have no fixed shape or volume and spread out to fill whatever '
                'container they occupy. Unlike solids and liquids, gas particles are far apart from each other and '
                'move very rapidly in all directions.',
        'topic': 'gases and gas laws'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Gas pressure is caused by the constant collisions of gas molecules against the walls of their '
                'container. The more frequently particles collide and the harder each collision, the higher the '
                'pressure. Pressure is measured in units such as atmospheres (atm), pascals (Pa), or millimetres of '
                'mercury (mmHg); standard atmospheric pressure is 101,325 Pa or 1 atm.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Boyle's Law states that at constant temperature, the pressure of a fixed amount of gas is inversely "
                'proportional to its volume: P₁V₁ = P₂V₂. If you squeeze a gas into half its volume, the pressure '
                'doubles because the same number of particles hit a smaller area more frequently. This principle '
                'underlies the action of syringes, bicycle pumps, and breathing.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Charles's Law states that at constant pressure, the volume of a fixed amount of gas is directly "
                'proportional to its absolute temperature: V₁/T₁ = V₂/T₂, where temperature must always be in Kelvin. '
                'A balloon shrinks in cold weather because cooling reduces particle speed, so they push outward less '
                'forcefully. Converting Celsius to Kelvin: K = °C + 273.15.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Gay-Lussac's Law states that at constant volume, the pressure of a fixed amount of gas is directly "
                'proportional to its absolute temperature: P₁/T₁ = P₂/T₂. This is why sealed aerosol cans carry '
                'warnings not to heat them — rising temperature increases pressure, risking explosion. Gas particles '
                'move faster at higher temperatures, striking container walls harder and more often.',
        'topic': 'gases and gas laws'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': "The combined gas law merges Boyle's, Charles's, and Gay-Lussac's laws: P₁V₁/T₁ = P₂V₂/T₂. This "
                'equation is useful when pressure, volume, and temperature all change simultaneously for a fixed '
                'amount of gas. Temperature must be expressed in Kelvin for all gas law calculations to be valid.',
        'topic': 'gases and gas laws'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The ideal gas law PV = nRT includes the amount of gas (n, in moles) and the universal gas constant R '
                '(8.314 J/mol·K or 0.08206 L·atm/mol·K). An ideal gas is a theoretical model assuming no '
                'intermolecular attractions and negligible particle volume. Real gases approach ideal behaviour at '
                'high temperatures and low pressures, where molecules are far apart.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Dalton's Law of Partial Pressures states that the total pressure of a gas mixture equals the sum of "
                'the partial pressures of each component: P_total = P₁ + P₂ + P₃ + … Each gas exerts pressure '
                'independently, as if it were the only gas present. This law is applied in calculating the pressure of '
                'gases collected over water and in designing breathing mixtures for scuba diving.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Graham's Law of Effusion states that the rate of effusion of a gas through a tiny hole is inversely "
                'proportional to the square root of its molar mass: rate₁/rate₂ = √(M₂/M₁). Lighter gases effuse '
                'faster. Hydrogen (M = 2 g/mol) effuses four times faster than oxygen (M = 32 g/mol) because √(32/2) = '
                '4. This principle is used in uranium isotope separation for nuclear fuel.',
        'topic': 'gases and gas laws'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Real gases deviate from ideal behaviour at high pressures and low temperatures. At high pressure, '
                'molecules are forced close together and intermolecular attractions become significant, causing volume '
                'to be smaller than predicted. At low temperatures, molecules move slowly enough for intermolecular '
                'forces to pull them together, eventually causing condensation into liquid.',
        'topic': 'gases and gas laws'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The van der Waals equation corrects the ideal gas law for real gas behaviour: (P + a/V²)(V − b) = '
                "nRT. The constant 'a' accounts for intermolecular attractions that reduce effective pressure, and 'b' "
                'accounts for the finite volume occupied by gas molecules. Different gases have characteristic values '
                'of a and b depending on their molecular size and polarity.',
        'topic': 'gases and gas laws'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The root mean square (rms) speed of gas molecules is given by u_rms = √(3RT/M), where R is the gas '
                'constant, T is temperature in Kelvin, and M is molar mass in kg/mol. At 25°C, hydrogen molecules '
                'travel at about 1920 m/s on average while oxygen molecules travel at about 482 m/s. This explains why '
                'lighter gases diffuse and effuse faster than heavier ones.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Coordination chemistry studies metal complexes — compounds where a central metal ion is surrounded by '
                'molecules or ions called ligands. Ligands donate lone pairs of electrons to the metal ion, forming '
                'coordinate (dative) covalent bonds. Common ligands include water (H₂O), ammonia (NH₃), chloride '
                '(Cl⁻), and cyanide (CN⁻) ions.',
        'topic': 'coordination chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The coordination number of a metal complex is the total number of donor atoms directly bonded to the '
                'central metal ion. Common coordination numbers are 4 (giving tetrahedral or square planar geometry) '
                'and 6 (giving octahedral geometry). In [Cu(H₂O)₆]²⁺, copper has a coordination number of 6 because '
                'six water molecules surround the metal ion.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Ligands are classified by how many donor atoms they use to bind the metal. Monodentate ligands bind '
                'through one atom (NH₃, Cl⁻), bidentate ligands bind through two atoms (ethylenediamine), and '
                'polydentate ligands bind through many atoms. EDTA is a hexadentate ligand forming six bonds with a '
                'single metal ion, making it extremely stable — it is used to treat heavy metal poisoning.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Crystal field theory explains the colours and magnetic properties of transition metal complexes. When '
                'ligands approach a metal ion, they split the five d orbitals into two sets of different energies — '
                'lower t₂g and higher eₘ in octahedral complexes. Light of a specific wavelength is absorbed to '
                'promote electrons between the split d orbitals, and the complementary colour is observed.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The chelate effect is the extra thermodynamic stability of complexes formed by polydentate '
                '(chelating) ligands compared to an equivalent number of monodentate ligands. This arises from a large '
                'positive entropy change — replacing many monodentate ligands with one polydentate ligand releases '
                "more free particles into solution. The word 'chelate' comes from the Greek for 'claw'.",
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'IUPAC nomenclature for coordination compounds: ligands are named before the metal in alphabetical '
                "order; anionic ligands end in '-o' (chloro, cyano, hydroxo); neutral ligands keep their names except "
                "aqua (water), ammine (ammonia), and carbonyl (CO). The metal's oxidation state is given in Roman "
                'numerals. For example, [Fe(CN)₆]⁴⁻ is hexacyanoferrate(II) ion.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Geometric isomerism occurs in square planar and octahedral complexes. In the square planar complex '
                '[Pt(NH₃)₂Cl₂], the cis isomer has identical ligands on the same side and the trans isomer has them on '
                'opposite sides. Cisplatin (cis-[Pt(NH₃)₂Cl₂]) is an effective anticancer drug that cross-links DNA '
                'strands, while the trans isomer is biologically inactive.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The spectrochemical series ranks ligands from weakest to strongest crystal field splitting. '
                'Weak-field ligands (I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O) cause small Δ and favour high-spin complexes '
                'with more unpaired electrons. Strong-field ligands (NH₃ < en < CN⁻ < CO) cause large Δ and favour '
                'low-spin complexes. High-spin complexes are paramagnetic; low-spin complexes are often diamagnetic.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Haemoglobin is a coordination complex where iron(II) ions at the centre of porphyrin rings bind '
                'reversibly to oxygen. Each haemoglobin molecule contains four haem groups and carries four oxygen '
                'molecules. Carbon monoxide binds to haem iron about 200 times more strongly than oxygen does, '
                'blocking oxygen transport and causing potentially fatal CO poisoning.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Optical isomerism occurs in coordination complexes that are non-superimposable mirror images of each '
                'other, called enantiomers. Tris(ethylenediamine)cobalt(III), [Co(en)₃]³⁺, is a classic example — the '
                'Δ (delta) and Λ (lambda) enantiomers rotate plane-polarised light in opposite directions. Optical '
                'isomers can have different biological activities, which is important in pharmaceutical chemistry.',
        'topic': 'coordination chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Biochemistry is the study of chemical processes occurring inside living organisms. It investigates '
                'the structure, function, and interactions of biological molecules including carbohydrates, lipids, '
                'proteins, and nucleic acids. Understanding biochemistry is essential for medicine, nutrition, '
                'genetics, drug development, and biotechnology.',
        'topic': 'biochemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Carbohydrates are organic molecules with the general formula (CH₂O)n, made of carbon, hydrogen, and '
                'oxygen. Simple sugars (monosaccharides) like glucose (C₆H₁₂O₆) are the primary energy source for '
                'cells. Disaccharides like sucrose consist of two monosaccharides joined by a glycosidic bond. '
                'Polysaccharides like starch and glycogen store energy; cellulose provides structural support in plant '
                'cell walls.',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Proteins are large biological macromolecules built from amino acid monomers linked by peptide bonds '
                'formed through condensation reactions. There are 20 different amino acids, and the unique sequence in '
                "which they are joined (primary structure) determines the protein's three-dimensional shape and "
                'function. Proteins serve as enzymes, transport molecules, structural components, hormones, and '
                'antibodies.',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Lipids are hydrophobic biological molecules including triglycerides (fats and oils), phospholipids, '
                'waxes, and steroids. Triglycerides consist of three fatty acid chains esterified to a glycerol '
                'molecule and serve as long-term energy storage. Phospholipids form the bilayer of all cell membranes '
                'because their hydrophilic phosphate heads face water while their hydrophobic fatty acid tails face '
                'inward.',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'DNA (deoxyribonucleic acid) stores genetic information in the linear sequence of four nitrogenous '
                'bases: adenine (A), thymine (T), guanine (G), and cytosine (C). The two strands are held together by '
                'hydrogen bonds between complementary base pairs: A pairs with T (two hydrogen bonds) and G pairs with '
                'C (three hydrogen bonds). The double helix structure was elucidated by Watson, Crick, and Franklin in '
                '1953.',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Enzymes are biological catalysts — nearly all are proteins — that dramatically increase reaction '
                'rates by lowering activation energy. The active site has a specific shape complementary to the '
                'substrate (lock-and-key model); in induced fit, the enzyme changes shape slightly upon substrate '
                'binding. Enzyme activity is sensitive to temperature and pH — most human enzymes operate optimally '
                'near 37°C and pH 7.4.',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Cellular respiration is the biochemical process by which cells oxidise glucose to produce ATP '
                '(adenosine triphosphate). The overall aerobic equation is C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ~38 ATP. It '
                'occurs in three stages: glycolysis (cytoplasm, produces 2 ATP), the Krebs cycle (mitochondrial '
                'matrix), and oxidative phosphorylation via the electron transport chain (inner mitochondrial '
                'membrane, produces ~34 ATP).',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Photosynthesis converts light energy into chemical energy stored as glucose. The overall equation is '
                '6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. The light-dependent reactions in thylakoid membranes '
                'split water, produce ATP and NADPH, and release oxygen. The Calvin cycle in the chloroplast stroma '
                'uses ATP and NADPH to fix CO₂ into glucose.',
        'topic': 'biochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Protein structure has four levels of organisation. Primary structure is the amino acid sequence. '
                'Secondary structure involves local folding into alpha helices or beta sheets stabilised by hydrogen '
                'bonds between backbone atoms. Tertiary structure is the overall 3D fold of a single polypeptide, '
                'stabilised by disulfide bridges, hydrophobic interactions, and ionic bonds. Quaternary structure '
                'describes assemblies of multiple polypeptide subunits.',
        'topic': 'biochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'DNA replication is semi-conservative — each new DNA molecule contains one original strand and one '
                'newly synthesised strand. The enzyme helicase unwinds the double helix; primase lays RNA primers; DNA '
                "polymerase adds complementary nucleotides in the 5'→3' direction. The leading strand is synthesised "
                'continuously; the lagging strand is synthesised in short Okazaki fragments joined by DNA ligase.',
        'topic': 'biochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Transcription converts the DNA sequence into messenger RNA (mRNA). RNA polymerase reads the template '
                'DNA strand and assembles complementary mRNA, using uracil (U) instead of thymine. In eukaryotes, the '
                "pre-mRNA is processed: introns (non-coding sequences) are removed by splicing, and a 5' cap and "
                'poly-A tail are added before the mature mRNA exits the nucleus for translation.',
        'topic': 'biochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Translation converts the mRNA sequence into a polypeptide chain at the ribosome. Transfer RNA (tRNA) '
                'molecules carry specific amino acids; each tRNA has an anticodon complementary to an mRNA codon. The '
                'ribosome reads codons (triplets of bases) sequentially, links amino acids via peptide bonds, and '
                'releases the completed protein at a stop codon. The genetic code is degenerate — multiple codons '
                'encode the same amino acid.',
        'topic': 'biochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Enzyme inhibitors reduce catalytic activity. Competitive inhibitors bind the active site, directly '
                'blocking substrate access — increasing substrate concentration can overcome this inhibition. '
                "Non-competitive (allosteric) inhibitors bind a different site, changing the enzyme's shape and "
                'reducing activity regardless of substrate concentration. Many drugs work as enzyme inhibitors — '
                'statins inhibit HMG-CoA reductase to reduce cholesterol synthesis.',
        'topic': 'biochemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Polymers are very large molecules (macromolecules) built from many small repeating units called '
                'monomers joined together by chemical bonds. The process of joining monomers is called polymerisation. '
                'Common everyday polymers include polyethylene (plastic bags), nylon (clothing), rubber (tyres), and '
                'DNA (the biological polymer that stores genetic information).',
        'topic': 'polymer chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Addition polymerisation occurs when monomers containing carbon-carbon double bonds join together '
                'without losing any atoms. The C=C double bond breaks and monomers link into a long chain. '
                "Poly(ethene), made by polymerising thousands of ethene (CH₂=CH₂) molecules, is the world's most "
                'widely produced plastic, used for bottles, bags, pipes, and packaging.',
        'topic': 'polymer chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Condensation polymerisation occurs when monomers react together and release a small molecule — '
                'usually water — at each junction. Nylon-6,6 forms from a diamine (hexane-1,6-diamine) and a '
                'dicarboxylic acid (hexanedioic acid), releasing water and forming amide bonds (–CO–NH–). Polyester '
                'forms similarly from a diol and a dicarboxylic acid, releasing water and forming ester bonds.',
        'topic': 'polymer chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Thermoplastic polymers soften and can be reshaped when heated, then harden again on cooling — a '
                'reversible process. Examples include polyethylene, polypropylene, PVC, and polystyrene. Thermosetting '
                'polymers (thermosets) undergo irreversible crosslinking when first heated, forming a rigid 3D network '
                'that cannot be remelted. Epoxy resin, Bakelite, and melamine are thermosets.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The degree of polymerisation (DP) is the average number of monomer units per polymer chain. Longer '
                'chains generally produce stronger, tougher polymers with higher melting temperatures. Polymer molar '
                'mass is reported as number-average (Mn) or weight-average (Mw) because chains vary in length — the '
                'ratio Mw/Mn is the dispersity (formerly polydispersity index, PDI) and indicates the breadth of the '
                'chain length distribution.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Copolymers contain two or more different types of monomers. In alternating copolymers (ABABAB…), '
                'monomers strictly alternate. Block copolymers have long sequences of each monomer (AAAA…BBBB…). '
                'Random copolymers have an irregular sequence. Graft copolymers have side chains of one monomer '
                'attached to a backbone of another. Varying monomer composition allows polymer properties — '
                'flexibility, strength, solubility — to be finely tuned.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Natural rubber is a polymer of isoprene (2-methylbuta-1,3-diene) extracted as latex from the rubber '
                'tree Hevea brasiliensis. Natural rubber is flexible but sticky and weak. Vulcanisation, discovered by '
                'Charles Goodyear, involves heating rubber with sulfur to form covalent crosslinks between polymer '
                'chains, dramatically improving strength, elasticity, and resistance to temperature extremes — '
                'essential for tyres.',
        'topic': 'polymer chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Biodegradable polymers break down in the environment through microbial action, addressing plastic '
                'pollution. Polylactic acid (PLA), produced by polymerising lactic acid from fermented plant starch, '
                'is a biodegradable thermoplastic used in packaging, medical sutures, and implants. Designing '
                'biodegradable polymers requires balancing mechanical performance with controlled degradation rate '
                'under intended conditions.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Conducting polymers can conduct electricity, unlike most plastics which are insulators. Polyacetylene '
                'was the first known conducting polymer, earning its discoverers Heeger, MacDiarmid, and Shirakawa the '
                '2000 Nobel Prize in Chemistry. Electrical conductivity arises from delocalised electrons along '
                'conjugated alternating single-double bond systems. Doping — adding oxidising or reducing agents — '
                'greatly increases conductivity.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Tacticity describes the stereochemical arrangement of side groups along a polymer chain. In isotactic '
                'polymers, all side groups are on the same side of the backbone. In syndiotactic polymers, they '
                'alternate sides. In atactic polymers, the arrangement is random. Isotactic polypropylene is highly '
                'crystalline and strong; atactic polypropylene is amorphous and rubbery — demonstrating how '
                'stereochemistry profoundly influences material properties.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Living polymerisation is a chain-growth polymerisation where termination reactions are absent, giving '
                'precise control over chain length and architecture. All chains begin simultaneously and grow at '
                'similar rates, producing polymers with very low dispersity (Mw/Mn close to 1). Living polymerisation '
                'enables the synthesis of well-defined block copolymers, star polymers, and other complex '
                'architectures for advanced materials applications.',
        'topic': 'polymer chemistry'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'A colloid is a mixture in which tiny particles (1–1000 nm) of one substance are dispersed throughout '
                'another without settling out. Unlike true solutions, colloid particles are large enough to scatter a '
                'beam of light — an effect called the Tyndall effect. Milk, fog, smoke, paint, and gelatin are common '
                'everyday examples of colloids.',
        'topic': 'colloids and mixtures'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'Mixtures can be classified as homogeneous or heterogeneous. In a homogeneous mixture (solution), '
                'composition is uniform throughout — saltwater and air are examples. In a heterogeneous mixture, '
                'components are visibly distinct and unevenly distributed — soil, salad, and concrete are examples. '
                'Colloids appear homogeneous to the naked eye but are heterogeneous at the nanoscale.',
        'topic': 'colloids and mixtures'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Three types of mixtures are classified by particle size. Solutions have particles smaller than 1 nm '
                'and are transparent. Colloids have particles of 1–1000 nm, appear homogeneous, scatter light (Tyndall '
                'effect), and do not settle. Suspensions have particles larger than 1000 nm, are cloudy, and settle on '
                'standing. Muddy river water is a suspension; clear river water after settling may be colloidal.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Colloids are classified by the phases of the dispersed material and the dispersing medium. A sol has '
                'solid particles in a liquid (blood, paint). A gel has liquid trapped in a solid network (gelatin, '
                'silica gel). An emulsion has liquid droplets in a liquid (milk, mayonnaise). A foam has gas bubbles '
                'in a liquid (whipped cream) or solid (polystyrene). An aerosol has liquid drops (fog) or solid '
                'particles (smoke) in gas.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Emulsions are colloids of two immiscible liquids — typically oil and water. They are inherently '
                'unstable and separate over time without emulsifiers. Emulsifiers are amphiphilic molecules with a '
                'hydrophilic head and hydrophobic tail (lecithin, soap, proteins). They surround oil droplets and '
                'prevent coalescence, stabilising products like mayonnaise, homogenised milk, salad dressings, and '
                'cosmetic creams.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Common separation techniques exploit differences in physical properties. Filtration separates an '
                'insoluble solid from a liquid. Evaporation concentrates or removes a solvent to isolate a dissolved '
                'solid. Simple distillation separates a liquid solvent from a dissolved solid. Fractional distillation '
                'separates liquids with different but close boiling points. Chromatography separates components by '
                'their differing affinities for stationary and mobile phases.',
        'topic': 'colloids and mixtures'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Brownian motion is the random, erratic movement of colloidal particles caused by unequal bombardment '
                'by surrounding solvent molecules. It was first observed by botanist Robert Brown in 1827 watching '
                'pollen grains in water. Brownian motion continuously randomises colloidal particle positions, '
                'preventing them from settling under gravity — an important factor in colloidal stability.',
        'topic': 'colloids and mixtures'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Colloidal particles carry surface charges — usually negative — that cause mutual repulsion, keeping '
                'particles dispersed. Adding an electrolyte (salt) introduces counterions that neutralise surface '
                'charges, reducing repulsion and allowing particles to aggregate. This coagulation is exploited in '
                'water treatment: alum (aluminium sulfate) coagulates fine suspended clay and organic matter so it can '
                'be filtered out.',
        'topic': 'colloids and mixtures'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Fractional distillation separates a mixture of miscible liquids with different boiling points. In an '
                'industrial fractionating column, vapour rises and partially condenses at different heights — '
                'fractions with lower boiling points rise higher before condensing. Crude oil is separated this way '
                'into fractions including LPG, naphtha, petrol, kerosene, diesel, fuel oil, and bitumen, each '
                'collected at its characteristic temperature range.',
        'topic': 'colloids and mixtures'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Aerogels are the lightest solid materials known — a form of gel where the liquid component has been '
                'replaced by gas without collapsing the solid framework. Silica aerogel can have a density as low as '
                '0.001 g/cm³, just three times the density of air. Their highly porous nanoscale structure gives '
                'extraordinary thermal insulation, with applications in space suits, building insulation, and oil '
                'spill cleanup.',
        'topic': 'colloids and mixtures'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Dialysis separates small molecules from large colloidal particles using a semi-permeable membrane '
                'with pores that allow small molecules (water, ions, glucose) to pass through but retain larger '
                'colloidal particles and macromolecules. Renal dialysis machines mimic kidney function for patients '
                'with kidney failure, removing urea, excess salts, and water from blood while retaining blood cells '
                'and proteins.',
        'topic': 'colloids and mixtures'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Lyophilic (solvent-loving) colloids are thermodynamically stable because the dispersed particles '
                'interact favourably with the solvent. Proteins, starch, and gum arabic form lyophilic colloids in '
                'water. Lyophobic (solvent-fearing) colloids are thermodynamically unstable and require additional '
                'stabilisation by adsorbed charge or emulsifiers. Gold sols and metal hydroxide colloids are lyophobic '
                'and can be irreversibly coagulated by adding electrolytes.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Redox reactions involve the transfer of electrons between substances. Oxidation is the loss of '
                'electrons, and reduction is the gain of electrons — they always occur simultaneously. The mnemonic '
                'OIL RIG helps: Oxidation Is Loss, Reduction Is Gain. The substance that loses electrons (and causes '
                'reduction) is the reducing agent; the substance that gains electrons (and causes oxidation) is the '
                'oxidising agent.',
        'topic': 'redox reactions'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Many familiar processes are redox reactions. Combustion is rapid oxidation — fuel reacts with oxygen, '
                'losing electrons to oxygen atoms and releasing energy. Rusting of iron is slow oxidation: Fe reacts '
                'with O₂ and H₂O to eventually form Fe₂O₃·nH₂O (rust). Photosynthesis involves oxidation of water and '
                'reduction of carbon dioxide. Biological respiration is a controlled series of redox reactions '
                'releasing energy from glucose.',
        'topic': 'redox reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Oxidation states (oxidation numbers) are assigned to track electron transfer in redox reactions. Key '
                'rules: elements in pure form have oxidation state 0; in monoatomic ions, it equals the charge; oxygen '
                'is usually −2 (except −1 in peroxides); hydrogen is +1 with nonmetals, −1 with metals; the sum of '
                'oxidation states equals the overall charge of the species. Increases in oxidation state indicate '
                'oxidation; decreases indicate reduction.',
        'topic': 'redox reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The reactivity series ranks metals in order of their tendency to be oxidised (lose electrons). Metals '
                'high in the series (potassium, sodium, magnesium, zinc) are easily oxidised — strong reducing agents. '
                'Metals low in the series (copper, silver, gold) resist oxidation. A more reactive metal displaces a '
                'less reactive one from its salt solution: zinc + copper sulfate → zinc sulfate + copper.',
        'topic': 'redox reactions'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Half-equations separate a redox reaction into its oxidation and reduction components, each balanced '
                'separately. For the reaction between zinc and copper ions: Zn → Zn²⁺ + 2e⁻ (oxidation) and Cu²⁺ + 2e⁻ '
                '→ Cu (reduction). The overall equation is found by adding the half-equations so electrons cancel. The '
                'number of electrons lost must always equal the number gained.',
        'topic': 'redox reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Balancing redox equations in acidic solution uses a systematic method: split into half-equations; '
                'balance atoms other than O and H; balance O by adding H₂O; balance H by adding H⁺; balance charge by '
                'adding electrons; multiply half-equations so electrons cancel; add them together. In basic solution, '
                'add OH⁻ to each side equal to the number of H⁺ ions, then simplify water molecules.',
        'topic': 'redox reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Disproportionation is a special redox reaction where the same element is simultaneously oxidised and '
                'reduced. Chlorine reacts with cold dilute sodium hydroxide: Cl₂ + 2NaOH → NaCl + NaOCl + H₂O. '
                'Chlorine (oxidation state 0) is both reduced to Cl⁻ (−1) in NaCl and oxidised to Cl⁺ (+1) in NaOCl '
                '(sodium hypochlorite, the active ingredient in bleach).',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Redox titrations use a standardised oxidising or reducing agent to quantitatively determine the '
                'amount of a reducing or oxidising agent in a sample. Potassium permanganate (KMnO₄, deep purple) is a '
                'common oxidising titrant — it decolourises as it oxidises the analyte, acting as its own indicator. '
                'The endpoint is the first permanent pale pink colour showing excess KMnO₄.',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The standard reduction potential (E°) measures the tendency of a half-cell reaction to proceed as a '
                'reduction under standard conditions (1 M, 1 atm, 25°C), relative to the standard hydrogen electrode '
                '(E° = 0.00 V). A more positive E° means a greater tendency to be reduced. The standard cell potential '
                'E°cell = E°cathode − E°anode. If E°cell is positive, the overall cell reaction is spontaneous.',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Biological redox reactions are central to life. In cellular respiration, NADH and FADH₂ carry '
                'electrons from glucose oxidation to the mitochondrial electron transport chain. Electrons pass '
                'through protein complexes (I, II, III, IV), releasing energy at each step to pump protons across the '
                'inner mitochondrial membrane. The resulting proton gradient drives ATP synthase. Oxygen is the final '
                'electron acceptor, reduced to water.',
        'topic': 'redox reactions'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Corrosion is the electrochemical oxidation of metals by reaction with their environment. Iron rusting '
                'requires both water and oxygen: the iron surface acts as an anode where Fe → Fe²⁺ + 2e⁻, and nearby '
                'areas act as cathodes. Prevention methods include galvanising (zinc coating — zinc is preferentially '
                'oxidised, protecting iron), painting, greasing, stainless steel alloys, and cathodic protection using '
                'sacrificial magnesium or zinc anodes.',
        'topic': 'redox reactions'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Thermochemistry studies the heat changes that accompany chemical reactions. Exothermic reactions '
                'release heat to the surroundings (ΔH negative), causing the temperature of the surroundings to rise — '
                'combustion and neutralisation are examples. Endothermic reactions absorb heat from the surroundings '
                '(ΔH positive), causing the temperature to fall — thermal decomposition and dissolving ammonium '
                'nitrate in water are examples.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Enthalpy (H) is a thermodynamic quantity measuring the heat content of a system at constant pressure. '
                'The enthalpy change ΔH = H_products − H_reactants. For exothermic reactions ΔH < 0; for endothermic '
                'reactions ΔH > 0. Standard enthalpy changes are measured at 298 K and 100 kPa. The standard enthalpy '
                'of combustion of methane is −890 kJ/mol, meaning 890 kJ of heat are released per mole burned.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Specific heat capacity (c) is the energy required to raise the temperature of 1 gram of a substance '
                'by 1°C (or 1 K). Water has an unusually high specific heat capacity of 4.18 J/g°C. The heat '
                'transferred in a calorimetry experiment is calculated as q = mcΔT, where m is mass in grams and ΔT is '
                'the temperature change. A coffee-cup calorimeter measures the heat of reaction by recording the '
                'temperature change of a known mass of water.',
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Hess's Law states that the total enthalpy change of a reaction is the same regardless of the number "
                'of steps, because enthalpy is a state function. This allows calculation of enthalpy changes for '
                'reactions that cannot be measured directly by combining known thermochemical equations. If a reaction '
                'is reversed, ΔH changes sign; if multiplied by a factor, ΔH is multiplied by the same factor.',
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The standard enthalpy of formation (ΔH°f) is the enthalpy change when one mole of a compound is '
                'formed from its elements in their standard states at 298 K and 100 kPa. By definition, ΔH°f for any '
                'element in its standard state is zero. The standard enthalpy of any reaction is calculated as: ΔH°rxn '
                "= ΣΔH°f(products) − ΣΔH°f(reactants), applying Hess's Law.",
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Bond enthalpies are average energies required to break one mole of a specific bond type in gaseous '
                'molecules. Breaking bonds requires energy (endothermic); forming bonds releases energy (exothermic). '
                'The approximate enthalpy change of a reaction is: ΔH ≈ Σ(bonds broken) − Σ(bonds formed). This method '
                'is approximate because bond enthalpies are averages and do not account for molecular environment.',
        'topic': 'thermochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Entropy (S) measures the degree of disorder or dispersal of energy in a system. Entropy increases '
                'when solids dissolve, gases expand, temperature rises, or reactions produce more moles of gas. The '
                'second law of thermodynamics states that the total entropy of the universe always increases in a '
                'spontaneous process: ΔS_universe = ΔS_system + ΔS_surroundings > 0.',
        'topic': 'thermochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gibbs free energy (G) combines enthalpy and entropy to predict spontaneity at constant temperature '
                'and pressure: ΔG = ΔH − TΔS. A reaction is spontaneous when ΔG < 0, non-spontaneous when ΔG > 0, and '
                'at equilibrium when ΔG = 0. Temperature determines which factor dominates: at high T, the −TΔS term '
                'dominates; at low T, the ΔH term dominates. This explains why some endothermic reactions are '
                'spontaneous at high temperatures.',
        'topic': 'thermochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The relationship between Gibbs free energy and the equilibrium constant is: ΔG° = −RT ln K. A large '
                'equilibrium constant (K >> 1) corresponds to a large negative ΔG°, meaning products are strongly '
                'favoured. This equation bridges thermodynamics and equilibrium chemistry. The Gibbs free energy also '
                'relates to electrochemistry: ΔG° = −nFE°cell, connecting spontaneity, equilibrium constants, and cell '
                'potentials.',
        'topic': 'thermochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': "The Born-Haber cycle applies Hess's Law to calculate lattice enthalpies of ionic compounds "
                'indirectly. It includes enthalpy changes for: atomisation of elements, ionisation energies, electron '
                'affinities, and lattice formation. For NaCl, ΔH°lattice can be calculated from the other known steps. '
                'Comparing theoretical and experimental lattice enthalpies reveals the degree of covalent character — '
                'a large difference indicates significant covalency.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Electrochemistry studies the relationship between chemical energy and electrical energy. Galvanic '
                '(voltaic) cells convert chemical energy into electrical energy through spontaneous redox reactions. '
                'Electrolytic cells use electrical energy from an external source to drive non-spontaneous redox '
                'reactions. Both types consist of two electrodes — an anode (oxidation) and a cathode (reduction) — '
                'connected by an electrolyte.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A galvanic cell generates electricity from a spontaneous redox reaction. In the Daniell cell, a zinc '
                'anode dissolves (Zn → Zn²⁺ + 2e⁻) while copper deposits at the cathode (Cu²⁺ + 2e⁻ → Cu). Electrons '
                'flow through the external circuit from anode to cathode. A salt bridge (KNO₃ solution in a U-tube) '
                'maintains electrical neutrality by allowing ion migration between the half-cells.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The standard electrode potential (E°) measures the tendency of a half-cell to be reduced relative to '
                'the standard hydrogen electrode (SHE, assigned E° = 0.00 V). All standard conditions are 1 mol/L ion '
                'concentration, 25°C, and 1 atm. The standard cell potential is: E°cell = E°cathode − E°anode. A '
                'positive E°cell confirms the reaction is spontaneous in the direction written.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Faraday's first law of electrolysis: the mass of substance deposited at an electrode is directly "
                "proportional to the charge passed. Faraday's second law: equal amounts of charge deposit masses "
                'proportional to molar mass divided by ionic charge. The charge passed Q = It (current × time). One '
                'mole of electrons (one Faraday, F = 96,485 C) deposits one mole of a singly charged ion at the '
                'electrode.',
        'topic': 'electrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Nernst equation adjusts cell potential for non-standard conditions: E = E° − (RT/nF)lnQ, where R '
                "is the gas constant, T is temperature in Kelvin, n is moles of electrons transferred, F is Faraday's "
                'constant, and Q is the reaction quotient. At equilibrium, E = 0 and Q = Keq, giving: ln Keq = '
                'nFE°/RT, which links electrochemistry, kinetics, and thermodynamics.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Electrolysis of brine (concentrated aqueous sodium chloride) produces three industrial products: '
                'chlorine gas at the anode (2Cl⁻ → Cl₂ + 2e⁻), hydrogen gas at the cathode (2H₂O + 2e⁻ → H₂ + 2OH⁻), '
                'and sodium hydroxide (NaOH) in solution. This chlor-alkali process is one of the most important '
                'industrial electrolytic processes, producing essential raw materials for PVC, bleach, and soapmaking.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Fuel cells electrochemically convert fuel and oxygen directly into electricity without combustion. In '
                'a hydrogen fuel cell, H₂ is oxidised at the anode (H₂ → 2H⁺ + 2e⁻) and O₂ is reduced at the cathode '
                '(O₂ + 4H⁺ + 4e⁻ → 2H₂O). The only product is water. Fuel cells are more efficient than internal '
                'combustion engines and produce no direct CO₂ emissions, making them important for clean energy '
                'transport.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Electroplating deposits a thin metal layer onto an object by electrolysis. The object to be plated is '
                'the cathode; the plating metal is the anode; the electrolyte contains ions of the plating metal. '
                'Metal ions are reduced and deposited on the cathode object while the anode dissolves to replenish '
                'ions. Electroplating is used for corrosion protection (zinc plating), decoration (gold/silver '
                'plating), and electronics (copper plating circuit boards).',
        'topic': 'electrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Lithium-ion batteries are rechargeable cells that power phones, laptops, and electric vehicles. '
                'During discharge, lithium ions move from the graphite anode through a liquid electrolyte to the '
                'lithium metal oxide cathode while electrons flow through the external circuit generating current. '
                'During charging, an external voltage reverses this process. Their high energy density, long cycle '
                'life, and declining cost have made them dominant in portable electronics.',
        'topic': 'electrochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Chemical equilibrium is reached in a reversible reaction when the forward and reverse reaction rates '
                'become equal, so concentrations of reactants and products remain constant over time. Both reactions '
                'continue occurring simultaneously — equilibrium is dynamic, not static. The double arrow (⇌) in a '
                'chemical equation indicates a reversible reaction. Equilibrium can be approached from either '
                'direction.',
        'topic': 'chemical equilibrium'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Le Chatelier's principle states that if a system at equilibrium is disturbed by a change in "
                'concentration, temperature, or pressure, the equilibrium shifts in the direction that counteracts the '
                'disturbance. Adding a reactant shifts equilibrium toward products. Increasing pressure shifts '
                'equilibrium toward fewer moles of gas. For an exothermic reaction, raising temperature shifts '
                'equilibrium toward reactants (decreasing Kc).',
        'topic': 'chemical equilibrium'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The equilibrium constant Kc is written using molar concentrations of products over reactants, each '
                'raised to the power of their stoichiometric coefficient. For aA + bB ⇌ cC + dD: Kc = [C]^c[D]^d / '
                "[A]^a[B]^b. Pure solids and pure liquids are excluded from the expression — their 'concentrations' "
                'are constant and incorporated into Kc. The value of Kc only changes when temperature changes.',
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The reaction quotient (Q) has the same algebraic form as Kc but uses concentrations at any point in '
                'the reaction, not necessarily at equilibrium. Comparing Q to Kc predicts the direction the reaction '
                'will proceed: if Q < Kc, the reaction proceeds forward to produce more products; if Q > Kc, it '
                'proceeds in reverse; if Q = Kc, the system is at equilibrium and no net change occurs.',
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "The Haber process synthesises ammonia: N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ΔH = −92 kJ/mol. Le Chatelier's "
                'principle suggests high pressure (shifts right — fewer gas moles) and low temperature (shifts right — '
                'exothermic). But low temperature gives an impractically slow rate. A compromise of 400–500°C with an '
                'iron catalyst and 150–200 atm optimises yield and rate. About 150 million tonnes of NH₃ are produced '
                'annually for fertilisers.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Kp is the equilibrium constant expressed in terms of partial pressures of gases. It is related to Kc '
                'by: Kp = Kc(RT)^Δn, where Δn is the change in moles of gas (products − reactants) and R = 0.08206 '
                'L·atm/mol·K. Kp = Kc when Δn = 0 (equal moles of gas on both sides). Kp is preferred when dealing '
                'with gas-phase reactions where pressures are easily measured.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The solubility product constant Ksp applies to the dissolution equilibrium of sparingly soluble ionic '
                'compounds. For silver chloride: AgCl(s) ⇌ Ag⁺(aq) + Cl⁻(aq), Ksp = [Ag⁺][Cl⁻] = 1.8 × 10⁻¹⁰. A small '
                'Ksp indicates a very insoluble compound. Ksp values are used to predict whether precipitation will '
                'occur — if the ion product (Q) exceeds Ksp, a precipitate forms.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The common ion effect suppresses the solubility of a sparingly soluble salt when a soluble salt '
                'sharing a common ion is added. Adding NaCl to a saturated AgCl solution increases [Cl⁻], causing Q > '
                'Ksp, so more AgCl precipitates until equilibrium is re-established. This is an application of Le '
                "Chatelier's principle and is used in gravimetric analysis to ensure complete precipitation.",
        'topic': 'chemical equilibrium'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Stoichiometry is the quantitative study of reactants and products in chemical reactions, based on the '
                'law of conservation of mass. The coefficients in a balanced equation give the molar ratios of all '
                'species. For example, in 2H₂ + O₂ → 2H₂O, 2 moles of hydrogen react with 1 mole of oxygen to produce '
                '2 moles of water — in a 2:1:2 molar ratio.',
        'topic': 'stoichiometry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'The mole (mol) is the SI unit for amount of substance. One mole contains exactly 6.022 × 10²³ '
                "particles (Avogadro's number, Nₐ). One mole of any element has a mass in grams equal to its relative "
                'atomic mass — so one mole of carbon-12 is exactly 12 g. This makes the mole a convenient bridge '
                'between the atomic scale and laboratory-measurable masses.',
        'topic': 'stoichiometry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Molar mass is the mass of one mole of a substance in g/mol. For compounds, it is calculated by '
                'summing the atomic masses of all atoms in the formula. Water (H₂O) has molar mass = 2(1.008) + 16.00 '
                '= 18.02 g/mol. Moles are converted to mass (or vice versa) using: moles = mass (g) / molar mass '
                '(g/mol). Molar mass links measurable mass to countable moles of particles.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The limiting reagent is the reactant that is completely consumed first, determining the maximum '
                'amount of product that can form. All other reactants are in excess. To identify the limiting reagent, '
                'calculate the moles of product each reactant could produce and choose the smaller amount. For '
                'example, if 2 mol H₂ and 2 mol O₂ react (2H₂ + O₂ → 2H₂O), hydrogen is limiting — it produces only 2 '
                'mol H₂O while oxygen could produce 4 mol.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Percentage yield measures the efficiency of a reaction: % yield = (actual yield / theoretical yield) '
                '× 100%. Actual yield is what you experimentally obtain; theoretical yield is the maximum calculated '
                'from stoichiometry using the limiting reagent. Yields less than 100% occur due to incomplete '
                'reactions, side reactions, product losses during purification, and equilibrium limitations. In '
                'industrial chemistry, maximising yield reduces cost and waste.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Empirical formula shows the simplest whole-number ratio of atoms in a compound. Molecular formula '
                'shows the actual number of each atom in one molecule. To find empirical formula: convert mass percent '
                'to moles of each element, divide by the smallest number of moles, round to whole numbers. For '
                'example, a compound with 40% C, 6.7% H, 53.3% O gives the empirical formula CH₂O (formaldehyde, '
                'glucose, and acetic acid all share this empirical formula).',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Molarity (M) is the number of moles of solute dissolved per litre of solution: M = n/V. A 2.0 M NaCl '
                'solution contains 2.0 mol NaCl per litre. To prepare 500 mL of 0.10 M HCl from concentrated HCl, use '
                'the dilution equation M₁V₁ = M₂V₂ to calculate the required volume of stock solution. Molarity is the '
                'most commonly used concentration unit in chemistry calculations.',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Percentage composition is the mass percentage of each element in a compound: % element = (molar mass '
                'of element in formula / molar mass of compound) × 100%. For CO₂ (molar mass 44.01 g/mol): %C = '
                '(12.01/44.01) × 100 = 27.3% and %O = 72.7%. Percentage composition is determined experimentally by '
                'combustion analysis and used to find empirical formulas.',
        'topic': 'stoichiometry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gas stoichiometry uses the fact that at standard temperature and pressure (STP: 0°C, 1 atm), one mole '
                'of any ideal gas occupies 22.4 L. This molar volume allows conversion between moles and gas volumes '
                'directly without weighing. For example, the complete combustion of 1 mol methane (CH₄ + 2O₂ → CO₂ + '
                '2H₂O) consumes 2 mol O₂ (44.8 L at STP) and produces 1 mol CO₂ (22.4 L at STP).',
        'topic': 'stoichiometry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Atom economy is a green chemistry metric measuring what fraction of starting material atoms end up in '
                'the desired product: atom economy = (molar mass of desired product / total molar mass of all '
                'products) × 100%. Addition reactions have 100% atom economy. Substitution reactions typically have '
                'lower atom economy because a leaving group is discarded as waste. High atom economy reduces cost and '
                'environmental impact.',
        'topic': 'stoichiometry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Back titration is used when a substance cannot be titrated directly — for example, because it reacts '
                'too slowly or is insoluble. A known excess of reagent reacts completely with the analyte; the '
                'unreacted excess is then titrated with a second standard solution. The amount of analyte = initial '
                'moles of reagent − moles of excess reagent. Back titration is used to determine the CaCO₃ content of '
                'limestone and the aspirin content of tablets.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Nuclear chemistry studies changes in atomic nuclei, unlike ordinary chemistry which involves electron '
                'rearrangements. Nuclear reactions involve protons and neutrons and release energy millions of times '
                "greater than chemical reactions. This energy is described by Einstein's equation E = mc², where c is "
                'the speed of light (3 × 10⁸ m/s) and even tiny mass changes produce enormous energy.',
        'topic': 'nuclear chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Radioactive decay is the spontaneous transformation of an unstable nucleus to a more stable one by '
                'emitting radiation. Alpha (α) decay emits a helium-4 nucleus, decreasing atomic number by 2 and mass '
                'number by 4. Beta-minus (β⁻) decay converts a neutron to a proton plus an electron (beta particle), '
                'increasing atomic number by 1. Gamma (γ) radiation is high-energy electromagnetic radiation '
                'accompanying other decay types.',
        'topic': 'nuclear chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Half-life (t½) is the time for exactly half the atoms in a radioactive sample to decay. After one '
                'half-life, 50% remains; after two, 25%; after three, 12.5%. The decay is exponential: N = '
                'N₀(½)^(t/t½). Half-lives range enormously — from microseconds for highly unstable nuclei to billions '
                'of years for uranium-238 (t½ = 4.5 × 10⁹ years). After 10 half-lives, only 0.1% of the original '
                'material remains.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Carbon-14 dating (radiocarbon dating) estimates the age of organic materials up to about 50,000 years '
                'old. Living organisms continuously absorb atmospheric carbon-14; when they die, absorption stops and '
                'carbon-14 decays (t½ = 5,730 years). The ratio of carbon-14 to stable carbon-12 in a sample is '
                'measured with a mass spectrometer and used to calculate the time since death. This technique '
                'revolutionised archaeology.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Nuclear fission is the splitting of a heavy nucleus (like U-235 or Pu-239) into two smaller nuclei, '
                'releasing 2–3 neutrons and enormous energy. These neutrons can trigger further fissions, creating a '
                'chain reaction. In a nuclear reactor, the chain reaction is controlled using neutron-absorbing '
                'control rods and a moderator (heavy water or graphite) to slow neutrons for more efficient fission. '
                'Uncontrolled chain reactions produce a nuclear explosion.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Nuclear fusion combines light nuclei — typically isotopes of hydrogen (deuterium and tritium) — to '
                'form a heavier nucleus, releasing vast amounts of energy. The Sun produces energy through fusion, '
                'fusing about 600 million tonnes of hydrogen per second. Fusion releases about 4× more energy per gram '
                'than fission and produces no long-lived radioactive waste. Achieving controlled fusion on Earth '
                'requires confining plasma at temperatures exceeding 100 million °C.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Mass defect is the difference between the mass of an atomic nucleus and the sum of masses of its '
                "individual protons and neutrons. This 'missing' mass is converted to the nuclear binding energy that "
                'holds the nucleus together, per E = mc². Iron-56 has the highest binding energy per nucleon (8.8 '
                'MeV), making it the most stable nucleus. Reactions of lighter nuclei (fusion) or heavier nuclei '
                '(fission) toward iron release energy.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Radioactive decay follows first-order kinetics: the decay rate is proportional to the number of '
                'undecayed nuclei. The rate equation is dN/dt = −λN, where λ is the decay constant. The integrated '
                'form is N = N₀e^(−λt). The decay constant and half-life are related by: t½ = ln 2/λ = 0.693/λ. '
                'Activity (A = λN, in becquerels) decreases exponentially with the same half-life as the number of '
                'atoms.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Nuclear medicine uses radioactive isotopes for diagnosis and treatment. Technetium-99m (t½ = 6 hours) '
                'is the most widely used diagnostic radioisotope — it emits gamma rays for external imaging by a gamma '
                'camera and its short half-life minimises patient radiation dose. Iodine-131 treats thyroid cancer '
                'because the thyroid selectively absorbs iodine, delivering targeted radiation to cancerous tissue. '
                'PET scans use fluorine-18 labelled glucose to image metabolically active tumours.',
        'topic': 'nuclear chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Transmutation converts one element into another through nuclear reactions. Natural transmutation '
                'occurs through radioactive decay. Artificial transmutation uses particle accelerators to bombard '
                'target nuclei with high-energy particles. All transuranic elements (atomic number > 92) have been '
                'produced artificially — most are extremely short-lived. Nuclear transmutation can convert long-lived '
                'radioactive waste into shorter-lived isotopes, a potential strategy for waste management.',
        'topic': 'nuclear chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'High-level radioactive waste from nuclear reactors contains fission products and transuranic elements '
                'that remain dangerously radioactive for thousands of years. Safe disposal requires isolation from the '
                'biosphere for periods far exceeding recorded human history. Deep geological repositories — placing '
                'waste in stable rock formations 500–1000 m underground — are the internationally accepted strategy. '
                "Finland's Onkalo repository, currently under construction, is the world's first permanent deep "
                'geological repository.',
        'topic': 'nuclear chemistry'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'A solution is a homogeneous mixture in which a solute is uniformly dissolved in a solvent. Water is '
                'called the universal solvent because it dissolves more substances than any other liquid. The polarity '
                'of water molecules allows it to surround and separate ions (hydration) and to dissolve polar covalent '
                'molecules through dipole-dipole interactions and hydrogen bonding.',
        'topic': 'solution chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Solubility is the maximum mass of solute that dissolves in a given volume of solvent at a specific '
                'temperature to produce a saturated solution. Adding more solute beyond saturation produces excess '
                'undissolved solute. A supersaturated solution contains more dissolved solute than a saturated '
                'solution and is unstable — adding a seed crystal causes rapid crystallisation of the excess.',
        'topic': 'solution chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Temperature affects solubility differently for different solutes. For most solid solutes, solubility '
                'in water increases with temperature — more kinetic energy overcomes the lattice energy. For gases '
                'dissolved in water, solubility decreases with rising temperature — higher kinetic energy allows gas '
                'molecules to escape solution. This explains why warm water holds less dissolved oxygen, affecting '
                'aquatic ecosystems during warm weather.',
        'topic': 'solution chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "The rule 'like dissolves like' means polar solvents dissolve polar and ionic solutes, while nonpolar "
                'solvents dissolve nonpolar solutes. Water (polar) dissolves NaCl (ionic) and glucose (polar) but not '
                'oil (nonpolar). Hexane (nonpolar) dissolves fats and grease but not salt. This principle governs '
                'extraction of chemicals, drug solubility, and the function of cell membranes in separating polar '
                'cytoplasm from nonpolar membrane interiors.',
        'topic': 'solution chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'When ionic compounds dissolve in water, they dissociate into their constituent ions in a process '
                'called dissociation. The ions become surrounded by water molecules (hydrated) through ion-dipole '
                'interactions. NaCl(s) → Na⁺(aq) + Cl⁻(aq). Electrolytes are substances that produce ions in solution '
                'and conduct electricity. Strong electrolytes (NaCl, HCl, NaOH) dissociate completely; weak '
                'electrolytes (acetic acid, ammonia) only partially dissociate.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Colligative properties depend only on the number of dissolved solute particles, not their identity. '
                "They include: vapour pressure lowering (Raoult's law), boiling point elevation (ΔTb = Kb × m × i), "
                "freezing point depression (ΔTf = Kf × m × i), and osmotic pressure (π = MRT). The van 't Hoff factor "
                '(i) accounts for dissociation — for NaCl, i ≈ 2 because it produces two ions per formula unit.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Henry's Law states that the solubility of a gas in a liquid at constant temperature is directly "
                'proportional to the partial pressure of that gas above the liquid: C = kH × P. Carbonated drinks are '
                'bottled under high CO₂ pressure; opening releases pressure and CO₂ effervesces from solution. '
                'Deep-sea divers face decompression sickness (the bends) if they ascend too rapidly — dissolved N₂ '
                'comes out of solution as bubbles in tissues.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Osmosis is the net movement of water molecules through a selectively permeable membrane from lower to '
                'higher solute concentration (lower to higher osmotic pressure). Osmotic pressure π = MRTi, where M is '
                "molarity, R is gas constant, T is absolute temperature, and i is the van 't Hoff factor. Reverse "
                'osmosis applies pressure greater than osmotic pressure to force water through the membrane — the '
                'basis for water desalination technology.',
        'topic': 'solution chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Molality (m) is the number of moles of solute per kilogram of solvent: m = n_solute/kg_solvent. '
                'Unlike molarity, molality does not change with temperature because it is based on mass rather than '
                'volume. Molality is used in colligative property calculations because these properties depend on the '
                'ratio of solute to solvent molecules, not their absolute concentrations in a volume that can change '
                'with temperature.',
        'topic': 'solution chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Debye-Hückel theory explains why real electrolyte solutions deviate from ideal behaviour. Strong '
                'ion-ion interactions in concentrated solutions cause activity coefficients to deviate from 1. The '
                'activity (effective concentration) of an ion is a = γc, where γ is the activity coefficient and c is '
                'the concentration. At infinite dilution, γ → 1 and real behaviour approaches ideal. This is important '
                'in precise pH measurements and equilibrium calculations.',
        'topic': 'solution chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Analytical chemistry identifies and quantifies the chemical composition of matter. Qualitative '
                'analysis determines what substances are present; quantitative analysis determines how much of each is '
                'present. Analytical chemistry underlies medicine (blood tests), environmental monitoring (pollutant '
                'detection), food safety (contamination testing), forensics (crime scene analysis), and industrial '
                'quality control.',
        'topic': 'analytical chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Chromatography separates mixtures based on differential migration through a stationary phase by a '
                'moving mobile phase. In paper chromatography, the stationary phase is the paper (cellulose), and the '
                'mobile phase is a solvent. Components with greater affinity for the mobile phase travel farther. The '
                'Rf value = distance moved by component / distance moved by solvent front, and is used for '
                'identification.',
        'topic': 'analytical chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Flame emission spectroscopy identifies metal ions by the characteristic colours they produce when '
                'heated in a flame. Sodium: persistent yellow-orange (589 nm). Potassium: lilac. Copper: blue-green. '
                'Lithium: crimson red. Calcium: brick red. The colours arise from electrons absorbing thermal energy, '
                'jumping to higher levels, then emitting photons of specific wavelengths when returning to lower '
                'levels — an atomic fingerprint.',
        'topic': 'analytical chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Acid-base titration determines the concentration of an unknown acid or base solution. A burette '
                'delivers the titrant of known concentration into the analyte solution containing an indicator. The '
                'equivalence point is when stoichiometrically equal moles of acid and base have reacted. The indicator '
                'changes colour at the endpoint (ideally matching the equivalence point). The calculation uses: n = cV '
                'to find moles and then concentration.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'UV-Visible spectrophotometry measures light absorption by solutions. Beer-Lambert Law: A = εcl, where '
                'A is absorbance (dimensionless), ε is the molar absorptivity (L/mol·cm), c is concentration (mol/L), '
                'and l is path length (cm). A calibration curve of absorbance vs known concentration allows unknown '
                'concentrations to be determined. This technique measures coloured compounds, proteins, nucleic acids '
                '(at 260 nm), and many drugs.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gas chromatography (GC) separates volatile compounds by passing them in an inert carrier gas through '
                'a long column coated with a stationary liquid phase. Components emerge at different retention times '
                'based on their affinity for the stationary phase. GC is used to measure blood alcohol levels in '
                'forensic testing, detect pesticide residues in food, identify flavour compounds in food science, and '
                'monitor environmental pollutants in air samples.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Mass spectrometry (MS) ionises molecules and separates ions by their mass-to-charge ratio (m/z). The '
                'molecular ion peak (M⁺) gives the molecular mass. Fragmentation produces characteristic peaks that '
                'act as a molecular fingerprint. GC-MS combines separation and identification, making it the gold '
                'standard for identifying unknowns in complex mixtures — used in drug testing, forensics, '
                'environmental analysis, and metabolomics.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Infrared (IR) spectroscopy identifies functional groups in organic molecules by measuring which '
                'infrared frequencies a compound absorbs. Key absorptions include: O-H stretch (broad, 2500–3300 cm⁻¹ '
                'in carboxylic acids; sharp 3200–3600 cm⁻¹ in alcohols), C=O stretch (~1710 cm⁻¹ in ketones, ~1735 '
                'cm⁻¹ in esters), N-H stretch (~3300–3500 cm⁻¹), and C≡N stretch (~2200 cm⁻¹). The fingerprint region '
                '(500–1500 cm⁻¹) is unique to each compound.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': '¹H NMR spectroscopy probes the chemical environment of hydrogen atoms in a molecule. Different types '
                'of protons resonate at different chemical shifts (δ, in ppm). Integration of peaks gives the ratio of '
                'proton types. Spin-spin splitting creates doublets (n+1 rule where n is adjacent protons): a CH₃ next '
                'to a CH₂ gives a triplet. NMR is the primary tool for structure determination of organic compounds, '
                'including pharmaceuticals.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gravimetric analysis determines the amount of a substance by converting it to a pure, insoluble solid '
                'of known composition, then weighing it precisely. To determine sulfate concentration, excess barium '
                'chloride is added to precipitate BaSO₄, which is filtered, dried at 150°C, and weighed. The mass of '
                'BaSO₄ is used with stoichiometry to calculate the original sulfate concentration. Gravimetric '
                'analysis gives highly accurate results but is slow and labour-intensive.',
        'topic': 'analytical chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Environmental chemistry investigates chemical processes in the environment and the impact of human '
                'activities on air, water, and soil quality. It draws on principles of analytical, physical, and '
                'organic chemistry to monitor pollutants, understand their fate and transport, and develop remediation '
                'strategies. Understanding environmental chemistry is critical for addressing climate change, '
                'pollution, and ecosystem degradation.',
        'topic': 'environmental chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'The enhanced greenhouse effect is caused by increasing concentrations of CO₂, CH₄, N₂O, and '
                'fluorinated gases from human activities trapping more infrared radiation in the atmosphere. Since '
                'industrialisation, atmospheric CO₂ has risen from 280 ppm to over 420 ppm (2023). The IPCC reports '
                'that average global temperatures have already risen by about 1.1°C above pre-industrial levels, '
                'causing more frequent extreme weather events.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Acid rain forms when SO₂ (from burning sulfur-containing coal) and NOₓ (from vehicle engines and '
                'power stations) react with atmospheric water to form H₂SO₄ and HNO₃. These acids lower rainfall pH '
                'below 5.6, damaging forests, acidifying lakes, corroding limestone and marble buildings, and '
                'depleting soil cations. Flue gas desulfurisation (scrubbers) in power stations removes SO₂ before '
                'emission.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Stratospheric ozone (O₃) absorbs 97–99% of the Sun's damaging UV-B and UV-C radiation. CFCs from "
                'refrigerants and aerosols diffuse into the stratosphere, where UV light releases chlorine radicals. '
                'Each Cl radical can catalytically destroy over 100,000 ozone molecules: Cl + O₃ → ClO + O₂; ClO + O → '
                'Cl + O₂. The Montreal Protocol (1987) phased out CFC production; stratospheric ozone is slowly '
                'recovering.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Eutrophication results from excess nitrogen and phosphorus from agricultural fertilisers and '
                'untreated sewage entering water bodies. This nutrients runoff promotes explosive algal blooms. When '
                "algae die, decomposition by aerobic bacteria consumes dissolved oxygen, creating hypoxic 'dead zones' "
                'where fish and other aquatic organisms cannot survive. The Gulf of Mexico dead zone, fed by nutrient '
                'runoff from the Mississippi basin, covers thousands of km².',
        'topic': 'environmental chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Heavy metal pollution — from lead, mercury, cadmium, arsenic, and chromium — poses serious '
                'environmental and health risks. These metals are toxic in low concentrations, do not degrade, and '
                'bioaccumulate up food chains through biomagnification. Mercury released from coal combustion and gold '
                'mining is converted to methylmercury by bacteria, accumulates in fish, and causes neurological '
                'damage. Phytoremediation uses plants like sunflowers and Indian mustard to absorb heavy metals from '
                'contaminated soil.',
        'topic': 'environmental chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Photochemical smog forms when sunlight drives reactions between nitrogen oxides and volatile organic '
                'compounds (VOCs) from vehicle exhaust and industry. These produce ground-level ozone (O₃) and '
                'peroxyacetyl nitrates (PANs) — collectively called secondary pollutants. Ground-level ozone damages '
                'lung tissue, reduces crop yields, and contributes to climate change. Catalytic converters in cars '
                'convert NOₓ, CO, and unburned hydrocarbons to N₂, CO₂, and H₂O.',
        'topic': 'environmental chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Carbon capture and storage (CCS) captures CO₂ from point sources — coal and gas power stations, '
                'cement plants — before it reaches the atmosphere, then compresses and injects it into geological '
                'formations. Suitable storage sites include depleted oil and gas reservoirs and deep saline aquifers. '
                "The world's largest CCS project, Sleipner in Norway, has stored over 20 million tonnes of CO₂ in the "
                'North Sea since 1996. CCS remains expensive and energy-intensive.',
        'topic': 'environmental chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The nitrogen cycle describes the biogeochemical movement of nitrogen through the environment. '
                'Nitrogen-fixing bacteria (Rhizobium in legume roots, free-living Azotobacter) convert atmospheric N₂ '
                'to NH₃/NH₄⁺. Nitrifying bacteria convert NH₄⁺ to NO₂⁻ then NO₃⁻. Plants absorb nitrate; animals '
                'consume plants. Denitrifying bacteria convert NO₃⁻ back to N₂. Human disruption through synthetic '
                'fertiliser production (Haber process) now exceeds natural nitrogen fixation.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Persistent organic pollutants (POPs) are highly toxic, resistant to environmental degradation, '
                'bioaccumulate in fatty tissues, and travel globally via wind and ocean currents. Examples include DDT '
                '(a banned pesticide), polychlorinated biphenyls (PCBs used in electrical equipment), and dioxins '
                '(industrial combustion byproducts). They are found in Inuit communities in the Arctic despite no '
                "local sources. The Stockholm Convention (2001) bans or severely restricts the 'dirty dozen' most "
                'dangerous POPs.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Green chemistry (sustainable chemistry) applies 12 principles to design chemical products and '
                'processes that reduce or eliminate hazardous substances. Key principles include: design syntheses '
                'with high atom economy; use renewable feedstocks; design for biodegradation; avoid unnecessary '
                'derivatisation steps; use safer solvents and reaction conditions. Green chemistry prevents pollution '
                'at the molecular design stage rather than treating waste after it is produced.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Ocean acidification results from the ocean absorbing about 30% of anthropogenic CO₂ emissions. CO₂ '
                'dissolves in seawater to form carbonic acid (H₂CO₃), which dissociates to release H⁺ ions, lowering '
                'pH. Since the Industrial Revolution, ocean surface pH has fallen from 8.21 to 8.10 — a 26% increase '
                'in hydrogen ion concentration. This threatens calcification in corals, oysters, sea urchins, and '
                'coccolithophores, disrupting marine food webs.',
        'topic': 'environmental chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Life cycle assessment (LCA) evaluates the total environmental impact of a product or process from raw '
                "material extraction through manufacturing, use, and disposal ('cradle to grave'). LCA quantifies "
                'energy consumption, greenhouse gas emissions, water use, and toxicological impacts at each stage. It '
                'enables identification of the most environmentally burdensome stages and supports decision-making in '
                'product design, purchasing, and policy. ISO 14040/44 provides the international standard for LCA '
                'methodology.',
        'topic': 'environmental chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Spectroscopy is the study of how matter interacts with electromagnetic radiation. Different types of '
                'radiation interact with matter in characteristic ways that reveal information about molecular and '
                'atomic structure. From radio waves to gamma rays, each region of the electromagnetic spectrum has '
                'corresponding spectroscopic techniques used to identify compounds, determine structures, and measure '
                'concentrations.',
        'topic': 'spectroscopy'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The electromagnetic spectrum spans a wide range of wavelengths and frequencies. From longest to '
                'shortest wavelength: radio waves, microwaves, infrared (IR), visible light (400–700 nm), ultraviolet '
                '(UV), X-rays, and gamma rays. Energy increases with frequency and decreases with wavelength: E = hf = '
                "hc/λ, where h is Planck's constant (6.626 × 10⁻³⁴ J·s). Each region probes different aspects of "
                'molecular structure.',
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Atomic emission spectroscopy identifies elements by the characteristic wavelengths of light their '
                'excited atoms emit. When atoms are energised (by flame, electric discharge, or plasma), electrons '
                'jump to higher energy levels. As they return to ground state, photons of specific wavelengths are '
                'emitted — producing a line spectrum unique to each element, like a fingerprint. This technique '
                'identifies elements in stars billions of light-years away from spectral analysis of their light.',
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Infrared (IR) spectroscopy exploits the fact that covalent bonds vibrate (stretch and bend) at '
                'characteristic frequencies in the infrared region. Bonds absorb IR radiation that matches their '
                'vibrational frequency, causing the bond to vibrate more strongly. The O−H bond in alcohols shows a '
                'broad absorption near 3300 cm⁻¹; the C=O carbonyl group shows a sharp, intense absorption near 1715 '
                'cm⁻¹. IR spectra are used to identify functional groups rapidly.',
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'UV-Visible spectroscopy measures absorption of UV (200–400 nm) and visible (400–700 nm) radiation by '
                'molecules. UV absorption is caused by electronic transitions — electrons promoted from bonding or '
                'non-bonding orbitals to higher energy orbitals. Conjugated systems (alternating double bonds) absorb '
                'at longer wavelengths: benzene absorbs at 254 nm; lycopene (11 conjugated double bonds) absorbs '
                'visible light and appears red. Beer-Lambert Law: A = εcl enables quantitative concentration '
                'measurement.',
        'topic': 'spectroscopy'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Mass spectrometry ionises molecules and separates them by mass-to-charge ratio (m/z) in a magnetic or '
                'electric field. Electron ionisation causes fragmentation — characteristic bond breaking produces a '
                'fragmentation pattern used to determine structure. The base peak is the most abundant fragment '
                '(tallest peak). Loss of specific masses reveals structural information: loss of 15 (CH₃), 29 (CHO), '
                '45 (OEt), or 77 (C₆H₅) are characteristic losses used to deduce molecular structure.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Raman spectroscopy measures inelastic scattering of laser light by molecules. When photons scatter '
                'off a molecule, most scatter elastically (Rayleigh scattering) but a small fraction exchange energy '
                'with molecular vibrations, producing shifted wavelengths (Raman shift). Raman spectroscopy is '
                'complementary to IR — vibrations that are IR-inactive (symmetric bonds like C=C, N=N) are often '
                'Raman-active. Portable Raman spectrometers are used in gemstone authentication, pharmaceutical '
                'quality control, and forensics.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Nuclear Magnetic Resonance (NMR) spectroscopy uses strong magnetic fields and radio waves to probe '
                'the chemical environment of atomic nuclei, typically ¹H or ¹³C. In an external field, nuclei align '
                'and precess at a characteristic Larmor frequency. Chemical shift (δ, ppm) reflects the electronic '
                'environment: TMS (tetramethylsilane) is the reference at δ = 0. ¹H NMR gives information about the '
                'number of chemically distinct protons, their environments, and their connectivity through coupling '
                'patterns.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'X-ray crystallography determines the three-dimensional atomic structure of crystalline materials. '
                'X-rays are diffracted by the regular array of atoms in a crystal, producing a diffraction pattern '
                "(Bragg's Law: nλ = 2d sin θ). Computational analysis of the pattern reveals the positions of all "
                'atoms. This technique determined the double-helical structure of DNA (1953), the structures of '
                'haemoglobin, insulin, and thousands of proteins — transforming biology and medicine.',
        'topic': 'spectroscopy'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Atomic absorption spectroscopy (AAS) measures the absorption of specific wavelengths of light by free '
                'atoms in the gas phase. The sample is atomised in a flame or graphite furnace; light from a '
                "hollow-cathode lamp emitting the element's characteristic wavelengths passes through. The amount "
                'absorbed is proportional to the atomic concentration (Beer-Lambert Law). AAS is highly selective and '
                'sensitive for quantitative elemental analysis in water, blood, food, and environmental samples.',
        'topic': 'spectroscopy'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Microwave spectroscopy probes the rotation of gas-phase molecules. Molecules with a permanent dipole '
                'moment absorb microwave radiation at frequencies corresponding to transitions between rotational '
                'energy levels. Rotational spectra give precise bond lengths and bond angles. Microwave ovens use 2.45 '
                'GHz radiation that is absorbed by the permanent dipole of water molecules, causing them to rotate '
                'rapidly and generate heat throughout food.',
        'topic': 'spectroscopy'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Food chemistry studies the chemical composition, structure, and properties of foods and the changes '
                'that occur during processing, storage, and cooking. Food consists mainly of carbohydrates, proteins, '
                'fats, water, vitamins, minerals, and flavour compounds. Understanding food chemistry helps improve '
                'nutritional value, flavour, texture, shelf life, and food safety.',
        'topic': 'food chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The Maillard reaction is the non-enzymatic browning that occurs when amino acids react with reducing '
                'sugars at temperatures above about 140°C. It produces hundreds of complex flavour and aroma compounds '
                'responsible for the characteristic taste and colour of cooked meat, bread crusts, roasted coffee, and '
                'toasted cereals. Louis-Camille Maillard described the reaction in 1912; it is one of the most '
                'important reactions in food chemistry.',
        'topic': 'food chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Caramelisation is the thermal decomposition of sugars at temperatures above 160°C (for sucrose), '
                'producing hundreds of compounds with characteristic brown colour and caramel flavour. Unlike the '
                'Maillard reaction, caramelisation requires no amino acids. Both reactions produce acrylamide, a '
                'potentially carcinogenic compound found in high concentrations in potato crisps, chips, and '
                'overtoasted bread when high-starch foods are cooked at high temperatures.',
        'topic': 'food chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Food preservatives extend shelf life by preventing microbial growth or chemical deterioration. Salt '
                'and sugar preserve by reducing water activity (osmotic stress kills bacteria). Vinegar (acetic acid) '
                'and citric acid lower pH, inhibiting bacterial growth. Sodium benzoate and potassium sorbate are '
                'antimicrobial. Antioxidants like vitamin C (ascorbic acid) and vitamin E (tocopherols) prevent '
                'rancidity in fats by interrupting free radical chain reactions.',
        'topic': 'food chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Emulsifiers are molecules with both hydrophilic and hydrophobic regions that stabilise emulsions by '
                'reducing interfacial tension between oil and water droplets. Lecithin (from egg yolk and soy) '
                'emulsifies mayonnaise and chocolate. Mono- and diglycerides are common food emulsifiers. Casein '
                'proteins in milk emulsify fat globules. Without emulsifiers, oil-and-water foods like mayonnaise '
                'would rapidly separate into distinct phases.',
        'topic': 'food chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Rancidity is the deterioration of fats and oils caused by hydrolysis (hydrolytic rancidity) or '
                'oxidation (oxidative rancidity). Oxidative rancidity is a free-radical chain reaction where oxygen '
                "attacks unsaturated C=C bonds, producing aldehydes and ketones with unpleasant 'off' flavours. "
                'Polyunsaturated fats are more susceptible than saturated fats. Antioxidants (BHA, BHT, vitamin E) '
                'terminate the chain reaction; vacuum packaging and refrigeration slow the process.',
        'topic': 'food chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Fermentation uses microorganisms — bacteria, yeasts, or moulds — to convert sugars into other '
                'products through anaerobic respiration. Yeast fermentation produces ethanol and CO₂ (bread-making, '
                'brewing, winemaking). Lactic acid bacteria ferment lactose to lactic acid (yoghurt, cheese, kimchi, '
                'sauerkraut). Acetic acid bacteria convert ethanol to acetic acid (vinegar). Fermentation also '
                'increases nutritional value by producing B vitamins and making minerals more bioavailable.',
        'topic': 'food chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Vitamins are organic micronutrients required in small amounts for normal physiological function. '
                'Fat-soluble vitamins (A, D, E, K) are stored in body fat and liver — excess intake can be toxic. '
                'Water-soluble vitamins (B vitamins and C) are not stored and must be consumed regularly; excess is '
                'excreted in urine. Vitamin C (ascorbic acid) is easily destroyed by heat and oxygen — cooking and '
                'processing can significantly reduce its concentration in food.',
        'topic': 'food chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Food colourants add or restore colour to enhance visual appeal. Natural colourants include '
                'anthocyanins (red-purple, from berries), carotenoids (yellow-orange, from carrots and tomatoes), and '
                'chlorophylls (green, from plants). Artificial colourants include tartrazine (E102, yellow) and '
                'brilliant blue (E133). The stability of food colourants is affected by pH, light, oxygen, and heat. '
                'Some artificial colourants have been linked to hyperactivity in children, prompting bans in some '
                'countries.',
        'topic': 'food chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Protein denaturation is the unfolding of a protein's three-dimensional structure without breaking the "
                'primary amino acid sequence. Heat, acid, alkali, mechanical agitation, and organic solvents can '
                'denature proteins. Cooking an egg denatures egg white proteins (albumin), changing them from soluble '
                'and transparent to insoluble and white. Denaturing improves digestibility by exposing peptide bonds '
                'to proteases. Denaturation is usually irreversible.',
        'topic': 'food chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The glycaemic index (GI) measures how rapidly a carbohydrate food raises blood glucose compared to '
                'pure glucose (GI = 100). High GI foods (white bread, cornflakes) cause rapid blood glucose spikes and '
                'subsequent insulin surges. Low GI foods (lentils, oats, many fruits) cause a slower, more sustained '
                'rise. Consuming predominantly low-GI foods is associated with better glycaemic control in diabetes '
                'and reduced risk of cardiovascular disease.',
        'topic': 'food chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Pharmaceutical chemistry designs, synthesises, and evaluates drugs for medicinal use. A drug must '
                'have the correct molecular structure to bind its biological target (receptor, enzyme, or ion '
                'channel), reach the target in sufficient concentration, and be eliminated safely. The vast majority '
                'of candidate drug molecules fail during development — only about 1 in 10,000 makes it through '
                'clinical trials to become an approved medicine.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Drug pharmacokinetics describes what the body does to a drug — ADME: Absorption, Distribution, '
                'Metabolism, and Excretion. Oral drugs are absorbed in the gut and undergo first-pass metabolism in '
                'the liver before reaching the bloodstream. Lipophilic (fat-soluble) drugs cross cell membranes easily '
                'but are harder to excrete. Hydrophilic drugs are readily excreted by the kidneys but penetrate '
                'tissues poorly. The half-life of a drug determines dosing frequency.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Aspirin (acetylsalicylic acid) was synthesised by Felix Hoffmann at Bayer in 1897. It irreversibly '
                'inhibits cyclooxygenase (COX) enzymes, blocking prostaglandin synthesis and reducing pain, fever, and '
                'inflammation. Low-dose aspirin (75–100 mg/day) inhibits platelet aggregation and is used to prevent '
                "heart attacks and strokes. Aspirin's discovery from salicylic acid (found in willow bark) was a "
                'landmark in pharmaceutical chemistry.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Chirality is critically important in pharmaceutical chemistry. Many drugs are chiral molecules — they '
                'exist as non-superimposable mirror image pairs (enantiomers). Often only one enantiomer has the '
                "desired therapeutic activity; the other may be inactive or even harmful. Thalidomide's tragedy "
                'demonstrated this: one enantiomer treated morning sickness effectively while the other caused severe '
                'birth defects. Modern drug synthesis aims to produce enantiopure compounds.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Prodrugs are pharmacologically inactive compounds that are metabolised in the body into active drugs. '
                'They are designed to improve bioavailability, reduce toxicity, or enable targeted delivery. Codeine '
                'is a prodrug converted to morphine (10× more potent) in the liver by the enzyme CYP2D6 — genetic '
                'variations in this enzyme explain why some people get no pain relief from codeine while others are '
                "'ultra-rapid metabolisers' who may experience overdose.",
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Antibiotics target bacterial structures absent from human cells. Beta-lactam antibiotics '
                '(penicillins, cephalosporins) inhibit the enzyme transpeptidase, preventing bacterial cell wall '
                'synthesis — causing bacteria to lyse. Tetracyclines bind bacterial ribosomes (30S subunit) and block '
                'protein synthesis. Fluoroquinolones inhibit DNA gyrase and topoisomerase IV, preventing DNA '
                'replication. Resistance develops when bacteria evolve mechanisms to destroy, exclude, or bypass the '
                'antibiotic target.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Drug delivery systems control the rate, timing, and location of drug release in the body. '
                'Sustained-release formulations use polymer coatings or matrix systems to release drugs slowly, '
                'maintaining therapeutic levels and reducing dosing frequency. Liposomes — lipid bilayer vesicles — '
                'encapsulate drugs and improve targeting to tumours. Nanoparticle delivery systems can cross the '
                'blood-brain barrier. Transdermal patches deliver drugs through the skin into the bloodstream '
                'continuously.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'High-throughput screening (HTS) tests thousands to millions of chemical compounds against biological '
                "targets to identify 'hits' — compounds showing desired activity. Combinatorial chemistry generates "
                'large libraries of structurally diverse compounds simultaneously. Computer-aided drug design (CADD) '
                "uses computational modelling of the target protein's structure to predict which molecules will bind "
                'most effectively, reducing the number of compounds that need to be physically synthesised and tested.',
        'topic': 'pharmaceutical chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Industrial chemistry applies chemical principles and processes to manufacture useful products at '
                'large scale. The chemical industry produces medicines, fertilisers, plastics, fuels, detergents, '
                'paints, and thousands of other materials. Industrial chemistry must balance product yield, rate, '
                'selectivity, safety, and environmental impact. Economic viability requires continuous optimisation of '
                'process conditions and catalysts.',
        'topic': 'industrial chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The Haber process produces ammonia (NH₃) from nitrogen and hydrogen: N₂ + 3H₂ ⇌ 2NH₃. It uses an iron '
                'catalyst (promoted with K₂O and Al₂O₃), a temperature of 400–500°C, and a pressure of 150–200 atm, '
                'with 10–15% conversion per pass. Unreacted gases are recycled. Ammonia is used primarily for nitrogen '
                "fertilisers, which sustain food production for about half the world's population. Fritz Haber "
                'received the 1918 Nobel Prize in Chemistry.',
        'topic': 'industrial chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "The Contact process manufactures sulfuric acid (H₂SO₄), the world's most produced industrial "
                'chemical. Sulfur dioxide is oxidised to sulfur trioxide: 2SO₂ + O₂ ⇌ 2SO₃, using a vanadium(V) oxide '
                'catalyst at 450–550°C and 1–2 atm. SO₃ is absorbed into concentrated H₂SO₄ to form oleum, then '
                'diluted with water. Sulfuric acid is used in fertiliser production, petroleum refining, metal '
                'processing, and manufacturing synthetic fibres.',
        'topic': 'industrial chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Steam reforming of natural gas (mostly methane) produces synthesis gas — a mixture of hydrogen and '
                'carbon monoxide. The reaction CH₄ + H₂O ⇌ CO + 3H₂ uses a nickel catalyst at 700–1000°C. A further '
                'water-gas shift reaction (CO + H₂O ⇌ CO₂ + H₂) increases hydrogen yield. Steam reforming provides '
                'about 95% of global hydrogen production. This hydrogen is mainly used in the Haber process and '
                'petroleum refining.',
        'topic': 'industrial chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Fractional distillation of crude oil separates it into fractions based on boiling point differences '
                'in a fractionating column maintained at different temperatures at different heights. Fractions and '
                'their uses: LPG (<40°C, fuel); naphtha (40–175°C, chemical feedstock); petrol/gasoline (40–205°C, '
                'fuel); kerosene (175–325°C, aviation fuel); diesel (250–350°C, fuel); fuel oil (>350°C, ships, power '
                'stations); bitumen (residue, road surfaces).',
        'topic': 'industrial chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Cracking converts large, less useful hydrocarbon fractions into smaller, higher-value products. '
                'Catalytic cracking (fluid catalytic cracking, FCC) uses zeolite catalysts at 500°C to crack long '
                'alkane chains into petrol-range hydrocarbons and alkenes used as polymer feedstocks. Steam cracking '
                'uses very high temperatures (750–900°C) with steam. Cracking is essential because demand for petrol '
                'and chemical feedstocks exceeds supply from direct distillation.',
        'topic': 'industrial chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The chlor-alkali process electrolyses brine (concentrated NaCl solution) to produce three key '
                'industrial chemicals simultaneously: chlorine (Cl₂) at the anode, hydrogen (H₂) at the cathode, and '
                'sodium hydroxide (NaOH) in solution. These products are used for PVC production, bleach, '
                'disinfectants, paper bleaching, soap making, and aluminium production. The membrane cell process '
                'replaced earlier mercury cell processes for environmental reasons.',
        'topic': 'industrial chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Catalysts are essential to industrial chemistry — they increase reaction rates, improve selectivity, '
                'allow operation at lower temperatures, and reduce energy consumption. Heterogeneous catalysts (solid '
                'catalysts with gaseous or liquid reactants) are most common industrially: iron in the Haber process, '
                'vanadium oxide in the Contact process, platinum/rhodium in catalytic converters, and zeolites in '
                'petroleum cracking. Catalyst deactivation by poisoning (sulfur compounds) or fouling (coke '
                'deposition) is a major industrial concern.',
        'topic': 'industrial chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Process intensification aims to make chemical manufacturing more efficient by combining multiple unit '
                'operations or using novel reactor designs. Microreactors have channel dimensions of 10–1000 μm, '
                'enabling excellent heat and mass transfer, safer handling of hazardous reactions, and rapid process '
                'development. Continuous flow chemistry replaces batch reactors, improving consistency, safety, and '
                'efficiency. These approaches are transforming pharmaceutical manufacturing.',
        'topic': 'industrial chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Bioreactors carry out biochemical reactions using living cells or enzymes. Industrial fermentation '
                'uses large bioreactors (up to 500,000 litres) to produce beer, antibiotics (penicillin), amino acids '
                '(glutamic acid for MSG), and biofuels (bioethanol). Enzyme bioreactors use immobilised enzymes for '
                'continuous processing. Biopharmaceuticals — insulin, growth hormone, monoclonal antibodies — are '
                'produced in mammalian cell culture bioreactors, which require precise control of temperature, pH, '
                'dissolved oxygen, and nutrient supply.',
        'topic': 'industrial chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Water is essential for all life on Earth. The water molecule (H₂O) has a bent shape with a bond angle '
                'of 104.5° and is highly polar due to the electronegativity difference between oxygen and hydrogen. '
                'This polarity makes water an excellent solvent for ionic and polar compounds. Hydrogen bonding '
                'between water molecules gives it unusually high boiling point (100°C), surface tension, and specific '
                'heat capacity compared to molecules of similar size.',
        'topic': 'water chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Hard water contains dissolved calcium (Ca²⁺) and magnesium (Mg²⁺) ions, which form when water passes '
                'through limestone or chalk. Hard water reduces the lathering of soap (calcium stearate precipitates '
                'as scum), causes scale in pipes, boilers, and kettles, and blocks heat exchangers. Temporary hardness '
                '(from Ca(HCO₃)₂) is removed by boiling; permanent hardness (from CaSO₄) requires ion exchange, '
                'washing soda (Na₂CO₃), or water softeners.',
        'topic': 'water chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Drinking water treatment involves multiple stages. Sedimentation uses gravity to remove large '
                'particles. Coagulation adds aluminium sulfate (alum) to aggregate fine particles into larger flocs '
                'that settle more rapidly. Filtration through sand beds removes remaining particles and many '
                'microorganisms. Chlorination disinfects water by adding Cl₂ or sodium hypochlorite, which kills '
                'pathogenic bacteria and viruses. Fluoride may be added to reduce tooth decay.',
        'topic': 'water chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Dissolved oxygen (DO) content is a critical measure of water quality for aquatic ecosystems. At 20°C '
                'and 1 atm, water saturated with oxygen contains about 9 mg/L. Eutrophication and organic pollution '
                'deplete DO as microorganisms consume oxygen during decomposition. Fish require at least 5 mg/L DO; '
                'below 2 mg/L, fish die. The biological oxygen demand (BOD) measures how much oxygen microorganisms '
                'consume while decomposing organic matter in a water sample over 5 days.',
        'topic': 'water chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Desalination removes dissolved salts from seawater or brackish water. Reverse osmosis (RO) forces '
                'water through semi-permeable membranes under pressure (50–80 bar), leaving salts behind. Multi-stage '
                'flash (MSF) distillation heats seawater to form steam, which is condensed as fresh water. RO is more '
                'energy-efficient (~3 kWh/m³) than MSF (~10 kWh/m³). Saudi Arabia, UAE, and Israel produce large '
                'quantities of desalinated water — increasingly important as freshwater scarcity grows globally.',
        'topic': 'water chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Wastewater treatment removes contaminants from water before discharge. Primary treatment removes '
                'large solids by settling and screening. Secondary (biological) treatment uses aerobic bacteria in '
                'activated sludge tanks to decompose dissolved organic matter. Tertiary treatment uses sand '
                'filtration, UV disinfection, or membrane bioreactors to remove remaining nutrients, pathogens, and '
                'micropollutants. Emerging contaminants — pharmaceuticals, microplastics, endocrine disruptors — are '
                'not fully removed by conventional treatment.',
        'topic': 'water chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Chlorination of drinking water is essential for public health but produces disinfection by-products '
                '(DBPs) when chlorine reacts with natural organic matter. Trihalomethanes (THMs, e.g., chloroform '
                'CHCl₃) and haloacetic acids are the most common DBPs, and some are suspected carcinogens. Regulatory '
                'limits balance the risk of DBPs against the much larger risk of waterborne disease from '
                'under-disinfection. Alternative disinfectants include chloramines, ozone, and UV radiation.',
        'topic': 'water chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Materials chemistry studies the design, synthesis, and properties of materials with specific '
                'functions. Materials are classified as metals, ceramics, polymers, and composites, each with '
                'characteristic structures and properties. The relationship between atomic/molecular structure and '
                'bulk material properties is the central theme — understanding this enables rational design of '
                'stronger, lighter, more conductive, or more biocompatible materials.',
        'topic': 'materials chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Alloys are mixtures of a metal with one or more other elements (metals or nonmetals) to improve '
                'properties. Steel is iron alloyed with 0.2–2.1% carbon; carbon atoms fit in interstitial spaces and '
                'harden the iron by preventing dislocation movement. Stainless steel adds chromium (>10.5%), which '
                "forms a protective Cr₂O₃ layer preventing rust. Bronze (copper + tin) was one of history's first "
                'engineered alloys, enabling the Bronze Age.',
        'topic': 'materials chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Ceramics are inorganic, non-metallic materials typically made by high-temperature processing. '
                'Traditional ceramics (clay, porcelain, glass) are made from silicate minerals. Advanced ceramics '
                'include alumina (Al₂O₃), silicon carbide (SiC), and silicon nitride (Si₃N₄) — extremely hard, '
                'heat-resistant, and chemically inert. They are used in cutting tools, engine components, biomedical '
                'implants (alumina hip joints), and electronics (alumina substrate for microchips).',
        'topic': 'materials chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Semiconductors have electrical conductivity between metals and insulators, which can be controlled by '
                'temperature, impurities (doping), or electric fields. Silicon is the dominant semiconductor material. '
                'N-type doping adds electron donors (phosphorus, arsenic); p-type doping adds electron acceptors '
                '(boron, aluminium). P-n junctions — where p-type and n-type semiconductors meet — are the basis for '
                'diodes, solar cells, and transistors — the fundamental components of all modern electronics.',
        'topic': 'materials chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Superconductors conduct electricity with zero electrical resistance below a characteristic critical '
                'temperature (Tc). Conventional superconductors (like mercury, Tc = 4.2 K; niobium, Tc = 9.2 K) are '
                'explained by BCS theory — electron pairs (Cooper pairs) move through the lattice without scattering. '
                'High-temperature superconductors (copper oxide ceramics, Tc up to 138 K) are not fully understood. '
                'Superconductors are used in MRI magnets, particle accelerator magnets, and experimental power '
                'transmission cables.',
        'topic': 'materials chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Graphene is a single layer of carbon atoms arranged in a hexagonal lattice — the thinnest material '
                'ever made. It has extraordinary properties: the strongest material ever measured (130 GPa), highest '
                'intrinsic electrical conductivity, highest thermal conductivity, and is nearly transparent. Graphene '
                'has potential applications in flexible electronics, ultra-capacitors, water filtration membranes, '
                'composite materials, and biosensors. Andre Geim and Konstantin Novoselov received the 2010 Nobel '
                'Prize in Physics for its discovery.',
        'topic': 'materials chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Shape-memory alloys (SMAs) return to a predetermined shape after deformation when heated. Nitinol '
                '(nickel-titanium alloy) is the most common SMA, transforming between martensite (lower temperature, '
                'deformable) and austenite (higher temperature, rigid) crystal structures. Applications include '
                'self-expanding cardiovascular stents (body temperature triggers expansion), orthodontic wires, '
                'robotic actuators, and seismic damping devices in earthquake-resistant buildings.',
        'topic': 'materials chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Corrosion is the electrochemical degradation of metals. Iron (steel) corrodes especially rapidly '
                'because it forms a galvanic cell with less reactive areas. The iron acts as the anode and is '
                'oxidised: Fe → Fe²⁺ + 2e⁻. Fe²⁺ ions are further oxidised to Fe³⁺ and react with water to form rust '
                '(Fe₂O₃·nH₂O). Galvanising — coating with zinc — provides both a physical barrier and cathodic '
                '(sacrificial) protection, since zinc is more reactive and is preferentially oxidised.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The electrochemical series (electromotive series) arranges half-reactions in order of standard '
                'reduction potential (E°). The most positive E° indicates the strongest tendency to be reduced. Gold '
                '(E° = +1.50 V) resists oxidation; lithium (E° = −3.04 V) is oxidised very easily. Any species can '
                'oxidise one with a less positive (more negative) E°. The series allows prediction of spontaneous '
                'redox reactions and calculation of cell potentials.',
        'topic': 'electrochemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'The atmosphere is a mixture of gases held close to Earth by gravity. Dry air consists of 78.1% '
                'nitrogen (N₂), 20.9% oxygen (O₂), 0.93% argon (Ar), 0.04% carbon dioxide (CO₂), and trace amounts of '
                'other gases. Water vapour varies from 0–4%. The atmosphere is divided into layers by temperature '
                'profile: troposphere, stratosphere, mesosphere, thermosphere, and exosphere.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Ozone (O₃) in the stratosphere forms naturally when UV radiation breaks O₂ into oxygen atoms: O₂ + hν '
                '→ 2O, followed by O + O₂ → O₃. It is destroyed by reverse reactions and by catalytic cycles involving '
                'HOₓ, NOₓ, and halogens (especially Cl from CFCs). The Antarctic ozone hole forms each spring when Cl '
                "radicals from polar stratospheric cloud surfaces rapidly destroy ozone — the 'hole' is an area where "
                'ozone is thinned by 60–70%.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Tropospheric chemistry is driven by reactions of OH radicals (the 'detergent of the atmosphere'). OH "
                'is produced photochemically and attacks volatile organic compounds (VOCs), nitrogen oxides (NOₓ), and '
                'methane, initiating complex oxidation chains. The lifetime of greenhouse gases in the atmosphere is '
                'determined partly by OH chemistry — methane has a lifetime of about 12 years because it reacts with '
                'OH radicals.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Particulate matter (PM) in the atmosphere ranges from coarse particles (PM10, diameter < 10 μm) to '
                'fine particles (PM2.5, < 2.5 μm) and ultrafine particles (< 0.1 μm). PM2.5 is most harmful to health '
                'because it penetrates deep into the lungs and enters the bloodstream, causing cardiovascular and '
                'respiratory disease. Sources include vehicle emissions, industrial combustion, agricultural burning, '
                'and secondary formation from gas-phase reactions of SO₂ and NOₓ.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Astrochemistry studies the chemical composition, reactions, and abundances of atoms, molecules, and '
                'ions in space. The interstellar medium (ISM) contains clouds of gas and dust where over 200 molecular '
                'species have been detected by radio and infrared spectroscopy, including H₂, CO, water, formaldehyde, '
                'ethanol, and amino acid glycine. Interstellar chemistry drives the synthesis of organic molecules '
                'that may have seeded early Earth with the building blocks of life.',
        'topic': 'astrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Stars are giant nuclear fusion reactors. In solar-mass stars, the proton-proton chain fuses four '
                'hydrogen nuclei to form one helium-4 nucleus, releasing 26.7 MeV. In more massive stars, the CNO '
                'cycle dominates. Heavier elements up to iron are forged by stellar nucleosynthesis. Elements heavier '
                'than iron require neutron star mergers or supernova explosions — detected as kilonovae and confirmed '
                'by gravitational wave observations in 2017.',
        'topic': 'astrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Solid-state batteries replace the liquid electrolyte of lithium-ion batteries with a solid ceramic or '
                'glass-ceramic electrolyte. They are safer (no flammable liquid), can use lithium metal anodes (much '
                'higher energy density), and may last longer. However, manufacturing solid-solid interfaces with low '
                'resistance remains challenging. Solid-state batteries are considered the next generation of battery '
                'technology for electric vehicles and grid-scale energy storage.',
        'topic': 'electrochemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Chemical safety involves understanding hazards, risks, and correct procedures for handling chemicals. '
                'The Globally Harmonised System (GHS) provides standardised pictograms for chemical hazards: skull and '
                'crossbones (acute toxicity), flame (flammability), corrosion (skin or metal corrosion), exclamation '
                'mark (irritant), environmental hazard, and others. Safety Data Sheets (SDS/MSDS) provide '
                "comprehensive information on each chemical's hazards, safe handling, storage, and emergency "
                'procedures.',
        'topic': 'chemical safety'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Personal protective equipment (PPE) in a chemistry laboratory includes safety goggles (to protect '
                'eyes from splashes and vapours), lab coat (to protect skin and clothing), and appropriate gloves. '
                'Fume cupboards (hoods) protect from toxic or flammable vapours by drawing air away from the worker. '
                'The hierarchy of controls prioritises: elimination of hazard > substitution > engineering controls '
                '(fume hoods) > administrative controls > PPE.',
        'topic': 'chemical safety'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'COSHH (Control of Substances Hazardous to Health) regulations in the UK require risk assessment '
                'before working with hazardous substances. Risk = hazard × exposure. Reducing exposure through '
                'substitution (replacing a hazardous chemical with a safer one), engineering controls (ventilation), '
                'and procedural changes can reduce risk even for inherently hazardous substances. All accidental '
                'chemical releases, spills, or exposures must be reported.',
        'topic': 'chemical safety'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'LD50 (lethal dose 50%) is the dose of a chemical that kills 50% of a test population. It is expressed '
                'in mg of substance per kg of body weight. A lower LD50 indicates higher acute toxicity. Botulinum '
                'toxin has an LD50 of about 1–2 ng/kg (extremely toxic); table salt has LD50 of ~3000 mg/kg '
                '(relatively non-toxic). LD50 is a standard measure of acute oral toxicity but does not capture '
                'chronic toxicity, carcinogenicity, or environmental hazards.',
        'topic': 'chemical safety'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Soil chemistry studies the chemical composition, reactions, and properties of soil. Soil is a complex '
                'mixture of mineral particles (sand, silt, clay), organic matter, water, air, and living organisms. '
                "The cation exchange capacity (CEC) measures soil's ability to hold positively charged nutrient ions "
                '(Ca²⁺, Mg²⁺, K⁺, NH₄⁺) on clay and organic matter surfaces, retaining them against leaching by '
                'rainfall.',
        'topic': 'soil chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Soil pH profoundly affects plant nutrition and microbial activity. Most nutrients are most available '
                'at pH 6.0–7.0. Acidic soils (pH < 5.5) cause aluminium and manganese toxicity, phosphorus lock-up, '
                'and reduced microbial activity. Alkaline soils (pH > 7.5) cause iron, manganese, zinc, and boron '
                'deficiency. Lime (CaCO₃ or Ca(OH)₂) raises pH; sulfur or sulfuric acid lowers it. Soil pH is managed '
                'extensively in agriculture to optimise crop yields.',
        'topic': 'soil chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Nitrogen is the nutrient most limiting to plant growth. Plants can absorb nitrogen only as nitrate '
                '(NO₃⁻) or ammonium (NH₄⁺). The nitrogen cycle converts atmospheric N₂ to plant-available forms '
                'through nitrogen fixation (bacteria), nitrification (NH₄⁺ → NO₂⁻ → NO₃⁻ by Nitrosomonas and '
                'Nitrobacter bacteria), and mineralisation (decomposition of organic N). Synthetic nitrogen '
                'fertilisers (urea, ammonium nitrate) supplement natural nitrogen cycling but can cause nitrate '
                'leaching and N₂O (a potent greenhouse gas) emissions.',
        'topic': 'soil chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Quantum chemistry applies quantum mechanical principles to chemical systems to explain molecular '
                'structure, bonding, and reactivity. The Schrödinger equation (HΨ = EΨ) describes the behaviour of '
                'electrons in atoms and molecules — H is the Hamiltonian operator, Ψ is the wavefunction, and E is the '
                'energy. Exact solutions exist only for hydrogen; approximation methods are used for all '
                'multi-electron systems.',
        'topic': 'quantum chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Density functional theory (DFT) is the most widely used computational quantum chemical method. It '
                'calculates molecular electronic structure using electron density (rather than the many-electron '
                'wavefunction), making it computationally tractable for large molecules. DFT is used to predict '
                'molecular geometries, reaction energies, spectroscopic properties, and catalytic mechanisms. Walter '
                'Kohn received the 1998 Nobel Prize in Chemistry for developing DFT.',
        'topic': 'quantum chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Molecular orbital (MO) theory describes bonding in terms of orbitals extending over the entire '
                'molecule. Linear combination of atomic orbitals (LCAO) produces bonding MOs (lower energy, '
                'stabilising) and antibonding MOs (higher energy, destabilising, marked with *). Bond order = '
                '½(bonding electrons − antibonding electrons). For O₂, MO theory correctly predicts two unpaired '
                'electrons in π* orbitals, explaining its paramagnetism — which valence bond theory fails to predict.',
        'topic': 'quantum chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The photoelectric effect, explained by Einstein in 1905, showed that light consists of photons with '
                'energy E = hf. Electrons are only ejected from a metal surface if the photon frequency exceeds a '
                'threshold — below this, no electrons are emitted regardless of intensity. Above the threshold, '
                'kinetic energy of ejected electrons = hf − φ (work function). This demonstrated the particle nature '
                'of light and earned Einstein the Nobel Prize in Physics.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Aufbau principle states that electrons fill atomic orbitals in order of increasing energy. The '
                'filling order follows: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p… Note that 4s fills before 3d '
                'because it has lower energy in isolated atoms, but when transition metal ions form, 3d electrons are '
                'retained while 4s electrons are lost first. Chromium [Ar]3d⁵4s¹ and copper [Ar]3d¹⁰4s¹ are exceptions '
                'due to extra stability of half-filled and fully filled d orbitals.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Valence bond (VB) theory describes a covalent bond as the overlap of atomic orbitals containing one '
                'electron each from each bonded atom. The greater the orbital overlap, the stronger the bond. '
                'Hybridisation explains geometry: sp³ carbon (tetrahedral, 109.5°), sp² carbon (trigonal planar, 120°, '
                'one unhybridised p orbital available for π bonding), and sp carbon (linear, 180°, two unhybridised p '
                'orbitals). Hybridisation rationalises observed molecular shapes.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Aromaticity is a special stability associated with cyclic, planar molecules with 4n+2 π electrons '
                "(Hückel's rule, n = 0, 1, 2…). Benzene (C₆H₆) has 6 π electrons (n=1) delocalised over all six "
                'carbons in π molecular orbitals. This delocalisation provides about 150 kJ/mol of extra stabilisation '
                '(resonance energy). Aromatic compounds are more resistant to addition reactions (which would disrupt '
                'the ring) and prefer substitution reactions.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Henderson-Hasselbalch equation relates the pH of a buffer to the pKa of the weak acid and the '
                'ratio of conjugate base to acid concentrations: pH = pKa + log([A⁻]/[HA]). At the half-equivalence '
                'point of a titration, [A⁻] = [HA], so log(1) = 0 and pH = pKa. This equation is used to design buffer '
                'solutions for biological experiments, pharmaceutical formulations, and calibration standards.',
        'topic': 'acids and bases'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Polyprotic acids can donate more than one proton per molecule. Sulfuric acid (H₂SO₄) is diprotic: the '
                'first dissociation is complete (strong acid); the second has Ka₂ = 0.012 (weak). Phosphoric acid '
                '(H₃PO₄) is triprotic: Ka₁ = 7.1×10⁻³, Ka₂ = 6.3×10⁻⁸, Ka₃ = 4.2×10⁻¹³. Each successive dissociation '
                'is weaker because removing a proton from an increasingly negatively charged ion becomes progressively '
                'more difficult.',
        'topic': 'acids and bases'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The Periodic Law states that when elements are arranged in order of increasing atomic number, their '
                'physical and chemical properties show a periodic (repeating) pattern. This periodicity arises because '
                'electron configurations repeat — elements in the same group have the same valence electron '
                "configuration. Mendeleev's genius was recognising this pattern in 1869 before atomic numbers were "
                'understood, using atomic mass as his ordering principle.',
        'topic': 'periodic table'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Second period anomalies arise because Period 2 elements (Li, Be, B, C, N, O, F, Ne) differ from '
                'heavier members of their groups due to their small atomic size and inability to expand their valence '
                'shell beyond 8 electrons. Carbon forms pπ-pπ bonds readily (C=C, C=O, C≡C) while silicon prefers '
                'dπ-pπ bonds (weaker). Nitrogen and oxygen follow different bonding patterns than phosphorus and '
                'sulfur, which can have expanded octets.',
        'topic': 'periodic table'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Relativistic effects become significant for heavy elements (period 6 and beyond). At high atomic '
                'number, inner electrons near the nucleus move at speeds approaching the speed of light. Relativistic '
                'mass increase causes these electrons to contract (relativistic contraction of s and p orbitals), '
                'which indirectly causes d and f orbitals to expand. This explains the gold/silver colour difference, '
                "mercury's liquid state at room temperature, and the inertness of the 6s² pair in lead and bismuth.",
        'topic': 'periodic table'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Electrophilic aromatic substitution (EAS) is the key reaction of benzene and aromatic compounds. An '
                'electrophile attacks the electron-rich aromatic ring, and a hydrogen is lost to restore aromaticity. '
                'Examples include nitration (HNO₃/H₂SO₄, adding −NO₂), sulfonation (H₂SO₄, adding −SO₃H), halogenation '
                '(Cl₂/AlCl₃, adding −Cl), and Friedel-Crafts alkylation and acylation. Substituents already on the '
                'ring direct incoming groups to specific positions.',
        'topic': 'organic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Nucleophilic substitution reactions at saturated carbon follow two main mechanisms. SN2 reactions '
                'occur in one step: a nucleophile attacks the back face of the carbon bearing the leaving group, '
                'causing inversion of configuration (Walden inversion). SN1 reactions proceed through a planar '
                'carbocation intermediate, allowing attack from both faces to give a racemic mixture. Primary '
                'substrates favour SN2; tertiary substrates favour SN1; steric hindrance and solvent polarity '
                'determine the mechanism.',
        'topic': 'organic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Liquid crystals are a state of matter intermediate between crystalline solid and isotropic liquid. '
                'They flow like liquids but maintain some long-range molecular order. Nematic liquid crystals have '
                'molecules aligned along a common direction but with no positional order. Liquid crystal displays '
                '(LCDs) in phones, TVs, and monitors use electric fields to control the alignment of liquid crystal '
                'molecules, modulating light transmission through each pixel.',
        'topic': 'states of matter'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Clausius-Clapeyron equation describes how vapour pressure changes with temperature: ln(P₂/P₁) = '
                '−ΔH_vap/R × (1/T₂ − 1/T₁). It shows that vapour pressure increases exponentially with temperature. '
                'This equation is used to calculate boiling points at different pressures — important for vacuum '
                'distillation in pharmaceutical manufacturing where heat-sensitive compounds boil at lower '
                'temperatures under reduced pressure.',
        'topic': 'states of matter'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'A phase diagram maps the stable phases of a substance as a function of temperature and pressure. The '
                'triple point is the unique temperature and pressure at which solid, liquid, and gas coexist in '
                'equilibrium. For water, the triple point is 0.01°C and 612 Pa. Above the critical point (374°C, 218 '
                'atm for water), the liquid and gas phases become indistinguishable, forming a supercritical fluid '
                'with properties of both phases.',
        'topic': 'states of matter'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The Ostwald process converts ammonia to nitric acid in three steps: (1) catalytic oxidation of NH₃ '
                'over platinum-rhodium gauze catalyst at 900°C to produce NO; (2) oxidation of NO to NO₂ by '
                'atmospheric oxygen; (3) absorption of NO₂ in water to form HNO₃ and NO (which is recycled). Nitric '
                'acid is used primarily in fertiliser production (ammonium nitrate) and also in explosives and dyes '
                'manufacturing.',
        'topic': 'chemical reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The equilibrium position of a reaction can be described quantitatively by the Gibbs free energy. At '
                'equilibrium, ΔG = 0. For reactions far from equilibrium, ΔG = ΔG° + RT ln Q. Reactions proceed '
                'spontaneously in the direction that decreases ΔG toward zero. The standard free energy change ΔG° is '
                'related to the equilibrium constant by ΔG° = −RT ln K — a large negative ΔG° means a large K and '
                'strongly product-favoured equilibrium.',
        'topic': 'chemical reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Metabolism encompasses all chemical reactions in living organisms. Anabolism builds complex molecules '
                'from simple ones (requiring energy): protein synthesis, DNA replication, glycogen synthesis. '
                'Catabolism breaks down complex molecules to release energy: cellular respiration, lipolysis (fat '
                'breakdown), proteolysis (protein breakdown). ATP (adenosine triphosphate) is the universal energy '
                'currency — hydrolysis of ATP to ADP + Pᵢ releases 30.5 kJ/mol, coupling exergonic catabolic reactions '
                'to endergonic anabolic ones.',
        'topic': 'biochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Beta-oxidation is the metabolic pathway that degrades fatty acids to produce acetyl-CoA, NADH, and '
                'FADH₂ for energy production. Each cycle of beta-oxidation removes a two-carbon unit as acetyl-CoA and '
                'shortens the fatty acid chain by two carbons. A 16-carbon palmitic acid undergoes 7 cycles of '
                'beta-oxidation, producing 8 acetyl-CoA units. These feed the Krebs cycle, ultimately producing much '
                'more ATP per gram than glucose (39 ATP per glucose vs ~129 ATP per palmitate).',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Green chemistry's 12 principles, articulated by Anastas and Warner (1998), provide a framework for "
                'designing more sustainable chemical processes. The principles include: prevention of waste is better '
                'than treatment; atom economy maximises incorporation of reagents into products; design less hazardous '
                'chemical syntheses; use renewable feedstocks; design for degradation; use safer solvents and reaction '
                'conditions; and use catalysis rather than stoichiometric reagents.',
        'topic': 'green chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Solvent choice is critical in green chemistry because solvents constitute the majority of waste in '
                'chemical manufacturing. Traditional solvents (chlorinated hydrocarbons like DCM and chloroform) are '
                'toxic and environmentally persistent. Green alternatives include water, supercritical CO₂ (zero '
                'solvent residue), ionic liquids (negligible vapour pressure), and bio-derived solvents like ethyl '
                'lactate and 2-methylTHF from renewable feedstocks.',
        'topic': 'green chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'E-factor (environmental factor) quantifies the waste generated per kilogram of desired product in a '
                'chemical process. E-factor = kg waste / kg product. The pharmaceutical industry has E-factors of '
                '25–100+, producing far more waste than product. The oil refining industry has E-factors less than '
                '0.1. Reducing E-factors through catalytic processes, solvent recovery, and high atom economy '
                'reactions is a central goal of green chemistry in industrial manufacturing.',
        'topic': 'green chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A crystal is a solid in which atoms, ions, or molecules are arranged in a regularly repeating '
                'three-dimensional pattern called a crystal lattice. The smallest repeating unit is the unit cell. '
                'Crystal structures are classified into seven crystal systems (cubic, tetragonal, orthorhombic, '
                'hexagonal, trigonal, monoclinic, triclinic) based on the geometry of their unit cells. Most metals '
                'and ionic compounds are crystalline.',
        'topic': 'crystallography'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Ionic crystal structures depend on the ratio of cation to anion radii. The rock salt structure (NaCl) '
                'has each ion surrounded by six ions of opposite charge in an octahedral arrangement. The caesium '
                'chloride structure (CsCl) has a body-centred cubic arrangement with coordination number 8. The zinc '
                'blende structure (ZnS) has each ion tetrahedrally surrounded by four of the opposite type. Different '
                'structures give different physical properties.',
        'topic': 'crystallography'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Diamond and graphite are both allotropes (different structural forms) of carbon with vastly different '
                'properties. Diamond has a tetrahedral sp³ network where each carbon bonds to four others in an '
                'infinite 3D lattice — making it extremely hard (Mohs 10) with no free electrons (electrical '
                'insulator). Graphite has sp² carbons in flat hexagonal sheets with delocalised π electrons '
                '(electrical conductor) held together by weak van der Waals forces (lubricant and pencil core).',
        'topic': 'crystallography'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Transition metals occupy Groups 3–12 of the periodic table and are characterised by partially filled '
                'd orbitals. They show characteristic properties: multiple oxidation states, form coloured compounds, '
                'exhibit catalytic activity, form stable complex ions with ligands, and show ferromagnetic or '
                'paramagnetic behaviour. Iron, copper, zinc, titanium, and platinum are commercially important '
                'transition metals.',
        'topic': 'transition metals'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Transition metals exhibit variable oxidation states because the energies of the (n-1)d and ns '
                'orbitals are similar, so different numbers of electrons can be removed. Iron shows +2 (Fe²⁺, green) '
                'and +3 (Fe³⁺, yellow-brown) states. Manganese ranges from +2 (pale pink Mn²⁺) to +7 (deep purple '
                'MnO₄⁻). Copper shows +1 (Cu⁺, colourless) and +2 (Cu²⁺, blue). The multiple oxidation states make '
                'transition metals important industrial catalysts.',
        'topic': 'transition metals'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The colours of transition metal compounds arise from d-d electronic transitions. When ligands split d '
                'orbital energies (crystal field splitting), electrons absorb photons of visible light to move between '
                'the lower and upper d orbital sets. The wavelength absorbed (and thus the complementary colour '
                'observed) depends on the metal ion, its oxidation state, and the ligand field strength. [Cu(H₂O)₆]²⁺ '
                'is blue (absorbs orange); [Cu(NH₃)₄]²⁺ is deep blue-violet (larger Δ with stronger-field ammonia '
                'ligands).',
        'topic': 'transition metals'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Transition metals are essential catalysts in industrial chemistry. Iron catalyses the Haber process '
                '(ammonia synthesis). Vanadium(V) oxide (V₂O₅) catalyses SO₂ oxidation in the Contact process. '
                'Platinum and palladium catalyse automotive exhaust treatment. Nickel catalyses hydrogenation of '
                'vegetable oils. Transition metals function as heterogeneous catalysts by adsorbing reactants on their '
                'surfaces, weakening bonds and enabling reactions at lower activation energy.',
        'topic': 'transition metals'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Magnetism in transition metal compounds arises from unpaired electrons. Each unpaired electron has a '
                'magnetic moment due to its spin. Paramagnetic compounds are weakly attracted to magnetic fields '
                '(unpaired electrons, spins unaligned). Ferromagnetic materials (iron, cobalt, nickel) are strongly '
                'magnetised — unpaired electrons in domains align parallel. Antiferromagnetic materials have '
                'antiparallel alignment and show no net magnetism. Magnetic properties of compounds are measured by '
                'their magnetic moments, calculated from the number of unpaired electrons.',
        'topic': 'transition metals'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Medicinal chemistry combines chemistry, pharmacology, and biology to design and develop new drugs. '
                'The drug discovery process begins with identifying a biological target (a disease-causing protein or '
                "pathway), finding a 'hit' compound with initial activity, and optimising it into a 'lead' compound "
                'through systematic structural modifications that improve potency, selectivity, and pharmacokinetics '
                'while minimising toxicity.',
        'topic': 'medicinal chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Structure-activity relationships (SAR) describe how changes in a molecule's chemical structure affect "
                'its biological activity. Medicinal chemists systematically modify functional groups, chain lengths, '
                'stereochemistry, and ring systems to improve drug potency. Adding lipophilic groups improves membrane '
                "permeability; adding polar groups improves solubility. Lipinski's Rule of Five predicts oral "
                'bioavailability: molecular weight < 500, log P < 5, ≤5 H-bond donors, ≤10 H-bond acceptors.',
        'topic': 'medicinal chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Clinical trials evaluate new drugs in three phases. Phase I (20–100 healthy volunteers) tests safety '
                'and pharmacokinetics. Phase II (100–500 patients) tests efficacy and side effects. Phase III '
                '(1000–5000 patients) compares the new drug against current standard treatment in randomised '
                'controlled trials. Only after successful Phase III trials does a drug receive regulatory approval. '
                'The entire process from discovery to approval typically takes 10–15 years and costs over $1 billion.',
        'topic': 'medicinal chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Bioinorganic chemistry examines the roles of metal ions in biological systems. About one-third of all '
                'proteins require a metal cofactor. Essential metals include iron (haemoglobin, enzymes), zinc (over '
                '300 enzymes, immune function), copper (electron transfer proteins, oxidase enzymes), magnesium (ATP '
                'binding, chlorophyll), and calcium (signalling, muscle contraction, bone). Trace metals are required '
                'in tiny amounts but are essential — deficiency causes specific diseases.',
        'topic': 'bioinorganic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Haem is an iron-porphyrin complex central to biological oxygen transport and electron transfer. In '
                'haemoglobin and myoglobin, Fe²⁺ in haem reversibly binds O₂. In cytochromes (components of the '
                'electron transport chain), iron cycles between Fe²⁺ and Fe³⁺ to transfer electrons. Haem iron is much '
                'more bioavailable than non-haem iron (plant-based), explaining why anaemia is common in vegetarians '
                'and why meat is nutritionally important for iron status.',
        'topic': 'bioinorganic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Cisplatin [cis-Pt(NH₃)₂Cl₂] is one of the most important anticancer drugs. After entering cancer '
                'cells, chloride ligands are replaced by water, making the complex highly reactive. It then '
                'cross-links adjacent guanine bases on the same DNA strand, blocking replication and transcription, '
                'triggering apoptosis (programmed cell death). However, cisplatin has serious side effects '
                '(nephrotoxicity, neurotoxicity) and resistance develops — driving development of second (carboplatin) '
                'and third generation (oxaliplatin) platinum drugs.',
        'topic': 'bioinorganic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Raoult's Law states that the vapour pressure of a solvent above a solution is proportional to the "
                'mole fraction of solvent: P = X_solvent × P°_solvent. Adding a non-volatile solute always lowers '
                'vapour pressure. This explains why antifreeze solutions (ethylene glycol in water) have lower vapour '
                'pressure and higher boiling points than pure water, and why salty water boils above 100°C.',
        'topic': 'colligative properties'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Osmotic pressure (π) is the pressure required to prevent osmotic flow of solvent through a '
                "semi-permeable membrane: π = MRTi (van 't Hoff equation), where M is molarity, R is gas constant, T "
                "is absolute temperature, and i is the van 't Hoff factor. Blood has an osmotic pressure of about 7.7 "
                'atm. Intravenous solutions must be isotonic (same osmotic pressure as blood — 0.9% NaCl or 5% '
                'glucose) to prevent cell lysis or crenation.',
        'topic': 'colligative properties'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Alchemy was the forerunner of modern chemistry, practiced in Europe, the Islamic world, and China '
                'from antiquity until the 18th century. Alchemists sought to transmute base metals to gold, discover '
                "the philosopher's stone (granting immortality), and prepare universal medicines. Despite their "
                'mystical goals, alchemists made practical contributions: they discovered mineral acids, developed '
                'distillation apparatus, and accumulated extensive knowledge of chemical substances and reactions.',
        'topic': 'history of chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Antoine Lavoisier (1743–1794) is considered the father of modern chemistry. He demonstrated that '
                'combustion requires oxygen (not phlogiston, as previously believed), established the law of '
                'conservation of mass through careful quantitative experiments, developed the modern system of '
                'chemical nomenclature, and co-authored the first modern chemistry textbook. He was guillotined during '
                "the French Revolution's Reign of Terror at age 50.",
        'topic': 'history of chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "John Dalton's atomic theory (1803–1808) proposed: all matter consists of indivisible atoms; atoms of "
                'the same element are identical in mass and properties; atoms combine in simple whole-number ratios to '
                'form compounds; atoms are neither created nor destroyed in chemical reactions. This theory provided '
                'the first scientific atomic model and explained the laws of conservation of mass and definite '
                'proportions, founding modern chemistry on quantitative principles.',
        'topic': 'history of chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Marie Curie (1867–1934) pioneered research into radioactivity — a term she coined. She discovered '
                'polonium and radium, the first time chemical elements were identified through their radioactivity '
                'rather than conventional chemical means. She was the first woman to win a Nobel Prize (Physics, 1903) '
                'and the only person to win Nobel Prizes in two different sciences (Chemistry, 1911). Her work opened '
                'nuclear physics and led directly to cancer radiotherapy.',
        'topic': 'history of chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The discovery of penicillin by Alexander Fleming in 1928 and its development into a medicine by '
                'Howard Florey and Ernst Chain (Nobel Prize 1945) transformed medicine. The chemical structure of '
                'penicillin was elucidated by Dorothy Hodgkin using X-ray crystallography. The beta-lactam ring is '
                'essential for antibiotic activity. Industrial fermentation of Penicillium moulds produces penicillin '
                'at large scale, saving millions of lives from bacterial infections that were previously often fatal.',
        'topic': 'history of chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Linus Pauling won two Nobel Prizes: Chemistry (1954) for his work on the nature of the chemical bond '
                '(describing hybridisation, resonance, and electronegativity quantitatively) and Peace (1962) for his '
                "anti-nuclear weapons activism. His book 'The Nature of the Chemical Bond' (1939) is one of the most "
                'influential scientific books ever written. Pauling also proposed the alpha-helix and beta-sheet '
                'structures of proteins and independently proposed a DNA triple-helix structure (incorrectly) just '
                'before Watson and Crick solved it.',
        'topic': 'history of chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The global warming potential (GWP) compares the heat-trapping ability of a greenhouse gas relative to '
                'CO₂ over 100 years. CO₂ has GWP = 1 (reference). Methane (CH₄) has GWP = 28–36 — it traps more heat '
                'per molecule but has a shorter atmospheric lifetime (~12 years) than CO₂ (~hundreds of years). '
                'Nitrous oxide (N₂O) has GWP = 265–298 and persists for 120 years. Sulfur hexafluoride (SF₆, used in '
                'electrical switchgear) has GWP = 23,900 — the most potent known greenhouse gas.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Aerosol chemistry involves tiny solid or liquid particles suspended in the atmosphere. Sulfate '
                'aerosols from SO₂ emissions scatter incoming sunlight and cool the climate — large volcanic eruptions '
                'release SO₂ that can temporarily reduce global temperatures by 0.5°C. Black carbon (soot) from '
                'incomplete combustion absorbs sunlight and warms the atmosphere. Aerosols also act as cloud '
                'condensation nuclei — particles around which water vapour condenses to form cloud droplets, '
                'influencing precipitation and climate.',
        'topic': 'atmospheric chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Forensic chemistry applies chemical analysis to legal investigations. At crime scenes, forensic '
                'chemists analyse blood, drugs, explosives, fibres, glass, soil, paint, and poisons. Techniques '
                'include chromatography (GC-MS to identify drugs and accelerants), spectroscopy (IR for unknown '
                'substances, UV-Vis for blood analysis), immunoassay (rapid drug screening), and DNA analysis. '
                'Forensic evidence must meet strict chain-of-custody and quality assurance standards to be admissible '
                'in court.',
        'topic': 'forensic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Drug testing in sports (anti-doping) uses urine and blood samples analysed by GC-MS and liquid '
                'chromatography-MS (LC-MS). The World Anti-Doping Agency (WADA) maintains a prohibited substances list '
                'including anabolic steroids (testosterone, nandrolone), erythropoietin (EPO, blood doping), and '
                'stimulants. Hair testing can detect drug use up to 90 days after ingestion, unlike urine testing '
                'which typically detects use within 1–7 days.',
        'topic': 'forensic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Explosive detection uses trace chemical analysis — ion mobility spectrometry (IMS) detects picogram '
                'quantities of explosive vapours in airport security scanners. Common explosives include TNT '
                '(2,4,6-trinitrotoluene), RDX, PETN, and TATP (triacetone triperoxide — a home-made explosive favoured '
                'by terrorists, detectable by its characteristic acetone vapour). Post-blast analysis identifies '
                'explosive residues using GC-MS, ion chromatography, and colorimetric spot tests to determine the type '
                'of explosive used.',
        'topic': 'forensic chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Metals are extracted from ores using reduction methods appropriate to their reactivity. Very reactive '
                'metals (aluminium, magnesium) require electrolysis of their molten salts. Moderately reactive metals '
                '(iron, copper) can be reduced by carbon (coke) in a blast furnace or by smelting. Unreactive metals '
                '(gold, platinum) occur native (as free metal) and need minimal processing. The higher the reactivity, '
                'the more energy is required for extraction.',
        'topic': 'chemistry of metals'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The blast furnace extracts iron from iron ore (haematite, Fe₂O₃). Coke (carbon) reacts with air to '
                'form CO₂, then CO at high temperatures: CO₂ + C → 2CO. Carbon monoxide reduces iron oxide: Fe₂O₃ + '
                '3CO → 2Fe + 3CO₂. Limestone (CaCO₃) decomposes to CaO, which reacts with acidic silica impurities to '
                'form calcium silicate slag. Molten iron (pig iron, ~4% carbon) sinks to the bottom while slag floats '
                'above and is tapped off separately.',
        'topic': 'chemistry of metals'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Aluminium extraction requires electrolysis because aluminium is too reactive to be reduced by carbon '
                'economically. Aluminium oxide (Al₂O₃, alumina) from bauxite ore is dissolved in molten cryolite '
                '(Na₃AlF₆) to lower the melting point from 2000°C to ~950°C. Electrolysis produces liquid aluminium at '
                'the cathode (Al³⁺ + 3e⁻ → Al) and oxygen at carbon anodes (2O²⁻ → O₂ + 4e⁻). The anodes gradually '
                'oxidise and must be replaced. Aluminium smelting is highly energy-intensive — about 5% of global '
                'electricity is used for this purpose.',
        'topic': 'chemistry of metals'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Zone refining is used to produce ultra-pure metals and semiconductors for electronics. A narrow '
                'molten zone is passed slowly along a metal bar. Impurities concentrate in the molten zone (liquid '
                'phase) rather than the solidifying metal behind it, and are carried to one end of the bar where they '
                'accumulate. Multiple passes progressively purify the metal. Silicon for semiconductor devices must be '
                'purified to 99.9999999% (nine nines) purity using zone refining and Czochralski crystal growth.',
        'topic': 'chemistry of metals'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Carbon exists in several allotropic forms with dramatically different properties. Diamond (sp³ '
                'hybridisation, tetrahedral network) is the hardest known natural material. Graphite (sp² '
                'hybridisation, planar sheets) is soft and lubricating. Buckminsterfullerene C₆₀ (discovered 1985, '
                'Nobel Prize 1996) is a hollow sphere of 60 carbon atoms arranged in pentagons and hexagons like a '
                'football. Carbon nanotubes (1991) are cylindrical rolled graphene sheets with extraordinary strength '
                'and electrical properties.',
        'topic': 'carbon allotropes'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Fullerenes are closed-cage carbon molecules consisting of pentagons and hexagons of carbon atoms. C₆₀ '
                '(buckminsterfullerene) is the most abundant — each carbon is sp² hybridised, bonded to three '
                'neighbours, with one delocalised π electron. Fullerenes are excellent electron acceptors used in '
                'organic solar cells. Endohedral fullerenes contain a metal atom trapped inside (e.g., La@C₆₀), with '
                'potential applications in quantum computing and targeted drug delivery.',
        'topic': 'carbon allotropes'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Carbon nanotubes (CNTs) are seamless cylinders of rolled graphene. Single-walled CNTs (SWCNTs) have '
                'diameters of 0.8–2 nm; multi-walled CNTs consist of concentric tubes. Depending on the rolling angle '
                '(chirality), CNTs can be metallic conductors or semiconductors. CNTs are 100 times stronger than '
                'steel at 1/6 the density, have thermal conductivity exceeding diamond, and can carry current density '
                '1000 times greater than copper. Applications include composite materials, field emission displays, '
                'and biosensors.',
        'topic': 'carbon allotropes'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The mole concept is the central quantitative tool in chemistry, linking the atomic world to '
                'laboratory measurements. One mole (6.022 × 10²³ particles) of any substance has a mass in grams equal '
                'to its molar mass. Moles can be converted to mass (m = n × M), number of particles (N = n × Nₐ), or '
                'volume of gas at STP (V = n × 22.4 L). Mastering mole calculations is essential for stoichiometry, '
                'solution chemistry, and thermochemistry.',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Le Chatelier's principle is one of the most useful qualitative tools in chemistry, applying to any "
                'equilibrium system including chemical reactions, dissolution, phase changes, and acid-base '
                'equilibria. The key insight is that equilibrium systems self-regulate — any perturbation triggers a '
                'response that partially counteracts the perturbation. This principle guides industrial chemists in '
                'optimising conditions for reactions like the Haber process, the Contact process, and esterification.',
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Organic functional groups determine the characteristic chemical reactions of organic molecules. The '
                'order of priority for IUPAC naming (from highest to lowest): carboxylic acids (−COOH), esters '
                '(−COO−), aldehydes (−CHO), ketones (C=O), alcohols (−OH), amines (−NH₂), alkenes (C=C), alkynes '
                '(C≡C), haloalkanes. Each functional group has characteristic reactions: alcohols undergo oxidation, '
                'substitution, and elimination; carboxylic acids undergo esterification and decarboxylation.',
        'topic': 'organic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Spectroscopic data interpretation for structure determination follows a logical workflow. First, use '
                'mass spectrometry to determine molecular mass (M⁺) and identify fragments. Then use IR spectroscopy '
                'to identify functional groups present. Use ¹H NMR to determine the number and types of hydrogen '
                'environments, their integration ratios, and coupling patterns. Finally, use ¹³C NMR to count carbon '
                'environments. Combining all data usually enables unambiguous structure assignment of unknown organic '
                'compounds.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Born-Haber cycle illustrates how thermochemical cycles connect seemingly unrelated quantities. It '
                "uses Hess's Law to relate lattice enthalpy (difficult to measure directly) to measurable quantities: "
                'standard enthalpy of formation of the ionic compound, atomisation enthalpy of the metal, first '
                'ionisation energy of the metal, atomisation (bond dissociation) enthalpy of the nonmetal, and first '
                'electron affinity of the nonmetal. Discrepancies between theoretical and experimental values reveal '
                'partial covalent character.',
        'topic': 'thermochemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Chemical kinetics is the study of how fast chemical reactions occur and what factors affect their '
                'speed. Reaction rate is defined as the change in concentration of a reactant or product per unit '
                'time. Understanding reaction rates helps scientists control industrial processes, design medicines, '
                'and preserve food.',
        'topic': 'kinetics'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Four main factors affect the rate of a chemical reaction: temperature, concentration, surface area, '
                'and the presence of a catalyst. Increasing any of these generally speeds up a reaction. For example, '
                'grinding a solid into a fine powder increases its surface area, allowing more collisions between '
                'reactant particles per second.',
        'topic': 'kinetics'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Collision theory states that for a reaction to occur, particles must collide with the correct '
                'orientation and with energy equal to or greater than the activation energy. Not every collision leads '
                'to a reaction — only those with sufficient energy and proper geometry are successful. Increasing '
                'temperature raises the fraction of particles with enough energy to react successfully.',
        'topic': 'kinetics'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A Maxwell-Boltzmann distribution curve shows the spread of kinetic energies among particles in a gas '
                'at a given temperature. The area under the curve to the right of the activation energy represents the '
                'fraction of particles able to react. When temperature increases, the curve shifts right and flattens, '
                'meaning a greater proportion of particles exceed the activation energy.',
        'topic': 'kinetics'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The rate law of a reaction expresses how the reaction rate depends on reactant concentrations: rate = '
                'k[A]^m[B]^n. The exponents m and n are the reaction orders with respect to each reactant and must be '
                'determined experimentally. The rate constant k is specific to a reaction at a given temperature and '
                'increases with rising temperature.',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'A first-order reaction is one where the rate is directly proportional to the concentration of one '
                'reactant: rate = k[A]. The integrated rate law for a first-order reaction is ln[A] = ln[A]₀ − kt, '
                'which gives a straight line when ln[A] is plotted against time. Radioactive decay is a classic '
                'example of a first-order process.',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "A second-order reaction has a rate that depends on the square of one reactant's concentration or on "
                "the product of two reactants' concentrations: rate = k[A]². The integrated rate law is 1/[A] = 1/[A]₀ "
                '+ kt, giving a straight line when 1/[A] is plotted against time. The half-life of a second-order '
                'reaction increases as the initial concentration decreases.',
        'topic': 'kinetics'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The Arrhenius equation k = Ae^(−Ea/RT) quantitatively relates the rate constant to temperature and '
                'activation energy. Taking the natural log gives ln k = ln A − Ea/RT, which is a linear equation — a '
                'plot of ln k versus 1/T gives a straight line with slope −Ea/R. This allows the activation energy to '
                'be determined experimentally from rate constants measured at different temperatures.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'A reaction mechanism is the step-by-step sequence of elementary reactions by which reactants are '
                'converted to products. The slowest step in the mechanism is called the rate-determining step, because '
                'it controls the overall rate of the reaction. Reaction intermediates are species that are produced in '
                'one step and consumed in a subsequent step — they do not appear in the overall equation.',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Enzymes are biological catalysts that dramatically increase reaction rates in living organisms by '
                'lowering activation energy. The Michaelis-Menten model describes enzyme kinetics, where the enzyme '
                '(E) binds the substrate (S) to form an enzyme-substrate complex (ES), which then releases the product '
                '(P). The Michaelis constant (Km) represents the substrate concentration at which the reaction rate is '
                'half its maximum value (Vmax).',
        'topic': 'kinetics'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Homogeneous catalysts are in the same phase as the reactants, while heterogeneous catalysts are in a '
                'different phase. An example of heterogeneous catalysis is the catalytic converter in cars, where '
                'platinum and palladium metals on a ceramic surface convert toxic CO and NOₓ gases into less harmful '
                'CO₂ and N₂. Heterogeneous catalysts work by adsorbing reactant molecules onto their surface, '
                'weakening bonds and lowering activation energy.',
        'topic': 'kinetics'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'Air is a mixture of gases — about 78% nitrogen, 21% oxygen, and 1% argon, with small amounts of '
                'carbon dioxide and other gases. Gases have no fixed shape or volume and spread out to fill whatever '
                'container they occupy. Unlike solids and liquids, gas particles are far apart and move very fast in '
                'all directions.',
        'topic': 'gases and gas laws'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Gas pressure is caused by the constant collisions of gas molecules against the walls of their '
                'container. The more collisions per second and the harder each collision, the higher the pressure. '
                'Pressure is measured in units such as atmospheres (atm), pascals (Pa), or millimeters of mercury '
                '(mmHg); standard atmospheric pressure is 101,325 Pa or 1 atm.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Boyle's Law states that at constant temperature, the pressure of a gas is inversely proportional to "
                'its volume: P₁V₁ = P₂V₂. If you squeeze a gas into half its volume, the pressure doubles. This '
                'happens because the same number of particles are hitting a smaller area more frequently.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Charles's Law states that at constant pressure, the volume of a gas is directly proportional to its "
                'absolute temperature: V₁/T₁ = V₂/T₂, where temperature must be in Kelvin. A balloon inflated indoors '
                'shrinks when taken outside in cold weather because cooling the gas reduces particle speed and the gas '
                'contracts. Converting Celsius to Kelvin: K = °C + 273.15.',
        'topic': 'gases and gas laws'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Gay-Lussac's Law states that at constant volume, the pressure of a gas is directly proportional to "
                'its absolute temperature: P₁/T₁ = P₂/T₂. This is why pressure cookers build up pressure as '
                'temperature rises, and why sealed aerosol cans can explode if heated. The law is a consequence of gas '
                'particles moving faster and hitting walls harder at higher temperatures.',
        'topic': 'gases and gas laws'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': "The combined gas law merges Boyle's, Charles's, and Gay-Lussac's laws into one equation: P₁V₁/T₁ = "
                'P₂V₂/T₂. This is useful when all three variables — pressure, volume, and temperature — change '
                'simultaneously. It applies to a fixed amount of gas and requires temperature to be expressed in '
                'Kelvin.',
        'topic': 'gases and gas laws'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The ideal gas law PV = nRT combines all the gas laws and includes the amount of gas (n, in moles). R '
                'is the universal gas constant (8.314 J/mol·K or 0.08206 L·atm/mol·K). An ideal gas is a theoretical '
                'model that assumes no intermolecular attractions and infinitely small particle volume; real gases '
                'approximate ideal behavior best at high temperatures and low pressures.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Dalton's Law of Partial Pressures states that the total pressure of a mixture of gases equals the sum "
                'of the partial pressures of each individual gas: P_total = P₁ + P₂ + P₃ + … Each gas exerts its '
                'pressure independently, as if it were the only gas present. This law is used in scuba diving to '
                'calculate safe breathing mixtures and in analyzing atmospheric pressure.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Graham's Law of Effusion states that the rate of effusion (escape of gas through a tiny hole) is "
                "inversely proportional to the square root of the gas's molar mass: rate₁/rate₂ = √(M₂/M₁). Lighter "
                'gases effuse faster than heavier gases. For example, hydrogen (M = 2 g/mol) effuses about four times '
                'faster than oxygen (M = 32 g/mol) because √(32/2) = 4.',
        'topic': 'gases and gas laws'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Real gases deviate from ideal behavior at high pressures and low temperatures. At high pressure, gas '
                'molecules are forced close together and intermolecular attractions become significant, reducing the '
                'volume compared to ideal predictions. At low temperatures, molecules move slowly enough for '
                'intermolecular forces to have a noticeable effect, causing gases to condense into liquids.',
        'topic': 'gases and gas laws'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The van der Waals equation corrects the ideal gas law for real gas behavior: (P + a/V²)(V − b) = nRT. '
                "The constant 'a' corrects for intermolecular attractions (which reduce pressure), and 'b' corrects "
                'for the finite volume of gas molecules (which reduces available space). Different gases have '
                'different values of a and b depending on their size and polarity.',
        'topic': 'gases and gas laws'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The root mean square (rms) speed of gas molecules is given by u_rms = √(3RT/M), where R is the gas '
                'constant, T is temperature in Kelvin, and M is the molar mass in kg/mol. This formula shows that '
                'lighter molecules move faster at a given temperature. At 25°C, hydrogen molecules move at about 1920 '
                'm/s on average, while oxygen molecules move at about 482 m/s.',
        'topic': 'gases and gas laws'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Coordination chemistry studies metal complexes — compounds where a central metal ion is surrounded by '
                'molecules or ions called ligands. Ligands donate lone pairs of electrons to the metal ion, forming '
                'coordinate (dative) covalent bonds. Common ligands include water (H₂O), ammonia (NH₃), chloride ions '
                '(Cl⁻), and cyanide ions (CN⁻).',
        'topic': 'coordination chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The coordination number of a metal complex is the total number of ligand atoms directly bonded to the '
                'central metal ion. Common coordination numbers are 4 (tetrahedral or square planar) and 6 '
                '(octahedral). For example, in [Cu(H₂O)₆]²⁺, copper has a coordination number of 6 because six water '
                'molecules surround it.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Ligands are classified by the number of donor atoms they use to bind to the metal. Monodentate '
                'ligands bind through one atom (e.g., NH₃, Cl⁻), bidentate ligands bind through two atoms (e.g., '
                'ethylenediamine, en), and polydentate ligands bind through multiple atoms. EDTA '
                '(ethylenediaminetetraacetic acid) is a hexadentate ligand that can form six bonds with a single metal '
                'ion, making it extremely stable.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Crystal field theory explains the colors and magnetic properties of transition metal complexes. When '
                'ligands approach a metal ion, they split the d orbitals into two sets of different energies. The '
                'energy difference (crystal field splitting energy, Δ) determines the color of the complex, because '
                'light of a specific energy is absorbed to promote electrons between the split d orbitals.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The chelate effect refers to the extra stability of complexes formed by polydentate ligands compared '
                'to those with the same number of monodentate ligands. This stability arises from the large positive '
                'entropy change when multiple monodentate ligands are replaced by one polydentate ligand, because the '
                'number of free particles in solution increases. Chelation is exploited in medicine — EDTA is used as '
                'an antidote for heavy metal poisoning.',
        'topic': 'coordination chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'IUPAC nomenclature for coordination compounds follows specific rules: ligands are named before the '
                "metal, anionic ligands end in '-o' (e.g., chloro, cyano), neutral ligands keep their names (except "
                'water = aqua, ammonia = ammine). The oxidation state of the metal is given in Roman numerals in '
                'parentheses. For example, [Fe(CN)₆]⁴⁻ is named hexacyanoferrate(II) ion.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Geometric isomerism occurs in square planar and octahedral complexes where ligands can be arranged '
                'differently around the metal. In a square planar complex like [Pt(NH₃)₂Cl₂], the cis isomer has '
                'identical ligands on the same side, while the trans isomer has them on opposite sides. Cisplatin '
                '(cis-[Pt(NH₃)₂Cl₂]) is a widely used anticancer drug, while the trans isomer is biologically '
                'inactive.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The spectrochemical series ranks ligands from weakest to strongest field based on their ability to '
                'split d orbitals. Weak-field ligands (like I⁻, Cl⁻, F⁻) cause small splitting and favor high-spin '
                'complexes, while strong-field ligands (like CN⁻ and CO) cause large splitting and favor low-spin '
                'complexes. High-spin complexes have more unpaired electrons and are paramagnetic, while low-spin '
                'complexes tend to be diamagnetic.',
        'topic': 'coordination chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Hemoglobin is a biological coordination complex where iron(II) ions at the center of heme groups bind '
                'reversibly to oxygen molecules. Each hemoglobin molecule contains four heme units and can carry four '
                'oxygen molecules. Carbon monoxide (CO) is a strong-field ligand that binds to the iron in hemoglobin '
                'about 200 times more strongly than oxygen, blocking oxygen transport and causing CO poisoning.',
        'topic': 'coordination chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Biochemistry is the study of the chemical processes that occur inside living organisms. It '
                'investigates the structure, function, and interactions of biological molecules such as carbohydrates, '
                'lipids, proteins, and nucleic acids. Understanding biochemistry is essential for medicine, nutrition, '
                'genetics, and drug development.',
        'topic': 'biochemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Carbohydrates are organic molecules made of carbon, hydrogen, and oxygen, typically in a 1:2:1 ratio. '
                'Simple sugars (monosaccharides) like glucose (C₆H₁₂O₆) are the main energy source for cells. Complex '
                'carbohydrates (polysaccharides) like starch and cellulose are made of long chains of monosaccharides '
                'linked by glycosidic bonds.',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Proteins are large biological molecules made of amino acid monomers linked by peptide bonds. There '
                'are 20 different amino acids, and the unique sequence in which they are joined determines the '
                "protein's structure and function. Proteins carry out a vast range of functions including catalysis "
                '(enzymes), transport (hemoglobin), structural support (collagen), and immune defense (antibodies).',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Lipids are a diverse group of hydrophobic (water-insoluble) biological molecules including fats, '
                'oils, phospholipids, and steroids. Triglycerides — the main form of stored fat — consist of three '
                'fatty acid chains esterified to a glycerol molecule. Phospholipids form the bilayer of cell membranes '
                'because they have a hydrophilic (water-attracting) head and two hydrophobic (water-repelling) tails.',
        'topic': 'biochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'DNA (deoxyribonucleic acid) stores genetic information in the sequence of its four nitrogenous bases: '
                'adenine (A), thymine (T), guanine (G), and cytosine (C). The two strands of DNA are held together by '
                'hydrogen bonds between complementary base pairs: A pairs with T, and G pairs with C. The double helix '
                'structure of DNA was discovered by Watson and Crick in 1953, building on X-ray data from Rosalind '
                'Franklin.',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Enzymes are biological catalysts — nearly all are proteins — that speed up chemical reactions in '
                'cells by lowering the activation energy. Each enzyme has an active site with a specific shape that '
                'fits only certain substrate molecules, described by the lock-and-key model. Enzyme activity is '
                'affected by temperature, pH, and the presence of inhibitors — most human enzymes work best around '
                '37°C and pH 7.4.',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Cellular respiration is the biochemical process by which cells break down glucose to produce ATP '
                "(adenosine triphosphate), the cell's primary energy currency. The overall equation is C₆H₁₂O₆ + 6O₂ → "
                '6CO₂ + 6H₂O + energy (ATP). It occurs in three stages: glycolysis (in the cytoplasm), the Krebs '
                'cycle, and oxidative phosphorylation (both in the mitochondria).',
        'topic': 'biochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Photosynthesis is the process by which plants, algae, and some bacteria convert light energy into '
                'chemical energy stored as glucose. The overall equation is 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + '
                '6O₂. It takes place in two stages: the light-dependent reactions (in the thylakoid membranes) and the '
                'Calvin cycle (in the stroma of chloroplasts).',
        'topic': 'biochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Protein structure is organized at four levels. Primary structure is the amino acid sequence. '
                'Secondary structure involves local folding into alpha helices or beta sheets stabilized by hydrogen '
                'bonds. Tertiary structure is the overall 3D shape of a single polypeptide, maintained by various '
                'interactions including disulfide bridges, hydrophobic interactions, and ionic bonds. Quaternary '
                'structure describes the assembly of multiple polypeptide subunits.',
        'topic': 'biochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'DNA replication is the process by which a cell copies its DNA before cell division. The double helix '
                'unwinds and each strand serves as a template for building a new complementary strand, following the '
                "base-pairing rules. The enzyme DNA polymerase adds nucleotides to the growing strand in the 5' to 3' "
                'direction, producing two identical DNA molecules from one — a process described as semi-conservative '
                'replication.',
        'topic': 'biochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Competitive inhibitors reduce enzyme activity by binding to the active site and blocking substrate '
                'access. Non-competitive inhibitors bind to a different site (allosteric site), changing the shape of '
                'the enzyme and reducing its activity. Competitive inhibition can be overcome by increasing substrate '
                'concentration, but non-competitive inhibition cannot, because the inhibitor does not compete with the '
                'substrate.',
        'topic': 'biochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The polymerase chain reaction (PCR) is a laboratory technique that rapidly amplifies specific DNA '
                'sequences. It uses repeated cycles of denaturation (DNA strands separate at ~95°C), annealing '
                '(primers bind to target sequences at ~55°C), and extension (DNA polymerase builds new strands at '
                '~72°C). PCR is used in forensic science, medical diagnostics, and genetic research to detect and '
                'analyze tiny amounts of DNA.',
        'topic': 'biochemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Polymers are very large molecules (macromolecules) made of many repeating units called monomers '
                'joined together. The process of joining monomers is called polymerization. Common examples include '
                'polyethylene (plastic bags), nylon (clothing), and DNA (biological polymer).',
        'topic': 'polymer chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Addition polymerization occurs when monomers with carbon-carbon double bonds join together without '
                'losing any atoms. The double bond breaks and the monomers link into a long chain. Poly(ethene) — '
                'commonly called polyethylene — is made by polymerizing thousands of ethene (CH₂=CH₂) molecules and is '
                'used to make plastic bottles, bags, and packaging.',
        'topic': 'polymer chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Condensation polymerization occurs when monomers join together with the loss of a small molecule, '
                'usually water. Nylon-6,6 is a condensation polymer formed from two types of monomers: a diamine and a '
                'dicarboxylic acid. Each time two monomers link, a water molecule is expelled, forming an amide bond '
                '(–CO–NH–).',
        'topic': 'polymer chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Thermoplastics are polymers that soften and can be reshaped when heated, then harden again on '
                'cooling. Examples include polyethylene, polystyrene, and PVC. Thermosetting polymers, such as epoxy '
                'resin and Bakelite, undergo irreversible chemical crosslinking when first heated and cannot be '
                'remelted — they char or burn if overheated.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The degree of polymerization (DP) is the number of monomer units in a polymer chain. Polymer '
                'properties such as strength, flexibility, and melting point depend heavily on chain length — longer '
                'chains generally produce stronger, higher-melting polymers. The average molar mass of a polymer '
                'sample is often reported as number-average (Mn) or weight-average (Mw) molar mass because polymer '
                'chains vary in length.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Copolymers are polymers made from two or more different types of monomers. In alternating copolymers, '
                'the monomers alternate regularly (ABABAB…); in block copolymers, long sequences of each monomer '
                'appear in blocks (AAABBBAAABBB…); in random copolymers, the sequence is irregular. Varying the '
                'monomer composition allows polymer properties to be finely tuned for specific applications.',
        'topic': 'polymer chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Rubber is a natural polymer made from latex — a milky fluid produced by the rubber tree (Hevea '
                'brasiliensis). Natural rubber is made of polyisoprene chains, which are flexible but sticky and weak. '
                'Vulcanization, discovered by Charles Goodyear, involves heating rubber with sulfur to form crosslinks '
                'between polymer chains, making it stronger, more elastic, and resistant to temperature changes.',
        'topic': 'polymer chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Biodegradable polymers are designed to break down in the environment through microbial action, '
                'reducing plastic pollution. Polylactic acid (PLA), made from fermented plant starch, is a '
                'biodegradable thermoplastic used in packaging and medical implants. Designing biodegradable polymers '
                'involves balancing mechanical performance with controlled degradation rate.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Conducting polymers are a class of polymers that can conduct electricity, unlike most plastics which '
                'are insulators. Polyacetylene was the first discovered conducting polymer, earning its discoverers '
                'the 2000 Nobel Prize in Chemistry. Conductivity arises from the delocalization of electrons along '
                'conjugated double bond systems in the polymer backbone, and can be increased by a process called '
                'doping.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Tacticity describes the spatial arrangement of side groups along a polymer chain. Isotactic polymers '
                'have all side groups on the same side, syndiotactic polymers alternate sides, and atactic polymers '
                'have random arrangement. Isotactic polypropylene is highly crystalline and strong, while atactic '
                'polypropylene is amorphous and rubbery — the same monomer gives very different materials depending on '
                'tacticity.',
        'topic': 'polymer chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Smart polymers, also called stimuli-responsive polymers, change their properties in response to '
                'external triggers such as temperature, pH, light, or electric fields. Poly(N-isopropylacrylamide) '
                '(PNIPAM) undergoes a sharp, reversible phase transition at about 32°C — below this temperature it '
                'swells in water, above it it collapses. These materials are used in drug delivery systems that '
                'release medication only under specific conditions.',
        'topic': 'polymer chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Spectroscopy is the study of how matter interacts with electromagnetic radiation. Different types of '
                'radiation (radio waves, infrared, visible light, X-rays) interact with matter in different ways, '
                'giving information about the structure and composition of substances. Spectroscopy is one of the most '
                'powerful tools in analytical chemistry, used to identify unknown compounds and study molecular '
                'structure.',
        'topic': 'spectroscopy'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The electromagnetic spectrum arranges all forms of radiation by wavelength and frequency — from '
                'long-wavelength radio waves to short-wavelength gamma rays. Visible light is a tiny portion of the '
                'spectrum, with wavelengths between about 400 nm (violet) and 700 nm (red). The energy of '
                'electromagnetic radiation increases with frequency and decreases with wavelength: E = hf, where h is '
                "Planck's constant.",
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Atomic emission spectroscopy works by exciting atoms with heat or electrical energy, causing '
                'electrons to jump to higher energy levels. When the electrons fall back to lower levels, they emit '
                'photons of specific wavelengths that appear as bright lines in the emission spectrum. Each element '
                "has a unique emission spectrum — a 'fingerprint' — which allows its identification even in distant "
                'stars.',
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Infrared (IR) spectroscopy exploits the fact that chemical bonds vibrate at characteristic '
                'frequencies in the infrared region of the spectrum. When IR radiation of the matching frequency hits '
                'a bond, energy is absorbed and the bond vibrates more strongly. Key absorption bands include O–H '
                'stretching (~3300 cm⁻¹), C=O stretching (~1715 cm⁻¹), and N–H stretching (~3300–3500 cm⁻¹), allowing '
                'functional groups to be identified.',
        'topic': 'spectroscopy'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'UV-Visible (UV-Vis) spectroscopy measures how much ultraviolet or visible light a solution absorbs at '
                'different wavelengths. The Beer-Lambert Law states that absorbance A = εcl, where ε is the molar '
                'absorptivity, c is concentration, and l is path length. This allows chemists to determine the '
                'concentration of a colored solution quantitatively by measuring its absorbance at the wavelength of '
                'maximum absorption (λmax).',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': '¹H NMR spectroscopy gives information about the number and chemical environment of hydrogen atoms in '
                'a molecule. Each chemically distinct type of proton gives a separate signal at a different chemical '
                'shift (δ, measured in ppm). The area under each peak (integration) is proportional to the number of '
                'protons causing it, and splitting patterns (doublets, triplets) arise from coupling with neighboring '
                'protons.',
        'topic': 'spectroscopy'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Mass spectrometry ionizes molecules and separates the resulting ions by their mass-to-charge ratio '
                '(m/z). The molecular ion peak (M⁺) gives the molar mass of the compound. Fragmentation peaks reveal '
                'structural information because bonds break in characteristic ways — for example, loss of 15 mass '
                'units often indicates loss of a methyl (CH₃) group.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Raman spectroscopy is complementary to IR spectroscopy and provides information about molecular '
                'vibrations. It is based on the inelastic scattering of laser light — a small fraction of scattered '
                'photons have different energy from the incident light, and the energy shift corresponds to '
                'vibrational frequencies of bonds. Raman spectroscopy is particularly useful for studying symmetric '
                'bonds (like C=C in alkenes) that are IR-inactive.',
        'topic': 'spectroscopy'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'X-ray crystallography determines the three-dimensional structure of crystalline materials, including '
                'proteins and small molecules, by analyzing the diffraction pattern of X-rays passed through the '
                'crystal. The wavelength of X-rays (~0.1 nm) is comparable to the spacing between atoms in crystals, '
                'allowing atomic positions to be mapped with high precision. It was used to determine the structures '
                'of DNA, insulin, and thousands of other biological molecules.',
        'topic': 'spectroscopy'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Atomic absorption spectroscopy (AAS) measures the absorption of light by free atoms in the gas phase. '
                'A sample is atomized (vaporized into atoms) and illuminated by light from a lamp emitting the '
                "element's characteristic wavelengths. The amount of light absorbed is proportional to the "
                'concentration of that element, making AAS highly sensitive and selective for quantitative elemental '
                'analysis in water, food, and environmental samples.',
        'topic': 'spectroscopy'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'A colloid is a mixture where tiny particles of one substance (1–1000 nm in size) are dispersed '
                'throughout another without settling out. Unlike true solutions, colloid particles are large enough to '
                'scatter light — a beam of light through a colloid is visible as a glowing path, known as the Tyndall '
                'effect. Milk, fog, smoke, and gelatin are common examples of colloids.',
        'topic': 'colloids and mixtures'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'Mixtures can be classified as homogeneous or heterogeneous. In a homogeneous mixture (solution), the '
                'composition is uniform throughout, like saltwater or air. In a heterogeneous mixture, the components '
                'are visibly distinct and not evenly distributed, like salad, soil, or concrete.',
        'topic': 'colloids and mixtures'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'The three main types of mixtures based on particle size are solutions (particle size < 1 nm), '
                'colloids (1–1000 nm), and suspensions (> 1000 nm). Solutions are transparent and do not scatter '
                'light. Suspensions are cloudy and settle on standing, while colloids appear homogeneous but scatter '
                'light (Tyndall effect) and do not settle.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Colloids are classified by the phases of the dispersed particles and the dispersion medium. A sol has '
                'solid particles dispersed in a liquid (e.g., paint, blood). An emulsion has liquid droplets in a '
                'liquid (e.g., mayonnaise, milk). A gel has liquid trapped in a solid network (e.g., gelatin, silica '
                'gel), and a foam has gas bubbles dispersed in a liquid or solid (e.g., whipped cream, polystyrene).',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Emulsions are colloids where two immiscible liquids (like oil and water) are mixed together. They are '
                'usually unstable and separate over time, but can be stabilized by emulsifiers — molecules with a '
                'hydrophilic head and a hydrophobic tail, like soap or lecithin. Emulsifiers surround oil droplets and '
                'prevent them from coalescing, keeping products like mayonnaise and salad dressings stable.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Separation techniques exploit differences in physical and chemical properties to separate mixtures. '
                'Filtration separates an insoluble solid from a liquid. Distillation separates liquids by boiling '
                'point differences. Chromatography separates substances based on their different affinities for a '
                'stationary phase and a mobile phase.',
        'topic': 'colloids and mixtures'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Brownian motion is the random, zigzag movement of colloid particles caused by uneven bombardment by '
                'solvent molecules. It was first observed by botanist Robert Brown in 1827 when studying pollen grains '
                'suspended in water. Brownian motion keeps colloidal particles dispersed and prevents them from '
                'settling under gravity.',
        'topic': 'colloids and mixtures'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Coagulation is the process of destabilizing a colloid so that the dispersed particles clump together '
                'and settle out. Adding an electrolyte (salt) neutralizes the surface charges on colloid particles, '
                'causing them to aggregate. This principle is used in water treatment plants, where alum (aluminum '
                'sulfate) is added to cause fine clay and silt particles to coagulate and settle, clarifying the '
                'water.',
        'topic': 'colloids and mixtures'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Fractional distillation is used to separate a mixture of liquids with different but close boiling '
                'points. The mixture is heated and vapors rise through a fractionating column — components with lower '
                'boiling points reach the top first and are condensed and collected. This technique is used '
                'industrially to separate crude oil into fractions like petrol, kerosene, diesel, and lubricating oil.',
        'topic': 'colloids and mixtures'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Aerogels are a remarkable type of colloid (specifically a gel) where the liquid component has been '
                'replaced by gas, producing the lightest solid materials known. Silica aerogel can have densities as '
                'low as 0.001 g/cm³ — only about three times the density of air. Their extremely porous structure '
                'makes them outstanding thermal insulators, used in NASA space suits and building insulation.',
        'topic': 'colloids and mixtures'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Dialysis is a separation technique that uses a semi-permeable membrane to separate small molecules '
                '(like ions and small organic molecules) from larger colloidal particles. Small particles pass through '
                'the membrane pores while large colloidal particles cannot. Dialysis is used in kidney dialysis '
                'machines to remove waste products like urea from the blood of patients with kidney failure.',
        'topic': 'colloids and mixtures'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Redox reactions are chemical reactions that involve the transfer of electrons from one substance to '
                'another. Oxidation is the loss of electrons and reduction is the gain of electrons — they always '
                'occur together. The substance that loses electrons is oxidized and is called the reducing agent, '
                'while the substance that gains electrons is reduced and is called the oxidizing agent.',
        'topic': 'redox reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Oxidation states (oxidation numbers) are used to track electron transfer in redox reactions. An '
                'increase in oxidation state indicates oxidation, and a decrease indicates reduction. For example, in '
                "the reaction Fe + CuSO₄ → FeSO₄ + Cu, iron's oxidation state increases from 0 to +2 (oxidized) while "
                "copper's decreases from +2 to 0 (reduced).",
        'topic': 'redox reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Rules for assigning oxidation states: the oxidation state of a pure element is 0; for monoatomic ions '
                'it equals the charge; oxygen is usually −2 (except in peroxides where it is −1); hydrogen is +1 when '
                'bonded to nonmetals and −1 when bonded to metals; the sum of oxidation states in a neutral compound '
                "is 0 and in a polyatomic ion equals the ion's charge.",
        'topic': 'redox reactions'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'In everyday life, many important processes are redox reactions. Combustion (burning) is oxidation — '
                'fuel reacts with oxygen, losing electrons to oxygen atoms. Rusting of iron is slow oxidation: 4Fe + '
                '3O₂ + 6H₂O → 4Fe(OH)₃, eventually forming iron(III) oxide (rust). Biological respiration is also a '
                'controlled series of redox reactions that release energy from glucose.',
        'topic': 'redox reactions'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Half-equations separate a redox reaction into its oxidation and reduction components. For example, '
                'the reaction between zinc and copper sulfate can be split into: Zn → Zn²⁺ + 2e⁻ (oxidation '
                'half-equation) and Cu²⁺ + 2e⁻ → Cu (reduction half-equation). When combining half-equations, the '
                'number of electrons lost must equal the number gained.',
        'topic': 'redox reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Balancing redox equations in acidic solution requires adding H⁺ ions and water molecules. The steps '
                'are: split into half-equations, balance atoms other than O and H, balance O by adding H₂O, balance H '
                'by adding H⁺, balance charge by adding electrons, then combine half-equations so electrons cancel. In '
                'basic solution, the final equation is further adjusted by adding OH⁻ to neutralize H⁺ ions.',
        'topic': 'redox reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Disproportionation is a special type of redox reaction where the same element is simultaneously '
                'oxidized and reduced. For example, chlorine gas reacts with cold dilute sodium hydroxide: Cl₂ + 2NaOH '
                '→ NaCl + NaOCl + H₂O. In this reaction, chlorine (oxidation state 0) is both reduced to Cl⁻ (−1) in '
                'NaCl and oxidized to Cl⁺ (+1) in NaOCl.',
        'topic': 'redox reactions'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The reactivity series of metals is fundamentally a ranking of metals by their tendency to be oxidized '
                '(lose electrons). Metals high in the series (like potassium and sodium) are easily oxidized and are '
                'powerful reducing agents. Metals low in the series (like gold and silver) resist oxidation, which is '
                'why they are found as native elements in nature and are prized for jewelry and electronics.',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Redox titrations use a known oxidizing or reducing agent of known concentration to determine the '
                'amount of a reducing or oxidizing agent in a sample. Potassium permanganate (KMnO₄) is a common '
                'oxidizing titrant — it is deep purple in solution and acts as its own indicator, becoming colorless '
                'when all the reducing agent has been consumed. Iodometric titrations use thiosulfate to measure the '
                'amount of iodine liberated in a redox reaction.',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The standard reduction potential (E°) measures the tendency of a half-reaction to proceed as a '
                'reduction under standard conditions. By connecting two half-cells, the spontaneous direction of a '
                'redox reaction can be predicted: the half-cell with the more positive E° undergoes reduction '
                '(cathode) and the other undergoes oxidation (anode). The overall cell potential E°cell = E°cathode − '
                'E°anode; if positive, the reaction is spontaneous.',
        'topic': 'redox reactions'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Biological redox reactions are central to life. In cellular respiration, NADH and FADH₂ carry '
                'electrons from glucose oxidation to the electron transport chain in the mitochondria. These electrons '
                'are passed through a series of protein complexes, releasing energy used to pump protons and drive ATP '
                'synthesis, before finally reducing oxygen to water. This controlled electron transfer extracts far '
                'more energy from glucose than simple combustion would allow cells to capture.',
        'topic': 'redox reactions'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Thermochemistry is the study of heat energy changes that occur during chemical reactions. When a '
                'reaction releases heat to the surroundings, it is called exothermic, and the surroundings feel '
                'warmer. When a reaction absorbs heat from the surroundings, it is called endothermic, and the '
                'surroundings feel cooler.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Enthalpy (H) is a measure of the total heat content of a system at constant pressure. The enthalpy '
                'change (ΔH) of a reaction tells us how much heat is released or absorbed. A negative ΔH means heat is '
                'released (exothermic), while a positive ΔH means heat is absorbed (endothermic).',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Specific heat capacity is the amount of energy needed to raise the temperature of 1 gram of a '
                'substance by 1°C. Water has a very high specific heat capacity of 4.18 J/g·°C, which is why oceans '
                'and large lakes help moderate the climate. The formula q = mcΔT is used to calculate heat energy, '
                'where m is mass, c is specific heat capacity, and ΔT is the temperature change.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'A calorimeter is a device used to measure the heat energy released or absorbed during a chemical '
                'reaction. In a simple coffee-cup calorimeter, a reaction takes place in an insulated cup and the '
                'temperature change of the water is recorded. The heat gained or lost by the water equals the heat '
                'released or absorbed by the reaction, assuming no heat escapes.',
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Hess's Law states that the total enthalpy change for a reaction is the same regardless of the number "
                'of steps taken. This allows chemists to calculate enthalpy changes for reactions that cannot be '
                'measured directly by combining known thermochemical equations. If a reaction is reversed, the sign of '
                'ΔH is reversed; if it is multiplied by a factor, ΔH is multiplied by the same factor.',
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Standard enthalpy of formation (ΔHf°) is the enthalpy change when one mole of a compound is formed '
                'from its elements in their standard states at 298 K and 100 kPa. The standard enthalpy of formation '
                'of any element in its standard state is defined as zero. The standard enthalpy of a reaction can be '
                'calculated using: ΔH°rxn = ΣΔHf°(products) − ΣΔHf°(reactants).',
        'topic': 'thermochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Bond enthalpy is the average energy required to break one mole of a specific type of bond in gaseous '
                'molecules. Breaking bonds always requires energy (endothermic), while forming bonds always releases '
                'energy (exothermic). The overall enthalpy change of a reaction can be estimated by summing bond '
                'enthalpies broken (positive) and subtracting bond enthalpies formed (negative).',
        'topic': 'thermochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Entropy (S) is a measure of the degree of disorder or randomness in a system. Processes that increase '
                'disorder — such as dissolving a solid in water, melting ice, or expanding a gas — are accompanied by '
                'an increase in entropy (ΔS > 0). The second law of thermodynamics states that the total entropy of '
                'the universe always increases in any spontaneous process.',
        'topic': 'thermochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gibbs free energy (G) combines enthalpy and entropy to predict whether a reaction is spontaneous. The '
                'equation is ΔG = ΔH − TΔS, where T is the temperature in Kelvin. A reaction is spontaneous when ΔG is '
                'negative, non-spontaneous when ΔG is positive, and at equilibrium when ΔG = 0.',
        'topic': 'thermochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The standard enthalpy of combustion is the heat released when one mole of a substance burns '
                'completely in excess oxygen under standard conditions. Fuels are compared using their calorific '
                'values — the energy released per gram of fuel burned. Hydrogen has one of the highest calorific '
                'values (142 kJ/g), making it an attractive clean fuel since its only combustion product is water.',
        'topic': 'thermochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': "The Born-Haber cycle is a thermochemical cycle that applies Hess's Law to calculate lattice "
                'enthalpies of ionic compounds indirectly. It accounts for all enthalpy changes involved in forming an '
                'ionic solid from its elements, including atomization, ionization, electron affinity, and lattice '
                'formation. Comparing experimental and theoretical lattice enthalpies reveals the degree of covalent '
                'character in a supposedly ionic bond.',
        'topic': 'thermochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': "Kirchhoff's Law states that the enthalpy change of a reaction varies with temperature according to "
                'the heat capacities of reactants and products. If the products have higher heat capacities than the '
                'reactants, ΔH becomes more positive (less exothermic) at higher temperatures. This correction is '
                'important in industrial processes where reactions occur at temperatures far from standard conditions.',
        'topic': 'thermochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Electrochemistry is the study of the relationship between electricity and chemical reactions. It '
                'includes processes where chemical energy is converted to electrical energy (as in batteries) and '
                'where electrical energy drives chemical reactions (as in electrolysis). These processes involve the '
                'transfer of electrons between substances in oxidation-reduction (redox) reactions.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A galvanic (voltaic) cell converts chemical energy into electrical energy through a spontaneous redox '
                'reaction. It consists of two half-cells — one where oxidation occurs (the anode) and one where '
                'reduction occurs (the cathode). Electrons flow through an external wire from the anode to the '
                'cathode, producing an electric current.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The standard electrode potential (E°) measures the tendency of a half-cell to be reduced relative to '
                'the standard hydrogen electrode, which is assigned a value of 0.00 V. A more positive E° means a '
                'greater tendency to be reduced. The standard cell potential is calculated as E°cell = E°cathode − '
                'E°anode, and a positive E°cell indicates a spontaneous reaction.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'A salt bridge is an essential component of a galvanic cell that maintains electrical neutrality by '
                'allowing ions to flow between the two half-cells. Without a salt bridge, charge would build up in '
                'each half-cell and the reaction would stop. It is typically a U-shaped tube filled with an '
                'electrolyte solution such as potassium nitrate (KNO₃).',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'In electrolytic cells, an external power supply drives a non-spontaneous redox reaction. At the '
                'cathode, reduction occurs (cations gain electrons), and at the anode, oxidation occurs (anions lose '
                'electrons). Electrolysis is used industrially to extract reactive metals like aluminum from their '
                'ores and to electroplate metals with a thin coating of another metal.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Faraday's laws of electrolysis describe the relationship between the quantity of electricity passed "
                'through an electrolytic cell and the amount of substance deposited. The first law states that the '
                'mass of substance deposited is proportional to the charge passed (Q = It, where I is current and t is '
                'time). The second law states that the masses of different substances deposited by the same charge are '
                'proportional to their molar masses divided by their ionic charges.',
        'topic': 'electrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Nernst equation adjusts the standard cell potential to account for non-standard conditions: E = '
                'E° − (RT/nF)lnQ, where R is the gas constant, T is temperature in Kelvin, n is the number of moles of '
                "electrons transferred, F is Faraday's constant (96,485 C/mol), and Q is the reaction quotient. At "
                'equilibrium, E = 0 and Q = K, linking electrochemistry to thermodynamics.',
        'topic': 'electrochemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Corrosion is the electrochemical degradation of metals by reaction with their environment. Iron '
                'rusting is a common example — iron acts as the anode and is oxidized to Fe²⁺ ions in the presence of '
                'water and oxygen. Corrosion can be prevented by galvanizing (coating with zinc), painting, or using '
                'sacrificial anodes made of a more reactive metal like magnesium.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Fuel cells are electrochemical devices that continuously convert chemical energy into electrical '
                'energy as long as fuel is supplied. In a hydrogen fuel cell, hydrogen is oxidized at the anode and '
                'oxygen is reduced at the cathode, producing water and electricity. Fuel cells are more efficient than '
                'combustion engines and produce no harmful emissions, making them promising for clean energy '
                'applications.',
        'topic': 'electrochemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The electrochemical series ranks metals and other substances in order of their standard electrode '
                'potentials. Metals at the top of the series (like lithium and potassium) are the strongest reducing '
                'agents and most easily oxidized. Metals at the bottom (like gold and platinum) are the strongest '
                'oxidizing agents and most resistant to corrosion, which is why they are used in jewelry and '
                'electronics.',
        'topic': 'electrochemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Lithium-ion batteries are rechargeable electrochemical cells widely used in phones, laptops, and '
                'electric vehicles. During discharge, lithium ions move from the anode (graphite) through an '
                'electrolyte to the cathode (lithium metal oxide), generating electrical energy. During charging, the '
                'process is reversed using an external power source, restoring the original chemical state.',
        'topic': 'electrochemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Chemical equilibrium is reached in a reversible reaction when the forward and reverse reactions occur '
                'at the same rate, so concentrations of reactants and products remain constant over time. This does '
                'not mean the reaction has stopped — both forward and reverse reactions continue simultaneously. The '
                'double arrow (⇌) in a chemical equation indicates a reversible reaction that can reach equilibrium.',
        'topic': 'chemical equilibrium'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Le Chatelier's principle states that if a system at equilibrium is subjected to a change in "
                'concentration, temperature, or pressure, the equilibrium will shift in the direction that opposes the '
                'change. For example, if more reactant is added to a system at equilibrium, the equilibrium shifts '
                'forward to produce more products. This principle is used to optimize industrial chemical processes.',
        'topic': 'chemical equilibrium'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The equilibrium constant expression (Kc) is written using the molar concentrations of products '
                'divided by reactants, each raised to the power of their stoichiometric coefficients. For the reaction '
                'aA + bB ⇌ cC + dD, Kc = [C]^c[D]^d / [A]^a[B]^b. Pure solids and pure liquids are excluded from the '
                'expression because their concentrations do not change.',
        'topic': 'chemical equilibrium'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'When Kc is much greater than 1, the equilibrium position lies far to the right and products are '
                'favored. When Kc is much less than 1, the equilibrium lies far to the left and reactants are favored. '
                'A Kc close to 1 means significant amounts of both reactants and products are present at equilibrium.',
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The reaction quotient (Q) has the same mathematical form as Kc but uses concentrations at any point '
                'during a reaction, not just at equilibrium. Comparing Q to Kc predicts the direction a reaction will '
                'proceed: if Q < Kc, the reaction proceeds forward; if Q > Kc, the reaction proceeds in reverse; if Q '
                '= Kc, the system is at equilibrium.',
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'In the Haber process for making ammonia, nitrogen and hydrogen gases react reversibly: N₂ + 3H₂ ⇌ '
                "2NH₃, ΔH = −92 kJ/mol. To maximize ammonia yield, Le Chatelier's principle suggests using high "
                'pressure (shifts equilibrium right, fewer gas moles) and low temperature (shifts right for exothermic '
                'reaction). In practice, a compromise temperature of around 450°C is used with an iron catalyst to '
                'achieve an acceptable rate.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Kp is the equilibrium constant expressed in terms of partial pressures of gases, rather than '
                'concentrations. It is related to Kc by the equation Kp = Kc(RT)^Δn, where Δn is the change in the '
                'number of moles of gas (moles of gaseous products minus moles of gaseous reactants). Kp and Kc are '
                'equal when Δn = 0.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The solubility product constant (Ksp) is a type of equilibrium constant that applies to the '
                'dissolution of sparingly soluble ionic compounds. For AgCl dissolving in water: AgCl(s) ⇌ Ag⁺(aq) + '
                'Cl⁻(aq), Ksp = [Ag⁺][Cl⁻]. A small Ksp indicates a very insoluble compound. Ksp values are used in '
                'precipitation reactions and analytical chemistry to predict whether a precipitate will form.',
        'topic': 'chemical equilibrium'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The common ion effect occurs when a soluble salt is added to a solution that already contains one of '
                'its ions, reducing the solubility of a sparingly soluble compound. For example, adding NaCl to a '
                'saturated AgCl solution increases [Cl⁻], shifting the equilibrium to the left and causing more AgCl '
                "to precipitate. This is an application of Le Chatelier's principle to solubility equilibria.",
        'topic': 'chemical equilibrium'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Temperature is the only factor that changes the value of the equilibrium constant Kc. Increasing '
                'temperature for an endothermic reaction increases Kc (shifts equilibrium toward products), while '
                'increasing temperature for an exothermic reaction decreases Kc (shifts toward reactants). Changes in '
                'concentration or pressure shift the equilibrium position but do not change the value of Kc.',
        'topic': 'chemical equilibrium'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Stoichiometry is the study of the quantitative relationships between reactants and products in '
                'chemical reactions. The coefficients in a balanced chemical equation represent the molar ratios in '
                'which substances react and are produced. For example, in 2H₂ + O₂ → 2H₂O, two moles of hydrogen react '
                'with one mole of oxygen to produce two moles of water.',
        'topic': 'stoichiometry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'The mole is the SI unit for amount of substance, and one mole contains exactly 6.022 × 10²³ particles '
                "(Avogadro's number). Just as a 'dozen' always means 12, a 'mole' always means 6.022 × 10²³. One mole "
                'of carbon-12 has a mass of exactly 12 grams, which means the molar mass of any element in g/mol '
                'numerically equals its atomic mass in amu.',
        'topic': 'stoichiometry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Molar mass is the mass of one mole of a substance, expressed in grams per mole (g/mol). For '
                'compounds, molar mass is calculated by adding the atomic masses of all atoms in the formula. For '
                'example, water (H₂O) has a molar mass of (2 × 1) + 16 = 18 g/mol, so 18 grams of water contains one '
                'mole, or 6.022 × 10²³ molecules.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The limiting reagent is the reactant that is completely consumed first in a chemical reaction, '
                'determining the maximum amount of product that can form. The excess reagent is the reactant that '
                'remains after the reaction is complete. To identify the limiting reagent, calculate how many moles of '
                'product each reactant could produce and choose the one that gives the smaller amount.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Percent yield measures the efficiency of a chemical reaction by comparing the actual yield (what you '
                'actually obtained) to the theoretical yield (the maximum possible amount based on stoichiometry). The '
                'formula is: percent yield = (actual yield / theoretical yield) × 100%. A percent yield of 100% is '
                'rarely achieved due to side reactions, incomplete reactions, or losses during purification.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Empirical formula gives the simplest whole-number ratio of atoms in a compound, while the molecular '
                'formula gives the actual number of each type of atom in one molecule. For example, hydrogen peroxide '
                'has an empirical formula of HO and a molecular formula of H₂O₂. To find the molecular formula, divide '
                'the molar mass of the compound by the empirical formula mass and multiply the subscripts.',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Concentration of a solution is measured in molarity (M), defined as the number of moles of solute '
                'dissolved per liter of solution: M = moles of solute / liters of solution. A 2 M solution of NaCl '
                'contains 2 moles of NaCl in every liter of solution. Molarity is used in stoichiometric calculations '
                'involving solutions to convert between volume and moles.',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'When diluting a solution, the number of moles of solute remains constant even as volume increases. '
                'The dilution equation M₁V₁ = M₂V₂ is used to calculate the new concentration or volume after '
                'dilution. For example, to prepare 500 mL of a 0.5 M NaCl solution from a 2 M stock, you would take '
                '125 mL of the stock and add water to reach 500 mL.',
        'topic': 'stoichiometry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Percentage composition is the mass percentage of each element in a compound. It is calculated as: '
                '(mass of element in one mole of compound / molar mass of compound) × 100%. For example, in CO₂ (molar '
                'mass = 44 g/mol), carbon makes up (12/44) × 100% = 27.3% and oxygen makes up 72.7% by mass.',
        'topic': 'stoichiometry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gas stoichiometry uses the molar volume of an ideal gas at standard temperature and pressure (STP: '
                '0°C and 1 atm), which is 22.4 L/mol. This allows chemists to work with volumes of gases directly in '
                'stoichiometric calculations. For example, the complete combustion of 1 mol of methane (CH₄ + 2O₂ → '
                'CO₂ + 2H₂O) produces 22.4 L of CO₂ at STP.',
        'topic': 'stoichiometry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Titration calculations use stoichiometry to find the unknown concentration of a solution. At the '
                'equivalence point, the moles of acid equal the moles of base (for a 1:1 ratio reaction). Using the '
                'formula n = cV, if 25.0 mL of 0.100 M NaOH neutralizes an HCl solution of unknown concentration, and '
                'it takes 20.0 mL of HCl, the concentration of HCl is 0.125 M.',
        'topic': 'stoichiometry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Atom economy is a measure of how efficiently atoms in reactants are incorporated into the desired '
                'product. It is calculated as: (molar mass of desired product / total molar mass of all products) × '
                '100%. High atom economy reactions are preferred in green chemistry because they produce less waste '
                'and use starting materials more efficiently.',
        'topic': 'stoichiometry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Nuclear chemistry studies changes in atomic nuclei, including radioactive decay, fission, and fusion. '
                'Unlike chemical reactions that involve electrons, nuclear reactions involve protons and neutrons and '
                'release far greater amounts of energy. The energy released in nuclear reactions is described by '
                "Einstein's equation E = mc², where m is the mass lost and c is the speed of light.",
        'topic': 'nuclear chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Radioactive decay is the process by which an unstable atomic nucleus loses energy by emitting '
                'radiation. The three main types of nuclear radiation are alpha (α) particles (helium-4 nuclei), beta '
                '(β) particles (high-speed electrons), and gamma (γ) rays (high-energy electromagnetic radiation). '
                'Alpha particles are the least penetrating and can be stopped by paper, beta by thin aluminum, and '
                'gamma requires thick lead or concrete.',
        'topic': 'nuclear chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Half-life is the time it takes for half of the radioactive atoms in a sample to decay. After one '
                'half-life, 50% of the original atoms remain; after two half-lives, 25% remain; after three, 12.5%, '
                'and so on. Half-lives vary enormously — uranium-238 has a half-life of 4.5 billion years, while '
                'francium-223 has a half-life of only 22 minutes.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Carbon-14 dating is used to estimate the age of organic materials up to about 50,000 years old. '
                'Living organisms continuously absorb carbon-14 from the atmosphere, but when they die, the carbon-14 '
                'begins to decay with a half-life of 5,730 years. By measuring the ratio of carbon-14 to carbon-12 in '
                'a sample, scientists can calculate how long ago the organism died.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Nuclear fission is the splitting of a heavy nucleus (such as uranium-235 or plutonium-239) into two '
                'smaller nuclei, releasing a large amount of energy and several neutrons. These released neutrons can '
                'trigger further fission reactions in a chain reaction. Controlled chain reactions in nuclear reactors '
                'produce electricity, while uncontrolled chain reactions are the basis of nuclear weapons.',
        'topic': 'nuclear chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Nuclear fusion is the process in which two light nuclei combine to form a heavier nucleus, releasing '
                'enormous amounts of energy. The Sun produces energy through fusion, primarily by fusing hydrogen '
                'nuclei (protons) into helium. Fusion releases more energy per gram of fuel than fission and produces '
                'no long-lived radioactive waste, making it a promising future energy source, though it remains '
                'technically challenging to achieve on Earth.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Mass defect is the difference between the mass of an atomic nucleus and the sum of the masses of its '
                "individual protons and neutrons. This 'missing' mass is converted into binding energy that holds the "
                'nucleus together, as described by E = mc². The binding energy per nucleon is greatest for iron-56, '
                'which is why elements near iron are the most stable.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Radioactive decay follows first-order kinetics, meaning the rate of decay is directly proportional to '
                'the number of undecayed nuclei present. The decay equation is N = N₀e^(−λt), where N is the number of '
                'nuclei at time t, N₀ is the initial number, and λ is the decay constant. The half-life is related to '
                'the decay constant by t₁/₂ = ln2/λ = 0.693/λ.',
        'topic': 'nuclear chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Nuclear medicine uses radioactive isotopes (radioisotopes) for diagnosis and treatment. '
                'Technetium-99m is the most widely used diagnostic radioisotope because it emits gamma rays that can '
                'be detected externally and has a short half-life of 6 hours, minimizing radiation exposure. '
                'Iodine-131 is used to treat thyroid cancer because the thyroid gland selectively absorbs iodine, '
                'delivering targeted radiation to cancerous cells.',
        'topic': 'nuclear chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Transmutation is the conversion of one element into another through nuclear reactions. Artificial '
                'transmutation is achieved by bombarding nuclei with high-energy particles such as protons, neutrons, '
                'or alpha particles in a particle accelerator. All elements heavier than uranium (transuranic '
                'elements) have been produced artificially through transmutation reactions.',
        'topic': 'nuclear chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Nuclear waste management is a major challenge of nuclear power generation. High-level radioactive '
                'waste from nuclear reactors contains long-lived radioisotopes such as plutonium-239 (half-life: '
                '24,100 years) that must be safely isolated from the environment for thousands of years. Current '
                'strategies include deep geological repositories — burying waste in stable rock formations far '
                'underground.',
        'topic': 'nuclear chemistry'},
    {   'grade': '6',
        'subject': 'chemistry',
        'text': 'A solution is a homogeneous mixture of two or more substances. The substance present in the larger '
                'amount is the solvent, and the substance dissolved in it is the solute. For example, in saltwater, '
                'water is the solvent and sodium chloride is the solute.',
        'topic': 'solution chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Solubility is the maximum amount of solute that can dissolve in a given amount of solvent at a '
                'specific temperature. When a solution contains the maximum dissolved solute, it is called saturated. '
                'Adding more solute beyond this point results in excess undissolved solute remaining at the bottom of '
                'the container.',
        'topic': 'solution chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Temperature affects the solubility of substances differently. For most solid solutes, solubility '
                'increases with temperature — sugar dissolves much more readily in hot water than cold water. However, '
                'for gases dissolved in liquids, solubility decreases as temperature increases, which is why warm soda '
                'goes flat faster than cold soda.',
        'topic': 'solution chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "The rule 'like dissolves like' describes the general principle that polar solvents dissolve polar "
                'solutes, and nonpolar solvents dissolve nonpolar solutes. Water is a polar solvent and readily '
                'dissolves ionic compounds like NaCl and polar molecules like sugar. Nonpolar solvents like hexane '
                'dissolve fats and oils, which are nonpolar, but will not dissolve ionic salts.',
        'topic': 'solution chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'When ionic compounds dissolve in water, they dissociate into their component ions. This process is '
                'called dissociation, and the ions become surrounded by water molecules in a process called hydration. '
                'For example, NaCl dissolves as: NaCl(s) → Na⁺(aq) + Cl⁻(aq), and the resulting ions can conduct '
                'electricity, making the solution an electrolyte.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Colligative properties are properties of solutions that depend only on the number of dissolved '
                'particles, not on their identity. They include boiling point elevation, freezing point depression, '
                'osmotic pressure, and vapor pressure lowering. For example, dissolving salt in water raises its '
                'boiling point and lowers its freezing point, which is why salt is used to de-ice roads in winter.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Osmosis is the movement of water molecules through a selectively permeable membrane from a region of '
                'lower solute concentration to a region of higher solute concentration. Osmotic pressure is the '
                'pressure that must be applied to prevent this movement. Osmosis is critical in biological systems — '
                'it governs the movement of water into and out of cells.',
        'topic': 'solution chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': "Henry's Law states that the solubility of a gas in a liquid is directly proportional to the partial "
                'pressure of that gas above the liquid: C = kH × P. This is why carbonated drinks are bottled under '
                'high pressure to keep CO₂ dissolved. When the bottle is opened, pressure drops and CO₂ bubbles out of '
                'solution.',
        'topic': 'solution chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Molality (m) is a concentration unit defined as the number of moles of solute per kilogram of '
                'solvent: m = moles of solute / kg of solvent. Unlike molarity, molality does not change with '
                'temperature because it is based on mass rather than volume. It is used in colligative property '
                'calculations, where the freezing point depression is given by ΔTf = Kf × m, with Kf being the '
                'cryoscopic constant of the solvent.',
        'topic': 'solution chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Supersaturated solutions contain more dissolved solute than a saturated solution at the same '
                'temperature. They are unstable — adding a seed crystal or disturbing the solution causes rapid '
                'crystallization of the excess solute. Hand warmers use this principle: sodium acetate in a '
                'supersaturated solution crystallizes rapidly when triggered, releasing heat.',
        'topic': 'solution chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': "The van 't Hoff factor (i) accounts for the number of particles a solute produces when it dissolves, "
                'and corrects colligative property calculations for electrolytes. For NaCl, which dissociates into two '
                'ions, i ≈ 2; for MgCl₂, i ≈ 3. The corrected freezing point depression is ΔTf = i × Kf × m, which '
                'explains why ionic solutes are more effective at lowering freezing points than molecular solutes.',
        'topic': 'solution chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Analytical chemistry is the branch of chemistry focused on identifying what substances are present in '
                'a sample (qualitative analysis) and determining how much of each substance is present (quantitative '
                'analysis). It is used in medicine, environmental monitoring, food safety, forensics, and industry. '
                'Techniques range from simple precipitation tests to sophisticated instruments like mass '
                'spectrometers.',
        'topic': 'analytical chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Chromatography is a technique used to separate and identify mixtures by passing them through a '
                'stationary phase with a moving solvent (mobile phase). In paper chromatography, the different '
                'components of a mixture travel different distances up the paper based on their solubility and '
                'attraction to the paper. The Rf value (ratio of distance traveled by component to distance traveled '
                'by solvent) helps identify substances.',
        'topic': 'analytical chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Flame tests are a simple qualitative analytical technique for identifying metal ions based on the '
                'color of light emitted when the metal is heated in a flame. Sodium gives a persistent yellow-orange '
                'flame, potassium a lilac flame, copper a blue-green flame, and lithium a crimson red flame. These '
                'colors result from electrons in the metal atoms absorbing energy and emitting specific wavelengths of '
                'light when they return to lower energy levels.',
        'topic': 'analytical chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Titration is a quantitative analytical technique used to determine the concentration of an unknown '
                'solution by reacting it with a standard solution of known concentration. An indicator or pH meter is '
                'used to detect the equivalence point, where the reaction is complete. The concentration is then '
                'calculated using stoichiometry from the volumes and concentrations used.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Spectrophotometry measures how much light a substance absorbs at specific wavelengths. Beer-Lambert '
                'Law states that absorbance (A) is directly proportional to the concentration (c) and path length (l) '
                'of the solution: A = εcl, where ε is the molar absorptivity. This allows chemists to determine the '
                'concentration of a colored solution by measuring how much light it absorbs.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gas chromatography (GC) separates volatile compounds by passing them through a long column coated '
                'with a stationary phase. Different compounds travel through the column at different speeds and emerge '
                'at different times, called retention times. GC is used in forensics to analyze blood alcohol levels, '
                'in environmental chemistry to detect pollutants, and in food chemistry to identify flavors and '
                'aromas.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Mass spectrometry identifies compounds by ionizing them and separating the resulting ions by their '
                'mass-to-charge ratio (m/z). The fragmentation pattern of a molecule in the mass spectrum acts like a '
                'fingerprint that can be matched to known compounds. Combined with gas chromatography (GC-MS), it is '
                'one of the most powerful analytical tools for identifying unknown substances in complex mixtures.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Nuclear Magnetic Resonance (NMR) spectroscopy probes the chemical environment of specific nuclei '
                '(usually ¹H or ¹³C) in a molecule by measuring their response to a strong magnetic field. The '
                'resulting spectrum gives information about the number, type, and arrangement of atoms in a molecule. '
                'NMR is the primary technique for determining the structure of organic molecules and is also the basis '
                'of MRI scanning in medicine.',
        'topic': 'analytical chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Gravimetric analysis determines the amount of a substance by converting it to a pure, stable solid '
                'that can be weighed accurately. For example, the amount of sulfate in a sample can be found by '
                'precipitating it as barium sulfate (BaSO₄), filtering, drying, and weighing the precipitate. The mass '
                'of the precipitate is used with stoichiometry to calculate the original amount of sulfate.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Infrared (IR) spectroscopy identifies functional groups in organic molecules by measuring which '
                'wavelengths of infrared radiation a sample absorbs. Different bonds vibrate at characteristic '
                'frequencies — for example, the O–H bond absorbs strongly around 3200–3600 cm⁻¹ and the C=O bond '
                'around 1700 cm⁻¹. By analyzing the absorption peaks, chemists can deduce which functional groups are '
                'present in an unknown compound.',
        'topic': 'analytical chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Back titration is used when direct titration of a substance is not practical — for example, when the '
                'analyte reacts too slowly or is insoluble. A known excess of reagent is added to react completely '
                'with the analyte, and the unreacted excess is then titrated with a second standard solution. The '
                'amount of analyte is calculated from the difference between the initial excess and the unreacted '
                'amount.',
        'topic': 'analytical chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Environmental chemistry studies the chemical processes occurring in the environment and the impact of '
                'human activities on ecosystems. It examines how chemicals enter, move through, and are transformed in '
                'air, water, and soil. Understanding environmental chemistry is important for addressing pollution, '
                'climate change, and the safety of ecosystems and human health.',
        'topic': 'environmental chemistry'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'The greenhouse effect is a natural process where gases like carbon dioxide (CO₂), methane (CH₄), and '
                'water vapor in the atmosphere trap heat from the Sun. This keeps Earth warm enough to support life. '
                'However, human activities — especially burning fossil fuels — are increasing concentrations of these '
                'gases, intensifying the greenhouse effect and causing global temperatures to rise.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Acid rain is caused by sulfur dioxide (SO₂) and nitrogen oxides (NOₓ) released from burning fossil '
                'fuels and vehicle emissions. These gases react with water vapor in the atmosphere to form sulfuric '
                'acid and nitric acid, which fall as rain with a pH below 5.6. Acid rain damages forests, kills '
                'aquatic life in lakes, corrodes buildings and statues, and depletes soil nutrients.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "The ozone layer in the stratosphere absorbs most of the Sun's harmful ultraviolet (UV) radiation, "
                'protecting life on Earth. Chlorofluorocarbons (CFCs), once used in refrigerants and aerosols, break '
                'down in the stratosphere and release chlorine atoms that catalytically destroy ozone molecules. The '
                'Montreal Protocol (1987) phased out CFC production and the ozone layer is slowly recovering.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Water pollution occurs when harmful substances — such as industrial chemicals, fertilizer runoff, '
                'heavy metals, or plastic waste — contaminate rivers, lakes, or oceans. Eutrophication is caused by '
                'excess nitrogen and phosphorus from agricultural fertilizers entering waterways, leading to algal '
                'blooms that deplete oxygen and kill aquatic life. Monitoring and regulating chemical discharge is '
                'essential for protecting water quality.',
        'topic': 'environmental chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Heavy metals such as lead, mercury, and cadmium are toxic environmental pollutants that accumulate in '
                'the food chain through a process called biomagnification. Organisms at the top of the food chain, '
                'including humans, accumulate the highest concentrations. Mercury poisoning, for example, damages the '
                'nervous system, and industrial discharge of mercury into waterways has caused serious public health '
                'disasters.',
        'topic': 'environmental chemistry'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Photochemical smog forms when sunlight drives chemical reactions between nitrogen oxides (NOₓ) and '
                'volatile organic compounds (VOCs) from vehicle exhaust. These reactions produce ground-level ozone '
                '(O₃) and other secondary pollutants that are harmful to respiratory health. Photochemical smog is '
                'most severe in sunny cities with heavy traffic, such as Los Angeles and Beijing.',
        'topic': 'environmental chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Carbon capture and storage (CCS) is a technology designed to reduce CO₂ emissions by capturing the '
                'gas at point sources like power plants and storing it underground in geological formations. The '
                'captured CO₂ is compressed and injected into porous rock structures such as depleted oil fields or '
                'saline aquifers. CCS is considered an important transitional technology for reducing atmospheric '
                'greenhouse gas concentrations.',
        'topic': 'environmental chemistry'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The nitrogen cycle describes the movement of nitrogen through the atmosphere, soil, water, and living '
                'organisms. Nitrogen-fixing bacteria convert atmospheric N₂ into ammonia (NH₃), which plants can '
                'absorb as nitrates (NO₃⁻). Denitrifying bacteria complete the cycle by converting nitrates back to '
                'N₂. Human disruption of this cycle through synthetic fertilizer production is a major environmental '
                'concern.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Persistent organic pollutants (POPs) are toxic chemical compounds that resist environmental '
                'degradation, accumulate in living tissue, and spread globally through air and water. Examples include '
                'DDT (a banned pesticide), polychlorinated biphenyls (PCBs), and dioxins. The Stockholm Convention '
                '(2001) is an international treaty that bans or restricts the production and use of the most dangerous '
                'POPs.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Green chemistry is a philosophy of chemical design that seeks to reduce or eliminate the use and '
                'generation of hazardous substances. Its 12 principles include designing reactions for atom economy, '
                'using renewable feedstocks, and avoiding toxic solvents. Green chemistry addresses pollution at the '
                'source rather than treating waste after it is produced, making industrial chemistry more sustainable.',
        'topic': 'environmental chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Ocean acidification is caused by the absorption of excess CO₂ from the atmosphere into seawater, '
                'forming carbonic acid (H₂CO₃). Since the Industrial Revolution, ocean pH has dropped from about 8.2 '
                'to 8.1 — a 26% increase in acidity. This threatens marine organisms that build calcium carbonate '
                'shells and skeletons, including corals, oysters, and many plankton species fundamental to ocean food '
                'webs.',
        'topic': 'environmental chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Life cycle assessment (LCA) is an analytical tool used to evaluate the total environmental impact of '
                'a product or process from raw material extraction through production, use, and disposal — often '
                "called 'cradle to grave' analysis. LCA measures factors like energy consumption, water use, "
                'greenhouse gas emissions, and waste generation at each stage. It helps chemists and engineers design '
                'more sustainable products and processes.',
        'topic': 'environmental chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'The nucleus of an atom is incredibly small compared to the overall size of the atom. If an atom were '
                'the size of a football stadium, the nucleus would be about the size of a marble at the center. '
                "Despite its tiny size, the nucleus contains almost all of the atom's mass because protons and "
                'neutrons are much heavier than electrons.',
        'topic': 'atomic structure'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Protons and neutrons are not truly fundamental particles — they are made of even smaller particles '
                'called quarks. Each proton and neutron contains three quarks held together by the strong nuclear '
                'force. However, for most chemistry purposes, protons, neutrons, and electrons are treated as the '
                'basic building blocks of atoms.',
        'topic': 'atomic structure'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'When atoms lose or gain electrons to form ions, their size changes noticeably. Cations (positive '
                'ions) are smaller than their parent atoms because losing electrons reduces electron-electron '
                'repulsion and the remaining electrons are pulled closer to the nucleus. Anions (negative ions) are '
                'larger than their parent atoms because the extra electrons increase repulsion and expand the electron '
                'cloud.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The de Broglie hypothesis proposed that electrons have wave-like properties, which led to the '
                'development of quantum mechanics and the modern atomic model. The Heisenberg uncertainty principle '
                'states that it is impossible to know both the exact position and exact momentum of an electron '
                'simultaneously. This fundamental uncertainty is why we use probability clouds (orbitals) rather than '
                'fixed paths to describe electron locations.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Isoelectronic species are atoms or ions that have the same number of electrons but different numbers '
                'of protons. For example, Na⁺, Mg²⁺, Al³⁺, and Ne all have 10 electrons. Among isoelectronic species, '
                'the one with the most protons has the smallest radius because the higher nuclear charge pulls the '
                'same number of electrons in more tightly.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The four quantum numbers — principal (n), angular momentum (l), magnetic (mₗ), and spin (mₛ) — '
                'uniquely identify each electron in an atom. The principal quantum number n describes the energy level '
                'or shell. The angular momentum quantum number l describes the shape of the orbital: l=0 is s, l=1 is '
                'p, l=2 is d, and l=3 is f.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Mass spectrometry is an analytical technique used to measure the masses and relative abundances of '
                'isotopes in a sample. A sample is vaporized and ionized, and the ions are separated by their '
                'mass-to-charge ratio in a magnetic field. The resulting mass spectrum is used to calculate the '
                'relative atomic mass of an element from the masses and percentages of its isotopes.',
        'topic': 'atomic structure'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Flame tests can be used to identify metal ions based on the color of light they emit when heated. '
                'Sodium produces a bright yellow flame, potassium gives a lilac color, and copper produces a '
                'blue-green flame. These colors arise because electrons in the metal atoms absorb energy and jump to '
                'higher energy levels, then release that energy as visible light when they fall back down.',
        'topic': 'atomic structure'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The emission spectrum of hydrogen consists of specific lines of colored light, not a continuous '
                'rainbow. These lines correspond to electrons falling from higher energy levels to lower ones and '
                'releasing photons of specific energy. The Balmer series consists of visible light emissions and was '
                "one of the key pieces of evidence that supported Bohr's model of the atom.",
        'topic': 'atomic structure'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Radioactive decay occurs when an unstable nucleus spontaneously emits particles or energy to become '
                'more stable. Alpha decay releases a helium-4 nucleus (2 protons + 2 neutrons), reducing the atomic '
                'number by 2 and mass number by 4. Beta decay converts a neutron into a proton, increasing the atomic '
                'number by 1 while the mass number stays the same.',
        'topic': 'atomic structure'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Coordinate (dative) covalent bonds form when both electrons in the shared pair come from the same '
                'atom. This is different from a regular covalent bond where each atom contributes one electron. An '
                'example is the formation of the ammonium ion (NH₄⁺), where nitrogen donates a lone pair of electrons '
                'to a hydrogen ion (H⁺).',
        'topic': 'chemical bonding'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'VSEPR (Valence Shell Electron Pair Repulsion) theory predicts the shape of molecules based on the '
                'idea that electron pairs around a central atom repel each other and arrange themselves as far apart '
                'as possible. A molecule with four bonding pairs and no lone pairs takes a tetrahedral shape with bond '
                'angles of 109.5°. The presence of lone pairs reduces bond angles because lone pairs exert greater '
                'repulsion than bonding pairs.',
        'topic': 'chemical bonding'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Dipole-dipole interactions occur between polar molecules that have a permanent positive end and a '
                'permanent negative end. The positive end of one molecule is attracted to the negative end of a '
                'neighboring molecule. These interactions are stronger than London dispersion forces and explain why '
                'polar molecules like HCl have higher boiling points than nonpolar molecules of similar size.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'In ionic compounds, the lattice energy is the energy released when gaseous ions come together to form '
                'one mole of an ionic solid. Higher lattice energies result in more stable ionic compounds with higher '
                'melting points. Lattice energy increases with greater ionic charge and smaller ionic radii, which is '
                'why MgO (with Mg²⁺ and O²⁻) has a much higher melting point than NaCl.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'The Born-Haber cycle is an energy cycle used to calculate lattice energies that cannot be measured '
                "directly. It applies Hess's law by summing the enthalpy changes for a series of steps — including "
                'atomization, ionization, and electron affinity — that lead to the formation of an ionic compound. '
                'Comparing the theoretical and experimental lattice energies reveals how much covalent character an '
                'ionic bond has.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Hybridization describes how atomic orbitals mix to form new hybrid orbitals suited for bonding. In '
                'methane (CH₄), the one 2s and three 2p orbitals of carbon mix to form four equivalent sp³ hybrid '
                'orbitals arranged tetrahedrally. In ethene (C₂H₄), sp² hybridization leaves one unhybridized p '
                'orbital on each carbon, which overlaps sideways to form the π bond of the double bond.',
        'topic': 'chemical bonding'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Nonpolar covalent bonds form between atoms with equal or very similar electronegativity values, '
                'meaning electrons are shared equally. Molecules like H₂, Cl₂, and N₂ contain nonpolar bonds because '
                'both atoms are identical. Even in molecules with polar bonds, the overall molecule can be nonpolar if '
                'the bond dipoles cancel out due to symmetrical geometry, as in CO₂ and CCl₄.',
        'topic': 'chemical bonding'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': "The strength of hydrogen bonding significantly affects the properties of biological molecules. DNA's "
                'double helix is held together by hydrogen bonds between complementary base pairs — adenine with '
                'thymine and guanine with cytosine. Although each individual hydrogen bond is weak, the large number '
                'of them in a DNA molecule provides considerable overall stability.',
        'topic': 'chemical bonding'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The pH of rain is naturally around 5.6 because carbon dioxide in the atmosphere dissolves in '
                'rainwater to form carbonic acid (H₂CO₃). Acid rain has a pH below 5.6 and is caused by sulfur dioxide '
                'and nitrogen oxides from burning fossil fuels reacting with water. Acid rain damages ecosystems, '
                'corrodes metals and stone structures, and acidifies lakes and soils.',
        'topic': 'acids and bases'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The concentration of hydrogen ions and hydroxide ions in water are related by the ionic product of '
                'water: Kw = [H⁺][OH⁻] = 1 × 10⁻¹⁴ mol²/L² at 25°C. In a neutral solution, [H⁺] = [OH⁻] = 1 × 10⁻⁷ '
                'mol/L, giving a pH of 7. If [H⁺] increases, [OH⁻] must decrease proportionally so that their product '
                'remains 1 × 10⁻¹⁴.',
        'topic': 'acids and bases'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'A conjugate acid-base pair differs by a single proton. When an acid donates a proton, it becomes its '
                'conjugate base; when a base accepts a proton, it becomes its conjugate acid. For example, in the '
                'reaction CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺, acetic acid and acetate are a conjugate pair, as are water '
                'and the hydronium ion.',
        'topic': 'acids and bases'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Amphoteric substances can act as either an acid or a base depending on the reaction conditions. Water '
                'is the most common example — it donates a proton to strong bases (acting as an acid) and accepts a '
                'proton from strong acids (acting as a base). Amino acids and aluminum oxide are other examples of '
                'amphoteric substances.',
        'topic': 'acids and bases'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The half-equivalence point in an acid-base titration is where exactly half of the weak acid has been '
                'neutralized. At this point, the concentration of the weak acid equals the concentration of its '
                'conjugate base, and the pH equals the pKa of the acid. This relationship comes from the '
                'Henderson-Hasselbalch equation: pH = pKa + log([A⁻]/[HA]).',
        'topic': 'acids and bases'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Stomach acid is primarily hydrochloric acid (HCl) with a pH of about 1.5 to 3.5. This strongly acidic '
                'environment helps break down food and kills many harmful bacteria. Antacids work by neutralizing '
                'excess stomach acid using bases such as calcium carbonate (CaCO₃), magnesium hydroxide (Mg(OH)₂), or '
                'sodium bicarbonate (NaHCO₃).',
        'topic': 'acids and bases'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Sulfuric acid (H₂SO₄) is the most widely produced industrial chemical in the world. It is a diprotic '
                'acid, meaning it can donate two protons per molecule. It is used in the manufacture of fertilizers, '
                'car batteries, detergents, and in refining petroleum.',
        'topic': 'acids and bases'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'The rate of a chemical reaction can be measured by tracking how quickly a reactant is used up or how '
                'fast a product is formed over time. Reaction rate is usually expressed in mol/L/s (moles per liter '
                'per second). A graph of concentration versus time shows a curve that becomes less steep as the '
                'reaction slows down and reactants are consumed.',
        'topic': 'chemical reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The rate law of a reaction expresses how the reaction rate depends on the concentration of reactants. '
                'For a reaction where rate = k[A]^m[B]^n, the exponents m and n are the reaction orders with respect '
                'to each reactant, and k is the rate constant. The overall reaction order is m + n, and these orders '
                'must be determined experimentally, not from the stoichiometric equation.',
        'topic': 'chemical reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': "Hess's Law states that the total enthalpy change of a reaction is the same regardless of the route "
                'taken, as long as the initial and final conditions are the same. This means you can calculate '
                'enthalpy changes for reactions that are difficult to measure directly by adding or subtracting known '
                "thermochemical equations. Hess's Law is a consequence of the fact that enthalpy is a state function.",
        'topic': 'chemical reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Precipitation reactions occur when two aqueous solutions are mixed and an insoluble solid '
                '(precipitate) forms. For example, mixing silver nitrate (AgNO₃) solution with sodium chloride (NaCl) '
                'solution produces white silver chloride (AgCl) precipitate. Ionic equations can be simplified to net '
                'ionic equations by removing spectator ions that do not participate in the reaction.',
        'topic': 'chemical reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Combustion is a type of oxidation reaction where a substance reacts rapidly with oxygen, releasing '
                'energy as heat and light. Complete combustion of hydrocarbons produces carbon dioxide and water. '
                'Incomplete combustion, which occurs when oxygen is limited, produces carbon monoxide and soot (carbon '
                'particles), both of which are harmful to health.',
        'topic': 'chemical reactions'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The Arrhenius equation relates reaction rate constant to temperature: k = Ae^(-Ea/RT), where Ea is '
                'the activation energy, R is the gas constant, T is the temperature in Kelvin, and A is the frequency '
                'factor. As temperature increases, the exponential term increases, so k increases and the reaction '
                'proceeds faster. This mathematical relationship explains why a 10°C rise in temperature can roughly '
                'double many reaction rates.',
        'topic': 'chemical reactions'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Electrolysis is a process in which electrical energy is used to drive a non-spontaneous chemical '
                'reaction. In the electrolysis of water, a direct electric current splits water molecules into '
                'hydrogen gas at the cathode and oxygen gas at the anode: 2H₂O → 2H₂ + O₂. This redox reaction is '
                'endothermic and requires a continuous supply of electrical energy.',
        'topic': 'chemical reactions'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The modern periodic table contains 118 confirmed elements, arranged in 7 periods and 18 groups. The '
                'first 94 elements occur naturally on Earth, while elements 95 to 118 are synthetic and have been '
                'created in laboratories through nuclear reactions. Many of the heavier synthetic elements exist for '
                'only fractions of a second before decaying.',
        'topic': 'periodic table'},
    {   'grade': '10',
        'subject': 'chemistry',
        'text': 'Electron affinity is the energy change that occurs when an atom in the gas phase gains one electron '
                'to form a negative ion. Elements with high electron affinity (like fluorine and chlorine) strongly '
                'attract additional electrons. Electron affinity generally increases across a period and decreases '
                'down a group, following a similar trend to ionization energy.',
        'topic': 'periodic table'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'Metalloids, also called semimetals, have properties intermediate between metals and nonmetals. '
                'Silicon and germanium are metalloids that are semiconductors — they conduct electricity under certain '
                'conditions. This property makes them essential in computer chips, solar cells, and transistors, '
                'forming the basis of the modern electronics industry.',
        'topic': 'periodic table'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'The lanthanides and actinides are two rows of elements placed separately below the main periodic '
                'table. The lanthanides (elements 57–71) are rare earth metals used in magnets, lasers, and '
                'phosphorescent materials. The actinides (elements 89–103) are all radioactive; uranium and plutonium '
                'are the most well-known due to their use in nuclear reactors and weapons.',
        'topic': 'periodic table'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Successive ionization energies of an element show a dramatic jump when an electron is removed from a '
                "complete inner shell. For example, magnesium's first two ionization energies are relatively low (it "
                'loses 2 outer electrons easily), but the third ionization energy is much higher because the third '
                'electron must be removed from a full inner shell. This pattern confirms the number of outer electrons '
                'an element has.',
        'topic': 'periodic table'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Diagonal relationships exist between certain elements in the periodic table that are diagonally '
                'adjacent, such as lithium and magnesium, or beryllium and aluminum. These pairs share similar '
                'chemical properties due to having similar charge density (charge-to-size ratio). For example, both '
                'lithium and magnesium form nitrides directly with nitrogen and have carbonates that decompose on '
                'heating.',
        'topic': 'periodic table'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Group 2 elements, known as alkaline earth metals, include magnesium, calcium, and barium. They are '
                'less reactive than Group 1 metals but still react with water and oxygen. Calcium is essential for '
                'strong bones and teeth in living organisms, and its compounds are used in cement and plaster.',
        'topic': 'periodic table'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Alkynes are hydrocarbons containing at least one carbon-carbon triple bond (C≡C) and follow the '
                'general formula CₙH₂ₙ₋₂. Ethyne (C₂H₂), commonly known as acetylene, is the simplest alkyne and is '
                'used in oxyacetylene torches for welding because it burns at extremely high temperatures. Alkynes are '
                'more reactive than alkenes due to the additional π bond.',
        'topic': 'organic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Esters are organic compounds formed by the condensation reaction between a carboxylic acid and an '
                'alcohol, with water as a byproduct. They have the functional group –COO– and are often responsible '
                'for the pleasant smells of fruits and flowers. Ethyl ethanoate (CH₃COOC₂H₅) is a common ester used as '
                'a solvent in nail polish remover.',
        'topic': 'organic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Cracking is an industrial process in which large hydrocarbon molecules from crude oil are broken down '
                'into smaller, more useful molecules. Thermal cracking uses high temperatures and pressures, while '
                'catalytic cracking uses a zeolite catalyst at lower temperatures. Cracking is important because it '
                'produces alkenes like ethene, which are used as starting materials for making polymers and other '
                'chemicals.',
        'topic': 'organic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Amino acids are organic molecules that contain both an amine group (–NH₂) and a carboxylic acid group '
                '(–COOH). There are 20 standard amino acids that serve as the building blocks of proteins. The unique '
                'sequence in which amino acids are linked by peptide bonds determines the structure and function of '
                'each protein.',
        'topic': 'organic chemistry'},
    {   'grade': '11',
        'subject': 'chemistry',
        'text': 'Addition reactions occur across double or triple bonds in unsaturated organic molecules. For example, '
                'ethene reacts with bromine water (Br₂) in an addition reaction to form 1,2-dibromoethane: CH₂=CH₂ + '
                'Br₂ → CH₂BrCH₂Br. This reaction is used as a test for unsaturation — bromine water is decolorized '
                'when added to a compound containing a C=C or C≡C bond.',
        'topic': 'organic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Optical isomers (enantiomers) are molecules that are non-superimposable mirror images of each other, '
                'similar to left and right hands. They occur when a carbon atom is bonded to four different groups, '
                'making it a chiral center. Enantiomers have identical physical properties but rotate plane-polarized '
                'light in opposite directions, and can have very different biological activities.',
        'topic': 'organic chemistry'},
    {   'grade': '12',
        'subject': 'chemistry',
        'text': 'Amines are organic compounds derived from ammonia (NH₃) by replacing one or more hydrogen atoms with '
                'organic groups. Primary amines have one organic group attached to nitrogen, such as methylamine '
                '(CH₃NH₂). Amines are basic because the lone pair on nitrogen can accept a proton, and they react with '
                'carboxylic acids to form amide bonds.',
        'topic': 'organic chemistry'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'When water is heated at sea level (101.3 kPa), it boils at 100°C. However, at higher altitudes where '
                'atmospheric pressure is lower, water boils at lower temperatures. This is because the reduced '
                'pressure means molecules need less kinetic energy to escape from the liquid surface into the gas '
                'phase, which is why cooking food takes longer at high altitudes.',
        'topic': 'states of matter'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': "Gay-Lussac's Law states that at constant volume, the pressure of a fixed amount of gas is directly "
                'proportional to its absolute temperature: P₁/T₁ = P₂/T₂. This explains why aerosol cans warn against '
                'heating — as temperature rises, pressure inside the sealed can increases and may cause it to burst. '
                'Temperature must always be in Kelvin for this calculation.',
        'topic': 'states of matter'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': "The ideal gas law combines Boyle's, Charles's, and Gay-Lussac's laws into one equation: PV = nRT, "
                'where P is pressure, V is volume, n is the number of moles of gas, R is the universal gas constant '
                '(8.314 J/mol·K), and T is temperature in Kelvin. An ideal gas is a theoretical model that assumes no '
                'intermolecular forces and particles with no volume; real gases deviate from this at high pressures '
                'and low temperatures.',
        'topic': 'states of matter'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': 'Surface tension is a property of liquids caused by intermolecular forces pulling liquid molecules at '
                "the surface inward. This creates a thin 'skin' on the surface that allows small insects like water "
                'striders to walk on water. Liquids with stronger intermolecular forces, like water, have higher '
                'surface tension than liquids with weaker forces, like ethanol.',
        'topic': 'states of matter'},
    {   'grade': '8',
        'subject': 'chemistry',
        'text': "Viscosity is a measure of a fluid's resistance to flow. Honey is more viscous than water because its "
                'large molecules have stronger intermolecular interactions. Viscosity generally decreases as '
                'temperature increases because the added thermal energy gives molecules enough energy to overcome '
                'intermolecular attractions and flow more freely.',
        'topic': 'states of matter'},
    {   'grade': '7',
        'subject': 'chemistry',
        'text': 'Deposition is the phase change in which a gas converts directly into a solid without passing through '
                'the liquid phase. It is the reverse of sublimation. Frost forming on windows on a cold night is an '
                'example of deposition — water vapor in the air converts directly into solid ice crystals when it '
                'contacts the cold glass surface.',
        'topic': 'states of matter'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'The critical point of a substance is the temperature and pressure above which the distinction between '
                'liquid and gas phases disappears. Above the critical temperature, a substance exists as a '
                'supercritical fluid, which has properties of both a liquid and a gas. Supercritical carbon dioxide is '
                'used in decaffeinating coffee and dry cleaning because it acts as a solvent but evaporates completely '
                'without leaving residue.',
        'topic': 'states of matter'},
    {   'grade': '9',
        'subject': 'chemistry',
        'text': 'At absolute zero (0 Kelvin, or −273.15°C), particles would theoretically have minimum possible energy '
                'and all motion would essentially stop. No substance has ever been cooled to exactly absolute zero, '
                'though scientists have reached temperatures within billionths of a degree of it. The Kelvin scale '
                'starts at absolute zero, making it the natural scale for thermodynamic and gas law calculations.',
        'topic': 'states of matter'}]
