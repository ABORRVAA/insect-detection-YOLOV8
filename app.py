from flask import Flask, render_template, request, redirect, session
from ultralytics import YOLO
import cv2
import os
import mysql.connector

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secretkey'  # Secret key for sessions

# Load YOLOv8 model
model = YOLO("best_model.pt")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Apsara@13ams",  # Update this with your actual MySQL password
    database="farmers"
)
cursor = conn.cursor(dictionary=True)

# Custom messages based on insect class
def get_message(label_names):
    # Add debug print to see what's being detected
    print("Detected labels:", label_names)
    
    messages = {
        "Rice Weevil": """________________________________________
🐞 Name of Insect:
Rice Weevil (Sitophilus oryzae)
________________________________________
🌾 Crops It Affects:
•	Rice
•	Wheat
•	Maize (Corn)
•	Barley
•	Sorghum
•	Oats
•	Rye
•	Processed cereals and stored grains
________________________________________
⚠ Symptoms and Damage It Causes:
•	Adult weevils bore into whole grains to lay eggs.
•	Larvae feed inside the grain, hollowing it out from the inside.
•	Infested grain appears:
o	With small round exit holes
o	Powdery residues or grain dust
o	Unpleasant odor
•	Causes loss of weight, nutritional value, and seed viability.
•	May lead to secondary fungal/mold infestation due to moisture buildup.
•	Hidden infestation is common – grains may look normal outside.
________________________________________
🧹 Immediate Removal Methods:
1.	Sun-dry the infested grain to kill larvae and adults (3–4 hours, 2–3 days).
2.	Winnow or sieve to remove broken grains and adult weevils.
3.	Fumigation with aluminum phosphide tablets (only with certified applicators).
4.	Discard heavily infested grain – do not mix with good stock.
5.	Vacuum-clean and sanitize storage spaces thoroughly.
________________________________________
🛡 Prevention Steps:
•	Store only well-dried (below 12% moisture) and unbroken grains.
•	Use airtight metal or plastic containers; avoid porous materials like jute.
•	Add natural repellents like:
o	Neem leaves or neem powder
o	Bay leaves or curry leaves
o	Turmeric powder (dry)
•	Use inert dusts like diatomaceous earth or ash (safe and food-grade).
•	Avoid excess nitrogen fertilizer in the field, which may increase susceptibility.
________________________________________
🔁 Future Precautions:
•	Practice FIFO (First In, First Out) to avoid long-term stagnation.
•	Never mix new grain with old stock unless both are inspected and clean.
•	Regularly monitor grain using traps, or by sampling and soaking test.
•	Rotate crops and avoid planting susceptible cereals repeatedly on the same land.
________________________________________
🏠 🔒 Storage Precautions (Essential for Long-Term Storage):
🏗 1. Storage Structure:
•	Use sealed metal bins, HDPE drums, or hermetic bags (e.g., PICS).
•	Avoid direct floor storage—place bags on wooden pallets.
•	Ensure structures are well-ventilated, dry, and protected from rain.
🧹 2. Sanitation:
•	Before each storage season:
o	Clean godowns thoroughly—remove old residues, dust, and dead insects.
o	Disinfect bins using hot water or approved grain-safe insecticides.
•	Clean tools, sacks, and weighing machines regularly.
🌡 3. Environmental Control:
•	Maintain cool, dry conditions (weevils thrive in warm and moist environments).
•	Use exhaust fans, blowers, or dehumidifiers if storing at scale.
•	Keep room humidity below 60%.
🔎 4. Monitoring & Early Detection:
•	Install light traps or sticky traps to catch adults.
•	Inspect grains monthly for:
o	Exit holes
o	Grain powder
o	Live weevils crawling in bags
📦 5. Packaging & Labeling:
•	Use double-lined bags (plastic-lined jute or multi-layered sacks).
•	Clearly label bags with storage date and crop variety.
•	Use tight stitching and stack in a crisscross manner to allow airflow.
________________________________________
✅ Bonus Tip (For Farmers):
To check for hidden rice weevils:
Put 100g of grains in a glass of water. Wait 10 minutes — floating grains may be infested.
________________________________________
""",
        "Angoumois grain moth": """"🦋 Name of Insect:
Angoumois Grain Moth (Sitotroga cerealella)

🌾 Crops It Affects:
• Rice
• Wheat
• Maize (Corn)
• Barley
• Sorghum
• Oats
• Rye
• Stored and whole cereal grains

⚠ Symptoms and Damage It Causes:
• Females lay eggs on or near whole grains.
• Larvae bore into the grain and feed inside, making it hollow.
• Exit holes appear when larvae mature and moths emerge.
• Infested grains may look dusty, light, or break easily.
• Damaged grains are unfit for consumption or planting.
• May lead to reduced grain germination.

🧹 Immediate Removal Methods:

Sun-dry grains for 3–4 hours over 2–3 days to kill eggs and larvae.

Sieve and winnow grains to remove damaged or light-weight kernels.

Use pheromone or light traps to catch adult moths.

Fumigation using aluminum phosphide (by certified professionals only).

Dispose of heavily infested grain — do not mix with good stock.

🛡 Prevention Steps:
• Store only clean, well-dried grains (moisture <12%).
• Use sealed, airtight containers (metal/plastic).
• Add repellents like neem leaves, dry turmeric powder, or bay leaves.
• Use food-safe inert dusts like diatomaceous earth.
• Avoid storing grains in damp or humid environments.

🔁 Future Precautions:
• Practice FIFO (First In, First Out).
• Do not mix new grain with old stock unless both are inspected.
• Regularly monitor for signs like dust, webbing, or moth sightings.
• Rotate cereal crops in the field to break pest cycles.

🏠 🔒 Storage Precautions (Essential for Long-Term Storage):
🏗 1. Storage Structure:
• Use hermetic bags or sealed metal bins.
• Avoid direct contact with floor—place bags on pallets.
🧹 2. Sanitation:
• Clean storage rooms and bins before use.
• Sanitize equipment and sacks.
🌡 3. Environmental Control:
• Store in cool, dry spaces.
• Use fans or dehumidifiers to control humidity (<60%).
🔎 4. Monitoring & Early Detection:
• Use traps and check for flying moths.
• Inspect grains monthly for holes or moth activity.
📦 5. Packaging & Labeling:
• Use double-lined bags.
• Label storage date and crop variety.
• Stack bags in cross-layered format for airflow.

✅ Bonus Tip (For Farmers):
To detect hidden moth damage: Soak grains in water. Floating grains may be infested from inside.""",
        "Indian meal mouth adult":""""🦋 Name of Insect:
Indian Meal Moth (Adult) (Plodia interpunctella)

🌾 Crops It Affects:
• Wheat
• Rice
• Corn
• Dried fruits
• Nuts
• Pet foods
• Chocolates and other stored dry foods

⚠ Symptoms and Damage It Causes:
• Adults lay eggs on exposed grain or packaged goods.
• Larvae spin silk, causing webbing and clumping of grains.
• Grain becomes moldy or clumped due to webbing and moisture.
• Adult moths seen flying around kitchen or storehouse.
• Foul smell and contamination make grains inedible.

🧹 Immediate Removal Methods:

Discard all infested and webbed food items.

Vacuum-clean storage areas and containers.

Use pheromone/sticky traps to trap adults.

Wipe shelves with vinegar or soapy water.

Deep-clean surrounding areas where moths are seen.

🛡 Prevention Steps:
• Keep grains in airtight containers.
• Do not leave grains open or loosely packed.
• Use natural repellents (bay leaves, neem).
• Keep pantry clean and inspect regularly.
• Avoid mixing fresh grains with old or open packets.

🔁 Future Precautions:
• Freeze newly bought grains for 3–4 days before storage.
• Do not store food near warmth or lights.
• Regularly clean shelves and grain containers.
• Avoid storing grains near sweets, dry fruits, and nuts.

🏠 🔒 Storage Precautions (Essential for Long-Term Storage):
🏗 1. Structure:
• Use metal/plastic airtight bins.
• Keep storage units dry and cool.
🧹 2. Sanitation:
• Clean before adding new stock.
• Wipe with natural disinfectants.
🌡 3. Control Environment:
• Use fans or exhausts to remove excess heat.
• Store food in dark, low-humidity areas.
🔎 4. Monitor Early:
• Use light/pheromone traps.
• Monitor monthly.
📦 5. Package Properly:
• Use well-sealed multilayered bags or containers.
• Label storage and check expiry.

✅ Bonus Tip:
Adult moths are attracted to light — avoid storing grains in exposed areas with bright bulbs or tube lights.""",
        "Indian meal mouth egg": """🥚 Insect Stage:
Indian Meal Moth Egg

🌾 Crops/Food It Affects:
• Rice, wheat, corn, oats
• Chocolates, nuts, dry fruits
• Animal feed
• Processed foods and stored cereals

⚠ Symptoms and Damage It Causes:
• Eggs are laid in cracks, crevices, or on the surface of grains.
• Hatch within 2–5 days depending on temperature.
• Invisible to the naked eye — infestations go unnoticed until larvae appear.
• Infested grains become clumped with webbing over time.
• Secondary damage from mold, foul smell.

🧹 Immediate Removal Methods:

Freeze suspected grains at -18°C for 4–7 days.

Sun-dry grains in open trays (3–4 hours daily).

Clean containers with hot water and dry thoroughly.

Sieve and discard infested portions.

Do not mix with other food stocks.

🛡 Prevention Steps:
• Freeze grains before long storage.
• Use airtight, insect-proof storage.
• Add neem leaves or bay leaves to deter eggs.
• Clean shelves, corners, and lids regularly.
• Store in dry, cool conditions (humidity <60%).

🔁 Future Precautions:
• Practice monthly inspection of stored items.
• Keep grains in separate, labeled lots.
• Avoid bulk storage unless conditions are controlled.
• Rotate storage — old stock out first.

🏠 🔒 Storage Tips:
• Use sealed drums or thick plastic containers.
• Avoid moisture by drying grains after washing.
• Clean bins and bags with natural disinfectants.

✅ Bonus Tip:
Store a few bay leaves in your grain container — their strong smell can deter egg-laying by moths.""",
        "Khapara bettle": """🪲 Name of Insect:
Khapra Beetle (Trogoderma granarium)
________________________________________
🌾 Crops It Affects:
•	Wheat
•	Rice
•	Barley
•	Maize (Corn)
•	Sorghum
•	Oats
•	Pulses (Lentils, Chickpeas)
•	Oilseeds (like groundnuts)
•	Processed food products (like flour and cereal products)
________________________________________
⚠ Symptoms and Damage It Causes:
•	Feeding damage primarily caused by larvae, which graze on grain surfaces.
•	Grains appear scratched, broken, or powdery.
•	Weight loss and nutritional deterioration of stored grain.
•	Infested grains are often mixed with cast skins, hairs, and feces, making them unfit for consumption.
•	Causes heating and moisture increase, accelerating spoilage.
•	Highly resistant to many control methods and very difficult to eradicate.
•	Heavy infestations can cause up to 70% grain damage.
________________________________________
🧹 Immediate Removal Methods:
1.	Isolate and quarantine infested grains immediately.
2.	Burn or bury heavily infested stocks to prevent spread.
3.	Use fumigation with aluminum phosphide or methyl bromide (requires professional supervision and permits).
4.	Thoroughly clean storage bins and surrounding areas, removing all grain dust and residue.
5.	Apply contact insecticides on storage surfaces (approved for grain use).
________________________________________
🛡 Prevention Steps:
•	Store only dry, clean grain (less than 10% moisture).
•	Use airtight, insect-proof containers or metal bins.
•	Avoid long-term storage without periodic checking.
•	Inspect grains regularly (at least once a month).
•	Avoid storing grains near cracks, crevices, or wooden walls (where eggs can hide).
________________________________________
🔁 Future Precautions:
•	Do not mix old and new stocks; always clean storage areas between batches.
•	Practice FIFO (First In, First Out) stock rotation.
•	Treat storage areas with insecticidal sprays or dusts before loading grains.
•	Use natural deterrents like neem powder or bay leaves inside storage containers.
•	Install sticky traps or light traps for early detection.
•	If large-scale storage, temperature control (cooling) can reduce insect survival.
________________________________________
""",
        "Khapara bettle larva": """🐛 Name of Insect Stage:
Khapra Beetle Larva
Scientific Name: Trogoderma granarium (Larval stage)
________________________________________
🔍 Identification Features:
Feature	Description
Color	Pale yellow to golden-brown body with a dark brown head
Size	1.6 mm to 5 mm (grows with age)
Shape	Elongated, flattened, hairy body
Distinctive Trait	Two tufts of long bristles at the rear end
Movement	Crawls slowly; avoids light and hides in cracks, grain dust, and crevices
________________________________________
🔁 Life Cycle Overview:
Stage	Duration	Description
Egg	4–6 days	Laid in grain dust, cracks, or near food source
Larva	20–40+ days	Most destructive stage; feeds aggressively and sheds hairs
Pupa	3–7 days	Pupates in grain debris or crevices
Adult	5–10 days lifespan	Adults do not feed; they only reproduce
🔸 Larvae can enter a diapause (hibernation-like) state and survive up to 7 years without food or water.
________________________________________
⚠ Symptoms and Damage Caused by Larvae:
•	Feeds on grain surface, flour, cereal dust, and broken grains
•	Results in powdered grain, contamination, and bad odor
•	Grain loses weight and quality
•	Infested grain contains:
o	Larval hairs
o	Cast skins
o	Fecal matter
•	Increases moisture and heat, leading to fungal growth
•	Health hazard: Larval hairs may cause allergic reactions, asthma, or dermatitis in humans
________________________________________
🧹 Immediate Removal & Control Methods:
1.	Isolate infested stock immediately to avoid spreading.
2.	Fumigation using:
o	Aluminum phosphide tablets (must be applied by licensed professionals)
o	Methyl bromide (in countries where permitted)
3.	Burn or deeply bury heavily infested grain.
4.	Heat treatment:
o	Expose grains to 60°C for 1 hour or more
5.	Cold treatment:
o	Store at –10°C for 7 days to kill larvae in diapause
6.	Apply diatomaceous earth to grain and storage areas to dehydrate larvae.
7.	Vacuum cracks, corners, and shelves of all residue, cobwebs, and dust.
________________________________________
🛡 Prevention Steps:
•	Store only dry, clean, and deinfested grains
•	Maintain grain moisture below 10%
•	Use metal or hermetically sealed plastic bins
•	Clean and disinfect storage rooms thoroughly before every season
•	Use natural repellents like:
o	Neem leaf powder
o	Turmeric powder (dry)
o	Bay leaves (as insect deterrent)
•	Regular monitoring with sticky traps or visual inspections
________________________________________
🔁 Future Precautions:
•	Never mix old and new stock
•	Rotate stock regularly — follow FIFO (First In, First Out)
•	Ensure no cracks or crevices are left untreated in storage units
•	Install mesh screens or nets in windows and vents to prevent entry of flying pests
•	Use pest-proof packaging (triple-layer bags, plastic-lined sacks)
________________________________________
🏠 Storage Precautions (Focused on Larvae):
Area	Precaution
Containers	Use airtight bins; avoid jute or cloth bags unless lined with plastic
Environment	Keep storage rooms cool, dry, and dark
Structure	Seal all cracks, crevices, and wall joints
Monitoring	Regular inspections every 2–4 weeks
Hygiene	Deep clean floors, corners, ceilings, shelves — vacuum preferred
________________________________________
✅ Pro Tip (For Farmers/Traders):
Sprinkle a small amount of neem leaf powder or turmeric on the top and bottom of stored grain bags as a natural larval deterrent.
________________________________________
""",
        "Lesser grain boree": """🪲 Name of Insect:
Lesser Grain Borer (Rhyzopertha dominica)
________________________________________
🌾 Crops It Affects:
•	Wheat
•	Rice
•	Barley
•	Maize (Corn)
•	Sorghum
•	Millets
•	Oats
•	Processed products (e.g., flour, cereal)
________________________________________
🔍 Identification:
Life Stage	Appearance
Adult	Small (2–3 mm), dark brown to black, cylindrical body with a bumpy thorax covering the head
Larva	Creamy white, grub-like, soft-bodied, hidden inside grain
Other Traits	Adults are strong fliers and emit a musty odor in infested grain
________________________________________
⚠ Symptoms and Damage It Causes:
•	Bores into whole grains; both larvae and adults feed inside
•	Converts grain to fine powder or frass from the inside out
•	Grains become hollow and brittle, often with tiny round exit holes
•	Results in:
o	Weight loss
o	Nutritional degradation
o	Complete disintegration of seeds
•	Can cause up to 50% grain loss in 3–6 months
•	Infestation causes musty odor and may promote mold growth
________________________________________
🧬 Life Cycle Overview:
Stage	Duration (Approx.)
Egg	3–5 days
Larva	2–3 weeks (inside grain)
Pupa	1 week
Adult	Lives up to 2–3 months; lays 300–500 eggs
Note: Entire lifecycle can complete in ~30–40 days under warm conditions (30–35°C)
________________________________________
🧹 Immediate Removal & Control Methods:
1.	Sun-dry infested grains for 2–3 days to kill internal larvae
2.	Sieve and winnow to remove damaged grains and debris
3.	Fumigation:
o	Use aluminum phosphide tablets in sealed environments (licensed application only)
4.	Cold treatment: Store grain at <15°C to halt reproduction
5.	Use Diatomaceous Earth (DE) as a safe, non-chemical grain protectant
6.	Clean and sanitize all containers, tools, and floors used for storage
________________________________________
🛡 Prevention Steps:
•	Store only dry grains (moisture < 12%)
•	Use hermetically sealed bags (e.g., PICS, GrainPro)
•	Apply neem leaf powder or turmeric as natural grain protectants
•	Keep grains in air-tight, insect-proof containers
•	Install UV light or pheromone traps for monitoring
________________________________________
🔁 Future Precautions:
•	Never mix new grain with old grain
•	Follow FIFO (First In, First Out) for stock rotation
•	Inspect monthly for odor, frass, and exit holes
•	Clean storage rooms thoroughly before refilling
•	Avoid storing near heat sources, grain dust, or wooden structures
________________________________________
🏠 Storage Precautions (Essential):
Area	Action
Structure	Use sealed metal bins, barrels, or triple-layer bags
Sanitation	Clean floors, walls, tools, and bins before every storage cycle
Ventilation	Maintain dry, cool airflow; avoid condensation
Elevated Bags	Use pallets to store grain bags off the floor
Detection	Place sticky traps or pheromone traps to catch adults early
________________________________________
✅ Simple Alert Message (Summary):
“Lesser grain borer detected! 🪲
Cause: Turns grains to powder internally.
Prevention: Store dry & airtight. Use neem or DE. Inspect monthly.”**
________________________________________
""",
        "Sawtoothed":"""🪲 Name of Insect:
Sawtoothed Grain Beetle (Oryzaephilus surinamensis)
________________________________________
🌾 Crops & Products It Affects:
•	Cereal grains (rice, wheat, oats, barley, maize)
•	Processed grains (flour, semolina, bran)
•	Dry fruits and nuts
•	Pulses and spices
•	Pet foods, packaged foods, and pasta products
•	Can also infest packaged food products in stores or homes
________________________________________
🔍 Identification:
Life Stage	Appearance
Adult	2.5–3.5 mm, flat, brown, with six saw-like projections (teeth) on each side of the thorax
Larva	Yellowish-white, small, slender, with brown head; up to 3 mm long
Other Traits	Adults are very fast movers and can crawl through tiny cracks in packaging
________________________________________
⚠ Symptoms and Damage It Causes:
•	Feeds on broken grains, grain dust, and processed food — does not infest whole sound grains
•	Causes:
o	Heating and moisture buildup in stored grains
o	Clumping, mold, and bad odor in food stock
o	Contamination with live beetles, cast skins, and fecal matter
•	Reduces grain quality, making it unfit for human or animal consumption
________________________________________
🧬 Life Cycle Overview:
Stage	Duration (Approx.)
Egg	3–5 days
Larva	2–3 weeks
Pupa	1 week
Adult	Lives up to 6–10 months; females lay 250–300 eggs in grain dust or crevices
🌀 Favorable Conditions:
•	Temperature: 25–35°C, Humidity: 60–75%
________________________________________
🧹 Immediate Removal & Control Methods:
1.	Sieve and winnow grains to remove dust, broken grains, and beetles
2.	Sun-dry the grain for 2–3 days to kill larvae and slow beetle activity
3.	Vacuum-clean and sanitize storage bins, cracks, and corners thoroughly
4.	Fumigation:
o	Use aluminum phosphide or CO₂ treatment under expert supervision
5.	Cold storage below 10°C can help prevent development and kill larvae
________________________________________
🛡 Prevention Steps:
•	Store only clean, unbroken, and dried grains (moisture < 12%)
•	Avoid keeping dusty or broken food items near clean grain
•	Use air-tight metal bins, HDPE containers, or hermetic bags
•	Place bay leaves, neem leaves, cloves, or turmeric powder inside storage
•	Install sticky traps or light traps for early detection
________________________________________
🔁 Future Precautions:
•	Never mix new grain with old stock
•	Follow FIFO (First In, First Out) to rotate storage
•	Monitor every 2–4 weeks for signs of contamination
•	Keep storage area free from open packages, spillage, or flour residues
•	Avoid overstocking and inspect unopened packages in retail or warehouse areas
________________________________________
🏠 Storage Precautions (Critical):
Aspect	Best Practice
Storage Area	Clean, dry, cool room with no cracks or crevices
Containers	Use sealed, pest-proof containers or lined sacks
Sanitation	Clean shelves, corners, and floors before and after each storage cycle
Humidity & Temp	Maintain humidity below 60% and temperature below 25°C
Inspection	Monthly visual checks for live beetles or powder in corners
Packaging	Avoid torn, dusty, or loosely closed bags in storage and retail shops
________________________________________
✅ Quick Alert Summary:
Sawtoothed Grain Beetle Detected! 🪲
Cause: Infests broken grains, processed foods, and packaged items.
Prevention: Store only dry, unbroken grain in airtight bins. Inspect monthly. Use neem/cloves as natural protectants.
________________________________________

""",
        "tobaco bettle": """🐞 Name of Insect:
Tobacco Beetle (Lasioderma serricorne)
Also known as: Cigarette Beetle
________________________________________
🌾 Crops & Products It Affects:
•	Tobacco leaves and cigarettes
•	Cereal grains (rice, wheat, maize)
•	Pulses
•	Flour, semolina, bread, biscuits
•	Spices (chilli, turmeric, coriander)
•	Dried fruits & nuts
•	Animal feeds
•	Books, dried flowers, museum specimens
________________________________________
🔍 Identification:
Life Stage	Description
Adult	Small (2–3 mm), reddish-brown, oval, hump-backed beetle with a fuzzy appearance
Larva	Creamy white, C-shaped, with a hairy body and brown head, up to 3 mm long
Movement	Adults are strong fliers and attracted to light; larvae move slowly in food
________________________________________
⚠ Symptoms and Damage It Causes:
•	Larvae bore into stored materials, reducing them to dust or frass
•	Grains and tobacco become powdery, often with small holes
•	Infested products may have bad odor and be webbed or moldy
•	Larval feeding contaminates food with frass (waste), cast skins, and hairs
•	Adults do not feed but lay eggs in stored products
•	Can destroy entire batches of processed foods or stored herbs if left unchecked
________________________________________
🧬 Life Cycle Overview:
Stage	Duration (Approx.)
Egg	6–10 days
Larva	4–6 weeks (feeding stage)
Pupa	1–2 weeks
Adult	Lives 2–4 weeks; females lay 30–100 eggs
🌀 Ideal conditions for reproduction:
Temperature: 28–35°C, Humidity: 70–80%
________________________________________
🧹 Immediate Removal & Control Methods:
1.	Identify and isolate infested materials immediately
2.	Sun-dry infested items (grains, spices, leaves) for 2–3 days
3.	Sieve, winnow, and discard contaminated materials
4.	Fumigation:
o	Use aluminum phosphide tablets (licensed personnel only)
o	Smaller items (like tobacco packs) can be sealed in bags with dry ice or CO₂ treatment
5.	Freeze small batches (–10°C for 5–7 days) to kill eggs and larvae
________________________________________
🛡 Prevention Steps:
•	Store food items in airtight containers (glass jars, plastic drums, metal bins)
•	Keep storage rooms dry and cool (below 60% humidity)
•	Place neem leaves, cloves, or dried bay leaves in stored items (natural deterrents)
•	Use UV light traps to detect flying adults
•	Apply diatomaceous earth or neem-based dusts in dry storage areas
________________________________________
🔁 Future Precautions:
•	Clean storage shelves and bins before and after every use
•	Avoid mixing old and new batches of grains, spices, or tobacco
•	Rotate stocks regularly — follow FIFO (First In, First Out)
•	Label and date stored items for inspection
•	Regularly inspect for:
o	Holes in packaging
o	Dust or powder at base
o	Tiny beetles flying near lights
________________________________________
🏠 Storage Precautions (Critical):
Storage Area	Action
Containers	Use air-tight, insect-proof containers (glass, metal, HDPE)
Structure	Keep rooms dry, sealed, and well-ventilated
Temperature	Ideal < 25°C; use fans or cold rooms if possible
Sanitation	Remove dust, residues, and sweep corners frequently
Inspection	Monthly checks for webbing, frass, beetles, and larvae
Pest Entry	Use mesh on windows and keep lights away from open stock areas (adults are light-attracted)
________________________________________
✅ Simple Alert Summary:
Tobacco Beetle detected! 🐞
Cause: Larvae bore into grains and spices, leaving powder and odor.
Prevention: Store dry, sealed, and inspect monthly. Use natural repellents like neem or cloves.
_______________________________________"""
    }
    
    # Check for exact matches first
    for name in label_names:
        print(f"Checking label: {name}")  # Debug print
        if name in messages:
            return messages[name]
            
    return "✅ No harmful insects detected."

# Home/Login Page
@app.route('/')
def home():
    return render_template("index.html", result_image=None, message=None)

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
        if cursor.fetchone():
            return render_template("register.html", error="User already exists")

        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, password)
        )
        conn.commit()
        return redirect('/')  # Redirect to login after successful registration

    return render_template("register.html")

# Login handler
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']

    # Validate user
    cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s", (name, password))
    user = cursor.fetchone()

    if user:
        session['name'] = user['name']
        session['email'] = user['email']
        session['phone'] = user['phone']
        return redirect('/dashboard')
    else:
        return render_template("index.html", error="❌ User not found or incorrect password.")

# Insect Detection Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'name' not in session:
        return redirect('/')

    message = None
    result_path = None

    if request.method == 'POST':
        image = request.files['image']
        image_path = 'static/uploaded.jpg'
        image.save(image_path)

        # Inference with YOLO
        img = cv2.imread(image_path)
        results = model.predict(img, conf=0.25)
        
        # Debug prints
        print("Model names:", model.names)
        label_names = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls)
                label = model.names[cls]
                label_names.append(label)
                print(f"Detected class: {cls}, label: {label}")
        
        # Save annotated image
        annotated = results[0].plot()
        result_path = 'static/result.jpg'
        cv2.imwrite(result_path, annotated)

        message = get_message(label_names)

    return render_template("dashboard.html", name=session['name'], result_image=result_path, message=message)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
