import json
from app.database.session import SessionLocal, Base, engine
from app.database.models import User, Crop, Disease, PricingConfig, ScanHistory
from app.core.security import get_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already seeded.")
            return

        print("Seeding initial database data...")

        # 1. Seed Pricing Config
        plus_features = json.dumps([
            "50 disease scans per month",
            "Detailed 'Why did this happen?' AI breakdown",
            "Downloadable PDF/Offline crop health reports",
            "Multi-crop history tracking",
            "Priority helpline support"
        ])
        pro_features = json.dumps([
            "500 disease scans per month",
            "Unlimited crop health tracking",
            "Direct 1-on-1 Agronomist consultation access",
            "Seasonal disease outbreak alerts",
            "Krishi Mitra / CSC operator assisted tools",
            "Advanced soil & weather advisory integration"
        ])

        plus_config = PricingConfig(plan_name="plus", price_inr=49.0, scan_limit=50, description="CropCare Plus — For Active Farmers", features=plus_features)
        pro_config = PricingConfig(plan_name="pro", price_inr=99.0, scan_limit=500, description="CropCare Pro — For Progressive Farmers & Cooperatives", features=pro_features)
        db.add_all([plus_config, pro_config])

        # 2. Seed Default Users
        users = [
            User(name="Ramesh Kumar (Farmer)", phone="9876543210", email="farmer@cropcare.ai", password_hash=get_password_hash("password123"), language="hi", role="farmer", subscription_plan="free", scan_count_month=1),
            User(name="Sunita Devi (Krishi Mitra)", phone="9876543211", email="mitra@cropcare.ai", password_hash=get_password_hash("password123"), language="hi", role="worker", subscription_plan="pro", scan_count_month=15),
            User(name="Dr. Anil Sharma (Agronomist)", phone="9876543212", email="expert@cropcare.ai", password_hash=get_password_hash("password123"), language="en", role="expert", subscription_plan="pro", scan_count_month=0),
            User(name="Kisan Kalyan FPO", phone="9876543213", email="fpo@cropcare.ai", password_hash=get_password_hash("password123"), language="en", role="b2b_org", subscription_plan="pro", scan_count_month=120),
            User(name="System Administrator", phone="9876543214", email="admin@cropcare.ai", password_hash=get_password_hash("admin123"), language="en", role="admin", subscription_plan="pro", scan_count_month=0),
        ]
        db.add_all(users)
        db.flush()

        # 3. Seed Crops
        crops_data = [
            {"name": "Tomato", "hindi_name": "टमाटर", "description": "Solanaceous fruit vegetable prone to fungal blights and viral leaf curls.", "icon": "tomato"},
            {"name": "Potato", "hindi_name": "आलू", "description": "Starchy tuber crop sensitive to late blight and moisture stress.", "icon": "potato"},
            {"name": "Rice", "hindi_name": "धान / चावल", "description": "Cereal staple vulnerable to blast fungus in humid conditions.", "icon": "rice"},
            {"name": "Apple", "hindi_name": "सेब", "description": "Temperate fruit crop vulnerable to apple scab and rust in cool wet seasons.", "icon": "apple"},
            {"name": "Corn", "hindi_name": "मक्का", "description": "High-yield cereal affected by leaf spot and rust in warm wet weather.", "icon": "corn"},
            {"name": "Wheat", "hindi_name": "गेहूं", "description": "Rabi grain crop vulnerable to stripe/yellow rust and spot blotch.", "icon": "wheat"},
            {"name": "Cotton", "hindi_name": "कपास", "description": "Cash fiber crop affected by leaf curl virus transmitted by whiteflies.", "icon": "cotton"},
        ]

        crop_objs = {}
        for c in crops_data:
            crop_obj = Crop(name=c["name"], hindi_name=c["hindi_name"], description=c["description"], icon=c["icon"])
            db.add(crop_obj)
            db.flush()
            crop_objs[c["name"]] = crop_obj

        # 4. Seed Diseases with comprehensive agricultural guidance
        diseases_data = [
            # Tomato Diseases
            {
                "crop_name": "Tomato",
                "name": "Tomato Leaf Blight",
                "hindi_name": "टमाटर पत्ता झुलसा (लीफ ब्लाइट)",
                "scientific_name": "Alternaria solani / Phytophthora infestans",
                "severity_level": "Medium",
                "description": "Fungal infection causing circular dark brown spots with concentric rings ('target board') on leaves, leading to yellowing and premature leaf drop.",
                "symptoms": [
                    "Brown or black necrotic spots on lower leaves first",
                    "Concentric ring pattern within leaf spots",
                    "Yellow halos surrounding the damaged tissue",
                    "Drying and curling of affected foliage",
                    "Dark sunken lesions on stems and fruit in later stages"
                ],
                "possible_causes": [
                    "Excess surface moisture and stagnant water around roots",
                    "High relative humidity (above 80%) for extended periods",
                    "Prolonged leaf wetness from overhead irrigation or morning dew",
                    "Poor air circulation within crowded crop canopy",
                    "Infected crop debris or volunteer plants from previous season"
                ],
                "favorable_conditions": [
                    "Temperatures between 24°C and 29°C",
                    "Warm, humid, rainy or foggy weather",
                    "Poor soil drainage"
                ],
                "immediate_actions": [
                    "Remove severely affected lower leaves and dispose of them away from the field (do not compost)",
                    "Avoid overhead irrigation; switch to drip or base furrow watering",
                    "Improve field ventilation by pruning suckers and weeding",
                    "Avoid touching healthy plants immediately after handling diseased foliage"
                ],
                "general_management": [
                    "Consult your local agricultural extension officer for approved bio-fungicides or copper-based protectors",
                    "Always read and strictly adhere to product label instructions and safety pre-harvest intervals",
                    "Ensure adequate potassium and balanced nitrogen nutrition to strengthen cell walls"
                ],
                "prevention": [
                    "Inspect crops regularly at least twice per week",
                    "Maintain proper row and plant spacing (at least 60 cm)",
                    "Use certified disease-free seeds and certified resistant cultivars",
                    "Practice 2-3 year crop rotation away from solanaceous crops (potato, eggplant, pepper)",
                    "Apply organic straw mulch around plant base to prevent soil splash onto foliage"
                ],
                "when_to_contact_expert": "If spots spread to more than 30% of foliage within 48 hours or dark sunken lesions appear on green fruits."
            },
            {
                "crop_name": "Tomato",
                "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
                "hindi_name": "टमाटर पीली पत्ती मरोड़ विषाणु (लीफ कर्ल)",
                "scientific_name": "Tomato Yellow Leaf Curl Virus",
                "severity_level": "High",
                "description": "Devastating viral disease transmitted by the silverleaf whitefly (Bemisia tabaci) leading to severe stunting, upward leaf cupping, and complete yield loss.",
                "symptoms": [
                    "Upward curling and cupping of leaf margins",
                    "Marked yellowing (chlorosis) between veins on young leaves",
                    "Severe stunting of new growth and shortened internodes",
                    "Bushy, dwarfed plant appearance",
                    "Flowers drop prematurely with zero to little fruit set"
                ],
                "possible_causes": [
                    "Infestation of silverleaf whiteflies carrying the virus",
                    "Hot, dry weather favoring whitefly population surges",
                    "Presence of infected weeds or adjacent old tomato/chilli fields",
                    "Use of uncertified nursery seedlings already carrying latent virus"
                ],
                "favorable_conditions": [
                    "Warm temperatures (28°C - 35°C) promoting rapid whitefly breeding",
                    "Dry spells during initial vegetative growth"
                ],
                "immediate_actions": [
                    "Rogue out (uproot) severely stunted and infected plants immediately; bag them in plastic and destroy",
                    "Install yellow sticky traps (15-20 traps per acre) at canopy level to monitor and capture whiteflies",
                    "Spray neem oil (5ml/liter water) or approved biopesticides to suppress vector nymphs",
                    "Protect remaining healthy plants with insect exclusion netting"
                ],
                "general_management": [
                    "Manage vector populations using integrated pest management (IPM) protocols",
                    "Avoid excessive nitrogen fertilization which produces tender succulence that attracts sap-sucking pests",
                    "Follow locally approved guidelines from your state agricultural university"
                ],
                "prevention": [
                    "Cultivate TYLCV-resistant or tolerant tomato hybrids",
                    "Erect 40-mesh insect-proof nylon nets over seedling nurseries",
                    "Maintain weed-free border zones around the field",
                    "Adopt reflective silver plastic mulches to repel alighting whiteflies"
                ],
                "when_to_contact_expert": "If whitefly swarms are visible under leaf surfaces or more than 10% of field demonstrates sudden upward cupping."
            },
            {
                "crop_name": "Tomato",
                "name": "Healthy Tomato",
                "hindi_name": "स्वस्थ टमाटर",
                "scientific_name": "Solanum lycopersicum",
                "severity_level": "Low",
                "description": "Plant foliage shows vibrant green coloration, balanced leaf expansion, and no visible fungal or viral lesions.",
                "symptoms": [
                    "Uniform green leaf pigmentation",
                    "No necrotic lesions, wilting, or unnatural spots",
                    "Stems are firm and vigorous",
                    "Normal flowering and healthy fruit development"
                ],
                "possible_causes": [
                    "Optimal soil nutrition and balanced moisture",
                    "Favorable microclimate and proper aeration",
                    "Absence of active fungal sporulation or insect vector pressure"
                ],
                "favorable_conditions": [
                    "Sunny days with moderate humidity and well-drained loamy soil"
                ],
                "immediate_actions": [
                    "Continue existing healthy agronomic practices",
                    "Maintain disciplined drip irrigation schedules"
                ],
                "general_management": [
                    "Monitor soil moisture before irrigating",
                    "Scout leaves twice a week to detect early warning signs"
                ],
                "prevention": [
                    "Maintain regular scouting routines",
                    "Mulch rows to prevent weed encroachment and regulate root temperatures"
                ],
                "when_to_contact_expert": "Routine consult if planning mid-season booster nutrients or micronutrient sprays."
            },
            # Potato Diseases
            {
                "crop_name": "Potato",
                "name": "Potato Early Blight",
                "hindi_name": "आलू अगेती झुलसा",
                "scientific_name": "Alternaria solani",
                "severity_level": "Medium",
                "description": "Common foliar fungal disease causing dark brown spots with characteristic concentric target-board rings on mature potato leaves.",
                "symptoms": [
                    "Small circular to irregular dark brown spots on older lower leaves",
                    "Spots develop concentric ridges resembling target boards",
                    "Surrounding leaf tissue becomes chlorotic (yellow)",
                    "Severely diseased foliage turns brown and collapses"
                ],
                "possible_causes": [
                    "Alternating periods of dry and wet weather conditions",
                    "Over-irrigation combined with nitrogen-deficient stressed crops",
                    "Presence of fungal spores surviving on solanaceous plant residues"
                ],
                "favorable_conditions": [
                    "Temperatures around 24°C - 30°C with high humidity"
                ],
                "immediate_actions": [
                    "Avoid overhead sprinkler irrigation during late afternoon",
                    "Remove and destroy heavily spotted bottom leaves",
                    "Improve nitrogen and potassium balance to alleviate plant physiological stress"
                ],
                "general_management": [
                    "Apply approved contact fungicides (such as mancozeb) as recommended by local extension advisory",
                    "Follow package label instructions and safety withholding intervals"
                ],
                "prevention": [
                    "Plant certified disease-free potato seed tubers",
                    "Rotate crops with non-host cereals or legumes for at least 3 years",
                    "Hill soil properly around tubers to shield them from spores washed by rain"
                ],
                "when_to_contact_expert": "If disease spreads upwards past mid-canopy during early tuber bulking."
            },
            {
                "crop_name": "Potato",
                "name": "Potato Late Blight",
                "hindi_name": "आलू पछेती झुलसा",
                "scientific_name": "Phytophthora infestans",
                "severity_level": "High",
                "description": "Rapidly destructive water-mold disease that can devastate whole fields in days under cool, humid conditions.",
                "symptoms": [
                    "Water-soaked dark lesions at leaf tips and margins",
                    "White fuzzy mildew growth on leaf undersides in morning dampness",
                    "Rapid leaf wilting, blackening, and foul odor in field",
                    "Brown rotten patches under tuber skin"
                ],
                "possible_causes": [
                    "Prolonged cool, overcast, damp weather with continuous leaf moisture",
                    "Airborne sporangia travelling on winds from neighboring infected plots",
                    "Infected cull piles or latent seed tubers"
                ],
                "favorable_conditions": [
                    "Temperatures 15°C - 22°C with humidity > 90% and heavy morning dew"
                ],
                "immediate_actions": [
                    "Apply systemic protective fungicide immediately following local agri-department alert",
                    "Eliminate overhead watering; ensure surface furrows drain freely",
                    "Destroy infected foliage (haulm killing) before harvest if tubers are maturing"
                ],
                "general_management": [
                    "Community-level coordinated spraying prevents airborne regional outbreaks",
                    "Strictly follow local university spray advisory schedules"
                ],
                "prevention": [
                    "Use resistant potato cultivars",
                    "Destroy all potato cull piles and volunteer plants before planting",
                    "Space rows generously to accelerate morning canopy drying"
                ],
                "when_to_contact_expert": "Immediate emergency notice recommended upon first confirmation of white mildew on leaf undersides."
            },
            # Rice Diseases
            {
                "crop_name": "Rice",
                "name": "Rice Blast",
                "hindi_name": "धान का झोंका / ब्लास्ट रोग",
                "scientific_name": "Magnaporthe oryzae",
                "severity_level": "High",
                "description": "Dangerous fungal disease producing spindle-shaped diamond lesions with gray centers, affecting leaves, collar, and panicle neck.",
                "symptoms": [
                    "Spindle-shaped elliptical lesions with pointed ends on leaf blades",
                    "Lesions have grayish center with dark reddish-brown borders",
                    "Lesions coalesce, causing entire leaves to dry and wither",
                    "Neck blast causes rotten black nodes and empty white heads (chaffy grain)"
                ],
                "possible_causes": [
                    "High doses of chemical nitrogen fertilizer",
                    "Extended periods of cloudiness, drizzle, and high relative humidity (>90%)",
                    "Dense seedling beds with stagnant standing air"
                ],
                "favorable_conditions": [
                    "Night temperatures 17°C - 23°C with heavy dew deposition"
                ],
                "immediate_actions": [
                    "Halt any further chemical nitrogen applications immediately",
                    "Drain excess standing water temporarily and maintain intermittent shallow wetting",
                    "Apply recommended bio-control agents (Pseudomonas fluorescens) or approved blast-specific fungicide"
                ],
                "general_management": [
                    "Follow state agricultural department recommendations for safe dosage",
                    "Ensure adequate silicon and potassium in basal fertilizer"
                ],
                "prevention": [
                    "Treat seeds with approved fungicides or hot-water treatment prior to sowing",
                    "Adopt blast-tolerant paddy varieties",
                    "Avoid late sowing in the season"
                ],
                "when_to_contact_expert": "If neck rot or panicle lesions emerge as crop approaches boot-leaf or flowering stage."
            },
            # Apple Diseases
            {
                "crop_name": "Apple",
                "name": "Apple Scab",
                "hindi_name": "सेब का पपड़ी रोग (एप्पल स्कैब)",
                "scientific_name": "Venturia inaequalis",
                "severity_level": "Medium",
                "description": "Foliar and fruit fungal disease characterized by olive-green velvety spots turning corky and cracked on fruit skin.",
                "symptoms": [
                    "Olive-green velvety spots on young leaves and blossoms",
                    "Lesions become dark brown, raised, and crust-like",
                    "Infected leaves curl, turn yellow, and drop prematurely",
                    "Fruits develop scabby dark corky lesions and cracks"
                ],
                "possible_causes": [
                    "Prolonged spring rains keeping leaves wet for 9+ hours",
                    "Overwintering fungal spores in fallen orchard leaf litter",
                    "Dense unpruned canopy shading interior leaves"
                ],
                "favorable_conditions": [
                    "Cool, damp weather with temperatures between 16°C and 24°C"
                ],
                "immediate_actions": [
                    "Prune crowded interior water sprouts to admit sunlight and dry foliage",
                    "Rake and shred or compost fallen leaves on orchard floor",
                    "Apply protective bio-fungicidal spray during green-tip stage"
                ],
                "general_management": [
                    "Monitor leaf wetness duration using orchard weather sensors if available",
                    "Follow IPM spray schedules timed with ascospore release"
                ],
                "prevention": [
                    "Plant scab-resistant apple rootstocks and varieties",
                    "Maintain generous spacing and annual canopy pruning",
                    "Spray urea (5%) on fallen leaves in autumn to accelerate decomposition"
                ],
                "when_to_contact_expert": "If scab lesions emerge on fruitlets prior to petal fall."
            },
            # Corn Diseases
            {
                "crop_name": "Corn",
                "name": "Corn Leaf Spot (Northern Corn Leaf Blight)",
                "hindi_name": "मक्के का पत्ती झुलसा / धब्बा रोग",
                "scientific_name": "Exserohilum turcicum",
                "severity_level": "Medium",
                "description": "Foliar disease of maize causing elongated cigar-shaped grayish-green lesions that diminish photosynthetic leaf area.",
                "symptoms": [
                    "Long, elliptical, cigar-shaped tan or grayish lesions (2 to 15 cm)",
                    "Dark fungal spore mats visible in lesions during damp mornings",
                    "Lower leaves blighted first, moving upward towards the ear leaf",
                    "Extensive leaf burning causing reduced grain fill"
                ],
                "possible_causes": [
                    "Frequent rainfall and high relative humidity during tasseling",
                    "Continuous corn-on-corn monoculture without rotation",
                    "Crop residue remaining on field surface from previous season"
                ],
                "favorable_conditions": [
                    "Moderate temperatures (18°C - 27°C) accompanied by heavy dews"
                ],
                "immediate_actions": [
                    "Avoid sprinkler irrigation during cool cloudy mornings",
                    "Ensure adequate plant nutrition (especially potassium)",
                    "Scout the third leaf below the ear to monitor economic threshold"
                ],
                "general_management": [
                    "Consult local Krishi Vigyan Kendra (KVK) for certified fungicide protocols if disease appears before tasseling"
                ],
                "prevention": [
                    "Select certified resistant corn hybrids",
                    "Practice minimum 1-year crop rotation with soybeans or pulses",
                    "Deep plow infected stover residues after harvest to break spore lifecycle"
                ],
                "when_to_contact_expert": "If lesions reach the ear leaf before blister or milk development stage."
            },
            # Wheat Diseases
            {
                "crop_name": "Wheat",
                "name": "Wheat Stripe Rust (Yellow Rust)",
                "hindi_name": "गेहूं का पीला रतुआ (येलो रस्ट)",
                "scientific_name": "Puccinia striiformis",
                "severity_level": "High",
                "description": "High-threat fungal infection producing bright yellow stripes of powdery pustules parallel to leaf veins, severely impairing photosynthesis.",
                "symptoms": [
                    "Parallel stripes of tiny yellow powdery pustules on leaf surface",
                    "Yellow powder rubs off onto fingers or clothing",
                    "Premature drying and chlorosis of leaves",
                    "Shriveled grains and reduced spike size"
                ],
                "possible_causes": [
                    "Cool, humid weather with frequent morning fog or light showers",
                    "Wind-borne urediniospores travelling long distances from foothill regions",
                    "Susceptible wheat variety sown over large contiguous areas"
                ],
                "favorable_conditions": [
                    "Temperatures 10°C - 15°C with high relative humidity and dew"
                ],
                "immediate_actions": [
                    "Alert local agricultural extension immediately upon spot identification",
                    "Apply approved triazole fungicide as prescribed by state agriculture advisory",
                    "Avoid late irrigation that induces prolonging damp microclimates"
                ],
                "general_management": [
                    "Participate in regional yellow rust surveillance programs",
                    "Follow dosage instructions precisely"
                ],
                "prevention": [
                    "Sow rust-resistant varieties recommended for your agro-climatic zone",
                    "Complete timely sowing in November to escape late season infection",
                    "Avoid excessive nitrogen fertilization"
                ],
                "when_to_contact_expert": "Contact extension authority immediately; yellow rust is an alert-grade community threat."
            },
            # Cotton Diseases
            {
                "crop_name": "Cotton",
                "name": "Cotton Leaf Curl Virus (CLCuV)",
                "hindi_name": "कपास पत्ता मरोड़ विषाणु (लीफ कर्ल)",
                "scientific_name": "Cotton Leaf Curl Virus",
                "severity_level": "High",
                "description": "Geminivirus transmitted by whiteflies leading to upward/downward leaf curling, vein thickening, and leaf-like enations on undersides.",
                "symptoms": [
                    "Upward or downward curling of leaf margins",
                    "Pronounced swelling and darkening of minor veins",
                    "Small cup-shaped or leaf-like outgrowths (enations) on leaf undersides",
                    "Severe stunting and reduced boll formation"
                ],
                "possible_causes": [
                    "High whitefly (Bemisia tabaci) populations",
                    "Presence of alternative weed hosts like wild okra or parthenium",
                    "Sowing susceptible non-certified varieties"
                ],
                "favorable_conditions": [
                    "High temperature and high humidity in early crop season"
                ],
                "immediate_actions": [
                    "Uproot and bury virus-infected plants during early vegetative phase",
                    "Manage whiteflies using neem formulations or recommended bio-insecticides",
                    "Erect yellow sticky traps across the field"
                ],
                "general_management": [
                    "Coordinate whitefly management across neighboring farms",
                    "Follow university IPM protocols"
                ],
                "prevention": [
                    "Sow only certified CLCuV-resistant Bt cotton hybrids",
                    "Eradicate weed hosts from field borders and water channels",
                    "Maintain balanced N-P-K nutrition"
                ],
                "when_to_contact_expert": "If vein enations appear on young plants within 45 days of germination."
            }
        ]

        for d in diseases_data:
            crop_obj = crop_objs[d["crop_name"]]
            disease_obj = Disease(
                crop_id=crop_obj.id,
                name=d["name"],
                hindi_name=d["hindi_name"],
                scientific_name=d["scientific_name"],
                severity_level=d["severity_level"],
                description=d["description"],
                symptoms=json.dumps(d["symptoms"]),
                possible_causes=json.dumps(d["possible_causes"]),
                favorable_conditions=json.dumps(d["favorable_conditions"]),
                immediate_actions=json.dumps(d["immediate_actions"]),
                general_management=json.dumps(d["general_management"]),
                prevention=json.dumps(d["prevention"]),
                when_to_contact_expert=d["when_to_contact_expert"]
            )
            db.add(disease_obj)

        # 5. Add sample historical scans for Demo
        db.flush()
        sample_scans = [
            ScanHistory(
                user_id=1,
                crop="Tomato",
                image_url="/sample_leaves/sample_tomato_blight.jpg",
                predicted_disease="Tomato Leaf Blight",
                confidence=0.94,
                severity="Medium",
                follow_up_data=json.dumps({"growth_stage": "Fruiting", "rainfall": "Moderate", "irrigation": "Every 2 days", "duration": "4 days"}),
                generated_explanation="Possible reasons include excess moisture, high humidity, prolonged leaf wetness, and poor air circulation.",
                symptoms_summary=json.dumps(["Brown spots on leaves", "Leaf discoloration", "Drying of affected areas"]),
                immediate_actions_summary=json.dumps(["Remove severely affected leaves", "Improve air circulation", "Avoid unnecessary leaf wetting"]),
                prevention_summary=json.dumps(["Inspect crops regularly", "Maintain proper spacing", "Use healthy planting material"]),
                district="Pune District",
                is_synced=True
            ),
            ScanHistory(
                user_id=1,
                crop="Potato",
                image_url="/sample_leaves/sample_potato_blight.jpg",
                predicted_disease="Potato Early Blight",
                confidence=0.88,
                severity="Medium",
                follow_up_data=json.dumps({"growth_stage": "Vegetative", "rainfall": "None", "irrigation": "Weekly", "duration": "6 days"}),
                generated_explanation="Possible reasons include alternating dry and wet weather, poor soil drainage, and fungal spores surviving from previous solanaceous crops.",
                symptoms_summary=json.dumps(["Target-board dark concentric rings", "Chlorotic yellow margins", "Lower foliage browning"]),
                immediate_actions_summary=json.dumps(["Avoid sprinkler wetting late in the day", "Prune lower dying foliage", "Ensure potassium balance"]),
                prevention_summary=json.dumps(["Use certified disease-free tubers", "3-year crop rotation", "Hill soil properly"]),
                district="Nashik District",
                is_synced=True
            ),
            ScanHistory(
                user_id=4,
                farmer_name="Harish Patel",
                farmer_phone="9823456789",
                crop="Rice",
                image_url="/sample_leaves/sample_rice_blast.jpg",
                predicted_disease="Rice Blast",
                confidence=0.91,
                severity="High",
                follow_up_data=json.dumps({"growth_stage": "Tillering", "rainfall": "Heavy", "irrigation": "Flooded", "duration": "3 days"}),
                generated_explanation="Possible reasons include excess nitrogen fertilizer, continuous drizzle with high humidity (>90%), and dense seedling density.",
                symptoms_summary=json.dumps(["Spindle-shaped diamond lesions", "Gray centers with red borders", "Leaf tip drying"]),
                immediate_actions_summary=json.dumps(["Halt additional urea fertilizer immediately", "Drain stagnant water to shallow depth", "Spray recommended bio-agent"]),
                prevention_summary=json.dumps(["Seed treatment with biocontrol", "Adopt resistant varieties", "Balanced silicon and potassium"]),
                district="Karnal District",
                is_synced=True
            )
        ]
        db.add_all(sample_scans)

        db.commit()
        print("Database seeded successfully with crops, diseases, sample users, and scans.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
