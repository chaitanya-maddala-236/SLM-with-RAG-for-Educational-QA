"""
geography_extended_v3.py
------------------------
Extended educational knowledge base — geography topics
for SLM with RAG Educational QA system.

NEW TOPICS (this file):
  geography:
    1. coasts and coastal landforms     — grades 6,7,8,9
    2. desertification and arid lands   — grades 7,8,9,10
    3. soil and land degradation        — grades 7,8,9,10
    4. weather and atmospheric processes — grades 6,7,8,9,10
    5. environmental management and conservation — grades 8,9,10,11
    6. demographic change and migration — grades 8,9,10,11
    7. geopolitics and borders          — grades 9,10,11,12

FORMAT: every dict has exactly 4 keys:
    text     — 2-4 sentences, self-contained educational content
    subject  — "geography"
    topic    — exact topic name (lowercase, as listed above)
    grade    — string "6" through "12"
"""

GEOGRAPHY_EXTENDED_V3 = [

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: coasts and coastal landforms
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "A coast is the strip of land where the sea meets the land. Coasts are "
                "always changing because of the action of waves, tides, and wind. "
                "Some coasts are being worn away (eroded) while others are growing "
                "as new material is deposited by the sea.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "6",
    },
    {
        "text": "Waves are formed by wind blowing over the surface of the sea. The stronger "
                "the wind and the longer the stretch of open water (called the fetch), the "
                "bigger the waves. When a wave reaches shallow water it slows down, the top "
                "falls forward, and the wave breaks onto the shore.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "6",
    },
    {
        "text": "Destructive waves are tall, powerful waves with a strong swash (water "
                "rushing up the beach) and a weak backwash. They erode the coastline. "
                "Constructive waves are lower, with a weak swash and a strong backwash, "
                "and they deposit material on beaches. Destructive waves are common in "
                "stormy weather; constructive waves in calm conditions.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "7",
    },
    {
        "text": "Coastal erosion happens through four main processes. Hydraulic action is "
                "the sheer force of waves crashing against cliffs. Abrasion is when rocks "
                "and pebbles carried by the sea scrape against cliff faces. Attrition is "
                "when rocks in the sea knock against each other and break into smaller, "
                "rounder pieces. Solution is when slightly acidic seawater dissolves "
                "chalk and limestone rocks.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "7",
    },
    {
        "text": "Headlands and bays form along coastlines where bands of hard and soft "
                "rock alternate. The softer rock erodes faster, forming curved bays, "
                "while the harder rock sticks out as headlands. Over time, waves "
                "concentrate their energy on headlands and gradually wear them back "
                "until the coastline becomes more even.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "7",
    },
    {
        "text": "Wave-cut platforms are flat, gently sloping rocky surfaces found at "
                "the base of cliffs. They form as waves erode a notch at the base of a "
                "cliff, causing the cliff above to collapse over time. The fallen material "
                "is gradually broken down and carried away, leaving a wide rocky platform "
                "exposed at low tide.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "8",
    },
    {
        "text": "Sea caves, arches, stacks, and stumps form in a sequence as headlands "
                "are eroded. Waves exploit weaknesses in the cliff to carve sea caves. "
                "If caves on opposite sides of a headland meet, an arch forms. When the "
                "arch roof collapses, an isolated column of rock called a stack remains. "
                "Further erosion reduces the stack to a low stump. Old Harry Rocks in "
                "Dorset, UK, are famous examples.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "8",
    },
    {
        "text": "Longshore drift transports sediment along the coast in a zigzag pattern. "
                "Waves approach the shore at an angle, pushing material up the beach "
                "(swash) in the direction of the wind. Gravity pulls the water and "
                "sediment straight back down the slope (backwash). Over thousands of "
                "wave cycles this moves material along the coast — sometimes many "
                "kilometres from its source.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "8",
    },
    {
        "text": "Spits are narrow ridges of sand or shingle that extend from the coast "
                "into the sea, often curving at their end due to secondary wind directions. "
                "They form where longshore drift is interrupted — for example at a river "
                "mouth or bay. Spurn Head in Yorkshire, UK extends about 5 km into the "
                "Humber estuary. Behind spits, sheltered mudflats and salt marshes often "
                "develop.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "8",
    },
    {
        "text": "Coastal management aims to protect coastlines from erosion and flooding. "
                "Hard engineering uses artificial structures: sea walls reflect wave energy; "
                "groynes trap sediment and widen beaches; rock armour (riprap) absorbs "
                "wave energy. These are expensive and can shift erosion problems "
                "to adjacent areas. Soft engineering works with natural processes and "
                "is generally more sustainable.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "9",
    },
    {
        "text": "Beach nourishment is a soft engineering strategy that replaces eroded "
                "beach material by pumping sand from offshore or importing it from "
                "elsewhere. Wide beaches absorb wave energy and protect cliffs and "
                "settlements behind them. Miami Beach in Florida has been nourished "
                "multiple times. Although expensive, beach nourishment maintains tourism "
                "value and provides natural flood defence.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "9",
    },
    {
        "text": "Managed retreat (or coastal realignment) allows the sea to flood low-lying "
                "coastal land that is uneconomic to defend, creating new intertidal habitats "
                "such as salt marshes. Salt marshes absorb wave energy, reduce flood risk, "
                "store carbon, and support wildlife. Managed retreat is increasingly seen "
                "as the most sustainable long-term response to sea-level rise in vulnerable "
                "low-lying areas.",
        "subject": "geography",
        "topic": "coasts and coastal landforms",
        "grade": "9",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: desertification and arid lands
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "A desert is an area that receives less than 250 mm of rainfall per year. "
                "Deserts cover about one-third of Earth's land surface. Hot deserts like "
                "the Sahara can reach over 50°C in the day and drop below 0°C at night. "
                "Cold deserts such as the Gobi in Central Asia are extremely dry but "
                "experience freezing winters.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "7",
    },
    {
        "text": "Plants and animals in deserts have special adaptations to survive extreme "
                "heat and drought. Cacti store water in their thick stems and have spines "
                "instead of leaves to reduce water loss. Camels can close their nostrils, "
                "have fat stored in their humps for energy, and their blood cells can "
                "shrink and swell to cope with dehydration. Many desert animals are "
                "nocturnal to avoid daytime heat.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "7",
    },
    {
        "text": "Desertification is the process by which fertile land in dry regions "
                "gradually turns into desert. It is caused by a combination of climate "
                "change (reduced rainfall) and human activities. It is not simply the "
                "expansion of existing deserts — it can occur in semi-arid areas far "
                "from any desert. Around 12 million hectares of productive land are lost "
                "to desertification every year.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "8",
    },
    {
        "text": "Human activities that cause desertification include overgrazing (too "
                "many animals eat all the vegetation, leaving bare soil), deforestation "
                "(trees are cut down, removing roots that hold soil together), and "
                "over-cultivation (farming the same land continuously exhausts soil "
                "nutrients). Without vegetation, topsoil is blown or washed away, "
                "leaving hard, infertile ground that cannot support crops.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "8",
    },
    {
        "text": "The Sahel region in sub-Saharan Africa stretches across ten countries "
                "from Senegal to Ethiopia. It has suffered severe desertification since "
                "the 1970s, driven by drought, population growth, and land pressure. "
                "Millions of people have been displaced or face food insecurity. The "
                "Sahel experiences irregular rainfall, and long droughts can devastate "
                "crops and livestock, triggering famine.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "8",
    },
    {
        "text": "The Great Green Wall is an African initiative to restore 100 million "
                "hectares of degraded land across the Sahel by 2030, creating a mosaic "
                "of green and productive land stretching 8,000 km from Senegal to Djibouti. "
                "By 2020, about 18% of the target had been achieved. The project combats "
                "desertification, improves food security, and stores carbon while creating "
                "rural livelihoods.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "9",
    },
    {
        "text": "Irrigation allows farming in arid areas by supplying water to crops "
                "artificially. However, poorly managed irrigation can cause salinisation — "
                "the build-up of salt in soil when water evaporates in hot conditions, "
                "leaving salts behind. Salinised soils become infertile and may be "
                "abandoned. Up to 20% of irrigated cropland worldwide is affected by "
                "soil salinisation, mostly in drylands.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "9",
    },
    {
        "text": "Sand dunes in deserts are constantly shaped by wind. Barchan dunes are "
                "crescent-shaped and form in areas with limited sand and a prevailing "
                "wind direction. Star dunes form where wind directions vary. Sand seas "
                "(ergs) cover about 25% of the Sahara. Desertification can allow sand "
                "dunes to encroach on farmland, roads, and even villages — a process "
                "called sand encroachment — seen in China, Egypt, and Iran.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "9",
    },
    {
        "text": "Sustainable land management in arid areas includes techniques like "
                "terracing hillsides to reduce runoff, planting drought-resistant trees "
                "as windbreaks (shelterbelts), and using traditional farming practices "
                "that have coexisted with dryland environments for centuries. In Niger, "
                "a technique called farmer-managed natural regeneration (FMNR) — "
                "allowing native trees to regrow from roots — has restored millions "
                "of hectares and improved crop yields.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "10",
    },
    {
        "text": "Climate change is expected to increase the extent and severity of "
                "desertification. Rising temperatures accelerate evaporation and reduce "
                "soil moisture. Many subtropical regions — including the Mediterranean, "
                "southern Africa, and southwestern USA — are projected to become drier. "
                "The IPCC estimates that 3 billion people could be exposed to land "
                "degradation by 2100 if current trends continue.",
        "subject": "geography",
        "topic": "desertification and arid lands",
        "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: soil and land degradation
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "Soil is a mixture of weathered rock particles, organic matter (humus), "
                "water, air, and billions of living organisms. It takes up to 1,000 years "
                "to form just 1 cm of topsoil naturally. Topsoil is the most fertile "
                "layer, rich in nutrients and organic matter. Without healthy soil, "
                "it is impossible to grow food.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "7",
    },
    {
        "text": "Soil degradation means a reduction in soil quality so that it can no "
                "longer support healthy plant growth. The main types are physical "
                "degradation (compaction by heavy machinery, loss of structure), "
                "chemical degradation (nutrient depletion, acidification, salinisation, "
                "contamination by pollutants), and biological degradation (loss of "
                "soil organisms and organic matter).",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "7",
    },
    {
        "text": "Soil erosion is the removal of topsoil by water or wind faster than it "
                "can be replaced. Water erosion occurs when rainfall hits bare soil, "
                "dislodging particles that are then carried away in runoff. Wind erosion "
                "is severe in dry, bare areas — the 1930s Dust Bowl in the US Great "
                "Plains eroded millions of hectares of cropland after drought and "
                "ploughing removed protective vegetation.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "8",
    },
    {
        "text": "Intensive agriculture accelerates soil degradation. Growing a single "
                "crop repeatedly (monoculture) depletes specific nutrients. Deep ploughing "
                "destroys soil structure and brings infertile subsoil to the surface. "
                "Overuse of chemical fertilisers can acidify soil and harm soil organisms. "
                "The UN estimates that about one-third of global soils are already "
                "moderately to highly degraded.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "8",
    },
    {
        "text": "Soil compaction occurs when heavy farm machinery or livestock compress "
                "soil particles together, reducing pore space. This limits water "
                "infiltration (increasing flooding risk), reduces aeration (harming "
                "plant roots and soil organisms), and makes it harder for roots to "
                "penetrate. In the UK, it is estimated that soil compaction costs "
                "agriculture £40–250 million per year in reduced yields.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "8",
    },
    {
        "text": "Soil organic matter (SOM) is the fraction of soil made up of plant and "
                "animal remains in various stages of decomposition, including humus. "
                "SOM improves soil structure, water retention, and nutrient availability. "
                "It is also a major carbon store — soils hold about twice as much carbon "
                "as the atmosphere. Practices that reduce organic matter (intensive "
                "tillage, burning crop residues) release this stored carbon as CO₂.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "9",
    },
    {
        "text": "Sustainable soil management practices can restore degraded land. "
                "No-till or minimum-till farming reduces erosion and preserves soil "
                "structure. Crop rotation replenishes nutrients and breaks pest and disease "
                "cycles. Cover crops planted between main crops protect bare soil from "
                "erosion and add organic matter. Composting and applying manure returns "
                "organic matter and nutrients to the soil.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "9",
    },
    {
        "text": "Soil contamination occurs when hazardous chemicals are deposited in soil, "
                "either through industrial accidents, mining, agricultural chemicals, or "
                "improper waste disposal. Heavy metals (lead, cadmium, arsenic) and "
                "persistent organic pollutants can accumulate in soil for decades or "
                "centuries. Contaminated soils can harm human health through ingestion "
                "of contaminated crops or water, and are costly to remediate.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "9",
    },
    {
        "text": "Land degradation costs the global economy an estimated $10 trillion "
                "per year through reduced crop yields, loss of ecosystem services, "
                "and increased flooding. The UN Decade on Ecosystem Restoration "
                "(2021–2030) aims to restore 350 million hectares of degraded land. "
                "The Economics of Land Degradation Initiative calculates that every "
                "$1 invested in land restoration returns $7–30 in economic benefits.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "10",
    },
    {
        "text": "Bioremediation uses living organisms — mostly microbes — to break down "
                "or neutralise soil pollutants. Some bacteria can metabolise petroleum "
                "hydrocarbons from oil spills; others convert toxic chromium to less "
                "harmful forms. Phytoremediation uses plants that absorb heavy metals "
                "into their tissues — sunflowers were used to extract caesium and "
                "strontium from soil at Chernobyl. These methods are cheaper and less "
                "disruptive than excavating and replacing contaminated soil.",
        "subject": "geography",
        "topic": "soil and land degradation",
        "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: weather and atmospheric processes
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "Weather is the day-to-day condition of the atmosphere — including "
                "temperature, rainfall, wind, and cloud cover. Climate is the average "
                "weather pattern for a region over at least 30 years. Weather changes "
                "from hour to hour, while climate changes over decades or centuries. "
                "The study of weather is called meteorology.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "6",
    },
    {
        "text": "The Sun heats the Earth's surface unevenly. Land heats up and cools down "
                "faster than the sea. Equatorial regions receive more direct solar radiation "
                "than polar regions. These differences create areas of high and low "
                "air pressure. Air moves from high pressure to low pressure — this "
                "movement is what we call wind.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "6",
    },
    {
        "text": "Air masses are large bodies of air with similar temperature and humidity "
                "throughout. The UK's weather is influenced by several air masses: polar "
                "maritime (cold, wet, from the north-west), tropical maritime (warm, wet, "
                "from the south-west), and continental (dry, cold in winter/hot in summer, "
                "from the east). Where two air masses meet, a front is formed.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "7",
    },
    {
        "text": "A front is the boundary between two air masses of different temperatures "
                "and densities. At a warm front, warm air gradually rises over cold air, "
                "producing steady rainfall ahead of the front. At a cold front, cold "
                "air undercuts warm air rapidly, causing it to rise steeply — producing "
                "heavy rain and thunderstorms. A depression (low pressure system) "
                "contains both types of front.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "7",
    },
    {
        "text": "Depressions (cyclones in mid-latitudes) are areas of low atmospheric "
                "pressure associated with unsettled weather — cloud, rain, and strong "
                "winds. Air spirals inward and upward into a depression, cooling and "
                "condensing to form clouds. Depressions move from west to east across "
                "the UK, bringing the characteristic sequence of changing weather "
                "over 2–3 days as they pass.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "8",
    },
    {
        "text": "Anticyclones are areas of high atmospheric pressure associated with "
                "settled, dry weather. Air sinks and warms, preventing cloud formation. "
                "In summer, anticyclones bring hot, sunny weather; in winter they bring "
                "cold, clear, frosty conditions with fog in sheltered valleys. "
                "Anticyclones move slowly and can persist for days or weeks, causing "
                "prolonged droughts or cold spells.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "8",
    },
    {
        "text": "Relief rainfall (orographic rainfall) occurs when moist air is forced "
                "to rise over a mountain range, cooling and condensing to produce "
                "heavy rain on the windward side. As the air descends the other side, "
                "it warms and dries, creating a rain shadow effect. The western "
                "mountains of Norway, the UK, and the Andes receive extremely high "
                "rainfall, while their eastern sides are much drier.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "8",
    },
    {
        "text": "Convectional rainfall occurs when strong surface heating causes air "
                "to rise rapidly, cool, and condense. It produces towering cumulonimbus "
                "clouds, intense short-duration rainfall, thunder, and lightning. "
                "It is common in tropical regions every afternoon, in mid-latitude "
                "summers, and during heatwaves. The strong updrafts can produce "
                "hailstones — ice pellets that grow as they are repeatedly carried "
                "up by air currents.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "8",
    },
    {
        "text": "The jet stream is a fast-moving ribbon of wind at high altitude "
                "(8–12 km) in the upper troposphere. It flows west to east at speeds "
                "of 100–400 km/h and steers depressions and weather systems across "
                "mid-latitudes. When the jet stream shifts or weakens, unusual weather "
                "results — a displaced jet stream contributed to the 2003 European "
                "heatwave and the prolonged UK floods of winter 2013–14.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "9",
    },
    {
        "text": "El Niño is a periodic warming of sea surface temperatures in the central "
                "and eastern Pacific Ocean, occurring roughly every 2–7 years. It disrupts "
                "normal atmospheric circulation, causing droughts in Australia, Indonesia, "
                "and India, and heavy rainfall in Peru and California. La Niña is the "
                "opposite (unusual cooling) and causes the reverse pattern. Together "
                "they are called the El Niño-Southern Oscillation (ENSO).",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "9",
    },
    {
        "text": "Weather forecasting uses data from a global network of weather stations, "
                "ships, buoys, weather balloons, satellites, and radar. Supercomputers run "
                "numerical weather prediction models that divide the atmosphere into a "
                "3D grid and solve equations governing fluid dynamics and thermodynamics. "
                "A 5-day forecast today is as accurate as a 1-day forecast was in 1980, "
                "thanks to improved models and more observations.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "10",
    },
    {
        "text": "Extreme weather events include heatwaves, cold snaps, droughts, floods, "
                "tropical cyclones, tornadoes, and blizzards. Climate change is altering "
                "the frequency and intensity of many extreme events. The probability of "
                "extreme heat events has increased substantially — the UK's first ever "
                "40°C temperature was recorded in July 2022. Attribution science can now "
                "quantify how much more likely an individual extreme event was made by "
                "climate change.",
        "subject": "geography",
        "topic": "weather and atmospheric processes",
        "grade": "10",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: environmental management and conservation
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "Environmental management involves the stewardship of natural resources "
                "and ecosystems to meet human needs while maintaining ecological health "
                "for future generations. It operates at scales from local (managing a "
                "nature reserve) to global (international climate agreements). Effective "
                "environmental management requires scientific knowledge, political will, "
                "and cooperation between governments, businesses, and communities.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "8",
    },
    {
        "text": "Protected areas are regions designated for conservation, where human "
                "activities are restricted. They include national parks, nature reserves, "
                "marine protected areas (MPAs), and biosphere reserves. Protected areas "
                "currently cover about 17% of the world's land and 8% of ocean. Research "
                "shows they are effective at conserving biodiversity when well-managed "
                "and enforced.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "8",
    },
    {
        "text": "Biodiversity hotspots are regions with exceptionally high numbers of "
                "endemic species (found nowhere else) that are under severe threat of "
                "habitat loss. The 36 identified biodiversity hotspots cover just 2.5% "
                "of Earth's land surface but contain over half of all plant species and "
                "nearly half of all vertebrate species. They include the Tropical Andes, "
                "Madagascar, the Philippines, and the Western Ghats of India.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "9",
    },
    {
        "text": "Deforestation is the permanent removal of forests to convert land to "
                "other uses, primarily agriculture. Tropical forests are disappearing at "
                "about 10 million hectares per year — an area roughly the size of Iceland. "
                "The Amazon is a particular concern: over 20% has already been cleared, "
                "and scientists warn that if deforestation reaches 20–25%, the forest "
                "could undergo a catastrophic 'dieback', transforming from rainforest "
                "to dry savanna.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "9",
    },
    {
        "text": "CITES (Convention on International Trade in Endangered Species) is an "
                "international agreement that regulates trade in over 38,000 species of "
                "animals and plants. Species are listed on three appendices based on their "
                "extinction risk. Appendix I species (e.g., tigers, rhinos, elephants) "
                "cannot be commercially traded. CITES has prevented the extinction of "
                "many species but enforcement remains challenging, particularly for "
                "illegal wildlife trade.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "9",
    },
    {
        "text": "Marine protected areas (MPAs) are ocean zones where human activities "
                "such as fishing, drilling, and development are restricted. Fully protected "
                "MPAs, called no-take zones, allow fish populations to recover — fish "
                "inside reserves can be up to five times more abundant than outside. "
                "Spillover of fish beyond MPA boundaries benefits fisheries. However, "
                "only about 3% of the ocean is in fully or highly protected MPAs.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "9",
    },
    {
        "text": "The concept of ecosystem services recognises that healthy ecosystems "
                "provide economic and social benefits to people. These include provisioning "
                "services (food, water, timber), regulating services (flood control, "
                "carbon storage, pollination), and cultural services (recreation, "
                "spiritual value). Placing economic values on ecosystem services — "
                "for example, estimating the cost of replacing natural flood protection "
                "with engineering — can make conservation economically compelling.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "10",
    },
    {
        "text": "The Aichi Biodiversity Targets were a set of 20 global goals agreed under "
                "the Convention on Biological Diversity (CBD) for 2010–2020. None of the "
                "20 targets was fully met. The Kunming-Montreal Global Biodiversity "
                "Framework (2022) set new targets for 2030, including protecting 30% of "
                "land and oceans (the '30x30' target) and restoring 30% of degraded "
                "ecosystems. Meeting these targets requires an estimated $700 billion "
                "per year in conservation finance.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "10",
    },
    {
        "text": "Payment for Ecosystem Services (PES) schemes pay landowners to manage "
                "land in ways that generate ecosystem services. Costa Rica's PES programme "
                "pays farmers to protect and restore forests, having helped reverse "
                "deforestation and double forest cover since the 1980s. REDD+ (Reducing "
                "Emissions from Deforestation and Forest Degradation) is an international "
                "climate framework that compensates developing countries for protecting "
                "forests.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "10",
    },
    {
        "text": "Environmental impact assessments (EIAs) are formal evaluations of the "
                "likely environmental effects of proposed development projects — such as "
                "roads, dams, mines, and housing estates — before planning permission is "
                "granted. EIAs identify mitigation measures and may lead to projects "
                "being modified or rejected. Strategic environmental assessments (SEAs) "
                "apply the same principle to policies and plans rather than individual "
                "projects.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "11",
    },
    {
        "text": "The concept of planetary boundaries defines nine Earth system processes "
                "within which humanity can safely operate. Breaching a boundary risks "
                "pushing the Earth system into a new, potentially hostile state. "
                "Scientists estimate that six of the nine boundaries have already been "
                "crossed, including climate change, biosphere integrity, land-system "
                "change, and introduction of novel entities (plastics and chemicals). "
                "This framework guides global sustainability policy.",
        "subject": "geography",
        "topic": "environmental management and conservation",
        "grade": "11",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: demographic change and migration
    # ══════════════════════════════════════════════════════════════════════════
#Change from here to here

[
    {
        "text": "An ecosystem is a community of living things (plants, animals, and microorganisms) interacting with each other and their non-living environment. Every ecosystem has two main parts: biotic factors (living things) and abiotic factors (non-living things like sunlight, water, and temperature). A pond, a forest, and a coral reef are all examples of ecosystems.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "6"
    },
    {
        "text": "A biome is a large region of the Earth with a similar climate, vegetation, and wildlife. The main biomes include tropical rainforest, desert, grassland, tundra, taiga, and temperate deciduous forest. Each biome is home to plants and animals specially adapted to survive in those conditions.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "6"
    },
    {
        "text": "Tropical rainforests are found near the equator where it is hot and wet all year. They cover only about 6% of Earth's land surface but are home to over 50% of all plant and animal species. The Amazon rainforest in South America is the world's largest tropical rainforest, covering about 5.5 million square kilometres.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "6"
    },
    {
        "text": "The tundra biome is found in the Arctic and on high mountaintops where temperatures are extremely cold. The ground is permanently frozen below the surface in a layer called permafrost, which prevents trees from growing. Low-lying plants like mosses, lichens, and shrubs survive here by growing very quickly during the short summer.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "7"
    },
    {
        "text": "Food chains show how energy passes from one living thing to another in an ecosystem. Energy starts with producers (usually plants) that capture sunlight through photosynthesis, then flows to primary consumers (herbivores), secondary consumers (carnivores), and decomposers. Only about 10% of the energy at each level is passed on to the next, which is why food chains rarely have more than five links.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "7"
    },
    {
        "text": "The taiga, also called boreal forest, is the world's largest land biome, stretching across Canada, Russia, and Scandinavia. It is dominated by coniferous trees such as spruce, fir, and pine that are adapted to cold winters and thin, acidic soils. The taiga stores enormous amounts of carbon and plays a critical role in regulating the global climate.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "7"
    },
    {
        "text": "Coral reefs are marine ecosystems built by tiny animals called coral polyps that secrete calcium carbonate skeletons. Although they cover less than 1% of the ocean floor, coral reefs support about 25% of all marine species. Rising ocean temperatures cause coral bleaching \u2014 a stress response that can kill reefs if temperatures remain elevated for too long.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "8"
    },
    {
        "text": "Biodiversity refers to the variety of life in an ecosystem, including the number of species, genetic diversity within species, and diversity of ecosystems. High biodiversity makes ecosystems more resilient \u2014 if one species is lost, others can fill its role. Tropical rainforests have the highest biodiversity of any land biome, while tundra and deserts have the lowest.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "8"
    },
    {
        "text": "Nutrient cycling is the process by which chemical elements such as carbon, nitrogen, and phosphorus move through an ecosystem. Decomposers \u2014 bacteria and fungi \u2014 break down dead organic matter and return nutrients to the soil, where they are absorbed again by plants. Without decomposers, dead material would accumulate and nutrients would remain locked in unusable form.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "8"
    },
    {
        "text": "Human activities are causing biodiversity loss at an unprecedented rate \u2014 scientists estimate the current extinction rate is 100 to 1,000 times higher than the natural background rate. The main drivers are habitat destruction, overexploitation, invasive species, pollution, and climate change. The IUCN Red List currently identifies over 42,000 species as threatened with extinction.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "9"
    },
    {
        "text": "Ecosystem services are the benefits that natural ecosystems provide to humans, both directly and indirectly. Provisioning services include food, fresh water, and timber; regulating services include flood control, carbon storage, and pollination; cultural services include recreation and tourism. Economists estimate the value of global ecosystem services at over $125 trillion per year \u2014 far exceeding global GDP.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "10"
    },
    {
        "text": "Succession is the process by which an ecosystem changes over time as different communities of organisms replace each other. Primary succession begins on bare rock or volcanic lava, starting with pioneer species like lichens that break down rock into soil. Over hundreds to thousands of years, the ecosystem develops into a stable climax community such as a mature forest.",
        "subject": "geography",
        "topic": "ecosystems and biomes",
        "grade": "10"
    },
    {
        "text": "Urbanisation is the process by which an increasing proportion of a country's population moves to live in towns and cities. For the first time in history, more than half of the world's people now live in urban areas. Urbanisation is driven by rural\u2013urban migration and natural population increase within cities.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "7"
    },
    {
        "text": "People move from rural areas to cities for many reasons. Push factors include lack of jobs, poor services, and natural disasters in the countryside. Pull factors include better employment opportunities, hospitals, schools, and entertainment in cities.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "7"
    },
    {
        "text": "Megacities are urban areas with populations of more than 10 million people. In 1950 there were only two megacities \u2014 New York and Tokyo. By 2024 there are over 35 megacities, and most of them are in developing countries in Asia, Africa, and Latin America.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "8"
    },
    {
        "text": "Squatter settlements, also called slums or shanty towns, are areas of informal housing built without legal permission, usually on the edges of rapidly growing cities in developing countries. An estimated 1 billion people globally live in such settlements, which often lack clean water, sanitation, and electricity. Dharavi in Mumbai and Kibera in Nairobi are two of the world's largest and most studied slums.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "8"
    },
    {
        "text": "The urban heat island (UHI) effect describes how cities are significantly warmer than surrounding rural areas. Dark surfaces like tarmac and rooftops absorb more solar radiation, while buildings trap heat and reduce wind. City centres can be up to 5\u00b0C warmer than nearby countryside, increasing energy demand for cooling and worsening air quality.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "8"
    },
    {
        "text": "Counter-urbanisation is the movement of people away from large cities into smaller towns and rural areas. It is common in wealthy developed countries where car ownership and remote working allow people to live farther from city centres. This trend can lead to the decline of inner-city areas and put pressure on rural infrastructure and housing.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "9"
    },
    {
        "text": "Urban gentrification occurs when wealthier residents move into previously low-income inner-city areas, renovating properties and attracting new businesses. While this can reduce crime and improve the built environment, it typically raises rents and displaces existing lower-income communities. London's Brixton and New York's Brooklyn are well-documented examples of gentrified neighbourhoods.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "9"
    },
    {
        "text": "Sustainable urban development aims to meet the needs of city residents today without compromising the ability of future generations to do the same. Strategies include expanding public transport to reduce car use, creating green spaces, improving energy efficiency of buildings, and managing waste through recycling. Curitiba in Brazil and Copenhagen in Denmark are frequently cited as models of sustainable urban planning.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "9"
    },
    {
        "text": "Urban sprawl is the uncontrolled outward expansion of cities into surrounding rural and suburban land. It increases car dependency, destroys habitats, and raises the cost of providing infrastructure such as roads and utilities. Strategies to limit sprawl include greenbelt policies that prohibit development in designated zones around cities.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "10"
    },
    {
        "text": "The concept of a primate city describes a country's largest city that is disproportionately dominant in population, economic activity, and political power compared to all other cities. Bangkok contains about 11 million people \u2014 nearly 17% of Thailand's population \u2014 and dominates the national economy. Primate cities are more common in developing countries and can concentrate inequality geographically.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "10"
    },
    {
        "text": "Smart cities use digital technology and data collection to improve urban services and quality of life. Sensors monitor traffic flow, energy usage, air quality, and waste levels in real time, allowing city managers to respond efficiently. Singapore and Songdo in South Korea are leading examples, though critics raise concerns about surveillance and data privacy.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "11"
    },
    {
        "text": "Rapid urbanisation in sub-Saharan Africa presents unique challenges. Africa's urban population is expected to triple to 1.5 billion by 2050, faster than any other region. Many cities lack the infrastructure investment and governance capacity to absorb this growth sustainably, leading to expansion of informal settlements and pressure on water and sanitation systems.",
        "subject": "geography",
        "topic": "urbanisation and cities",
        "grade": "11"
    },
    {
        "text": "A natural hazard is a naturally occurring event that has the potential to cause harm to people or damage to property. Examples include earthquakes, volcanic eruptions, hurricanes, floods, and wildfires. A natural hazard only becomes a natural disaster when it significantly affects people \u2014 a large earthquake in an uninhabited desert is a hazard but not a disaster.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "7"
    },
    {
        "text": "Earthquakes occur when energy stored in rocks along fault lines is suddenly released, sending seismic waves through the Earth. Most earthquakes happen at tectonic plate boundaries, although intraplate earthquakes can also occur far from boundaries. The point underground where the earthquake originates is called the focus; the point on the surface directly above is the epicentre.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "7"
    },
    {
        "text": "Volcanoes erupt when magma, gas, and ash are expelled from the Earth's interior through a vent. Explosive eruptions occur when thick, gas-rich magma blocks the vent, building up pressure until it blasts apart. Effusive eruptions produce flowing rivers of low-viscosity lava and are generally less immediately dangerous to life.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "8"
    },
    {
        "text": "Tropical cyclones (also called hurricanes or typhoons depending on where they form) are intense rotating storm systems that develop over warm ocean water above 26.5\u00b0C. They produce extreme winds exceeding 119 km/h, heavy rainfall, and a storm surge \u2014 a wall of ocean water pushed ashore that causes most cyclone-related deaths. They lose strength rapidly when they move over land or cooler water.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "8"
    },
    {
        "text": "Flooding is the world's most common and costly natural hazard. River flooding occurs when rainfall or snowmelt exceeds a river's capacity; coastal flooding is caused by storm surges and sea-level rise; flash floods result from sudden intense rainfall in areas with little infiltration. Human factors such as deforestation, urbanisation, and floodplain development significantly increase flood risk.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "8"
    },
    {
        "text": "Vulnerability to natural hazards is not equal \u2014 it is strongly shaped by levels of economic development. The 2010 Haiti earthquake (magnitude 7.0) killed over 200,000 people, while a similar-magnitude earthquake in New Zealand in 2011 killed 185. Haiti's high death toll reflected poor building standards, weak emergency services, and political instability \u2014 factors linked to poverty.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "9"
    },
    {
        "text": "The disaster risk equation states that risk = hazard \u00d7 vulnerability \u00f7 capacity. Capacity includes the resources, infrastructure, and governance a society has to prepare for, respond to, and recover from disasters. Wealthier countries with good early warning systems, building codes, and emergency services have much greater capacity to reduce disaster risk.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "9"
    },
    {
        "text": "Tsunamis are series of ocean waves triggered by sudden large-scale displacement of water, most commonly by submarine earthquakes. The 2004 Indian Ocean tsunami, triggered by a magnitude 9.1 earthquake off Sumatra, killed around 230,000 people across 14 countries. The Pacific Tsunami Warning System, established in 1949, now monitors seismic activity and issues warnings to coastal communities.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "9"
    },
    {
        "text": "Wildfire frequency and intensity are increasing globally due to climate change, prolonged droughts, and human land management. Wildfires clear vegetation, destroy habitats, release large amounts of CO2, and cause air quality crises affecting millions. Australia's 'Black Summer' of 2019\u201320 burned over 18 million hectares, killed an estimated 3 billion animals, and generated smoke that circled the globe.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "10"
    },
    {
        "text": "Hazard mapping and land-use planning are key tools for reducing exposure to natural hazards. GIS (Geographic Information Systems) is used to identify and map hazard-prone zones, allowing planners to restrict construction in high-risk areas. Japan's comprehensive hazard maps for earthquakes, tsunamis, and volcanic ash fall are among the most detailed in the world.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "10"
    },
    {
        "text": "Climate change is altering the distribution and intensity of many natural hazards. Warmer sea surface temperatures are expected to increase the intensity of tropical cyclones, even if their total frequency stays similar. Sea-level rise amplifies coastal flooding hazards, and prolonged droughts increase wildfire and landslide risk \u2014 making integrated disaster risk reduction increasingly urgent.",
        "subject": "geography",
        "topic": "natural hazards",
        "grade": "11"
    },
    {
        "text": "Economic development refers to improvements in the economic wellbeing and quality of life of people in a country. It is measured not just by income but by access to education, healthcare, and other services. Geographers often distinguish between economic growth (an increase in output) and economic development (a broader improvement in living standards).",
        "subject": "geography",
        "topic": "economic development",
        "grade": "9"
    },
    {
        "text": "Gross Domestic Product (GDP) per capita is the most commonly used measure of a country's economic development. It is calculated by dividing a country's total economic output by its population. However, GDP per capita is criticised for masking inequality \u2014 a country can have a high average income while most citizens remain poor.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "9"
    },
    {
        "text": "The Human Development Index (HDI) was created by the United Nations in 1990 as a broader measure of development. It combines three dimensions: a long and healthy life (life expectancy), access to knowledge (mean and expected years of schooling), and a decent standard of living (GNI per capita). Norway consistently ranks first on the HDI, while countries in sub-Saharan Africa occupy the lowest positions.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "9"
    },
    {
        "text": "Rostow's Stages of Economic Growth model (1960) proposed that all countries pass through five stages of development: traditional society, preconditions for take-off, take-off, drive to maturity, and high mass consumption. The model was influential but is criticised for being too linear and for assuming all countries should follow the Western industrialisation path. It also ignores colonialism's role in creating global inequality.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "10"
    },
    {
        "text": "The development gap refers to the growing economic inequality between the world's richest and poorest countries. The richest 10% of the global population earn about 40% of total world income, while the poorest 10% earn only 2\u20133%. This gap has multiple causes including colonial history, debt, unfair trade rules, and political instability.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "10"
    },
    {
        "text": "Foreign direct investment (FDI) occurs when companies from one country invest in businesses or infrastructure in another country. FDI can bring jobs, technology, and skills to developing economies. However, critics argue that transnational corporations (TNCs) often repatriate profits back to their home country rather than reinvesting locally, limiting long-term development benefits.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "10"
    },
    {
        "text": "Microfinance refers to the provision of small loans (microcredit) and other financial services to low-income individuals who cannot access traditional banking. Pioneered by the Grameen Bank in Bangladesh, founded by Muhammad Yunus in 1983, microfinance has helped millions \u2014 particularly women \u2014 start small businesses and escape poverty. Over 140 million borrowers globally now use microfinance services.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "10"
    },
    {
        "text": "The Gini coefficient is a statistical measure of income inequality within a country, ranging from 0 (perfect equality) to 1 (one person holds all income). South Africa has one of the world's highest Gini coefficients at around 0.63, reflecting extreme inequality rooted in its apartheid history. Scandinavian countries consistently record the lowest Gini coefficients \u2014 around 0.25\u20130.28.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "11"
    },
    {
        "text": "Dependency theory, associated with scholars like Andr\u00e9 Gunder Frank, argues that developing nations are kept in a state of dependence by wealthy core nations through trade relationships that favour the core. Raw materials flow cheaply from the periphery and return as expensive manufactured goods, locking developing countries into low-value economic activity. This neo-colonial relationship is seen as perpetuating the development gap.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "11"
    },
    {
        "text": "The Sustainable Development Goals (SDGs), adopted by all UN member states in 2015, set 17 interconnected goals to be achieved by 2030, ranging from ending poverty and hunger to ensuring clean energy and climate action. Progress has been severely disrupted by the COVID-19 pandemic and conflict, with the UN reporting in 2023 that fewer than 15% of SDG targets are on track. The SDGs reflect a shift from purely economic to holistic conceptions of development.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "11"
    },
    {
        "text": "Remittances \u2014 money sent home by migrant workers \u2014 are a major source of development finance for many low-income countries. Global remittance flows reached $857 billion in 2023, exceeding foreign aid by a factor of three. Countries like Tajikistan, Tonga, and Lebanon receive remittances equivalent to over 30% of their GDP, making them heavily dependent on diaspora income.",
        "subject": "geography",
        "topic": "economic development",
        "grade": "11"
    },
    {
        "text": "Globalisation is the process by which the world is becoming increasingly interconnected through trade, communication, migration, and the sharing of ideas and culture. Improvements in transport and communications technology since the mid-20th century have dramatically accelerated globalisation. Today, a smartphone contains components manufactured in dozens of different countries.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "9"
    },
    {
        "text": "International trade involves countries buying (importing) and selling (exporting) goods and services to each other. Countries tend to export goods in which they have a comparative advantage \u2014 meaning they can produce them more efficiently relative to other goods. World merchandise trade totalled about $24 trillion in 2023, with China, the USA, and Germany being the largest trading nations.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "9"
    },
    {
        "text": "Transnational corporations (TNCs) are companies that operate in multiple countries, with headquarters in one country and production or sales operations in others. TNCs drive globalisation by spreading capital, technology, and employment across borders. Apple, Toyota, and Unilever are examples of TNCs whose supply chains and markets span the entire globe.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "9"
    },
    {
        "text": "Free trade refers to trade between countries without tariffs (import taxes), quotas, or other barriers. Organisations such as the World Trade Organization (WTO) promote free trade, arguing it increases economic efficiency and raises living standards. Critics argue that free trade can disadvantage developing countries whose industries cannot compete with heavily subsidised producers in wealthy nations.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "10"
    },
    {
        "text": "Global supply chains are the network of organisations, people, and resources involved in producing and delivering a product from raw material to final consumer. A typical car may include parts manufactured in over 30 countries. The COVID-19 pandemic exposed the fragility of just-in-time global supply chains when factory shutdowns in one region caused shortages worldwide.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "10"
    },
    {
        "text": "The digital economy refers to economic activity that relies on digital computing technology, including e-commerce, digital services, and platform businesses. Platforms such as Amazon, Alibaba, and Uber operate globally but are concentrated in a small number of countries. By 2022, the digital economy accounted for over 15% of global GDP, with growth accelerating rapidly in developing countries.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "10"
    },
    {
        "text": "Deindustrialisation is the decline of manufacturing industry in developed countries, often linked to globalisation. As TNCs relocated factories to lower-wage countries, manufacturing cities in the UK, USA, and Germany saw mass unemployment and urban decline. Detroit, once the centre of US car manufacturing with 1.8 million residents, lost over 60% of its population as the automotive industry shifted production.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "10"
    },
    {
        "text": "Trade blocs are groups of countries that agree to reduce or eliminate trade barriers between themselves. The European Union (EU) is the world's largest single market, allowing free movement of goods, services, capital, and people among its 27 members. Regional trade agreements can boost member economies but may divert trade away from non-members and create new inequalities.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "11"
    },
    {
        "text": "The terms of trade describe the ratio between the prices a country receives for its exports and the prices it pays for its imports. Many developing countries that rely on exporting raw commodities (such as coffee, copper, or cotton) face unfavourable terms of trade because commodity prices fluctuate and tend to rise more slowly than manufactured goods. This structural disadvantage is called the commodity trap.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "11"
    },
    {
        "text": "Fair trade is a trading movement that aims to ensure producers in developing countries receive a guaranteed minimum price for their goods and better working conditions. Products such as Fairtrade-certified coffee, cocoa, and bananas carry a premium that is reinvested in producer communities. By 2022, global Fairtrade sales exceeded \u20ac11.8 billion, though critics argue the premium rarely reaches the individual farmers it aims to help.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "11"
    },
    {
        "text": "Deglobalisation refers to a trend of reducing economic integration, driven by rising nationalism, protectionism, geopolitical rivalry, and lessons from supply chain disruptions. The US\u2013China trade war (from 2018), Brexit (2020), and post-pandemic reshoring of manufacturing are cited as evidence of a deglobalisation shift. Economists debate whether this represents a fundamental reversal or a temporary adjustment in the globalisation trend.",
        "subject": "geography",
        "topic": "globalisation and trade",
        "grade": "12"
    },
    {
        "text": "Agriculture is the practice of cultivating land to grow crops and raise animals for food, fibre, and other products. About 50% of all habitable land on Earth is used for agriculture. Farming feeds around 8 billion people and employs about 1 billion workers globally \u2014 making it the world's largest industry by employment.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "7"
    },
    {
        "text": "There are two main types of farming: subsistence farming and commercial farming. Subsistence farmers grow food mainly to feed their own families with little surplus to sell. Commercial farming produces crops or livestock primarily to sell for profit and often relies on mechanisation, fertilisers, and pesticides to maximise yields.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "7"
    },
    {
        "text": "The Green Revolution of the 1960s and 1970s dramatically increased food production in Asia and Latin America through the introduction of high-yielding crop varieties, irrigation, and chemical fertilisers. Countries like India and Mexico dramatically increased wheat and rice production and avoided widespread famines. However, the Green Revolution also increased inequality, as wealthier farmers could more easily afford the new technologies.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "8"
    },
    {
        "text": "Food security exists when all people at all times have access to sufficient, safe, and nutritious food to meet their needs. About 733 million people globally experienced hunger in 2023 \u2014 roughly 1 in 11. Food insecurity is not simply caused by insufficient global food production; it is also driven by poverty, conflict, unequal distribution, and food waste.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "8"
    },
    {
        "text": "Intensive farming maximises output from a small area of land through high inputs of labour, machinery, fertilisers, and pesticides. Battery chicken farming and large-scale monoculture crops like maize are examples. While intensive farming increases yields and lowers food prices, it can cause serious environmental problems including soil degradation, water pollution, and biodiversity loss.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "8"
    },
    {
        "text": "Extensive farming uses large areas of land with relatively low inputs of labour and capital per hectare. Sheep and cattle ranching on the Australian outback or the North American Great Plains are classic examples. Yields per hectare are much lower than intensive farming, but the approach can be more sustainable and requires less chemical input.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "9"
    },
    {
        "text": "Soil degradation is a serious global threat to food security. Intensive cultivation, overgrazing, deforestation, and salinisation from poorly managed irrigation are stripping topsoil of nutrients and organic matter. The UN estimates that about 33% of the world's soils are already degraded, and at current rates, we may only have 60 years of topsoil remaining.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "9"
    },
    {
        "text": "Genetically modified (GM) crops have had their DNA altered to introduce desirable traits such as pest resistance, drought tolerance, or higher nutritional value. Golden Rice was engineered to produce beta-carotene (vitamin A precursor) to address deficiency in developing countries. GM crops are controversial \u2014 supporters highlight their potential to improve yields and nutrition, while critics raise concerns about ecological impacts and corporate control of the food supply.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "9"
    },
    {
        "text": "Water is the biggest constraint on agricultural expansion globally. Agriculture accounts for about 70% of all freshwater withdrawals worldwide. Irrigated agriculture produces about 40% of global food on only 20% of farmland, but unsustainable irrigation is depleting aquifers and causing soil salinisation in countries including India, Pakistan, and the USA.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "10"
    },
    {
        "text": "Food waste is a major challenge in global food systems. Approximately one-third of all food produced for human consumption \u2014 about 1.3 billion tonnes per year \u2014 is lost or wasted. In developed countries, most waste occurs at the retail and consumer level (unsold food, expired products); in developing countries, waste mainly occurs post-harvest due to lack of storage and refrigeration infrastructure.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "10"
    },
    {
        "text": "Agroecology is an approach to farming that applies ecological principles to agricultural systems, aiming to make food production sustainable and resilient. It emphasises biodiversity, natural pest control, crop rotation, and minimal chemical inputs. Unlike the Green Revolution approach, agroecology is knowledge-intensive rather than input-intensive, and is particularly suited to smallholder farmers in developing countries.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "11"
    },
    {
        "text": "The global food system is responsible for about 26% of all greenhouse gas emissions. Livestock farming alone contributes about 14.5% of global emissions through methane from digestion, nitrous oxide from manure, and deforestation for pasture. Shifting dietary patterns \u2014 particularly reducing meat consumption in wealthy countries \u2014 is identified by the IPCC as one of the most effective individual actions to reduce emissions.",
        "subject": "geography",
        "topic": "agriculture and food",
        "grade": "11"
    },
    {
        "text": "Energy resources are the sources from which we obtain the energy needed to power homes, transport, and industries. They are divided into non-renewable resources \u2014 including coal, oil, and natural gas \u2014 which take millions of years to form and will eventually run out, and renewable resources \u2014 including solar, wind, and hydro \u2014 which replenish naturally.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "7"
    },
    {
        "text": "Fossil fuels (coal, oil, and natural gas) currently supply about 80% of the world's energy. They formed from the compressed remains of ancient plants and animals over millions of years. Burning fossil fuels releases the carbon stored in them as CO2, making them the leading cause of human-driven climate change.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "7"
    },
    {
        "text": "Solar energy is generated by capturing the radiant light and heat from the Sun using photovoltaic (PV) panels or solar thermal systems. The amount of solar energy reaching Earth's surface in one hour is enough to meet global energy demand for an entire year. The cost of solar PV has fallen by over 90% since 2010, making it now the cheapest source of electricity in history.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "8"
    },
    {
        "text": "Wind energy is generated when moving air turns the blades of a wind turbine, driving a generator. Offshore wind farms benefit from stronger and more consistent winds than onshore ones. The Hornsea 2 offshore wind farm in the UK, completed in 2022, is one of the world's largest, with 165 turbines capable of powering over 1.3 million homes.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "8"
    },
    {
        "text": "Hydroelectric power (HEP) generates electricity by using the kinetic energy of flowing water to spin turbines. It is the world's largest source of renewable electricity, accounting for about 16% of global power generation. China's Three Gorges Dam, the world's largest power station, has a capacity of 22,500 MW but displaced over 1.3 million people during its construction.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "8"
    },
    {
        "text": "Energy mix refers to the combination of energy sources a country uses to meet its needs. Countries' energy mixes vary widely based on their natural resources, economic development, and policy choices. Iceland generates almost 100% of its electricity from geothermal and hydroelectric sources, while Poland still relies on coal for over 70% of its electricity.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "9"
    },
    {
        "text": "Nuclear energy generates electricity from the heat produced by nuclear fission \u2014 the splitting of uranium or plutonium atoms. It produces very low greenhouse gas emissions during operation and can generate large amounts of reliable baseload power. Major concerns include the safe disposal of radioactive waste, high construction costs, and the risk of accidents \u2014 as demonstrated by Chernobyl (1986) and Fukushima (2011).",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "9"
    },
    {
        "text": "Energy security refers to the reliable and affordable supply of energy to meet a country's needs. Countries that depend heavily on energy imports are vulnerable to price shocks and supply disruptions from producing countries. Russia's invasion of Ukraine in 2022 triggered a major European energy security crisis, forcing rapid acceleration of renewable energy deployment and diversification of gas supplies.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "10"
    },
    {
        "text": "The energy trilemma describes the challenge of simultaneously achieving energy security, energy equity (affordable access for all), and environmental sustainability. These three goals often conflict \u2014 for example, cheap fossil fuels provide energy equity but damage the environment, while renewable energy is sustainable but intermittent and sometimes costly. Governments must balance all three dimensions when setting energy policy.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "10"
    },
    {
        "text": "Energy poverty affects an estimated 775 million people who lack access to electricity, mostly in sub-Saharan Africa and South Asia. Without reliable energy, people cannot refrigerate medicines, power schools, or run small businesses \u2014 deepening poverty. Distributed renewable energy solutions such as solar home systems and mini-grids are increasingly providing electricity to remote communities faster than grid extension.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "10"
    },
    {
        "text": "The energy transition refers to the global shift from fossil fuels to low-carbon energy sources to address climate change. Renewable energy capacity additions broke records in 2023 for the 22nd consecutive year, and renewables now account for about 30% of global electricity generation. However, the transition must accelerate dramatically \u2014 the IEA estimates no new fossil fuel development projects should proceed if the world is to achieve net-zero emissions by 2050.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "11"
    },
    {
        "text": "Geopolitics of energy describes how control over energy resources shapes political and military relationships between nations. Oil-rich regions such as the Persian Gulf and the Caspian Sea have historically been sites of conflict and foreign intervention. As the energy transition accelerates, new geopolitical competition is emerging around critical minerals \u2014 such as lithium, cobalt, and rare earth elements \u2014 needed for batteries and renewable technologies.",
        "subject": "geography",
        "topic": "energy resources",
        "grade": "12"
    }
]

[
    {
        "text": "The water cycle is the continuous movement of water through Earth's systems. Water moves between the oceans, atmosphere, land, and living things. Energy from the Sun drives most of this movement.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6"
    },
    {
        "text": "Evaporation is when liquid water turns into water vapour and rises into the air. It mostly happens from oceans, lakes, and rivers when the Sun heats the water's surface. About 86% of all global evaporation comes from the oceans.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6"
    },
    {
        "text": "Condensation happens when water vapour in the air cools down and turns back into tiny liquid droplets. These droplets cluster around tiny dust particles in the air to form clouds. You can see condensation on a cold glass on a warm day.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6"
    },
    {
        "text": "Precipitation is any form of water that falls from clouds to the ground. It can fall as rain, snow, sleet, or hail depending on the temperature. Most precipitation falls back into the oceans because oceans cover about 71% of Earth.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6"
    },
    {
        "text": "When rain falls on land, some of it flows over the surface into rivers and streams \u2014 this is called surface runoff. The amount of runoff depends on how steep the land is, how much rain falls, and whether the ground is already wet. Runoff eventually carries water back to the oceans.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6"
    },
    {
        "text": "Transpiration is the process by which plants release water vapour through tiny pores in their leaves called stomata. A single large oak tree can transpire over 150 litres of water on a hot summer day. Together, evaporation and transpiration are called evapotranspiration.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7"
    },
    {
        "text": "Infiltration is when water soaks into the soil and moves downward through rock layers. The rate of infiltration depends on soil type \u2014 sandy soils allow water through quickly, while clay soils slow it down. Water that infiltrates deeply can become groundwater stored underground.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7"
    },
    {
        "text": "Groundwater is fresh water stored in the spaces and cracks within underground rock layers called aquifers. Aquifers act like giant underground sponges that can hold huge amounts of water. The Ogallala Aquifer in the USA holds enough water to fill Lake Huron.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7"
    },
    {
        "text": "Rivers are a vital part of the water cycle, carrying precipitation from highland areas back toward the sea. The Amazon River discharges about 209,000 cubic metres of water per second into the Atlantic Ocean. River systems drain large areas of land called drainage basins or catchments.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7"
    },
    {
        "text": "Clouds form when moist air rises, cools, and water vapour condenses around tiny particles such as dust or sea salt. Different cloud types form at different altitudes \u2014 cirrus clouds form above 6,000 m, while stratus clouds form below 2,000 m. The type of cloud affects what kind of precipitation falls.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7"
    },
    {
        "text": "The oceans are the largest store of water in the water cycle, holding about 97% of all Earth's water. Ocean water is salty, so it must evaporate first before it can fall as fresh precipitation on land. The ocean also absorbs and releases heat, which influences weather patterns globally.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "8"
    },
    {
        "text": "Human activities are disrupting the natural water cycle in several significant ways. Deforestation reduces transpiration and infiltration, increasing surface runoff and flooding risk. Urbanisation replaces permeable soil with impermeable concrete, dramatically increasing runoff and reducing groundwater recharge.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "8"
    },
    {
        "text": "Over-extraction of groundwater from aquifers is a growing global problem. In parts of India and the Middle East, groundwater is being used faster than it is naturally replenished \u2014 this is called aquifer depletion. When coastal aquifers are over-extracted, saltwater can intrude and contaminate the freshwater supply.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "8"
    },
    {
        "text": "Climate change is intensifying the water cycle by increasing global temperatures. Warmer air holds more moisture \u2014 for every 1\u00b0C rise in temperature, air can hold about 7% more water vapour. This leads to more intense rainfall events in some regions and longer droughts in others.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "8"
    },
    {
        "text": "Interception is a stage of the water cycle where precipitation is caught by vegetation before it reaches the ground. A dense forest canopy can intercept up to 40% of rainfall, which then evaporates back into the atmosphere. This reduces the amount of water reaching the soil and entering rivers.",
        "subject": "geography",
        "topic": "water cycle",
        "grade": "8"
    },
    {
        "text": "The carbon cycle describes how carbon atoms move between the atmosphere, oceans, land, and living organisms. Carbon exists in the atmosphere mainly as carbon dioxide (CO2). All living things are built from carbon-containing molecules.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "8"
    },
    {
        "text": "Photosynthesis is a key process in the carbon cycle where plants absorb CO2 from the atmosphere and convert it into glucose using sunlight. This removes carbon from the atmosphere and locks it into plant biomass. Tropical rainforests absorb enormous amounts of CO2, making them vital carbon stores.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "8"
    },
    {
        "text": "When plants and animals die, decomposers such as bacteria and fungi break down their remains. This process releases carbon back into the atmosphere as CO2 or into the soil as organic matter. In cold or waterlogged conditions, decomposition slows down and carbon can be stored for thousands of years as peat.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "8"
    },
    {
        "text": "Fossil fuels \u2014 coal, oil, and natural gas \u2014 are carbon stores formed from ancient organic matter buried millions of years ago. Burning fossil fuels releases this stored carbon back into the atmosphere as CO2. Humans currently emit about 37 billion tonnes of CO2 per year from fossil fuel combustion.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "The oceans act as a major carbon sink, absorbing about 25\u201330% of all human CO2 emissions each year. CO2 dissolves in seawater to form carbonic acid (H2CO3), making the oceans more acidic \u2014 a process called ocean acidification. Since industrialisation, ocean pH has dropped from 8.2 to about 8.1, threatening coral reefs and shellfish.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "Marine organisms such as plankton and coral absorb dissolved CO2 to build calcium carbonate shells. When they die, their shells sink to the ocean floor and over millions of years can form limestone rock. Limestone is therefore one of Earth's largest long-term carbon stores.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "Deforestation is a major disruptor of the carbon cycle. When forests are cleared and burned, the carbon stored in trees is rapidly released as CO2. Deforestation accounts for roughly 10\u201315% of global human CO2 emissions annually.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "Carbon stores, also called carbon reservoirs, include the atmosphere, oceans, soil, vegetation, and geological deposits. The largest carbon store is sedimentary rocks and marine sediments, holding an estimated 100 million gigatonnes of carbon. By contrast, the atmosphere holds only about 860 gigatonnes.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "Soil is a significant but often overlooked carbon store, holding about twice as much carbon as the atmosphere. Carbon enters soil through decomposing organic matter and root activity. Disrupting soils through intensive farming or construction can release stored carbon as CO2.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "9"
    },
    {
        "text": "The enhanced greenhouse effect is closely linked to the carbon cycle. Elevated atmospheric CO2 \u2014 now over 420 parts per million (ppm), the highest in 800,000 years \u2014 traps more heat in the atmosphere. This direct link between the carbon cycle and climate change makes reducing CO2 emissions a global priority.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "10"
    },
    {
        "text": "Methane (CH4) is another important carbon-containing greenhouse gas in the carbon cycle. It is released from wetlands, livestock digestion, and decomposing waste in landfills. Methane is about 80 times more potent a greenhouse gas than CO2 over a 20-year period.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "10"
    },
    {
        "text": "Carbon sequestration refers to the process of capturing and storing atmospheric CO2. Natural sequestration occurs through photosynthesis and ocean absorption; artificial methods include carbon capture and storage (CCS) technology that injects CO2 deep into geological formations. Restoring forests and peatlands is one of the most cost-effective natural sequestration strategies.",
        "subject": "geography",
        "topic": "carbon cycle",
        "grade": "10"
    },
    {
        "text": "The rock cycle describes how rocks are continuously formed, broken down, and reformed over millions of years. There are three main types of rock: igneous, sedimentary, and metamorphic. Each type can be transformed into another through various Earth processes.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "7"
    },
    {
        "text": "Igneous rocks form when magma (molten rock underground) or lava (molten rock at the surface) cools and solidifies. Granite is an intrusive igneous rock that cools slowly underground, forming large crystals. Basalt is an extrusive igneous rock that cools quickly at the surface, forming small crystals.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "7"
    },
    {
        "text": "Sedimentary rocks form from layers of sediment \u2014 tiny fragments of rock, shells, and organic material \u2014 that accumulate over time. As layers build up, the weight above compresses the lower layers in a process called compaction. Minerals dissolved in water cement the particles together through a process called cementation.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "7"
    },
    {
        "text": "Metamorphic rocks form when existing rocks are changed by intense heat, pressure, or both deep within the Earth's crust. The original rock does not melt but is altered in structure and mineral composition. For example, limestone is transformed into marble, and mudstone becomes slate under metamorphic conditions.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "7"
    },
    {
        "text": "Weathering is the breakdown of rocks at or near Earth's surface by physical, chemical, or biological processes. Physical weathering breaks rocks into smaller pieces without changing their chemical composition \u2014 freeze-thaw action is a common example. Chemical weathering alters the minerals in rock; for instance, rainwater reacts with limestone to dissolve it.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "8"
    },
    {
        "text": "Erosion is the process by which weathered rock fragments are transported away from their original location by agents such as rivers, glaciers, wind, or waves. Deposition occurs when the energy carrying the sediment decreases and the particles are dropped. Over geological time, deposited sediments can form new sedimentary rock layers.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "8"
    },
    {
        "text": "Crystallisation is the process during which minerals solidify from magma as it cools. The rate of cooling determines crystal size: slow cooling (intrusive igneous rocks) produces large, visible crystals, while rapid cooling (extrusive igneous rocks) produces fine-grained or glassy textures. Obsidian, a volcanic glass, forms when lava cools almost instantly.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "8"
    },
    {
        "text": "Subduction \u2014 the sinking of one tectonic plate beneath another \u2014 drives part of the rock cycle. As rocks are pulled down into the mantle, extreme heat and pressure can melt them back into magma. This magma may later rise again through volcanic activity, completing one pathway of the rock cycle.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "8"
    },
    {
        "text": "Geological time is essential to understanding the rock cycle, as most rock transformations take millions to hundreds of millions of years. The oldest known rocks on Earth \u2014 the Acasta Gneisses in Canada \u2014 are about 4.03 billion years old. Rock strata (layers) act as a record of Earth's history, with deeper layers generally being older.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "9"
    },
    {
        "text": "Rock formation through the rock cycle is closely linked to plate tectonic activity. Mid-ocean ridges produce new igneous rock as magma wells up between diverging plates. Mountain-building zones (orogenies) create conditions for both metamorphic rock formation and extensive folding of sedimentary strata.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "9"
    },
    {
        "text": "The concept of uniformitarianism, proposed by geologist James Hutton in 1788, states that geological processes operating today have always operated in the same way throughout Earth's history. This principle \u2014 'the present is the key to the past' \u2014 underpins our understanding of how rock cycles have shaped Earth over billions of years.",
        "subject": "geography",
        "topic": "rock cycle",
        "grade": "9"
    },
    {
        "text": "The Earth's outer shell (lithosphere) is broken into about 15 major tectonic plates that float on the semi-molten asthenosphere below. These plates move very slowly \u2014 typically 2 to 10 centimetres per year \u2014 driven by convection currents in the mantle. Most earthquakes and volcanoes occur at the boundaries between plates.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "8"
    },
    {
        "text": "At convergent plate boundaries, two plates move toward each other. When an oceanic plate meets a continental plate, the denser oceanic plate sinks beneath the lighter continental plate in a process called subduction. This can trigger powerful earthquakes and form chains of volcanoes called volcanic arcs.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "8"
    },
    {
        "text": "At divergent plate boundaries, two plates move apart from each other. This creates mid-ocean ridges where magma rises to fill the gap and forms new oceanic crust. The Mid-Atlantic Ridge is a famous divergent boundary that extends about 16,000 km and causes Iceland to grow by about 2.5 cm per year.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "8"
    },
    {
        "text": "At transform plate boundaries, two plates slide horizontally past each other. No crust is created or destroyed at these boundaries, but intense friction causes frequent earthquakes. The San Andreas Fault in California is a well-known transform boundary between the Pacific and North American plates.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "8"
    },
    {
        "text": "Alfred Wegener proposed the theory of continental drift in 1912, suggesting that all continents were once joined in a supercontinent he named Pangaea. Evidence supporting this includes matching fossil records on separated continents, similar rock formations on different continents, and the jigsaw-like fit of coastlines. Pangaea began breaking apart about 200 million years ago.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "9"
    },
    {
        "text": "Seismic waves are vibrations generated by earthquakes that travel through the Earth. Primary (P) waves are compressional and travel through solids and liquids; secondary (S) waves are shear waves that only travel through solids. By analysing how seismic waves travel through the Earth, scientists have mapped the planet's internal layers.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "9"
    },
    {
        "text": "The Richter scale measures the magnitude of an earthquake based on the amplitude of seismic waves. It is a logarithmic scale, meaning each whole number increase represents a tenfold increase in wave amplitude and roughly 31.6 times more energy released. A magnitude 7.0 earthquake releases about 1,000 times more energy than a magnitude 5.0 earthquake.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "9"
    },
    {
        "text": "Tsunamis are large ocean waves triggered mainly by submarine earthquakes at subduction zones. When the ocean floor suddenly shifts, it displaces a vast column of water that radiates outward as a series of waves. In deep water tsunamis travel at up to 800 km/h but may only be 1 metre high; they slow and grow to devastating heights near shore.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "9"
    },
    {
        "text": "Volcanoes form where magma reaches the Earth's surface. At subduction zones, water released from the sinking plate lowers the melting point of mantle rock, generating magma that rises to form composite volcanoes with explosive eruptions. At divergent boundaries and hotspots, less viscous magma produces shield volcanoes with gentle, flowing eruptions.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "10"
    },
    {
        "text": "When two continental plates collide at a convergent boundary, neither is dense enough to subduct, so the crust crumples and is pushed upward to form fold mountains. The Himalayas formed this way as the Indo-Australian plate collided with the Eurasian plate about 50 million years ago. This collision continues today, adding a few millimetres to the Himalayas' height each year.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "10"
    },
    {
        "text": "Seafloor spreading provides strong evidence for plate tectonics. Magnetic stripes recorded in oceanic crust on either side of mid-ocean ridges show that the seafloor spreads symmetrically as new crust forms. These stripes also record reversals in Earth's magnetic field, providing a timeline of crustal creation.",
        "subject": "geography",
        "topic": "plate tectonics",
        "grade": "10"
    },
    {
        "text": "A climate zone is a large region of the Earth that has similar patterns of temperature and rainfall throughout the year. The main climate zones are tropical, temperate, polar, arid, and Mediterranean. Where you live on Earth largely determines your local climate zone.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "6"
    },
    {
        "text": "Tropical climate zones are found near the equator, between about 23.5\u00b0N and 23.5\u00b0S latitude. They are very hot and wet all year round, with average temperatures above 18\u00b0C every month. The Amazon rainforest and Congo Basin are examples of areas with tropical climates.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "6"
    },
    {
        "text": "Polar climates are found near the North and South Poles, above about 66.5\u00b0 latitude. These regions are extremely cold with average temperatures below 0\u00b0C for most of the year. Very little precipitation falls, making polar regions technically cold deserts.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "6"
    },
    {
        "text": "Arid and semi-arid climate zones, commonly called deserts, receive less than 250 mm of rainfall per year. Temperatures can vary dramatically between day and night \u2014 the Sahara Desert can reach 50\u00b0C during the day but drop below freezing at night. Deserts cover about one-third of the Earth's land surface.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "7"
    },
    {
        "text": "Latitude \u2014 the distance from the equator \u2014 is the most important factor determining a region's climate zone. Areas near the equator receive the Sun's rays at a more direct angle, concentrating more energy and causing higher temperatures. As you move toward the poles, sunlight hits at a lower angle, spreading energy over a larger area and causing lower temperatures.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "7"
    },
    {
        "text": "Ocean currents play a major role in shaping climate zones. Warm currents such as the Gulf Stream carry tropical water northward and moderate the climate of Western Europe, making it much warmer than other regions at the same latitude. Cold currents, such as the Benguela Current off southwest Africa, cool coastal air and reduce rainfall, contributing to desert conditions.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "7"
    },
    {
        "text": "The Mediterranean climate zone is found on the west coasts of continents at about 30\u201345\u00b0 latitude. It is characterised by hot, dry summers and mild, wet winters. Regions with this climate include the Mediterranean Basin, California, and southwestern Australia, and they support distinctive vegetation such as drought-resistant shrublands (chaparral or maquis).",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "7"
    },
    {
        "text": "Monsoon climates experience dramatic seasonal changes in rainfall driven by shifting wind patterns. During summer, moist winds blow inland from the ocean bringing heavy rains; in winter, dry winds blow from the land outward. South and Southeast Asia depend on the summer monsoon for up to 80% of their annual rainfall, which is critical for agriculture.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "8"
    },
    {
        "text": "Climate zones are closely linked to biomes \u2014 large ecological communities of plants and animals adapted to specific climate conditions. Tropical climate zones support rainforest biomes with exceptional biodiversity. Arid zones support desert biomes with highly specialised drought-adapted species, while temperate zones support grasslands and deciduous forests.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "8"
    },
    {
        "text": "Seasons are caused by the tilt of Earth's axis (23.5\u00b0) as it orbits the Sun, and they affect temperature variation across climate zones. When the Northern Hemisphere is tilted toward the Sun, it experiences summer; at the same time, the Southern Hemisphere experiences winter. Regions near the equator experience little seasonal variation because the Sun angle does not change much throughout the year.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "8"
    },
    {
        "text": "Altitude also modifies climate zones independently of latitude. Temperature decreases by approximately 6.5\u00b0C for every 1,000 m of altitude \u2014 a lapse rate that creates distinct climate bands on mountains. This is why Mount Kilimanjaro in equatorial Tanzania still has a permanent ice cap at its summit above 5,895 m.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "9"
    },
    {
        "text": "The temperate climate zone lies between roughly 35\u00b0 and 65\u00b0 latitude in both hemispheres and has four distinct seasons. Precipitation is relatively evenly distributed throughout the year, and temperatures range from cold winters to warm summers. Most of Europe, China, and North America fall within temperate climate zones.",
        "subject": "geography",
        "topic": "climate zones",
        "grade": "9"
    },
    {
        "text": "A river begins at its source, which is often a spring, lake, or area of high rainfall in upland regions. The area of land drained by a river and all its tributaries is called the drainage basin or catchment area. The boundary between two drainage basins is called a watershed.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "7"
    },
    {
        "text": "Tributaries are smaller streams or rivers that flow into a larger main river, adding to its volume. The point where a tributary meets the main river is called a confluence. The River Thames, for example, receives numerous tributaries including the Cherwell, Kennet, and Wey.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "7"
    },
    {
        "text": "In the upper course of a river, the gradient is steep and the river has high energy. The main process here is vertical erosion, cutting downward into the rock to form a V-shaped valley. Interlocking spurs \u2014 ridges of land that jut into the valley from alternating sides \u2014 are a characteristic landform of the upper course.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "7"
    },
    {
        "text": "Waterfalls form when a river flows over a band of hard, resistant rock underlain by softer rock. The softer rock is eroded more quickly, creating a step and then an overhang of hard rock. Eventually the overhang collapses, and the waterfall retreats upstream, leaving a steep-sided gorge downstream.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "7"
    },
    {
        "text": "In the middle course, the river has more lateral (sideways) energy and begins to meander \u2014 to swing in wide S-shaped bends across a flat valley floor. The outside of each bend experiences more erosion (forming a river cliff), while the inside experiences deposition (forming a slip-off slope or point bar). Over time, meanders migrate across the floodplain.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "8"
    },
    {
        "text": "An oxbow lake forms when the neck of a meander becomes very narrow and the river cuts through it during a flood, taking a straighter course. The old meander loop becomes cut off from the main river, forming a curved, crescent-shaped lake. Over time, the oxbow lake may dry up or become a marsh.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "8"
    },
    {
        "text": "A floodplain is the flat area of land on either side of a river in its middle and lower course, built up from sediment deposited during floods. When a river floods, it loses velocity as it spreads over the floodplain and deposits fine alluvial sediment. This makes floodplains very fertile and many civilisations (such as ancient Egypt) developed on them.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "8"
    },
    {
        "text": "Rivers erode material through four main processes: hydraulic action (force of moving water), abrasion (sediment scraping the riverbed), attrition (sediment pieces colliding and breaking), and solution (chemical dissolution of soluble rock). They transport material by traction (rolling), saltation (bouncing), suspension (carrying fine particles), and solution. The load is deposited when the river's velocity decreases.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "8"
    },
    {
        "text": "In the lower course, the river has a very gentle gradient and carries a large load of fine sediment. The river may split into multiple channels called distributaries as it nears the sea \u2014 this network of channels forms a delta. The Nile Delta in Egypt and the Ganges-Brahmaputra Delta in Bangladesh are two of the world's largest deltas.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "9"
    },
    {
        "text": "A gorge is a narrow, steep-sided valley carved by a river through hard rock, often left behind as a waterfall retreats upstream. Gorges can also form when rivers cut rapidly through rock during periods of uplift. The Fish River Canyon in Namibia \u2014 over 160 km long and up to 550 m deep \u2014 is Africa's largest canyon.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "9"
    },
    {
        "text": "River management strategies include hard engineering (dams, embankments, channelisation) and soft engineering (floodplain zoning, river restoration, afforestation). Hard engineering can protect settlements from flooding but may increase flood risk downstream and damage ecosystems. Soft engineering works with natural processes and is generally more sustainable long-term.",
        "subject": "geography",
        "topic": "rivers and landforms",
        "grade": "9"
    },
    {
        "text": "Population geography studies how people are distributed across the Earth and why. The world population reached 8 billion in November 2022. Population distribution is uneven \u2014 over half of all people live in Asia, and large parts of the world such as the Sahara and Amazon rainforest are almost uninhabited.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "9"
    },
    {
        "text": "The birth rate is the number of live births per 1,000 people per year. The death rate is the number of deaths per 1,000 people per year. When the birth rate exceeds the death rate, the difference is called natural increase and the population grows.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "9"
    },
    {
        "text": "The Demographic Transition Model (DTM) describes how a country's birth and death rates change as it develops economically. In Stage 1 (pre-industrial), both rates are high. By Stage 5 (post-industrial), birth rates may fall below death rates, causing population decline \u2014 a situation seen in countries like Japan and Germany.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "9"
    },
    {
        "text": "Population pyramids are bar charts that show the age and sex structure of a population. A wide base and narrow top indicates a young, fast-growing population typical of developing countries with high birth rates. A near-rectangular or top-heavy pyramid indicates an ageing population with low birth rates, typical of developed countries.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "9"
    },
    {
        "text": "Migration is the movement of people from one place to another. Push factors are reasons that make people leave a place, such as poverty, conflict, or natural disasters. Pull factors attract people to a new location, such as better job opportunities, safety, or higher living standards.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "10"
    },
    {
        "text": "Urbanisation is the increasing proportion of a country's population living in towns and cities. Over 56% of the world's population now lives in urban areas, and this figure is projected to rise to 68% by 2050. Urbanisation is fastest in developing regions of Africa and Asia, driven by rural\u2013urban migration and natural population increase in cities.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "10"
    },
    {
        "text": "Megacities are urban areas with populations exceeding 10 million people. In 1990 there were only 10 megacities; by 2024 there are over 35, including Tokyo (37 million), Delhi (33 million), and Shanghai (29 million). Most megacities are now in developing countries, creating challenges around housing, sanitation, and transport infrastructure.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "10"
    },
    {
        "text": "Overpopulation occurs when a population exceeds the carrying capacity of its environment \u2014 the resources available cannot sustainably support the number of people. Sub-Saharan Africa and parts of South Asia face pressures from rapid population growth outpacing economic development. However, 'overpopulation' is debated: some argue it is not total numbers but overconsumption by wealthy nations that is the real issue.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "10"
    },
    {
        "text": "An ageing population is one with an increasing proportion of elderly people, typically those over 65. This creates economic challenges including a shrinking workforce, higher pension costs, and greater demand for healthcare. Japan has one of the oldest populations globally, with over 29% of its citizens aged 65 or above.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "11"
    },
    {
        "text": "Population policies are government strategies to manage population size. Pro-natalist policies encourage higher birth rates through financial incentives such as France's family benefit system. Anti-natalist policies aim to reduce birth rates; China's one-child policy (1980\u20132015) reduced fertility rates but created a severely skewed sex ratio and now an ageing demographic crisis.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "11"
    },
    {
        "text": "Dependency ratio is a measure comparing the economically active population (aged 15\u201364) to the dependent population (children under 15 and adults over 64). A high dependency ratio strains government finances because a smaller working-age group must support more dependants through taxation. Countries experiencing both an ageing population and falling birth rates face a 'double dependency' challenge.",
        "subject": "geography",
        "topic": "population geography",
        "grade": "11"
    },
    {
        "text": "The greenhouse effect is a natural process in which certain gases in the atmosphere \u2014 including water vapour, carbon dioxide, and methane \u2014 trap heat from the Sun, keeping Earth warm enough to support life. Without the natural greenhouse effect, Earth's average temperature would be about -18\u00b0C instead of +15\u00b0C. Human activities are intensifying this effect by adding extra greenhouse gases.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "9"
    },
    {
        "text": "Global warming refers to the long-term rise in Earth's average surface temperature. Since industrialisation began in the late 1800s, average global temperatures have risen by approximately 1.2\u00b0C. The Intergovernmental Panel on Climate Change (IPCC) warns that exceeding 1.5\u00b0C above pre-industrial levels will cause severe and potentially irreversible impacts.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "9"
    },
    {
        "text": "Rising sea levels are one of the most significant consequences of climate change. They are caused by two main processes: thermal expansion of ocean water as it warms, and the melting of glaciers and ice sheets. Global sea levels have risen about 20 cm since 1900, and the rate is accelerating \u2014 threatening low-lying nations such as Bangladesh and the Maldives.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "9"
    },
    {
        "text": "Climate change is making extreme weather events more frequent and intense. Heatwaves, intense rainfall events, prolonged droughts, and powerful tropical storms are all linked to a warmer atmosphere. The European heatwave of 2003 killed over 70,000 people and is now estimated to be at least five times more likely to occur due to climate change.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "10"
    },
    {
        "text": "Ice loss is a major indicator and amplifier of climate change. The Arctic is warming about four times faster than the global average, causing dramatic sea ice decline and permafrost thaw. As white ice melts and is replaced by darker ocean water, less sunlight is reflected \u2014 a process called ice-albedo feedback that accelerates further warming.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "10"
    },
    {
        "text": "Human activities are the dominant cause of current climate change, primarily through the burning of fossil fuels, deforestation, and agriculture. Natural factors such as volcanic eruptions and solar variation also influence climate but cannot explain the rapid warming observed since 1950. The IPCC states with over 95% confidence that humans are the main cause of recent warming.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "10"
    },
    {
        "text": "The Paris Agreement, adopted in 2015, is an international treaty in which nearly 200 countries pledged to limit global warming to well below 2\u00b0C, ideally 1.5\u00b0C, above pre-industrial levels. Countries submit Nationally Determined Contributions (NDCs) outlining their emission reduction plans. However, current pledges are still insufficient to meet the 1.5\u00b0C target.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "10"
    },
    {
        "text": "A carbon footprint is the total amount of greenhouse gas emissions, expressed in CO2 equivalent, caused directly and indirectly by an individual, organisation, or country. The average global carbon footprint is about 4 tonnes of CO2 per person per year, but the average American footprint is about 16 tonnes. Reducing carbon footprints can involve switching to renewable energy, changing diet, and reducing air travel.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "10"
    },
    {
        "text": "Feedback loops in the climate system can either amplify (positive feedback) or dampen (negative feedback) warming. The melting permafrost feedback is a concerning positive feedback: as permafrost thaws, it releases stored methane and CO2, causing more warming, which thaws more permafrost. These self-reinforcing loops can accelerate climate change beyond what human emissions alone would cause.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "11"
    },
    {
        "text": "Tipping points are thresholds in the climate system beyond which change becomes self-sustaining and potentially irreversible. Scientists have identified potential tipping points including the collapse of the West Antarctic Ice Sheet, dieback of the Amazon rainforest, and disruption of the Atlantic Meridional Overturning Circulation (AMOC). Crossing multiple tipping points could trigger cascading effects across Earth's systems.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "11"
    },
    {
        "text": "Solutions to climate change fall into two categories: mitigation (reducing emissions) and adaptation (adjusting to changes already occurring). Mitigation strategies include transitioning to renewable energy, increasing energy efficiency, and protecting forests. Adaptation strategies include building coastal defences, developing drought-resistant crops, and redesigning cities to cope with extreme heat.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "11"
    },
    {
        "text": "Climate justice highlights that the countries and communities least responsible for greenhouse gas emissions are often the most vulnerable to climate change impacts. Small island developing states and sub-Saharan Africa produce a tiny fraction of global emissions yet face existential threats from sea-level rise and drought. This inequity has become a central issue in international climate negotiations, with calls for wealthy nations to fund 'loss and damage' payments.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "12"
    },
    {
        "text": "Geoengineering refers to large-scale technological interventions designed to counteract climate change. Solar radiation management (SRM) proposals, such as injecting reflective aerosols into the stratosphere, could reduce incoming sunlight and cool the planet quickly. However, SRM does not address ocean acidification, carries risks of disrupting monsoon patterns, and raises profound ethical questions about who decides to alter the global climate.",
        "subject": "geography",
        "topic": "climate change",
        "grade": "12"
    }
]

#till here  




    {
        "text": "Demography is the study of human populations — their size, structure, "
                "and change over time. Population change is determined by birth rates, "
                "death rates, and migration. The natural population change equals "
                "births minus deaths. Net migration equals immigrants minus emigrants. "
                "Countries experiencing high birth rates, declining death rates, and "
                "net immigration are growing rapidly.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "8",
    },
    {
        "text": "The Demographic Transition Model (DTM) shows how a country's birth and "
                "death rates change as it develops economically. In Stage 1, both rates "
                "are high. In Stage 2, death rates fall (better medicine, food, sanitation) "
                "but birth rates remain high, causing rapid population growth. In Stage 3, "
                "birth rates begin to fall. In Stage 4, both rates are low and the "
                "population stabilises. Some add a Stage 5 where birth rates fall below "
                "death rates, causing population decline.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "8",
    },
    {
        "text": "A population pyramid is a paired bar chart showing the age and sex "
                "structure of a population. A wide-based pyramid indicates a young, "
                "fast-growing population with high birth rates, typical of developing "
                "countries. A near-vertical or top-heavy pyramid indicates an ageing "
                "population with low birth rates, typical of developed countries such "
                "as Germany, Japan, and South Korea.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "8",
    },
    {
        "text": "The world population reached 8 billion in November 2022. Population "
                "growth is concentrated in sub-Saharan Africa and South Asia. The UN "
                "projects world population will reach 9.7 billion by 2050 and peak at "
                "around 10.4 billion in the 2080s before potentially stabilising or "
                "declining. The most important driver of long-term population growth "
                "is now sub-Saharan Africa, where fertility rates remain high.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "9",
    },
    {
        "text": "An ageing population has an increasing proportion of older people, "
                "typically those aged 65 or over. It is caused by falling birth rates "
                "and increasing life expectancy. Japan has the world's oldest population, "
                "with over 29% of its citizens aged 65+. Ageing populations create "
                "economic challenges: a smaller working-age group must fund pensions "
                "and healthcare for a growing elderly population, increasing the "
                "dependency ratio.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "9",
    },
    {
        "text": "Population policies aim to manage population growth. Anti-natalist "
                "policies discourage births — China's one-child policy (1980–2015) "
                "used financial penalties and other measures to reduce birth rates. "
                "It succeeded in slowing growth but created a severely skewed sex ratio "
                "(due to a cultural preference for boys) and now a rapid ageing crisis. "
                "Pro-natalist policies in countries like France, Sweden, and South Korea "
                "offer financial incentives and parental leave to encourage childbearing.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "9",
    },
    {
        "text": "Migration can be classified by distance (internal/international), "
                "by cause (economic/forced/voluntary), or by permanence (permanent/temporary). "
                "Lee's push-pull theory identifies factors that push people away from "
                "their origin and pull them toward a destination. Intervening obstacles "
                "— cost, distance, language, legal barriers — reduce migration flows. "
                "Intervening opportunities may divert migrants to closer destinations.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "9",
    },
    {
        "text": "The global refugee crisis reached a record 117 million forcibly displaced "
                "people by mid-2024. Major sources of displacement include Sudan, Syria, "
                "Ukraine, Afghanistan, and Democratic Republic of Congo. The 1951 Refugee "
                "Convention defines a refugee as someone who cannot return home due to "
                "a well-founded fear of persecution based on race, religion, nationality, "
                "political opinion, or membership of a social group.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "10",
    },
    {
        "text": "Remittances — money sent home by migrants to their families — are a "
                "vital source of income for many developing countries. Global remittance "
                "flows to low- and middle-income countries exceeded $669 billion in 2023, "
                "more than three times the amount of official development aid. Countries "
                "such as Tajikistan, Tonga, and Somalia receive remittances equivalent "
                "to 30–50% of their GDP, making them highly dependent on diaspora income.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "10",
    },
    {
        "text": "Brain drain refers to the emigration of highly educated or skilled people "
                "from developing countries to wealthier ones in search of better "
                "opportunities and pay. It deprives sending countries of the human "
                "capital they need for development. Sub-Saharan Africa loses a significant "
                "proportion of its trained doctors and nurses to emigration. Brain gain "
                "or brain circulation describes how some migrants return home with new "
                "skills and investment, benefiting the sending country.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "10",
    },
    {
        "text": "Climate migration — movement driven by environmental change — is an "
                "emerging and growing phenomenon. Rising sea levels, extreme weather, "
                "droughts, and desertification are displacing communities. The World Bank "
                "estimates that climate change could force 216 million people to migrate "
                "within their own countries by 2050 in a business-as-usual scenario. "
                "Climate migrants currently have no specific legal protection under "
                "international refugee law.",
        "subject": "geography",
        "topic": "demographic change and migration",
        "grade": "11",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # TOPIC: geopolitics and borders
    # ══════════════════════════════════════════════════════════════════════════
    {
        "text": "Geopolitics is the study of how geography — location, resources, climate, "
                "and physical features — shapes political power and international relations. "
                "A country's geopolitical position influences its security, trade, and "
                "foreign policy. Russia's vast territory spanning two continents, the "
                "USA's protection by two oceans, and China's long Pacific coastline are "
                "all geopolitically significant.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "9",
    },
    {
        "text": "A state is a territory with defined borders, a permanent population, "
                "a government, and the capacity to enter into relations with other states. "
                "There are currently 195 recognised sovereign states. A nation is a "
                "group of people sharing a common identity — language, culture, or history. "
                "A nation-state is where state borders closely align with national identity. "
                "Many states contain multiple nations; some nations are spread across "
                "multiple states.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "9",
    },
    {
        "text": "International borders are the lines that separate sovereign states. "
                "Some borders follow natural features like rivers and mountain ranges "
                "(physical boundaries). Others are geometric lines drawn without regard "
                "to natural features or cultural divisions. Many African borders were "
                "drawn by European colonial powers at the Berlin Conference (1884–85), "
                "often cutting across ethnic and tribal territories — a major source of "
                "post-independence conflict.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "9",
    },
    {
        "text": "Disputed territories are areas whose sovereignty is contested between "
                "two or more states. Major examples include Kashmir (India, Pakistan, "
                "and China), the South China Sea (China, Vietnam, Philippines, Malaysia, "
                "Brunei), and the Golan Heights (Israel and Syria). Territorial disputes "
                "are often rooted in history, ethnicity, strategic value, or natural "
                "resources. The UN Convention on the Law of the Sea (UNCLOS) provides "
                "a framework for resolving maritime disputes.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "9",
    },
    {
        "text": "The South China Sea is one of the world's most strategically important "
                "bodies of water, through which about $3.5 trillion in trade passes "
                "annually. China claims about 90% of the South China Sea based on a "
                "'nine-dash line' that other regional states and a 2016 international "
                "tribunal reject. The area contains significant fish stocks, oil, and gas "
                "reserves, and has been the site of island-building and military "
                "installations.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "10",
    },
    {
        "text": "Resource geopolitics describes how competition for natural resources "
                "— oil, gas, water, minerals — shapes international relations and conflict. "
                "The Middle East's oil reserves have made it a region of intense great "
                "power interest since the early 20th century. The Democratic Republic "
                "of Congo's vast deposits of cobalt (essential for batteries) are linked "
                "to prolonged conflict. Rare earth elements, largely mined in China, "
                "are critical for electronics and renewable energy technology.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "10",
    },
    {
        "text": "Supranational organisations are bodies that operate above the level of "
                "individual states. The United Nations (UN) promotes international peace, "
                "security, and human rights, with 193 member states. The European Union "
                "(EU) is a deeper form of integration — members share a single market, "
                "many share a currency (euro), and EU law takes precedence over national "
                "law in many areas. NATO is a military alliance of 32 countries "
                "guaranteeing collective defence.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "10",
    },
    {
        "text": "The concept of geopolitical spheres of influence describes regions where "
                "a major power exerts dominant political, economic, or military control. "
                "During the Cold War, the USA and USSR divided much of the world into "
                "competing spheres. China's Belt and Road Initiative — investing in "
                "infrastructure across Asia, Africa, and Europe — is seen by many analysts "
                "as an attempt to extend China's geopolitical influence into the 21st "
                "century.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "10",
    },
    {
        "text": "Heartland theory, proposed by Halford Mackinder in 1904, argued that "
                "whoever controlled the 'Heartland' of Eurasia (the interior of Russia "
                "and Central Asia) could dominate the World Island (Eurasia + Africa) "
                "and thereby the world. Sea power theorist Alfred Mahan argued instead "
                "that global dominance came from controlling sea lanes. These classical "
                "geopolitical theories influenced 20th-century strategy and remain "
                "debated by international relations scholars.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "11",
    },
    {
        "text": "Arctic geopolitics is increasingly important as climate change melts "
                "sea ice, opening new shipping routes and revealing accessible resource "
                "deposits. The Arctic Council (8 Arctic states including Russia, USA, "
                "Canada, and Norway) manages cooperation. Russia, Canada, Denmark, "
                "and Norway have overlapping territorial claims to the Arctic seabed "
                "under UNCLOS. Russia has dramatically increased its Arctic military "
                "presence, including reopening Soviet-era military bases.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "11",
    },
    {
        "text": "Deglobalisation and a return to geopolitical competition between major "
                "powers — particularly the USA and China — is reshaping the international "
                "order. The rules-based international system built after 1945 faces "
                "challenges from rising nationalism, great-power rivalry, and the weaponisation "
                "of economic interdependence (trade wars, sanctions, technology restrictions). "
                "Russia's invasion of Ukraine in 2022 marked a sharp escalation of "
                "geopolitical competition in Europe.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "12",
    },
    {
        "text": "Water diplomacy is emerging as a critical area of geopolitics as freshwater "
                "scarcity intensifies. About 276 transboundary river basins are shared by "
                "two or more countries. The Nile Basin is shared by 11 nations; tensions "
                "between Egypt, Sudan, and Ethiopia over the Grand Ethiopian Renaissance "
                "Dam threaten conflict. The Mekong River Commission manages disputes "
                "among Cambodia, Laos, Thailand, and Vietnam. Water wars are considered "
                "increasingly plausible as aquifers are depleted.",
        "subject": "geography",
        "topic": "geopolitics and borders",
        "grade": "12",
    },
]


def get_documents():
    """Return all documents as a list of dicts."""
    return GEOGRAPHY_EXTENDED_V3


def get_texts_and_metadatas():
    """Return texts and metadata dicts suitable for a vector store."""
    texts = [doc["text"] for doc in GEOGRAPHY_EXTENDED_V3]
    metadatas = [
        {
            "subject": doc["subject"],
            "topic": doc["topic"],
            "grade": doc["grade"],
        }
        for doc in GEOGRAPHY_EXTENDED_V3
    ]
    return texts, metadatas


if __name__ == "__main__":
    import collections

    topic_counts = collections.Counter(d["topic"] for d in GEOGRAPHY_EXTENDED_V3)
    grade_counts = collections.Counter(d["grade"] for d in GEOGRAPHY_EXTENDED_V3)

    print(f"Total documents     : {len(GEOGRAPHY_EXTENDED_V3)}")
    print(f"Unique topics       : {len(topic_counts)}")
    print()
    print("Documents per topic:")
    for topic, count in sorted(topic_counts.items()):
        status = "OK  " if 10 <= count <= 15 else "WARN"
        print(f"  [{status}] {topic:<50} {count} docs")
    print()
    print("Documents per grade:")
    for g in sorted(grade_counts, key=int):
        print(f"  Grade {g}: {grade_counts[g]} docs")