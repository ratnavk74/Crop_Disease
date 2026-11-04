"""
Agronomic Disease Advisory Knowledge Base
Provides in-depth diagnostic data including:
- What disease was identified
- Why it happened (environmental & climatic drivers)
- Detailed Causes (pathogens, spores, vectors, transmission)
- In-depth Symptoms (early & advanced stages)
- Curative Treatment (chemical fungicides + organic/bio remedies)
- Comprehensive Prevention (resistant varieties, cultural methods, crop rotation)
- Voice narration scripts for farmer accessibility
"""

DISEASE_INFO = {
    'Wheat_Healthy': {
        'crop': 'Wheat (Triticum aestivum)',
        'disease_name': 'Healthy Wheat Crop',
        'display_name': 'Wheat - Healthy Foliage',
        'pathogen': 'None (Healthy vegetative growth)',
        'category': 'Healthy Crop',
        'severity': 'None / Healthy',
        'severity_level': 'Low',
        'affected_area_estimate': '0%',
        'why_it_happened': (
            'The crop is thriving under optimal microclimatic conditions: balanced soil fertility '
            '(adequate nitrogen, phosphorus, potassium, and zinc), clean seed stock, timely crown root '
            'initiation (CRI) irrigation, and lack of virulent pathogen inoculum or prolonged leaf moisture.'
        ),
        'cause': 'Healthy crop. No infectious pathogens or abiotic stress factors detected.',
        'causes': (
            'Optimal agronomic management: disease-free certified foundation seed, well-drained soil, '
            'proper sowing depth (4-5 cm), and absence of pathogen spore clouds from neighboring fields.'
        ),
        'symptoms': (
            'Lush green leaf blades with uniform chlorophyll distribution; smooth leaf margins; '
            'clean stems with no lesions, rust pustules, powdery mold, or chlorotic streaking.'
        ),
        'treatment': (
            'Maintain regular irrigation at critical growth stages (Tillering, Jointing, Flowering, Grain filling). '
            'Apply scheduled top-dressing of nitrogen/urea as per soil test recommendations.'
        ),
        'treatment_details': {
            'chemical': 'No chemical fungicide required.',
            'organic': 'Optional foliar spray of seaweed extract (2 ml/L) or Panchagavya (3%) at tillering to enhance grain weight.',
            'immediate_action': 'Continue normal crop monitoring and weed suppression.'
        },
        'prevention': (
            'Use certified rust-resistant seeds (e.g., HD-3086, PBW-550, WH-1105). '
            'Follow recommended crop rotation with legumes and monitor weekly during heading stage.'
        ),
        'prevention_details': {
            'resistant_varieties': 'HD-3086, PBW-550, WH-1105, DBW-187 (Karan Vandana), Raj-4037.',
            'cultural_practices': 'Maintain standard plant spacing (20-22.5 cm between rows); avoid water stagnation.',
            'soil_nutrition': 'Balanced N:P:K ratio (120:60:40 kg/ha) with 25 kg/ha Zinc Sulphate basal application.'
        },
        'voice_en': 'Good news! Your wheat crop is completely healthy. Continue normal irrigation and scheduled fertilizer applications.',
        'voice_hi': 'बधाई हो! आपकी गेहूं की फसल पूरी तरह स्वस्थ है। सामान्य सिंचाई और खाद प्रबंधन जारी रखें।',
        'voice_kn': 'ಉತ್ತಮ ಸುದ್ದಿ! ನಿಮ್ಮ ಗೋಧಿ ಬೆಳೆ ಸಂಪೂರ್ಣ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಸಾಮಾನ್ಯ ನೀರಾವರಿ ಮತ್ತು ಪೋಷಕಾಂಶಗಳ ನಿರ್ವಹಣೆಯನ್ನು ಮುಂದುವರಿಸಿ.'
    },

    'Maize_Healthy': {
        'crop': 'Maize / Corn (Zea mays)',
        'disease_name': 'Healthy Maize Crop',
        'display_name': 'Maize - Healthy Foliage',
        'pathogen': 'None (Healthy vegetative growth)',
        'category': 'Healthy Crop',
        'severity': 'None / Healthy',
        'severity_level': 'Low',
        'affected_area_estimate': '0%',
        'why_it_happened': (
            'Favorable growth conditions: well-aerated fertile loam soil, optimal daytime temperatures '
            '(21°C - 30°C), balanced organic matter, and absence of fungal blights or foliar pathogens.'
        ),
        'cause': 'Healthy crop. Vigorous leaf tissue with active photosynthesis.',
        'causes': (
            'High-vigor certified hybrid seed, adequate plant spacing allowing solar penetration, '
            'and proper nutrient replenishment without water-logging stress.'
        ),
        'symptoms': (
            'Broad, vibrant green leaves with strong midribs; intact epidermal cuticle; '
            'no necrotic lesions, rust pustules, tar spots, or leaf blight streaks.'
        ),
        'treatment': (
            'Maintain proper nutrients and irrigation. Apply split nitrogen doses at knee-high and tasseling stages.'
        ),
        'treatment_details': {
            'chemical': 'No chemical fungicides needed.',
            'organic': 'Neem cake application (200 kg/acre) during earthing up to enhance soil immunity and deter root pests.',
            'immediate_action': 'Ensure timely weeding and soil aeration around plant bases.'
        },
        'prevention': (
            'Regular field inspection. Use high-yield disease-tolerant hybrids and maintain clean field borders.'
        ),
        'prevention_details': {
            'resistant_varieties': 'DHM-117, CP-818, Dekalb 9108, Pioneer P3396, NK-6240.',
            'cultural_practices': 'Plant at 60 cm row-to-row and 20 cm plant-to-plant spacing to prevent dense microclimates.',
            'soil_nutrition': 'Balanced N:P:K (150:75:40 kg/ha) with FYM (Farm Yard Manure) @ 10 tonnes/ha.'
        },
        'voice_en': 'Your maize crop is healthy and vigorous. Maintain regular irrigation and weed control.',
        'voice_hi': 'आपकी मक्के की फसल एकदम स्वस्थ है। उचित सिंचाई और खरपतवार नियंत्रण जारी रखें।',
        'voice_kn': 'ನಿಮ್ಮ ಮೆಕ್ಕೆಜೋಳದ ಬೆಳೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ ಮತ್ತು ಉತ್ತಮವಾಗಿ ಬೆಳೆಯುತ್ತಿದೆ. ನಿಯಮಿತ ನೀರಾವರಿಯನ್ನು ಮುಂದುವರಿಸಿ.'
    },

    'Wheat_BlackRust': {
        'crop': 'Wheat (Triticum aestivum)',
        'disease_name': 'Black Rust (Stem Rust)',
        'display_name': 'Wheat - Black (Stem) Rust',
        'pathogen': 'Puccinia graminis f. sp. tritici (Obligate biotrophic fungus)',
        'category': 'Fungal Foliar & Culm Disease',
        'severity': 'Critical / Urgent',
        'severity_level': 'High',
        'affected_area_estimate': '35% - 55%',
        'why_it_happened': (
            'Why it happens: Black stem rust explodes when warm daytime temperatures (20°C to 30°C) '
            'coincide with high relative humidity and 6-8 hours of free moisture or morning dew on plant surfaces. '
            'Inoculum is carried thousands of kilometers across regional corridors via high-altitude wind currents '
            '(often originating from southern hills or alternate Berberis hosts).'
        ),
        'cause': (
            'Severe fungal infection caused by Puccinia graminis f. sp. tritici, invading stems and leaf sheaths.'
        ),
        'causes': (
            'Microscopic urediniospores carried by turbulent wind currents; penetration occurs through open stomata '
            'when moisture films exist. The fungal mycelium aggressively colonizes vascular bundle tissues, '
            'rupturing the plant epidermis and causing devastating water loss, nutrient theft, and lodging.'
        ),
        'symptoms': (
            'Large, elongated reddish-brown to dark chocolate-black pustules (uredinia) that rupture the epidermis '
            'leaving shredded tissue edges; primarily attacks stems, leaf sheaths, and glumes; in severe stages, '
            'stems turn brittle and break easily (lodging), leading to shriveled or empty grain heads.'
        ),
        'treatment': (
            'Apply systemic triazole fungicides immediately: Propiconazole 25% EC (Tilt) @ 1 ml/L or '
            'Tebuconazole 25.9% EC @ 1.25 ml/L. Ensure complete spray coverage on stems.'
        ),
        'treatment_details': {
            'chemical': (
                'Spray Propiconazole 25% EC (Tilt) @ 1 ml/L (200 ml in 200 L water/acre) or '
                'Azoxystrobin 18.2% + Difenoconazole 11.4% SC (Amistar Top) @ 1 ml/L. '
                'Repeat spray after 12-14 days if rust pustules persist.'
            ),
            'organic': (
                'Bio-control: Foliar spray of Trichoderma harzianum @ 5 g/L with 1% jaggery solution. '
                'Spray fermented butter-milk (sour buttermilk diluted 1:10 with water) to check early spore proliferation.'
            ),
            'immediate_action': (
                'ACT WITHIN 24-48 HOURS: Black stem rust can cause up to 70% yield loss in susceptible wheat if left untreated.'
            )
        },
        'prevention': (
            'Use resistant wheat varieties (e.g., HD-3086, DBW-187). Practice early sowing and eliminate alternate weed hosts.'
        ),
        'prevention_details': {
            'resistant_varieties': 'HD-3086, DBW-187 (Karan Vandana), WH-1105, GW-322, MACS-6222.',
            'cultural_practices': (
                'Early winter sowing (first fortnight of November) allows grain filling before temperatures rise to rust-favorable 25°C. '
                'Eradicate wild barberry (Berberis vulgaris) bushes near field perimeters.'
            ),
            'soil_nutrition': (
                'Avoid excessive nitrogen top-dressing which creates succulent stem tissue. '
                'Apply Muriate of Potash (MOP @ 40 kg/ha) to thicken epidermal cell walls.'
            )
        },
        'voice_en': (
            'Alert: Wheat Black Stem Rust detected with high severity. '
            'Immediately spray Propiconazole at 1 ml per liter of water on stems and leaves within 24 hours.'
        ),
        'voice_hi': (
            'चेतावनी! गेहूं में काला तना रतुआ (ब्लैक रस्ट) पाया गया है। '
            'गंभीर नुकसान से बचने के लिए तुरंत प्रोपिकोनाजोल 1 मिली प्रति लीटर पानी में मिलाकर तनों और पत्तियों पर छिड़कें।'
        ),
        'voice_kn': (
            'ಎಚ್ಚರಿಕೆ! ಗೋಧಿಯಲ್ಲಿ ಕಪ್ಪು ಕಾಂಡದ ತುಕ್ಕು ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. '
            'ತಕ್ಷಣ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ 1 ಮಿಲಿ ಪ್ರೊಪಿಕೊನಜೋಲ್ ಬೆರೆಸಿ ಕಾಂಡಗಳಿಗೆ ತಲುಪುವಂತೆ ಸಿಂಪಡಿಸಿ.'
        )
    },

    'Wheat_BrownRust': {
        'crop': 'Wheat (Triticum aestivum)',
        'disease_name': 'Brown Rust (Leaf Rust)',
        'display_name': 'Wheat - Brown (Leaf) Rust',
        'pathogen': 'Puccinia triticina (Fungal obligate parasite)',
        'category': 'Fungal Foliar Disease',
        'severity': 'Moderate / Treat Soon',
        'severity_level': 'Medium',
        'affected_area_estimate': '20% - 35%',
        'why_it_happened': (
            'Why it happens: Brown rust thrives in moderate temperatures (18°C to 25°C) coupled with persistent '
            'overnight dew or high relative humidity (>85%). It is the most widespread rust of wheat, '
            'occurring during early spring as daytime temperatures begin warming.'
        ),
        'cause': (
            'Fungal disease caused by Puccinia triticina, targeting leaf blades and interfering with photosynthesis.'
        ),
        'causes': (
            'Airborne urediniospores blown from infected regions. Spores land on leaf surfaces and germinate within '
            '3-4 hours of wetness, pushing infection pegs into leaf mesophyll cells and draining plant starches.'
        ),
        'symptoms': (
            'Small, circular to oval, bright orange-brown to cinnamon pustules scattered randomly across the upper leaf surface; '
            'pustules release powdery brown spores when wiped with fingers; in advanced stages, leaves turn prematurely yellow and wither.'
        ),
        'treatment': (
            'Use fungicides like Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole 25.9% EC @ 1 ml/L. '
            'Foliar spray with Mancozeb 75% WP @ 2.5 g/L if disease is in early phase.'
        ),
        'treatment_details': {
            'chemical': (
                'First spray: Propiconazole 25% EC @ 1 ml/L or Tebuconazole 25.9% EC @ 1 ml/L. '
                'Alternative: Mancozeb 75% WP @ 2.5 g/L for protective barrier. Coverage must include both sides of flag leaves.'
            ),
            'organic': (
                'Spray cold-pressed Neem oil (Azadirachtin 3000 ppm) @ 4 ml/L with liquid soap emulsifier. '
                'Apply Pseudomonas fluorescens foliar spray @ 5 g/L.'
            ),
            'immediate_action': (
                'Spray within 48-72 hours, especially protecting the upper flag leaf which contributes 60% of grain filling.'
            )
        },
        'prevention': (
            'Use certified seeds and rust-resistant varieties. Avoid delayed sowing and excessive nitrogen fertilizer.'
        ),
        'prevention_details': {
            'resistant_varieties': 'PBW-502, HD-2967, WH-1105, DBW-222, Raj-3765.',
            'cultural_practices': 'Destroy self-sown volunteer wheat plants during the fallow summer months.',
            'soil_nutrition': 'Balanced NPK fertigation with supplementary zinc and sulfur.'
        },
        'voice_en': (
            'Wheat Brown Leaf Rust detected with moderate severity. '
            'Apply Propiconazole or Tebuconazole at 1 ml per liter of water to protect your flag leaves.'
        ),
        'voice_hi': (
            'गेहूं में भूरा रतुआ (ब्राउन लीफ रस्ट) पाया गया है। '
            'ध्वज पत्ती को सुरक्षित रखने के लिए 1 मिली प्रोपिकोनाजोल प्रति लीटर पानी में मिलाकर छिड़काव करें।'
        ),
        'voice_kn': (
            'ಗೋಧಿಯಲ್ಲಿ ಕಂದು ಎಲೆ ತುಕ್ಕು ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. '
            'ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ 1 ಮಿಲಿ ಟೆಬುಕೊನಜೋಲ್ ಅಥವಾ ಪ್ರೊಪಿಕೊನಜೋಲ್ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.'
        )
    },

    'Wheat_YellowRust': {
        'crop': 'Wheat (Triticum aestivum)',
        'disease_name': 'Yellow Rust (Stripe Rust)',
        'display_name': 'Wheat - Yellow (Stripe) Rust',
        'pathogen': 'Puccinia striiformis f. sp. tritici',
        'category': 'Fungal Foliar Disease',
        'severity': 'Critical / Highly Aggressive',
        'severity_level': 'High',
        'affected_area_estimate': '40% - 60%',
        'why_it_happened': (
            'Why it happens: Stripe rust thrives under cool and moist weather conditions (temperatures between 9°C and 15°C) '
            'with persistent morning fog or continuous dew. It spreads with ferocious speed across northern plains and valleys '
            'during winter months, capable of completely defoliating fields if unmanaged.'
        ),
        'cause': (
            'Aggressive fungal infection caused by Puccinia striiformis f. sp. tritici, characterized by parallel stripe pustules.'
        ),
        'causes': (
            'Windborne spores transported over sub-Himalayan and plain belts. The fungus specifically colonizes leaf veins, '
            'forming continuous linear rows of yellow urediniospores that resemble stitches from a sewing machine.'
        ),
        'symptoms': (
            'Vivid yellow to lemon-orange pustules arranged in distinct, continuous parallel stripes along leaf veins; '
            'chlorosis quickly develops between stripes; leaves dry up and exhibit scorched appearance; '
            'grain development stops, causing severe yield collapse.'
        ),
        'treatment': (
            'Apply suitable triazole fungicides immediately: Propiconazole 25% EC (Tilt) @ 1 ml/L or '
            'Nativo (Trifloxystrobin 25% + Tebuconazole 50% WG) @ 0.6 g/L.'
        ),
        'treatment_details': {
            'chemical': (
                'Immediate foliar application: Propiconazole 25% EC @ 1 ml/L (200 ml in 200 L water/acre) or '
                'Nativo 75 WG @ 120 g/acre or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L. '
                'Repeat after 10-12 days if weather remains overcast and cool.'
            ),
            'organic': (
                'Emergency bio-treatment: Spray Trichoderma viride @ 5 g/L with 2 ml/L adhesive sticker; '
                'supplement with garlic-chilli bio-extract to suppress active spore dispersal.'
            ),
            'immediate_action': (
                'EMERGENCY: Spray within 24 hours of first spot detection! Delay of one week can cause 50-80% crop failure.'
            )
        },
        'prevention': (
            'Avoid excessive evening irrigation, plant resistant varieties (HD-3086, DBW-187), and practice field sanitation.'
        ),
        'prevention_details': {
            'resistant_varieties': 'HD-3086, DBW-187, DBW-303, PBW-725, HD-3226.',
            'cultural_practices': (
                'Avoid delayed sowing; do not apply irrigation on foggy or cloudy afternoons; '
                'maintain wide buffer strips between fields.'
            ),
            'soil_nutrition': 'Split nitrogen applications; avoid excess urea in late stages which increases plant tenderness.'
        },
        'voice_en': (
            'Critical Alert: Wheat Yellow Stripe Rust detected. '
            'This fungus spreads rapidly in cool weather. Spray Propiconazole or Nativo immediately within 24 hours.'
        ),
        'voice_hi': (
            'अति गंभीर चेतावनी! गेहूं में पीला रतुआ (येलो स्ट्राइप रस्ट) लगा है। '
            'यह ठंडे मौसम में बहुत तेजी से फैलता है। तुरंत 24 घंटे के अंदर प्रोपिकोनाजोल या नेटिवो का छिड़काव करें।'
        ),
        'voice_kn': (
            'ತುರ್ತು ಎಚ್ಚರಿಕೆ! ಗೋಧಿಯಲ್ಲಿ ಹಳದಿ ಪಟ್ಟೆ ತುಕ್ಕು ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. '
            'ತಕ್ಷಣ 24 ಗಂಟೆಯೊಳಗೆ ಪ್ರೊಪಿಕೊನಜೋಲ್ ಅಥವಾ ನ್ಯಾಟಿವೊ ಸಿಂಪಡಿಸಿ ಬೆಳೆ ರಕ್ಷಿಸಿ.'
        )
    },

    'Maize_Common_Rust': {
        'crop': 'Maize / Corn (Zea mays)',
        'disease_name': 'Common Rust of Maize',
        'display_name': 'Maize - Common Rust',
        'pathogen': 'Puccinia sorghi (Fungal obligate biotroph)',
        'category': 'Fungal Foliar Disease',
        'severity': 'Moderate / Manage Promptly',
        'severity_level': 'Medium',
        'affected_area_estimate': '22% - 38%',
        'why_it_happened': (
            'Why it happens: Common rust of maize develops rapidly when cool to moderate temperatures (16°C to 24°C) '
            'are paired with high relative humidity (>95%) and prolonged dew periods (overnight dews of 6+ hours). '
            'Often strikes post-monsoon or early kharif crops during cloudy weather.'
        ),
        'cause': (
            'Fungal infection caused by Puccinia sorghi, producing pustules on both upper and lower leaf surfaces.'
        ),
        'causes': (
            'Urediniospores carried by high winds from warmer southern breeding grounds or alternate wood sorrel (Oxalis) hosts. '
            'Spores germinate on wet foliage and directly penetrate leaf stomatal openings.'
        ),
        'symptoms': (
            'Small, circular to elongated, golden-brown to cinnamon-brown pustules scattered across both upper and lower leaf surfaces; '
            'unlike southern rust, pustules appear on both leaf sides; pustules turn brownish-black late in the season as teliospores form; '
            'leaves turn chlorotic, dry up from tips, and reduce photosynthesis.'
        ),
        'treatment': (
            'Apply fungicides such as Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L. '
            'Propiconazole 25% EC @ 1 ml/L is also highly effective.'
        ),
        'treatment_details': {
            'chemical': (
                'Spray Mancozeb 75% WP @ 2.5 g/L (Indofil M-45 @ 500 g/acre) or Azoxystrobin + Difenoconazole @ 1 ml/L '
                'or Propiconazole 25% EC @ 1 ml/L. Ensure deep spray penetration into the plant canopy.'
            ),
            'organic': (
                'Spray cold-pressed Neem oil (10,000 ppm) @ 3 ml/L or foliar application of bio-agent Bacillus subtilis @ 5 g/L. '
                'Remove and burn severely infected lower leaves.'
            ),
            'immediate_action': (
                'Spray when pustules first appear on upper leaves before silking stage to protect ear formation.'
            )
        },
        'prevention': (
            'Use resistant maize hybrids, maintain proper plant spacing, and destroy infected crop residues after harvest.'
        ),
        'prevention_details': {
            'resistant_varieties': 'DHM-117, HQPM-1, Bio-9681, PAC-740, Pioneer 30R77.',
            'cultural_practices': (
                'Maintain recommended spacing (60 x 20 cm) for air flow. Avoid sprinkler irrigation during evening hours.'
            ),
            'soil_nutrition': 'Balanced NPK fertigation with potash to boost leaf structural strength.'
        },
        'voice_en': (
            'Common Rust detected on maize leaves. '
            'Apply Mancozeb or Azoxystrobin fungicide promptly to prevent spread to developing corn ears.'
        ),
        'voice_hi': (
            'मक्के में कॉमन रस्ट (तुलासिता रतुआ) पाया गया है। '
            'रोग को भुट्टे तक फैलने से रोकने के लिए मैन्कोजेब या प्रोपिकोनाजोल का छिड़काव करें।'
        ),
        'voice_kn': (
            'ಮೆಕ್ಕೆಜೋಳದಲ್ಲಿ ಸಾಮಾನ್ಯ ತುಕ್ಕು ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. '
            'ತೆನೆಗಳಿಗೆ ಹರಡುವುದನ್ನು ತಡೆಯಲು ಮ್ಯಾಂಕೋಜೆಬ್ ಅಥವಾ ಪ್ರೊಪಿಕೊನಜೋಲ್ ಸಿಂಪಡಿಸಿ.'
        )
    },

    'Maize_Blight': {
        'crop': 'Maize / Corn (Zea mays)',
        'disease_name': 'Northern Corn Leaf Blight (NCLB) / Turcicum Leaf Blight',
        'display_name': 'Maize - Northern Leaf Blight',
        'pathogen': 'Exserohilum turcicum (syn. Helminthosporium turcicum)',
        'category': 'Destructive Fungal Blight',
        'severity': 'Critical / High Destruction Risk',
        'severity_level': 'High',
        'affected_area_estimate': '30% - 50%',
        'why_it_happened': (
            'Why it happens: Northern corn leaf blight explodes during warm, highly humid weather (18°C to 27°C) '
            'accompanied by heavy dews, frequent rain showers, and overcast days. The pathogen overwinters and survives '
            'in infected corn stubble left in the field from the prior season.'
        ),
        'cause': (
            'Severe fungal disease caused by Exserohilum turcicum, producing massive cigar-shaped necrotic lesions.'
        ),
        'causes': (
            'Conidia (spores) produced on infected crop debris in the soil are splashed by rain onto lower leaves. '
            'Secondary spread occurs when wind blows conidia onto upper leaves. The fungus enters through stomata or directly '
            'dissolves the leaf cuticle using cutinase enzymes, causing extensive tissue death.'
        ),
        'symptoms': (
            'Characteristic long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 to 15 cm in length); '
            'lesions develop dark olive-green fuzzy fungal spore mats in damp weather; '
            'individual lesions rapidly merge together, completely blighting whole leaves and giving a scorched field appearance; '
            'grain weight and ear fill are severely reduced.'
        ),
        'treatment': (
            'Apply appropriate systemic and contact fungicides: Mancozeb 75% WP @ 2.5 g/L or '
            'Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L or Tebuconazole 25.9% EC @ 1.25 ml/L.'
        ),
        'treatment_details': {
            'chemical': (
                'Spray Azoxystrobin + Difenoconazole @ 1 ml/L (200 ml/acre) or Mancozeb 75% WP @ 2.5 g/L or '
                'Pyraclostrobin 20% WG @ 1 g/L. Repeat spray at 10-14 day intervals if humid rainy conditions persist.'
            ),
            'organic': (
                'Spray Trichoderma viride @ 5 g/L with cow urine solution (10% diluted) as a protective bio-shield. '
                'Apply cold-pressed neem oil (Azadirachtin 1%) @ 3 ml/L.'
            ),
            'immediate_action': (
                'ACT IMMEDIATELY: Blight lesions can coalesce and destroy 50% of photosynthesizing canopy within 5 days.'
            )
        },
        'prevention': (
            'Deep summer plowing to bury crop residues, 2-year crop rotation with non-host crops (soybean/pulses), '
            'and planting certified blight-resistant hybrids.'
        ),
        'prevention_details': {
            'resistant_varieties': 'DHM-117, CP-808, Pioneer P3522, DKC-9141, Nandi-40.',
            'cultural_practices': (
                'Practice deep moldboard plowing after harvest to bury fungal-bearing corn stalks beneath 20 cm of soil. '
                'Rotate fields with legumes or mustard for at least 1-2 seasons. Avoid continuous corn-on-corn farming.'
            ),
            'soil_nutrition': (
                'Apply balanced potassium (K) fertilization to increase cell wall resistance against fungal penetration.'
            )
        },
        'voice_en': (
            'Critical Alert: Northern Corn Leaf Blight detected. '
            'Cigar-shaped lesions are spreading. Spray Mancozeb or Azoxystrobin within 48 hours to save the crop.'
        ),
        'voice_hi': (
            'गंभीर चेतावनी! मक्के में लीफ ब्लाइट (पत्ती का झुलसा रोग) देखा गया है। '
            'सिगार के आकार के धब्बे तेजी से फैल रहे हैं। 48 घंटे के भीतर मैन्कोजेब या एजॉक्सीस्ट्रोबिन का छिड़काव करें।'
        ),
        'voice_kn': (
            'ತುರ್ತು ಎಚ್ಚರಿಕೆ! ಮೆಕ್ಕೆಜೋಳದಲ್ಲಿ ಎಲೆ ಬ್ಲೈಟ್ (ಜುಲಸು ರೋಗ) ಪತ್ತೆಯಾಗಿದೆ. '
            'ಬೆಳೆ ಉಳಿಸಲು 48 ಗಂಟೆಗಳೊಳಗೆ ಮ್ಯಾಂಕೋಜೆಬ್ ಅಥವಾ ಅಜಾಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ ಸಿಂಪಡಿಸಿ.'
        )
    }
}


def get_recommendation(disease_key: str) -> dict:
    """
    Retrieves the comprehensive advisory profile for a given disease key.
    Falls back gracefully if an unexpected key is supplied.
    """
    if disease_key in DISEASE_INFO:
        return DISEASE_INFO[disease_key]

    # Flexible matching for normalized names
    normalized_key = disease_key.strip().replace(' ', '_').replace('-', '_')
    for k in DISEASE_INFO:
        if k.lower() == normalized_key.lower():
            return DISEASE_INFO[k]

    # Partial match
    for k in DISEASE_INFO:
        if k.lower() in normalized_key.lower() or normalized_key.lower() in k.lower():
            return DISEASE_INFO[k]

    # Generic fallback
    return {
        'crop': 'Cereal Crop',
        'disease_name': disease_key.replace('_', ' '),
        'display_name': disease_key.replace('_', ' '),
        'pathogen': 'Identified via Deep Learning CNN Classifier',
        'category': 'Plant Health Advisory',
        'severity': 'Medium',
        'severity_level': 'Medium',
        'affected_area_estimate': '15% - 25%',
        'why_it_happened': 'Environmental stress, persistent canopy humidity, and pathogen presence in field microclimate.',
        'cause': f'Identified as {disease_key.replace("_", " ")}.',
        'causes': 'Fungal or bacterial foliar disease favored by humid, warm conditions and air-borne spores.',
        'symptoms': 'Foliar discoloration, spots, or rust pustules on leaf blades and stems.',
        'treatment': 'Apply broad-spectrum protective fungicides such as Mancozeb 75% WP @ 2.5 g/L or Propiconazole @ 1 ml/L.',
        'treatment_details': {
            'chemical': 'Apply Mancozeb 75% WP @ 2.5 g/L or Propiconazole 25% EC @ 1 ml/L.',
            'organic': 'Spray cold-pressed Neem Oil @ 5 ml/L with liquid soap solution.',
            'immediate_action': 'Isolate infected plants and spray broad-spectrum fungicide.'
        },
        'prevention': 'Use certified disease-free seeds, practice crop rotation, and avoid excess canopy moisture.',
        'prevention_details': {
            'resistant_varieties': 'Consult local Krishi Vigyan Kendra (KVK) for recommended resistant cultivars.',
            'cultural_practices': 'Clean field sanitation and proper row spacing.',
            'soil_nutrition': 'Balanced N-P-K with organic compost.'
        },
        'voice_en': f'Crop disease detected: {disease_key.replace("_", " ")}. Follow standard fungicide management.',
        'voice_hi': f'फसल रोग की पहचान: {disease_key.replace("_", " ")}। अनुशंसित कवकनाशी का छिड़काव करें।',
        'voice_kn': f'ಬೆಳೆ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ: {disease_key.replace("_", " ")}.'
    }


def get_all_diseases() -> list:
    """Returns a list of all supported disease summaries for quick exploration."""
    return [
        {
            'key': k,
            'crop': v['crop'],
            'display_name': v['display_name'],
            'severity': v['severity'],
            'pathogen': v['pathogen']
        }
        for k, v in DISEASE_INFO.items()
    ]
