"""
Farmer-friendly explanations for CropShield AI.

The scientific advisory in ``utils/recommendation.py`` is detailed but written
for agronomists. This module adds two things that smallholder farmers asked
for most often:

* a one-sentence, plain-language reason why the disease happened;
* a numbered prevention checklist that can be followed step by step.

Content is available in English, Hindi and Kannada. The functions are kept
dependency-free so they can be imported from both the web app and the voice
assistant without circular imports.
"""

FARMER_GUIDES = {
    "en": {
        "Wheat_Healthy": {
            "reason": "This leaf is healthy. There are no disease spots, and the plant is getting enough light, water and nutrients.",
            "steps": [
                "Use certified, disease-free wheat seed every season.",
                "Irrigate at crown-root, tillering, jointing, flowering and grain-filling stages.",
                "Apply balanced NPK with zinc; avoid too much nitrogen, which makes leaves soft.",
                "Walk the field twice a week and check the lower leaves for early spots.",
                "Keep the field free of weeds and old crop residue that can hide fungus.",
                "Repeat the same seed, water and nutrition plan next season.",
            ],
        },
        "Maize_Healthy": {
            "reason": "This maize leaf is healthy. The colour is even and there are no rust pustules or blight lesions.",
            "steps": [
                "Sow certified hybrid seed treated with a recommended seed dressing.",
                "Keep the recommended plant spacing so air and sunlight reach every leaf.",
                "Irrigate at knee-high, tasselling and grain-filling stages; avoid waterlogging.",
                "Apply balanced NPK and split the nitrogen into two or three doses.",
                "Check the field twice a week, especially the lower leaves.",
                "Rotate maize with a legume to keep the soil and roots healthy.",
            ],
        },
        "Wheat_BlackRust": {
            "reason": "Black rust spores blow in from other wheat fields. Warm, humid weather with long dew periods lets them infect stems and leaves, and dense sowing helps the disease spread fast.",
            "steps": [
                "Before sowing, choose a certified black-rust-resistant wheat variety recommended for your district.",
                "Sow on time with the correct seed rate; do not sow too densely.",
                "Remove volunteer wheat and grass hosts around the field bunds.",
                "Avoid excess nitrogen and add potash so stems stay strong.",
                "Check the crop every week from tillering; look for dark brown pustules on stems.",
                "If pustules appear, spray the recommended fungicide at the label dose and repeat only as directed.",
                "After harvest, remove or deep-plough infected stubble before the next crop.",
            ],
        },
        "Wheat_BrownRust": {
            "reason": "Brown leaf rust survives on old wheat residue and volunteer plants, then spreads by wind. Cool, moist mornings and late-sown wheat make infection worse.",
            "steps": [
                "Use certified brown-rust-resistant seed suited to your area.",
                "Sow within the recommended sowing window; late sowing increases rust risk.",
                "Destroy volunteer wheat and infected crop residue before sowing.",
                "Apply balanced fertiliser and avoid excess nitrogen.",
                "Inspect the lower leaves weekly and look for small orange-brown pustules.",
                "Spray the recommended fungicide when the first pustules appear; follow the label dose.",
                "Rotate wheat with a non-host crop such as a pulse or oilseed.",
            ],
        },
        "Wheat_YellowRust": {
            "reason": "Yellow stripe rust spores travel long distances on the wind. Cool, moist weather and long dew periods help them attack, and an early infection can explode when spring turns warm.",
            "steps": [
                "Choose a certified yellow-rust-resistant wheat variety for your district.",
                "Sow early in the recommended window and avoid heavy seed rates.",
                "Remove volunteer wheat and infected residue from the field and bunds.",
                "Avoid excess nitrogen; keep potash and sulphur balanced.",
                "Scout weekly and look for bright yellow stripes of powder on the leaves.",
                "Spray the recommended fungicide as soon as stripes appear; repeat per label if needed.",
                "Keep a record of the affected patch so you can rotate crops next season.",
            ],
        },
        "Maize_Blight": {
            "reason": "The blight fungus survives in old maize stalks and leaves and spreads by wind and rain splash. Long cool, humid nights and dense planting let the long leaf spots grow and join together.",
            "steps": [
                "Use certified blight-resistant maize hybrid seed.",
                "Rotate maize with a legume or another non-host crop for at least one season.",
                "Bury or remove the previous maize stubble; do not leave it on the field.",
                "Keep correct plant spacing and control weeds so leaves dry quickly.",
                "Avoid overhead irrigation late in the evening.",
                "Check plants from the knee-high stage for long cigar-shaped grey-green spots.",
                "If spots spread, spray the recommended fungicide at the label dose.",
                "Balance nitrogen with potash and do not over-fertilise.",
            ],
        },
        "Maize_Common_Rust": {
            "reason": "Common rust spores blow in from other maize fields. Cool nights, heavy dew and high humidity help them infect, while dense crops and poor airflow speed up the spread.",
            "steps": [
                "Plant certified rust-resistant maize hybrids.",
                "Sow at the recommended spacing and thin crowded plants.",
                "Irrigate in the morning so leaves dry before night.",
                "Avoid excess nitrogen; apply balanced NPK with potash.",
                "Check the lower leaves twice a week for small reddish-brown pustules.",
                "Spray the recommended fungicide when pustules first appear; follow the label dose.",
                "Remove crop residue and rotate with a legume after harvest.",
            ],
        },
    },
    "hi": {
        "Wheat_Healthy": {
            "reason": "यह पत्ती स्वस्थ है। कोई रोग का धब्बा नहीं है और पौधे को पर्याप्त रोशनी, पानी और पोषण मिल रहा है।",
            "steps": [
                "हर सीजन प्रमाणित और रोगमुक्त गेहूं का बीज लें।",
                "जड़ बनने, कल्ले निकलने, गांठ बनने, फूल आने और दाना भरने के समय सिंचाई करें।",
                "संतुलित NPK के साथ जिंक दें; बहुत ज्यादा नाइट्रोजन से पत्तियां मुलायम होती हैं।",
                "हफ्ते में दो बार खेत का चक्कर लगाएं और नीचे की पत्तियों पर शुरुआती धब्बे देखें।",
                "खेत को खरपतवार और पुराने फसल अवशेष से साफ रखें।",
                "अगले सीजन भी यही बीज, सिंचाई और पोषण योजना दोहराएं।",
            ],
        },
        "Maize_Healthy": {
            "reason": "यह मक्का की पत्ती स्वस्थ है। रंग एक समान है और न रतुआ के फफोले हैं न झुलसा के धब्बे।",
            "steps": [
                "प्रमाणित हाइब्रिड बीज बोएं और बीज को अनुशंसित दवा से उपचारित करें।",
                "सही दूरी पर बोएं ताकि हर पत्ती को हवा और धूप मिले।",
                "घुटने की ऊंचाई, मंजरी और दाना भरने के समय सिंचाई करें; पानी जमा न होने दें।",
                "संतुलित NPK दें और नाइट्रोजन को दो या तीन बार में बांटें।",
                "हफ्ते में दो बार खेत देखें, खासकर नीचे की पत्तियां।",
                "दलहन के साथ फसल चक्र अपनाएं ताकि मिट्टी और जड़ें स्वस्थ रहें।",
            ],
        },
        "Wheat_BlackRust": {
            "reason": "काला रतुआ के बीजाणु दूसरे गेहूं के खेतों से हवा में आते हैं। गर्म, नम मौसम और लंबे समय तक ओस रहने से तना और पत्तियां संक्रमित होती हैं, और घनी बुवाई से रोग तेजी से फैलता है।",
            "steps": [
                "बुवाई से पहले अपने जिले के लिए अनुशंसित प्रमाणित काला-रतुआ प्रतिरोधी गेहूं की किस्म चुनें।",
                "सही समय पर सही बीज दर से बोएं; बहुत घनी बुवाई न करें।",
                "खेत के मेड़ों पर उगी स्वयंसेवी गेहूं और घास हटाएं।",
                "ज्यादा नाइट्रोजन न दें; पोटाश दें ताकि तना मजबूत रहे।",
                "कल्ले निकलने से हर हफ्ते फसल देखें; तने पर गहरे भूरे फफोले खोजें।",
                "फफोले दिखते ही अनुशंसित कवकनाशी लेबल की मात्रा में छिड़कें और निर्देश अनुसार दोहराएं।",
                "कटाई के बाद संक्रमित ठूंठ हटाएं या गहराई से जुताई करें।",
            ],
        },
        "Wheat_BrownRust": {
            "reason": "भूरा पत्ती रतुआ पुराने गेहूं के अवशेष और स्वयंसेवी पौधों पर जीवित रहता है, फिर हवा से फैलता है। ठंडी, नम सुबह और देर से बुवाई से संक्रमण बढ़ता है।",
            "steps": [
                "अपने क्षेत्र के लिए प्रमाणित भूरा-रतुआ प्रतिरोधी बीज लें।",
                "अनुशंसित समय पर बुवाई करें; देर से बुवाई से रतुआ का खतरा बढ़ता है।",
                "बुवाई से पहले स्वयंसेवी गेहूं और संक्रमित फसल अवशेष नष्ट करें।",
                "संतुलित खाद दें और अधिक नाइट्रोजन से बचें।",
                "हर हफ्ते नीचे की पत्तियां देखें और छोटे नारंगी-भूरे फफोले खोजें।",
                "पहले फफोले दिखते ही अनुशंसित कवकनाशी लेबल मात्रा में छिड़कें।",
                "गेहूं के बाद दलहन या तिलहन जैसी दूसरी फसल लें।",
            ],
        },
        "Wheat_YellowRust": {
            "reason": "पीला पट्टी रतुआ के बीजाणु हवा में बहुत दूर तक जाते हैं। ठंडा, नम मौसम और लंबी ओस संक्रमण में मदद करते हैं, और बसंत में गर्मी बढ़ने पर रोग तेजी से फैल सकता है।",
            "steps": [
                "अपने जिले के लिए प्रमाणित पीला-रतुआ प्रतिरोधी गेहूं किस्म चुनें।",
                "अनुशंसित समय पर जल्दी बुवाई करें और ज्यादा बीज न डालें।",
                "खेत और मेड़ों से स्वयंसेवी गेहूं व संक्रमित अवशेष हटाएं।",
                "अधिक नाइट्रोजन से बचें; पोटाश और गंधक संतुलित रखें।",
                "हर हफ्ते जांचें और पत्तियों पर चमकीली पीली धारियां देखें।",
                "धारियां दिखते ही अनुशंसित कवकनाशी छिड़कें; जरूरत हो तो लेबल अनुसार दोहराएं।",
                "प्रभावित हिस्से का रिकॉर्ड रखें ताकि अगले सीजन फसल चक्र बदल सकें।",
            ],
        },
        "Maize_Blight": {
            "reason": "झुलसा फंगस पुराने मक्का के तने-पत्तों में जीवित रहता है और हवा व बारिश की बौछार से फैलता है। लंबी ठंडी, नम रातें और घनी बुवाई से लंबे धब्बे बढ़कर जुड़ जाते हैं।",
            "steps": [
                "प्रमाणित झुलसा-प्रतिरोधी मक्का हाइब्रिड बीज लें।",
                "कम से कम एक सीजन मक्का के बाद दलहन या दूसरी फसल लें।",
                "पिछली मक्का की ठूंठ मिट्टी में दबाएं या खेत से हटाएं।",
                "सही दूरी रखें और खरपतवार निकालें ताकि पत्तियां जल्दी सूखें।",
                "शाम देर से ऊपर से सिंचाई न करें।",
                "घुटने की ऊंचाई से लंबे सिगार जैसे हरे-भूरे धब्बे देखें।",
                "धब्बे बढ़ें तो अनुशंसित कवकनाशी लेबल मात्रा में छिड़कें।",
                "नाइट्रोजन के साथ पोटाश संतुलित रखें और ज्यादा खाद न दें।",
            ],
        },
        "Maize_Common_Rust": {
            "reason": "सामान्य रतुआ के बीजाणु दूसरे मक्का खेतों से हवा में आते हैं। ठंडी रातें, भारी ओस और ज्यादा नमी संक्रमण कराती हैं, जबकि घनी फसल और कम हवा से रोग तेज फैलता है।",
            "steps": [
                "प्रमाणित रतुआ-प्रतिरोधी मक्का हाइब्रिड बोएं।",
                "अनुशंसित दूरी पर बोएं और ज्यादा घने पौधे निकाल दें।",
                "सुबह सिंचाई करें ताकि पत्तियां रात से पहले सूख जाएं।",
                "अधिक नाइट्रोजन से बचें; संतुलित NPK में पोटाश दें।",
                "हफ्ते में दो बार नीचे की पत्तियों पर छोटे लाल-भूरे फफोले देखें।",
                "पहले फफोले दिखते ही अनुशंसित कवकनाशी लेबल मात्रा में छिड़कें।",
                "कटाई के बाद अवशेष हटाएं और दलहन के साथ फसल चक्र अपनाएं।",
            ],
        },
    },
    "kn": {
        "Wheat_Healthy": {
            "reason": "ಈ ಎಲೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ರೋಗದ ಚುಕ್ಕೆಗಳಿಲ್ಲ ಮತ್ತು ಸಸ್ಯಕ್ಕೆ ಸಾಕಷ್ಟು ಬೆಳಕು, ನೀರು ಹಾಗೂ ಪೋಷಕಾಂಶ ಸಿಗುತ್ತಿದೆ.",
            "steps": [
                "ಪ್ರತಿ ಹಂಗಾಮಿನಲ್ಲಿ ಪ್ರಮಾಣೀಕೃತ, ರೋಗಮುಕ್ತ ಗೋಧಿ ಬೀಜ ಬಳಸಿ.",
                "ಬೇರು ಬರುವ, ಕವಲೊಡೆಯುವ, ಗಂಟು ಬರುವ, ಹೂವರಳುವ ಮತ್ತು ಕಾಳು ತುಂಬುವ ಹಂತಗಳಲ್ಲಿ ನೀರು ಹಾಕಿ.",
                "ಸಮತೋಲಿತ NPK ಜೊತೆ ಸತು ನೀಡಿ; ಹೆಚ್ಚು ಸಾರಜನಕ ಎಲೆಗಳನ್ನು ಮೆದುವಾಗಿಸುತ್ತದೆ.",
                "ವಾರಕ್ಕೆ ಎರಡು ಬಾರಿ ಹೊಲ ಸುತ್ತಿ ಕೆಳಗಿನ ಎಲೆಗಳಲ್ಲಿ ಆರಂಭಿಕ ಚುಕ್ಕೆಗಳನ್ನು ನೋಡಿ.",
                "ಕಳೆ ಮತ್ತು ಹಳೆಯ ಬೆಳೆ ಅವಶೇಷಗಳನ್ನು ತೆಗೆದು ಹೊಲ ಸ್ವಚ್ಛವಾಗಿಡಿ.",
                "ಮುಂದಿನ ಹಂಗಾಮಿನಲ್ಲೂ ಅದೇ ಬೀಜ, ನೀರು ಮತ್ತು ಪೋಷಕಾಂಶ ಯೋಜನೆ ಮುಂದುವರಿಸಿ.",
            ],
        },
        "Maize_Healthy": {
            "reason": "ಈ ಮೆಕ್ಕೆಜೋಳದ ಎಲೆ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಬಣ್ಣ ಸಮವಾಗಿದೆ ಮತ್ತು ತುಕ್ಕು ಅಥವಾ ಬ್ಲೈಟ್ ಗಾಯಗಳಿಲ್ಲ.",
            "steps": [
                "ಪ್ರಮಾಣೀಕೃತ ಹೈಬ್ರಿಡ್ ಬೀಜ ಬಿತ್ತಿ ಮತ್ತು ಶಿಫಾರಸು ಮಾಡಿದ ಬೀಜ ಔಷಧ ಹಾಕಿ.",
                "ಪ್ರತಿ ಎಲೆಗೂ ಗಾಳಿ-ಬೆಳಕು ಸಿಗುವಂತೆ ಸರಿಯಾದ ಅಂತರದಲ್ಲಿ ಬಿತ್ತಿ.",
                "ಮೊಳಕೆ, ಹೂವಿನ ಹಂತ ಮತ್ತು ಕಾಳು ತುಂಬುವ ಸಮಯದಲ್ಲಿ ನೀರು ಹಾಕಿ; ನೀರು ನಿಲ್ಲದಂತೆ ನೋಡಿ.",
                "ಸಮತೋಲಿತ NPK ನೀಡಿ ಮತ್ತು ಸಾರಜನಕವನ್ನು ಎರಡು-ಮೂರು ಬಾರಿ ಹಂಚಿ.",
                "ವಾರಕ್ಕೆ ಎರಡು ಬಾರಿ ಹೊಲ ನೋಡಿ, ಮುಖ್ಯವಾಗಿ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು.",
                "ಮಣ್ಣು ಮತ್ತು ಬೇರು ಆರೋಗ್ಯವಾಗಿರಲು ಮೆಕ್ಕೆಜೋಳದ ನಂತರ ದ್ವಿದಳ ಧಾನ್ಯ ಬೆಳೆಯಿರಿ.",
            ],
        },
        "Wheat_BlackRust": {
            "reason": "ಕಪ್ಪು ತುಕ್ಕು ಬೀಜಕಗಳು ಬೇರೆ ಗೋಧಿ ಹೊಲಗಳಿಂದ ಗಾಳಿಯಲ್ಲಿ ಬರುತ್ತವೆ. ಬೆಚ್ಚಗಿನ, ತೇವದ ಹವೆ ಮತ್ತು ದೀರ್ಘ ಇಬ್ಬನಿ ಕಾಂಡ ಹಾಗೂ ಎಲೆಗಳಿಗೆ ಸೋಂಕು ತರುತ್ತದೆ; ದಟ್ಟ ಬಿತ್ತನೆ ರೋಗವನ್ನು ವೇಗವಾಗಿ ಹರಡಿಸುತ್ತದೆ.",
            "steps": [
                "ಬಿತ್ತನೆಗೆ ಮೊದಲು ನಿಮ್ಮ ಜಿಲ್ಲೆಗೆ ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರಮಾಣೀಕೃತ ಕಪ್ಪು-ತುಕ್ಕು ನಿರೋಧಕ ಗೋಧಿ ತಳಿ ಆರಿಸಿ.",
                "ಸರಿಯಾದ ಸಮಯದಲ್ಲಿ ಸರಿಯಾದ ಬೀಜ ಪ್ರಮಾಣದಲ್ಲಿ ಬಿತ್ತಿ; ಅತಿ ದಟ್ಟವಾಗಿ ಬಿತ್ತಬೇಡಿ.",
                "ಹೊಲದ ಬದುಗಳಲ್ಲಿ ತಾನಾಗಿ ಬೆಳೆದ ಗೋಧಿ ಮತ್ತು ಹುಲ್ಲು ತೆಗೆಯಿರಿ.",
                "ಹೆಚ್ಚು ಸಾರಜನಕ ಬೇಡ; ಕಾಂಡ ಗಟ್ಟಿಯಾಗಲು ಪೊಟ್ಯಾಶ್ ನೀಡಿ.",
                "ಕವಲೊಡೆಯುವ ಹಂತದಿಂದ ವಾರಕ್ಕೊಮ್ಮೆ ಬೆಳೆ ಪರೀಕ್ಷಿಸಿ; ಕಾಂಡದ ಮೇಲೆ ಗಾಢ ಕಂದು ಗುಳ್ಳೆಗಳನ್ನು ನೋಡಿ.",
                "ಗುಳ್ಳೆಗಳು ಕಂಡ ತಕ್ಷಣ ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಲೇಬಲ್ ಪ್ರಮಾಣದಲ್ಲಿ ಸಿಂಪಡಿಸಿ.",
                "ಕಟಾವಿನ ನಂತರ ಸೋಂಕಿತ ಕೊಳವೆ/ಅವಶೇಷ ತೆಗೆಯಿರಿ ಅಥವಾ ಆಳವಾಗಿ ಉಳುಮೆ ಮಾಡಿ.",
            ],
        },
        "Wheat_BrownRust": {
            "reason": "ಕಂದು ಎಲೆ ತುಕ್ಕು ಹಳೆಯ ಗೋಧಿ ಅವಶೇಷ ಮತ್ತು ತಾನಾಗಿ ಬೆಳೆದ ಸಸ್ಯಗಳಲ್ಲಿ ಉಳಿದು ಗಾಳಿಯಿಂದ ಹರಡುತ್ತದೆ. ತಂಪು, ತೇವದ ಮುಂಜಾನೆ ಮತ್ತು ತಡವಾದ ಬಿತ್ತನೆ ಸೋಂಕನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ.",
            "steps": [
                "ನಿಮ್ಮ ಪ್ರದೇಶಕ್ಕೆ ಸೂಕ್ತವಾದ ಪ್ರಮಾಣೀಕೃತ ಕಂದು-ತುಕ್ಕು ನಿರೋಧಕ ಬೀಜ ಬಳಸಿ.",
                "ಶಿಫಾರಸು ಮಾಡಿದ ಸಮಯದಲ್ಲಿ ಬಿತ್ತಿ; ತಡವಾದ ಬಿತ್ತನೆ ಅಪಾಯ ಹೆಚ್ಚಿಸುತ್ತದೆ.",
                "ಬಿತ್ತನೆಗೆ ಮೊದಲು ತಾನಾಗಿ ಬೆಳೆದ ಗೋಧಿ ಮತ್ತು ಸೋಂಕಿತ ಅವಶೇಷ ನಾಶ ಮಾಡಿ.",
                "ಸಮತೋಲಿತ ಗೊಬ್ಬರ ನೀಡಿ; ಹೆಚ್ಚು ಸಾರಜನಕ ತಪ್ಪಿಸಿ.",
                "ವಾರಕ್ಕೊಮ್ಮೆ ಕೆಳಗಿನ ಎಲೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ ಸಣ್ಣ ಕಿತ್ತಳೆ-ಕಂದು ಗುಳ್ಳೆಗಳನ್ನು ನೋಡಿ.",
                "ಮೊದಲ ಗುಳ್ಳೆಗಳು ಕಂಡಾಗ ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕ ಲೇಬಲ್ ಪ್ರಮಾಣದಲ್ಲಿ ಸಿಂಪಡಿಸಿ.",
                "ಗೋಧಿಯ ನಂತರ ದ್ವಿದಳ ಧಾನ್ಯ ಅಥವಾ ಎಣ್ಣೆಕಾಳು ಬೆಳೆ ತಿರುಗಿಸಿ.",
            ],
        },
        "Wheat_YellowRust": {
            "reason": "ಹಳದಿ ಪಟ್ಟಿ ತುಕ್ಕು ಬೀಜಕಗಳು ಗಾಳಿಯಲ್ಲಿ ದೂರದವರೆಗೆ ಸಾಗುತ್ತವೆ. ತಂಪು, ತೇವದ ಹವೆ ಮತ್ತು ದೀರ್ಘ ಇಬ್ಬನಿ ಸೋಂಕಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತವೆ; ವಸಂತದಲ್ಲಿ ಬಿಸಿ ಹೆಚ್ಚಿದಾಗ ರೋಗ ವೇಗವಾಗಿ ಹರಡಬಹುದು.",
            "steps": [
                "ನಿಮ್ಮ ಜಿಲ್ಲೆಗೆ ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರಮಾಣೀಕೃತ ಹಳದಿ-ತುಕ್ಕು ನಿರೋಧಕ ಗೋಧಿ ತಳಿ ಆರಿಸಿ.",
                "ಶಿಫಾರಸು ಮಾಡಿದ ಅವಧಿಯಲ್ಲಿ ಬೇಗ ಬಿತ್ತಿ; ಹೆಚ್ಚು ಬೀಜ ಬೇಡ.",
                "ಹೊಲ ಮತ್ತು ಬದುಗಳಿಂದ ತಾನಾಗಿ ಬೆಳೆದ ಗೋಧಿ ಹಾಗೂ ಸೋಂಕಿತ ಅವಶೇಷ ತೆಗೆಯಿರಿ.",
                "ಹೆಚ್ಚು ಸಾರಜನಕ ತಪ್ಪಿಸಿ; ಪೊಟ್ಯಾಶ್ ಮತ್ತು ಗಂಧಕ ಸಮತೋಲನದಲ್ಲಿರಿಸಿ.",
                "ವಾರಕ್ಕೊಮ್ಮೆ ಪರೀಕ್ಷಿಸಿ ಎಲೆಗಳ ಮೇಲೆ ಪ್ರಕಾಶಮಾನ ಹಳದಿ ಪಟ್ಟಿಗಳನ್ನು ನೋಡಿ.",
                "ಪಟ್ಟಿಗಳು ಕಂಡ ತಕ್ಷಣ ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ; ಅಗತ್ಯವಿದ್ದರೆ ಲೇಬಲ್ ಪ್ರಕಾರ ಪುನರಾವರ್ತಿಸಿ.",
                "ಬಾಧಿತ ಭಾಗದ ದಾಖಲೆ ಇಟ್ಟು ಮುಂದಿನ ಹಂಗಾಮಿನಲ್ಲಿ ಬೆಳೆ ತಿರುಗಿಸಿ.",
            ],
        },
        "Maize_Blight": {
            "reason": "ಬ್ಲೈಟ್ ಶಿಲೀಂಧ್ರ ಹಳೆಯ ಮೆಕ್ಕೆಜೋಳದ ಕಾಂಡ-ಎಲೆಗಳಲ್ಲಿ ಉಳಿದು ಗಾಳಿ ಮತ್ತು ಮಳೆಯ ಹನಿಯಿಂದ ಹರಡುತ್ತದೆ. ದೀರ್ಘ ತಂಪು, ತೇವದ ರಾತ್ರಿಗಳು ಮತ್ತು ದಟ್ಟ ಬೆಳೆ ಉದ್ದ ಚುಕ್ಕೆಗಳನ್ನು ಬೆಳೆಸಿ ಜೋಡಿಸುತ್ತವೆ.",
            "steps": [
                "ಪ್ರಮಾಣೀಕೃತ ಬ್ಲೈಟ್-ನಿರೋಧಕ ಮೆಕ್ಕೆಜೋಳ ಹೈಬ್ರಿಡ್ ಬೀಜ ಬಳಸಿ.",
                "ಕನಿಷ್ಠ ಒಂದು ಹಂಗಾಮು ಮೆಕ್ಕೆಜೋಳದ ನಂತರ ದ್ವಿದಳ ಧಾನ್ಯ ಅಥವಾ ಬೇರೆ ಬೆಳೆ ಬೆಳೆಯಿರಿ.",
                "ಹಿಂದಿನ ಮೆಕ್ಕೆಜೋಳದ ಅವಶೇಷವನ್ನು ಮಣ್ಣಿನಲ್ಲಿ ಹೂಳಿ ಅಥವಾ ಹೊಲದಿಂದ ತೆಗೆಯಿರಿ.",
                "ಸರಿಯಾದ ಅಂತರ ಕಾಪಾಡಿ ಕಳೆ ತೆಗೆಯಿರಿ; ಎಲೆಗಳು ಬೇಗ ಒಣಗಲಿ.",
                "ಸಂಜೆ ತಡವಾಗಿ ಮೇಲಿನಿಂದ ನೀರು ಹಾಕಬೇಡಿ.",
                "ಮೊಳಕೆಯ ಎತ್ತರದಿಂದ ಉದ್ದ ಸಿಗಾರ್ ಆಕಾರದ ಬೂದು-ಹಸಿರು ಚುಕ್ಕೆಗಳನ್ನು ನೋಡಿ.",
                "ಚುಕ್ಕೆಗಳು ಹರಡಿದರೆ ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕ ಲೇಬಲ್ ಪ್ರಮಾಣದಲ್ಲಿ ಸಿಂಪಡಿಸಿ.",
                "ಸಾರಜನಕದೊಂದಿಗೆ ಪೊಟ್ಯಾಶ್ ಸಮತೋಲನ ಮಾಡಿ; ಹೆಚ್ಚು ಗೊಬ್ಬರ ಬೇಡ.",
            ],
        },
        "Maize_Common_Rust": {
            "reason": "ಸಾಮಾನ್ಯ ತುಕ್ಕು ಬೀಜಕಗಳು ಬೇರೆ ಮೆಕ್ಕೆಜೋಳ ಹೊಲಗಳಿಂದ ಗಾಳಿಯಲ್ಲಿ ಬರುತ್ತವೆ. ತಂಪು ರಾತ್ರಿ, ಭಾರೀ ಇಬ್ಬನಿ ಮತ್ತು ಹೆಚ್ಚು ತೇವಾಂಶ ಸೋಂಕು ತರುತ್ತವೆ; ದಟ್ಟ ಬೆಳೆ ಮತ್ತು ಕಡಿಮೆ ಗಾಳಿ ರೋಗ ಹರಡುವಿಕೆಯನ್ನು ವೇಗಗೊಳಿಸುತ್ತವೆ.",
            "steps": [
                "ಪ್ರಮಾಣೀಕೃತ ತುಕ್ಕು-ನಿರೋಧಕ ಮೆಕ್ಕೆಜೋಳ ಹೈಬ್ರಿಡ್ ಬಿತ್ತಿ.",
                "ಶಿಫಾರಸು ಮಾಡಿದ ಅಂತರದಲ್ಲಿ ಬಿತ್ತಿ; ದಟ್ಟವಾದ ಸಸಿಗಳನ್ನು ತೆಗೆಯಿರಿ.",
                "ಬೆಳಗ್ಗೆ ನೀರು ಹಾಕಿ; ಎಲೆಗಳು ರಾತ್ರಿಗೆ ಮೊದಲು ಒಣಗಲಿ.",
                "ಹೆಚ್ಚು ಸಾರಜನಕ ಬೇಡ; ಪೊಟ್ಯಾಶ್ ಸಹಿತ ಸಮತೋಲಿತ NPK ನೀಡಿ.",
                "ವಾರಕ್ಕೆ ಎರಡು ಬಾರಿ ಕೆಳಗಿನ ಎಲೆಗಳಲ್ಲಿ ಸಣ್ಣ ಕೆಂಪು-ಕಂದು ಗುಳ್ಳೆಗಳನ್ನು ನೋಡಿ.",
                "ಮೊದಲ ಗುಳ್ಳೆಗಳು ಕಂಡಾಗ ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕ ಲೇಬಲ್ ಪ್ರಮಾಣದಲ್ಲಿ ಸಿಂಪಡಿಸಿ.",
                "ಕಟಾವಿನ ನಂತರ ಅವಶೇಷ ತೆಗೆದು ದ್ವಿದಳ ಧಾನ್ಯದೊಂದಿಗೆ ಬೆಳೆ ತಿರುಗಿಸಿ.",
            ],
        },
    },
}


def get_farmer_guide(disease_key, lang="en"):
    """
    Return ``{"reason": str, "steps": [str, ...]}`` for a disease.

    Unknown diseases or languages fall back to English, and then to a short
    generic guide so the report page never shows an empty section.
    """
    language = (lang or "en").strip().lower().split("-")[0]
    guides = FARMER_GUIDES.get(language) or FARMER_GUIDES["en"]
    guide = guides.get(disease_key) or FARMER_GUIDES["en"].get(disease_key)

    if not guide:
        guide = {
            "reason": "The model found a crop health problem. Upload a clear photo and follow the advisory below.",
            "steps": [
                "Remove badly affected leaves and destroy them away from the field.",
                "Keep proper spacing so air and sunlight reach the plants.",
                "Avoid excess nitrogen and keep irrigation balanced.",
                "Check the field every week for new spots or pustules.",
                "Ask your local agriculture officer before spraying any chemical.",
            ],
        }

    return {
        "reason": guide.get("reason", ""),
        "steps": list(guide.get("steps", [])),
    }
