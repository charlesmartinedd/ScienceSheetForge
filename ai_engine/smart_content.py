"""
Smart Content Engine - Intelligent Templates for TPT-Quality Worksheets
Works reliably without API dependencies
Creates unique, engaging content every time
"""

import random
from typing import List, Dict, Tuple, Optional


class SmartContentEngine:
    """Generate engaging educational content using intelligent templates"""

    def __init__(self):
        self.init_content_databases()

    def init_content_databases(self):
        """Initialize comprehensive content databases"""

        # Science vocabulary with rich definitions
        self.vocab_database = {
            # Cell Biology
            "cell": {
                "definition": "The smallest unit of life that can function independently",
                "kid_friendly": "The tiny building block that all living things are made of",
                "fun_fact": "Your body has over 37 trillion cells!",
                "example": "A cell is like a tiny factory that makes everything your body needs."
            },
            "nucleus": {
                "definition": "The control center of the cell that contains DNA",
                "kid_friendly": "The brain of the cell that tells it what to do",
                "fun_fact": "The nucleus contains all your genetic information!",
                "example": "The nucleus is like the principal's office in a school."
            },
            "mitochondria": {
                "definition": "The powerhouse organelle that produces energy (ATP)",
                "kid_friendly": "The tiny power plant inside cells that makes energy",
                "fun_fact": "Mitochondria have their own DNA separate from the nucleus!",
                "example": "Mitochondria are like tiny batteries that keep cells running."
            },
            "chloroplast": {
                "definition": "Green organelle in plant cells where photosynthesis occurs",
                "kid_friendly": "The part of plant cells that makes food from sunlight",
                "fun_fact": "Chloroplasts are what make plants green!",
                "example": "Chloroplasts are like solar panels that capture sunlight."
            },
            "membrane": {
                "definition": "Thin barrier that surrounds and protects the cell",
                "kid_friendly": "The skin around a cell that controls what goes in and out",
                "fun_fact": "Cell membranes are only 2 molecules thick!",
                "example": "The cell membrane is like a security guard at a building entrance."
            },
            "cytoplasm": {
                "definition": "Jelly-like substance that fills the cell",
                "kid_friendly": "The gooey stuff inside cells where things float around",
                "fun_fact": "Cytoplasm is about 70% water!",
                "example": "Cytoplasm is like the air inside a room where everything moves."
            },
            "ribosome": {
                "definition": "Tiny structure that builds proteins in the cell",
                "kid_friendly": "The protein-making machine inside cells",
                "fun_fact": "Ribosomes are some of the smallest parts of a cell!",
                "example": "Ribosomes are like workers on an assembly line building products."
            },
            "vacuole": {
                "definition": "Storage sac in cells, especially large in plant cells",
                "kid_friendly": "The storage container inside cells",
                "fun_fact": "Plant vacuoles can take up 90% of the cell!",
                "example": "A vacuole is like a backpack where the cell stores supplies."
            },

            # General Biology
            "organism": {
                "definition": "Any living thing, from bacteria to blue whales",
                "kid_friendly": "Any living creature big or small",
                "fun_fact": "There are over 8.7 million species of organisms!",
                "example": "You, your pet, and even tiny bacteria are all organisms."
            },
            "tissue": {
                "definition": "Group of similar cells working together",
                "kid_friendly": "A team of cells doing the same job",
                "fun_fact": "Your skin is your body's largest tissue!",
                "example": "Muscle tissue is made of cells that work together to move your body."
            },
            "organ": {
                "definition": "Body part made of different tissues working together",
                "kid_friendly": "A body part with an important job",
                "fun_fact": "Your heart beats about 100,000 times per day!",
                "example": "Your stomach is an organ that helps digest food."
            },
            "system": {
                "definition": "Group of organs that work together for a function",
                "kid_friendly": "Organs teaming up to do big jobs in your body",
                "fun_fact": "Your digestive system is over 30 feet long!",
                "example": "Your circulatory system includes your heart and blood vessels."
            },

            # Molecular Biology
            "dna": {
                "definition": "Molecule that carries genetic instructions for life",
                "kid_friendly": "The instruction manual for building living things",
                "fun_fact": "If you uncoiled all your DNA, it would reach the sun and back 600 times!",
                "example": "DNA is like a recipe book that tells cells how to make you."
            },
            "protein": {
                "definition": "Large molecule made of amino acids that does work in cells",
                "kid_friendly": "Important molecules that help your body work",
                "fun_fact": "Proteins can do thousands of different jobs in your body!",
                "example": "Proteins are like tools that help build and fix your body."
            },
            "enzyme": {
                "definition": "Protein that speeds up chemical reactions in cells",
                "kid_friendly": "Special proteins that help chemical reactions happen faster",
                "fun_fact": "Enzymes can work millions of times faster than without them!",
                "example": "Enzymes are like assistants that help get work done quickly."
            },

            # Energy & Processes
            "energy": {
                "definition": "The ability to do work or cause change",
                "kid_friendly": "The power needed to make things happen",
                "fun_fact": "All energy on Earth originally comes from the Sun!",
                "example": "You use energy from food to run, play, and think."
            },
            "atp": {
                "definition": "Energy molecule that powers most cellular processes",
                "kid_friendly": "The energy currency that cells use",
                "fun_fact": "Your body makes and uses your body weight in ATP every day!",
                "example": "ATP is like the coins you use to pay for things in cells."
            },
            "photosynthesis": {
                "definition": "Process where plants make food using sunlight",
                "kid_friendly": "How plants turn sunlight into food",
                "fun_fact": "Photosynthesis produces all the oxygen we breathe!",
                "example": "Photosynthesis is like cooking food using only sunlight and air."
            },
            "respiration": {
                "definition": "Process that releases energy from food molecules",
                "kid_friendly": "How cells break down food to get energy",
                "fun_fact": "You breathe out carbon dioxide made during respiration!",
                "example": "Respiration is like burning fuel to power an engine."
            },
            "glucose": {
                "definition": "Simple sugar that is the main energy source for cells",
                "kid_friendly": "A type of sugar that gives cells energy",
                "fun_fact": "Your brain uses about half of your body's glucose!",
                "example": "Glucose is like gasoline that powers your body's cells."
            },
            "oxygen": {
                "definition": "Gas that animals breathe in and plants produce",
                "kid_friendly": "The air we breathe that keeps us alive",
                "fun_fact": "Oxygen makes up 21% of the air we breathe!",
                "example": "Your body needs oxygen like a fire needs air to keep burning."
            },
            "weathering": {
                "definition": "The breaking down of rocks into smaller pieces by wind, water, or ice",
                "kid_friendly": "When weather slowly breaks rocks apart",
                "fun_fact": "Tree roots can weather rocks by growing into cracks.",
                "example": "Rainwater freezes in rock cracks and causes weathering."
            },
            "erosion": {
                "definition": "Movement of weathered rock and soil by water, wind, gravity, or ice",
                "kid_friendly": "When bits of earth get carried away",
                "fun_fact": "The Grand Canyon was carved deeper every year by erosion.",
                "example": "Ocean waves erode beaches and move sand down the shore."
            },
            "sediment": {
                "definition": "Small particles of rock, soil, or organic matter dropped by erosion",
                "kid_friendly": "Tiny pieces of rock that settle in layers",
                "fun_fact": "Sediment layers can trap fossils for millions of years.",
                "example": "Sediment collects at the bottom of rivers and forms deltas."
            },
            "magma": {
                "definition": "Molten rock located beneath Earth's crust",
                "kid_friendly": "Hot melted rock deep underground",
                "fun_fact": "Magma chambers can be as wide as entire cities.",
                "example": "Magma rises toward the surface and erupts from volcanoes."
            },
            "lava": {
                "definition": "Molten rock that erupts onto Earth's surface",
                "kid_friendly": "Melted rock that flows out of a volcano",
                "fun_fact": "Lava can reach temperatures over 2,000°F (1,100°C).",
                "example": "Basalt rock forms when lava cools quickly."
            },
            "volcano": {
                "definition": "A mountain that can erupt and release magma, ash, and gases",
                "kid_friendly": "A mountain that can explode or ooze hot rock",
                "fun_fact": "About 1,500 volcanoes on Earth are considered active.",
                "example": "Mount St. Helens erupted in Washington State in 1980."
            },
            "earthquake": {
                "definition": "A sudden shaking of Earth's surface caused by tectonic plate movement",
                "kid_friendly": "When the ground shakes because Earth's plates move",
                "fun_fact": "Earthquakes can make the ground shift several meters in seconds.",
                "example": "Earthquakes are common along the Ring of Fire in the Pacific."
            },
            "tectonic plates": {
                "definition": "Large pieces of Earth's crust that move slowly over the mantle",
                "kid_friendly": "Huge puzzle pieces of Earth's crust that slowly slide around",
                "fun_fact": "Tectonic plates move about as fast as fingernails grow.",
                "example": "The Pacific Plate pushes against the North American Plate."
            },
            "climate": {
                "definition": "The long-term pattern of temperature and precipitation in an area",
                "kid_friendly": "The usual weather a place has year after year",
                "fun_fact": "Scientists study climate patterns using ice cores from glaciers.",
                "example": "Rainforests have a warm, wet climate all year long."
            },
            "precipitation": {
                "definition": "Water that falls from the atmosphere as rain, snow, sleet, or hail",
                "kid_friendly": "Water that falls from clouds to the ground",
                "fun_fact": "Some storms can drop hailstones the size of baseballs.",
                "example": "Precipitation replenishes rivers, lakes, and groundwater."
            },
            "evaporation": {
                "definition": "Process where liquid water absorbs energy and becomes water vapor",
                "kid_friendly": "When water turns into gas and floats into the air",
                "fun_fact": "Sunlight speeds up evaporation from oceans and puddles.",
                "example": "Evaporation from oceans drives Earth's water cycle."
            },
            "condensation": {
                "definition": "Process where water vapor cools and turns into liquid water droplets",
                "kid_friendly": "When water in the air cools and turns back into drops",
                "fun_fact": "Clouds form when water vapor condenses high in the sky.",
                "example": "Condensation makes drops on the outside of a cold glass."
            },
            "meteorologist": {
                "definition": "A scientist who studies weather and forecasts atmospheric conditions",
                "kid_friendly": "A scientist who studies and predicts the weather",
                "fun_fact": "Meteorologists use satellites and radar to track storms.",
                "example": "The meteorologist warned the town about the approaching hurricane."
            },
            "gravity": {
                "definition": "The force of attraction between objects that have mass",
                "kid_friendly": "The pull that keeps us on the ground",
                "fun_fact": "Gravity on the Moon is only about one-sixth as strong as on Earth.",
                "example": "Gravity makes dropped objects fall toward Earth's center."
            },
            "force": {
                "definition": "A push or pull that can change an object's motion",
                "kid_friendly": "Any push or pull on something",
                "fun_fact": "Forces always come in pairs—equal and opposite reactions.",
                "example": "Kicking a soccer ball applies force that makes it move."
            },
            "friction": {
                "definition": "A force that resists motion between surfaces that rub together",
                "kid_friendly": "A force that slows things down when they rub",
                "fun_fact": "Tires rely on friction to grip the road and stop safely.",
                "example": "Sliding on ice is easier because there is less friction."
            },
            "inertia": {
                "definition": "The tendency of an object to resist changes in motion",
                "kid_friendly": "Objects want to keep doing what they are doing",
                "fun_fact": "Seatbelts help protect people by overcoming inertia in a sudden stop.",
                "example": "A ball at rest stays still until a force pushes it."
            },
            "velocity": {
                "definition": "Speed of an object in a particular direction",
                "kid_friendly": "How fast something moves and which way it goes",
                "fun_fact": "The International Space Station travels at a velocity of 17,500 mph.",
                "example": "Running north at 5 miles per hour is a velocity."
            },
            "acceleration": {
                "definition": "How quickly velocity changes over time",
                "kid_friendly": "How fast something speeds up, slows down, or turns",
                "fun_fact": "Roller coasters use acceleration to create thrilling drops.",
                "example": "A bike accelerates when you pedal harder uphill."
            },
            "mass": {
                "definition": "The amount of matter in an object",
                "kid_friendly": "How much stuff is in something",
                "fun_fact": "Your mass stays the same even if you travel to the Moon.",
                "example": "A bowling ball has more mass than a basketball."
            },
            "density": {
                "definition": "A measure of how much mass is packed into a certain volume",
                "kid_friendly": "How tightly packed the matter in something is",
                "fun_fact": "Oil floats on water because it is less dense.",
                "example": "Ice is less dense than liquid water, so ice cubes float."
            },
            "temperature": {
                "definition": "A measure of how hot or cold something is",
                "kid_friendly": "How warm or chilly something feels",
                "fun_fact": "The Sun’s surface temperature is about 5,500°C.",
                "example": "A thermometer measures air temperature every day."
            },
            "conduction": {
                "definition": "Transfer of heat through direct contact between materials",
                "kid_friendly": "Heat moving when things touch",
                "fun_fact": "Metals conduct heat faster than wood or plastic.",
                "example": "A metal spoon in hot soup warms up by conduction."
            },
            "convection": {
                "definition": "Transfer of heat by the movement of fluids like air or water",
                "kid_friendly": "Heat moving because liquids or gases move",
                "fun_fact": "Convection currents in Earth's mantle help move tectonic plates.",
                "example": "Warm air rising and cool air sinking creates convection currents."
            },
            "radiation": {
                "definition": "Transfer of energy through space by electromagnetic waves",
                "kid_friendly": "Heat traveling in waves, even through space",
                "fun_fact": "Sunlight warms Earth by radiation across 93 million miles.",
                "example": "Feeling heat from a fire without touching it is radiation."
            },
            "orbit": {
                "definition": "The curved path of an object around a star, planet, or moon",
                "kid_friendly": "The path things take when they move around in space",
                "fun_fact": "Earth completes one orbit around the Sun every 365 days.",
                "example": "Satellites orbit Earth and send GPS signals."
            },
            "rotation": {
                "definition": "The spinning of an object around its axis",
                "kid_friendly": "When something spins around like a top",
                "fun_fact": "Earth’s rotation causes day and night every 24 hours.",
                "example": "Planets rotate while they orbit the Sun."
            },
            "galaxy": {
                "definition": "A huge system of stars, gas, and dust held together by gravity",
                "kid_friendly": "A giant family of stars held together in space",
                "fun_fact": "The Milky Way galaxy may contain over 100 billion planets.",
                "example": "Our Solar System is located in the Milky Way galaxy."
            },
            "nebula": {
                "definition": "A cloud of gas and dust in space where stars can form",
                "kid_friendly": "A big cloud of space dust where new stars are born",
                "fun_fact": "Some nebulae glow with beautiful colors from ionized gases.",
                "example": "The Orion Nebula is visible with a small telescope."
            },
            "comet": {
                "definition": "A ball of ice and dust that orbits the Sun and forms a tail when heated",
                "kid_friendly": "A space rock made of ice that grows a tail near the Sun",
                "fun_fact": "A comet’s tail always points away from the Sun because of solar wind.",
                "example": "Halley's Comet visits Earth's skies about every 76 years."
            },
            "asteroid": {
                "definition": "A rocky object orbiting the Sun, mostly between Mars and Jupiter",
                "kid_friendly": "A space rock that travels around the Sun",
                "fun_fact": "The largest asteroid, Ceres, is big enough to be a dwarf planet.",
                "example": "Many asteroids orbit in the asteroid belt."
            },
            "nutrient": {
                "definition": "A substance needed by organisms to live and grow",
                "kid_friendly": "Something in food that helps living things grow",
                "fun_fact": "Plants take in nutrients from soil and water through their roots.",
                "example": "Nitrogen is a nutrient that plants use to make proteins."
            },
            "fertilizer": {
                "definition": "Material added to soil to supply nutrients for plants",
                "kid_friendly": "Food for plants that helps them grow better",
                "fun_fact": "Compost is a natural fertilizer made from decayed plants and scraps.",
                "example": "Gardeners add fertilizer to soil to boost plant growth."
            },
            "pollination": {
                "definition": "Movement of pollen so plants can form seeds and fruits",
                "kid_friendly": "When pollen moves so plants can make seeds",
                "fun_fact": "Bees, butterflies, and even bats help pollinate plants.",
                "example": "Wind pollination helps corn plants produce kernels."
            },

            # Ecology
            "ecosystem": {
                "definition": "All living and nonliving things in an area",
                "kid_friendly": "A community of living things and their home",
                "fun_fact": "Even a single tree can be an ecosystem for hundreds of species!",
                "example": "A pond ecosystem includes fish, plants, water, and sunlight."
            },
            "habitat": {
                "definition": "The natural home of an organism",
                "kid_friendly": "The type of place where an animal or plant lives",
                "fun_fact": "Some animals can only survive in one specific habitat!",
                "example": "A polar bear's habitat is the Arctic ice and snow."
            },
            "adaptation": {
                "definition": "A feature that helps an organism survive",
                "kid_friendly": "A special body part or ability that helps survival",
                "fun_fact": "Adaptations can take millions of years to develop!",
                "example": "A giraffe's long neck is an adaptation for reaching tall trees."
            },
            "predator": {
                "definition": "An animal that hunts other animals",
                "kid_friendly": "An animal that catches and eats other animals",
                "fun_fact": "Some predators can run faster than race cars!",
                "example": "A lion is a predator that hunts zebras and antelope."
            },
            "prey": {
                "definition": "An animal that is hunted by a predator",
                "kid_friendly": "An animal that gets eaten by other animals",
                "fun_fact": "Prey animals often have eyes on the sides of their heads to see danger!",
                "example": "A rabbit is prey for foxes and hawks."
            },
            "producer": {
                "definition": "Organism that makes its own food",
                "kid_friendly": "Living things that create their own food from sunlight",
                "fun_fact": "Producers are the base of all food chains!",
                "example": "Plants are producers because they make food through photosynthesis."
            },
            "consumer": {
                "definition": "Organism that eats other living things",
                "kid_friendly": "Living things that must eat others for energy",
                "fun_fact": "Humans are consumers because we can't make our own food!",
                "example": "A deer is a consumer that eats plants for energy."
            },

            # Matter & Chemistry
            "matter": {
                "definition": "Anything that has mass and takes up space",
                "kid_friendly": "Everything you can touch and see",
                "fun_fact": "Matter is made of tiny particles called atoms!",
                "example": "Your desk, the air, and even you are all made of matter."
            },
            "atom": {
                "definition": "The smallest unit of matter",
                "kid_friendly": "The tiniest piece of stuff that still acts like that stuff",
                "fun_fact": "Atoms are so small that millions could fit on the period at the end of this sentence!",
                "example": "An atom is like a tiny LEGO brick that builds everything."
            },
            "molecule": {
                "definition": "Two or more atoms bonded together",
                "kid_friendly": "Atoms stuck together to make something new",
                "fun_fact": "Water molecules are made of 2 hydrogen atoms and 1 oxygen atom!",
                "example": "A molecule is like a small building made from atom blocks."
            },
        }

        # Question templates by difficulty
        self.question_templates = {
            "easy": [
                "What is a {word}?",
                "Where would you find {word}?",
                "What does {word} do?",
                "Why is {word} important?",
                "Name one fact about {word}.",
            ],
            "medium": [
                "Explain how {word} helps living things.",
                "Describe the role of {word} in {topic}.",
                "What would happen without {word}?",
                "Compare {word} to something in everyday life.",
                "How does {word} relate to {related_word}?",
            ],
            "hard": [
                "Analyze the relationship between {word} and {related_word}.",
                "Predict what would occur if {word} stopped functioning.",
                "Evaluate the importance of {word} in the ecosystem.",
                "Design an experiment to study {word}.",
                "Synthesize what you know about {word} to explain {concept}.",
            ]
        }

        # Engaging scenarios by theme
        self.scenario_themes = {
            "superhero": [
                "{hero} has the amazing power of {word}! When {villain} threatens the city, {hero} uses {power_description} to save the day!",
                "Meet {hero}, the defender with {word} abilities! Can you help {hero} understand how to use {power_description}?",
            ],
            "mystery": [
                "Detective {name} discovers a strange case involving {word}. Help solve the mystery by understanding how {word} works!",
                "The {word} Mystery: Something strange is happening in {location}. Use your knowledge of {word} to crack the case!",
            ],
            "adventure": [
                "On a journey through {location}, our explorer discovers the secrets of {word}. Join the adventure to learn more!",
                "Quest for the {word}! Travel through amazing places to understand this important science concept.",
            ],
            "real_world": [
                "Did you know {word} is working right now in {location}? Let's explore how {word} affects our daily lives!",
                "Look around you! {word} is happening everywhere. Discover how it works in the real world.",
            ]
        }

    def get_definition(self, word: str, grade_level: str = "3-5", style: str = "standard") -> str:
        """Get appropriate definition based on grade level"""
        word_lower = word.lower()

        if word_lower not in self.vocab_database:
            return f"A science term related to {word}"

        data = self.vocab_database[word_lower]

        # Choose definition based on grade level
        if grade_level in ["K", "K-2", "1", "2"]:
            return data.get("kid_friendly", data["definition"])
        else:
            return data["definition"]

    def get_fun_fact(self, word: str) -> str:
        """Get fun fact for a word"""
        word_lower = word.lower()
        if word_lower in self.vocab_database:
            return self.vocab_database[word_lower].get("fun_fact", "")
        return ""

    def get_example(self, word: str) -> str:
        """Get example for a word"""
        word_lower = word.lower()
        if word_lower in self.vocab_database:
            return self.vocab_database[word_lower].get("example", "")
        return ""

    def generate_crossword_clue(self, word: str, grade_level: str = "3-5", difficulty: str = "medium") -> str:
        """Generate an engaging crossword clue"""
        word_lower = word.lower()

        # Use definition as clue
        clue = self.get_definition(word, grade_level)

        # Make it more puzzle-like based on difficulty
        if difficulty == "easy":
            return clue
        elif difficulty == "medium":
            # Add "It is..." prefix
            return f"It is {clue[0].lower()}{clue[1:]}"
        else:  # hard
            # Make it more cryptic
            example = self.get_example(word)
            if example:
                return f"{example.split('.')[0]}"
            return clue

        return clue

    def generate_vocabulary_words(
        self,
        topic: str,
        count: int = 15,
        vocabulary_pool: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
    ) -> List[str]:
        """Generate relevant vocabulary words for a topic or NGSS standard context."""
        topic_keywords = {
            "cell": ["cell", "nucleus", "mitochondria", "chloroplast", "membrane", "cytoplasm", "ribosome", "vacuole", "dna", "protein"],
            "energy": ["energy", "atp", "photosynthesis", "respiration", "glucose", "oxygen", "mitochondria", "chloroplast"],
            "ecosystem": ["ecosystem", "habitat", "adaptation", "predator", "prey", "producer", "consumer", "organism"],
            "matter": ["matter", "atom", "molecule", "energy", "protein", "dna"],
            "organ": ["organ", "system", "tissue", "cell", "organism"],
            "earth": [
                "weathering", "erosion", "sediment", "rock", "soil", "water",
                "climate", "precipitation", "evaporation", "condensation",
                "volcano", "earthquake", "tectonic plates", "magma", "lava"
            ],
            "weather": ["meteorologist", "precipitation", "evaporation", "condensation", "climate", "temperature"],
            "space": ["planet", "star", "galaxy", "orbit", "gravity", "astronaut", "telescope", "comet", "asteroid", "nebula"],
            "force": ["force", "motion", "gravity", "friction", "inertia", "velocity", "acceleration", "mass"],
        }

        candidate_words = set()

        def _add_words(words: List[str]):
            for raw_word in words:
                cleaned = ''.join(ch for ch in raw_word if ch.isalpha())
                if cleaned and len(cleaned) >= 3:
                    candidate_words.add(cleaned.lower())

        if vocabulary_pool:
            _add_words(vocabulary_pool)

        if topics:
            for topic_name in topics:
                lowered = topic_name.lower()
                for key, words in topic_keywords.items():
                    if key in lowered:
                        _add_words(words)

        topic_lower = topic.lower()
        for key, words in topic_keywords.items():
            if key in topic_lower:
                _add_words(words)

        if not candidate_words:
            _add_words(list(self.vocab_database.keys()))

        words_list = list(candidate_words)
        random.shuffle(words_list)
        return words_list[:count]

    def generate_scenario(self, topic: str, grade_level: str, theme: str = None) -> str:
        """Generate an engaging scenario"""
        if theme is None:
            theme = random.choice(list(self.scenario_themes.keys()))

        template = random.choice(self.scenario_themes[theme])

        # Fill in template
        names = ["Alex", "Maya", "Sam", "Jordan", "Riley", "Casey", "Taylor", "Morgan"]
        heroes = ["Captain Science", "Professor Proton", "The Atom Avenger", "Cell Commander"]
        villains = ["Dr. Chaos", "The Disorder", "Professor Pollution"]
        locations = ["the laboratory", "the science center", "the nature reserve", "the research station"]

        scenario = template.format(
            word=topic,
            hero=random.choice(heroes),
            villain=random.choice(villains),
            name=random.choice(names),
            location=random.choice(locations),
            power_description=f"the power of {topic}",
        )

        return scenario


# Global instance
_smart_content = None

def get_smart_content() -> SmartContentEngine:
    """Get or create global smart content engine"""
    global _smart_content
    if _smart_content is None:
        _smart_content = SmartContentEngine()
    return _smart_content
