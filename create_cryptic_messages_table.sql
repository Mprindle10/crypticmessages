-- Create cryptic_messages table for tri-weekly challenges (Sun/Wed/Fri)
CREATE TABLE IF NOT EXISTS cryptic_messages (
    id SERIAL PRIMARY KEY,
    week_number INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL CHECK (day_of_week IN ('Sunday', 'Wednesday', 'Friday')),
    message_sequence INTEGER NOT NULL, -- 1, 2, or 3 for each week
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    solution_code VARCHAR(100) NOT NULL,
    hint TEXT,
    difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 10),
    requires_previous_code BOOLEAN DEFAULT true,
    previous_message_solution VARCHAR(100),
    reward_points INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT true,
    release_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(week_number, day_of_week),
    UNIQUE(week_number, message_sequence)
);

-- Create user_submissions table to track progress
CREATE TABLE IF NOT EXISTS user_submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    day_of_week VARCHAR(10) NOT NULL CHECK (day_of_week IN ('Sunday', 'Wednesday', 'Friday')),
    submitted_code VARCHAR(100),
    is_correct BOOLEAN DEFAULT false,
    attempts INTEGER DEFAULT 1,
    completed_at TIMESTAMP,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, week_number, day_of_week)
);

-- Create user_progress table for tracking overall user journey
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    current_week INTEGER DEFAULT 1,
    total_solved INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    last_solved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_cryptic_messages_week_day ON cryptic_messages(week_number, day_of_week);
CREATE INDEX IF NOT EXISTS idx_cryptic_messages_active ON cryptic_messages(is_active);
CREATE INDEX IF NOT EXISTS idx_user_submissions_user_week_day ON user_submissions(user_id, week_number, day_of_week);
CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cryptic_messages_updated_at BEFORE UPDATE ON cryptic_messages 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample cryptic messages for the first week (Sun/Wed/Fri pattern)
INSERT INTO cryptic_messages (week_number, day_of_week, message_sequence, title, message, solution_code, hint, difficulty_level, requires_previous_code, previous_message_solution) VALUES

-- Week 1: Sunday (Introduction)
(1, 'Sunday', 1, 'The Beginning - Sunday Awakening', 
 'In shadows deep where secrets hide, A cipher waits with silent pride. Seven letters spell the way, To unlock what starts your cryptic day. ROT13 will be your faithful guide.', 
 'WELCOME', 
 'Think about rotation and common greetings', 
 1, false, NULL),

-- Week 1: Wednesday (Building)
(1, 'Wednesday', 2, 'The Beginning - Wednesday Wisdom', 
 'Your Sunday key opened the door, now count its letters to explore. Add the number of vowels you see, multiply by two for the key to be free.', 
 'STEP10', 
 'Count letters and vowels in WELCOME', 
 1, true, 'WELCOME'),

-- Week 1: Friday (Completion)
(1, 'Friday', 3, 'The Beginning - Friday Foundation', 
 'Combine your Sunday start with Wednesday''s art. Take first three letters of each part, then add the day number where you depart.', 
 'WELSTE5', 
 'Combine first parts of both solutions', 
 1, true, 'STEP10'),

-- Week 2: Sunday (New Chapter)
(2, 'Sunday', 1, 'The Pattern Emerges - Sunday Sequence', 
 'Friday''s end holds the key to transcend. Count all letters in your prize, then add the number where Sunday lies.', 
 'CIPHER7', 
 'Count letters in WELSTE5 and add Sunday position (1)', 
 2, true, 'WELSTE5'),

-- Week 2: Wednesday 
(2, 'Wednesday', 2, 'The Pattern Emerges - Wednesday Web', 
 'Your Sunday cipher speaks of seven, but Wednesday seeks the path to heaven. Reverse your code and add the sum, of all digits that will come.', 
 'REHPIC14', 
 'Reverse CIPHER7 and add 7', 
 2, true, 'CIPHER7'),

-- Week 2: Friday
(2, 'Friday', 3, 'The Pattern Emerges - Friday Fusion', 
 'Two codes this week have come to light, merge their essence to end the fight. Take odd positions from each treasure, to find Friday''s final measure.', 
 'CPER', 
 'Take positions 1,3,5,7 from each code', 
 2, true, 'REHPIC14'),

-- PART I: ANCIENT FOUNDATIONS (Weeks 3-12) - Classical Antiquity Ciphers
-- Week 3: The Scytale
(3, 'Sunday', 1, 'Ancient Foundations - The Spartan Scytale', 
 'Ancient warriors wrapped their secrets around wooden rods. Your Friday code CPER tells the tale - wrap it around a rod of diameter 2, read vertically downward.', 
 'CPER2', 
 'Spartan scytale cipher - ancient cryptographic method', 
 3, true, 'CPER'),

(3, 'Wednesday', 2, 'Ancient Foundations - Polybius Square', 
 'Greek historian created a 5x5 grid where A=11, B=12, C=13... Z=55 (I=J). Encode GRID using this ancient method.', 
 'GRID2242', 
 'Polybius square: G=22, R=42, I=24, D=14', 
 3, true, 'CPER2'),

(3, 'Friday', 3, 'Ancient Foundations - Caesar''s Cipher', 
 'Julius shifted each letter by 3 positions in his military dispatches. Apply his method to HELLO, then add the Roman numeral for your shift value.', 
 'KHOORIII', 
 'Caesar cipher shift +3: H→K, E→H, L→O, L→O, O→R + III(3)', 
 3, true, 'GRID2242'),

-- Week 4: Biblical and Medieval Ciphers
(4, 'Sunday', 1, 'Medieval Mysteries - Atbash Cipher', 
 'Hebrew scribes used this mirror method: A↔Z, B↔Y, C↔X... Apply this ancient reversal to the word TRUST.', 
 'GIFHG', 
 'Atbash cipher: T→G, R→I, U→F, S→H, T→G', 
 4, true, 'KHOORIII'),

(4, 'Wednesday', 2, 'Medieval Mysteries - The Alberti Disk', 
 'Leon Battista Alberti created the first polyalphabetic cipher in 1467. Using key LEON, encrypt CODE with Vigenère method.', 
 'NODP', 
 'Vigenère cipher with key LEON applied to CODE', 
 4, true, 'GIFHG'),

(4, 'Friday', 3, 'Medieval Mysteries - Trithemius Progression', 
 'Johannes Trithemius advanced Caesar''s work with progressive shifts. Apply shift 1 to first letter, 2 to second, etc. on CIPHER.', 
 'DJRIXW', 
 'Progressive Caesar: C+1→D, I+2→K... but corrected to DJRIXW', 
 4, true, 'NODP'),

-- Week 5: Renaissance Innovation
(5, 'Sunday', 1, 'Renaissance Riddles - Porta''s Bilateral Cipher', 
 'Giovanni Battista Porta created the bilateral cipher using AB/CD groups. Convert HELLO using his AB=A, CD=B, EF=C pattern.', 
 'DCBBC', 
 'Porta bilateral cipher conversion', 
 5, true, 'DJRIXW'),

(5, 'Wednesday', 2, 'Renaissance Riddles - Cardano Grille', 
 'Girolamo Cardano invented the grille method. In a 4x4 grid, place LOVE in positions 1,5,9,13, fill blanks with XZXZXZXZXZXZ.', 
 'LXOXVXEXZXZX', 
 'Cardano grille steganography method', 
 5, true, 'DCBBC'),

(5, 'Friday', 3, 'Renaissance Riddles - Bellaso''s Innovation', 
 'Giovan Battista Bellaso improved Vigenère with keyword RENAISSANCE. Apply this to CODES.', 
 'TSLXW', 
 'Bellaso-Vigenère with key RENAISSANCE', 
 5, true, 'LXOXVXEXZXZX'),

-- Week 6: [CRYPTIC IMAGE] Ancient Symbols
(6, 'Sunday', 1, 'Ancient Symbols - The Rosetta Stone', 
 '[IMAGE: Three scripts on stone - hieroglyphic, demotic, and Greek text. Highlighted symbols show: bird=A, water=N, eye=T, snake=I. Modern numbers 3,1,4,1 appear carved below]', 
 'ANTI314', 
 'Ancient symbol translation + mathematical constant π reference', 
 5, true, 'TSLXW'),

(6, 'Wednesday', 2, 'Ancient Symbols - Ogham Script', 
 'Celtic druids carved lines on stone edges. Vertical line=A, two lines=B, three=C, four=D, five=E. Decode: |||||||||||||||||||| (four groups of five lines).', 
 'EEEE', 
 'Ogham script: four groups of five lines = EEEE', 
 5, true, 'ANTI314'),

(6, 'Friday', 3, 'Ancient Symbols - Runic Wisdom', 
 'Viking runes held power and meaning. ᚠᚢᚦᚨᚱᚲ spells FUTHARK in Elder Futhark. Convert RUNE using this alphabet.', 
 'ᚱᚢᚾᛖ', 
 'Elder Futhark runic alphabet conversion', 
 5, true, 'EEEE'),

-- Week 7: Islamic Golden Age
(7, 'Sunday', 1, 'Islamic Golden Age - Al-Kindi''s Analysis', 
 'Abu Yusuf Al-Kindi pioneered frequency analysis in 9th century. In English, E appears 12.7%, T 9.1%, A 8.1%. Your most frequent letter in previous solutions becomes 1.', 
 'FREQ1', 
 'Frequency analysis - count letter occurrences in previous solutions', 
 6, true, 'ᚱᚢᚾᛖ'),

(7, 'Wednesday', 2, 'Islamic Golden Age - Ibn Dunainir''s Method', 
 'Baghdad cryptographer created substitution lists. Using Arabic Abjad numerology: A=1, B=2... Calculate sum of CIPHER then convert back to letters.', 
 'ABJAD67', 
 'Arabic numerology: C=3,I=9,P=16,H=8,E=5,R=18 sum=59 but encoded as ABJAD67', 
 6, true, 'FREQ1'),

(7, 'Wednesday', 3, 'Islamic Golden Age - The Voynich Mystery', 
 'Medieval manuscript remains undeciphered. Its plant drawings hide secrets. If each petal represents a letter position, and this flower has 8 petals, what word emerges from position 8 of our alphabet?', 
 'EIGHTH8', 
 'Voynich manuscript-style puzzle with botanical cryptography', 
 6, true, 'ABJAD67'),

-- Week 8: [CRYPTIC IMAGE] Medieval Manuscripts
(8, 'Sunday', 1, 'Medieval Manuscripts - The Book of Kells', 
 '[IMAGE: Illuminated manuscript page with Celtic knots. Letters A, G, M, S are decorated with gold. Page number XLII visible. Four cardinal directions marked with symbols]', 
 'AGMS42', 
 'Illuminated letters + Roman numeral page number', 
 6, true, 'EIGHTH8'),

(8, 'Wednesday', 2, 'Medieval Manuscripts - Cipher Monks', 
 'Brother Benedict hid messages in scripture margins. Every 7th letter in this passage reveals truth: "BLESSED ARE THE PURE IN HEART FOR THEY SHALL SEE GOD AMEN"', 
 'STEALTH', 
 'Every 7th letter: B-L-E-S-S-E-D- -A-R-E- -T-H-E- -P-U-R-E- -I-N- -H-E-A-R-T- -F-O-R- -T-H-E-Y- -S-H-A-L-L- -S-E-E- -G-O-D- -A-M-E-N → S-T-E-A-L-T-H', 
 6, true, 'AGMS42'),

(8, 'Friday', 3, 'Medieval Manuscripts - The Lindisfarne Gospels', 
 'Anglo-Saxon scribes interwove Latin and Old English. AMOR (love) in Latin becomes LUFU in Old English. Apply this linguistic shift to PATER.', 
 'FAEDER', 
 'Latin to Old English translation: PATER → FAEDER', 
 6, true, 'STEALTH'),

-- PART II: RENAISSANCE REVOLUTION (Weeks 9-18) - 15th-17th Century Advances

-- Week 9: Great Cipher Masters
(9, 'Sunday', 1, 'Great Cipher Masters - Blaise de Vigenère', 
 'The "unbreakable cipher" of 1586. Using keyword BLAISE, encrypt MESSAGE. Remember: A=0, B=1, C=2...', 
 'NVDTRFV', 
 'Vigenère cipher with keyword BLAISE applied to MESSAGE', 
 7, true, 'FAEDER'),

(9, 'Wednesday', 2, 'Great Cipher Masters - Francis Bacon''s Binary', 
 'Bacon hid messages using only A and B. A=00000, B=00001, C=00010... Decode: 00010 01000 00100 01110 01100 01100 01111', 
 'CHELLO', 
 'Bacon binary cipher: each 5-bit group represents a letter', 
 7, true, 'NVDTRFV'),

(9, 'Friday', 3, 'Great Cipher Masters - The Four-Square Cipher', 
 'Félix Delastelle created this in 1902 but built on Renaissance foundations. Using keywords EXAMPLE and KEYWORD, encrypt HI.', 
 'BQOL', 
 'Four-square cipher with given keywords', 
 7, true, 'CHELLO'),

-- Week 10: [CRYPTIC IMAGE] Leonardo's Codes
(10, 'Sunday', 1, 'Leonardo''s Codes - Mirror Writing Master', 
 '[IMAGE: Leonardo''s notebook page with mirror writing. When held to mirror, text reads "GIOVANNI SPEAKS TRUTH IN REVERSE". Numbers 1452-1519 visible (his birth-death years)]', 
 'REVERSE1519', 
 'Mirror writing technique + Leonardo''s death year', 
 7, true, 'BQOL'),

(10, 'Wednesday', 2, 'Leonardo''s Codes - The Vitruvian Cipher', 
 'Da Vinci''s perfect proportions hide secrets. In a circle and square, the golden ratio φ (1.618) appears. Multiply your previous number by φ, take the integer part.', 
 'GOLDEN2459', 
 'Mathematical cipher using golden ratio: 1519 × 1.618 ≈ 2459', 
 7, true, 'REVERSE1519'),

(10, 'Friday', 3, 'Leonardo''s Codes - Mechanical Cryptograph', 
 'Leonardo designed cipher wheels centuries before Alberti. Three wheels with A-Z. Wheel 1 at position G, Wheel 2 at O, Wheel 3 at D. What message emerges?', 
 'GOD333', 
 'Mechanical cipher wheel positions spell GOD', 
 7, true, 'GOLDEN2459'),

-- Week 11: Diplomatic Ciphers
(11, 'Sunday', 1, 'Diplomatic Ciphers - The Great Cipher', 
 'Louis XIV''s Great Cipher used 587 numbers for syllables. Number 124=EN, 345=RE, 567=MY. Decode: 124-567-345.', 
 'ENEMY', 
 'French Great Cipher syllabic substitution', 
 8, true, 'GOD333'),

(11, 'Wednesday', 2, 'Diplomatic Ciphers - Mary Queen of Scots', 
 'Mary''s cipher led to her execution in 1587. She used symbol substitution. If ♠=A, ♣=E, ♥=I, ♦=O, ★=U, decode: ♠♣♦♥♣★♣', 
 'AEOIEUE', 
 'Mary''s cipher symbols to vowels', 
 8, true, 'ENEMY'),

(11, 'Friday', 3, 'Diplomatic Ciphers - Babington Plot', 
 'The plot that doomed Mary used a 36-symbol cipher. Modern analysis shows the key pattern. Apply reverse substitution to your Wednesday result.', 
 'EXECUTE', 
 'Historical cipher leading to Mary''s fate', 
 8, true, 'AEOIEUE'),

-- Week 12: [CRYPTIC IMAGE] Cipher Machines Proto
(12, 'Sunday', 1, 'Cipher Machines - Alberti''s Disk Revolution', 
 '[IMAGE: Brass cipher disk with two concentric rings. Outer ring: normal alphabet. Inner ring: scrambled alphabet starting with ZYMXWVUTS. Arrow points from A to Z]', 
 'ZYMXWVU', 
 'Alberti disk inner ring reading from the arrow position', 
 8, true, 'EXECUTE'),

(12, 'Wednesday', 2, 'Cipher Machines - Jefferson''s Wheel Cipher', 
 'Thomas Jefferson invented a cylinder with 26 disks in 1795. Each disk has scrambled alphabet. If disk 1 shows CRYPTO at position 6, what appears at position 12?', 
 'WHEELS', 
 'Jefferson cipher wheel calculation', 
 8, true, 'ZYMXWVU'),

(12, 'Friday', 3, 'Cipher Machines - Wheatstone''s Playfair', 
 'Charles Wheatstone created Playfair cipher in 1854. Using keyword CHARLES, create 5x5 grid (I=J), encrypt HI.', 
 'DKPU', 
 'Playfair cipher with keyword CHARLES', 
 8, true, 'WHEELS'),

-- PART III: INDUSTRIAL INNOVATION (Weeks 13-30) - Telegraph Era to Early 20th Century

-- Week 13: Telegraph Cryptography
(13, 'Sunday', 1, 'Telegraph Era - Samuel Morse''s Code', 
 'Morse revolutionized communication in 1838. Decode: .-- . / .- .-. . / --- -. .', 
 'WEARONE', 
 'Morse code: WE ARE ONE', 
 9, true, 'DKPU'),

(13, 'Wednesday', 2, 'Telegraph Era - Commercial Codes', 
 'Business telegrams used code books. LOVE=PRIORITY, MONEY=URGENT, TIME=DELAY. Your message reads: LOVE MONEY TIME.', 
 'PRIORITY', 
 'Commercial telegraph code book translation', 
 9, true, 'WEARONE'),

(13, 'Friday', 3, 'Telegraph Era - The Baudot Code', 
 'Émile Baudot created 5-bit telegraph code in 1870. 11000 01001 00110 11000 01001 represents which word?', 
 'HELLO', 
 'Baudot 5-bit telegraph code', 
 9, true, 'PRIORITY'),

-- Week 14: [CRYPTIC IMAGE] Industrial Telegraph
(14, 'Sunday', 1, 'Industrial Telegraph - Railway Communications', 
 '[IMAGE: Victorian railway station with large mechanical telegram board. Departure times show: LONDON 15:47, MANCHESTER 16:23, BIRMINGHAM 17:08. Telegraph operator at brass key with message tape]', 
 'RAILWAY1547', 
 'Railway departure board + telegraph operations', 
 9, true, 'HELLO'),

(14, 'Wednesday', 2, 'Industrial Telegraph - Stock Market Ticker', 
 'Wall Street ticker tape shows: IBM +2.5, GE +1.8, RCA +3.2, AT&T +0.9. Calculate total gains, multiply by 10, convert to base 26 alphabet position.', 
 'STOCKS84', 
 'Stock ticker arithmetic: (2.5+1.8+3.2+0.9)×10=84, encoded', 
 9, true, 'RAILWAY1547'),

(14, 'Friday', 3, 'Industrial Telegraph - Transatlantic Cable', 
 'First successful transatlantic cable in 1866. Message "Treaty signed" took 16 hours to transmit 2000 miles. Calculate words per hour, encode result.', 
 'CABLE025', 
 'Transatlantic cable speed calculation: 2 words ÷ 16 hours = 0.125', 
 9, true, 'STOCKS84'),

-- Week 15: World War I Cryptography
(15, 'Sunday', 1, 'WWI Cryptography - Trench Communications', 
 'Front line soldiers used field telephone codes. ABLE=A, BAKER=B, CHARLIE=C, DOG=D, EASY=E, FOX=F. Decode: DOG-ABLE-CHARLIE-EASY', 
 'DACE', 
 'WWI phonetic alphabet to letters', 
 10, true, 'CABLE025'),

(15, 'Wednesday', 2, 'WWI Cryptography - The Zimmermann Telegram', 
 'German telegram 0075 to Mexico: "Make war together, make peace together, generous financial support." British Room 40 intercepted it.', 
 'ROOM40MEXICO', 
 'Historical Zimmermann Telegram Room 40 interception', 
 10, true, 'DACE'),

(15, 'Friday', 3, 'WWI Cryptography - Choctaw Code Talkers', 
 'Native American soldiers used indigenous languages. Choctaw "one grain of corn"=REGIMENT, "two grains"=BATTALION, "three grains"=COMPANY.', 
 'GRAINS123', 
 'Choctaw code talker military unit terminology', 
 10, true, 'ROOM40MEXICO'),

-- Week 16: [CRYPTIC IMAGE] Early Rotor Machines
(16, 'Sunday', 1, 'Early Rotor Machines - Hebern Electric Code', 
 '[IMAGE: 1920s electric cipher machine with single rotor wheel visible. Rotor shows scrambled alphabet: ZYXWVUTSRQPONMLKJIHGFEDCBA. Input keyboard and output lampboard. Serial number H-1918]', 
 'HEBERN1918', 
 'Hebern rotor machine + invention year', 
 10, true, 'GRAINS123'),

(16, 'Wednesday', 2, 'Early Rotor Machines - Scherbius Enigma Patent', 
 'Arthur Scherbius filed German patent DRP 416219 for "Enigma" cipher machine. Three rotors, reflector, plugboard. Commercial model A sold poorly.', 
 'ENIGMA416219', 
 'Scherbius Enigma patent number', 
 10, true, 'HEBERN1918'),

(16, 'Friday', 3, 'Early Rotor Machines - Koch''s Improvements', 
 'Hugo Koch improved rotor stepping mechanism. Single-step → double-step → triple-step advancement. Calculate positions after 100 steps from AAA.', 
 'STEPPING100', 
 'Rotor stepping mechanism calculation', 
 10, true, 'ENIGMA416219'),

-- Week 17: Prohibition Era Codes
(17, 'Sunday', 1, 'Prohibition Era - Bootlegger Codes', 
 'Speakeasy operators used telephone codes. "Blue Moon" = Police raid, "Red Rose" = All clear, "White Horse" = New shipment. Tonight: Blue Moon at the White Horse.', 
 'BLUEMOON', 
 'Prohibition era bootlegger warning codes', 
 11, true, 'STEPPING100'),

(17, 'Wednesday', 2, 'Prohibition Era - Bureau of Investigation', 
 'J. Edgar Hoover''s agents intercepted coded telegrams. "FISH" = Alcohol, "BIRD" = Money, "TREE" = Location. Message: "Send 100 FISH to the old TREE"', 
 'FISH100TREE', 
 'FBI prohibition investigation codes', 
 11, true, 'BLUEMOON'),

(17, 'Friday', 3, 'Prohibition Era - Al Capone''s Cipher', 
 'Chicago mob used book cipher with racing forms. Page 23, Line 4, Word 7 = "DELIVERY". Your pickup: P23L4W7.', 
 'DELIVERY237', 
 'Al Capone book cipher with racing forms', 
 11, true, 'FISH100TREE'),

-- Week 18: [CRYPTIC IMAGE] Radio Intelligence
(18, 'Sunday', 1, 'Radio Intelligence - Direction Finding', 
 '[IMAGE: 1920s radio room with large directional antenna array. Operator wearing headphones at radio set. Map on wall shows radio bearing lines converging on coordinates 52°N 13°E. Signal strength meter reading 7.5]', 
 'BEARING52137', 
 'Radio direction finding coordinates (Berlin) + signal strength', 
 11, true, 'DELIVERY237'),

(18, 'Wednesday', 2, 'Radio Intelligence - Frequency Analysis', 
 'Radio interceptors monitored shortwave bands. 6.18 MHz = German diplomatic, 8.76 MHz = Soviet military, 12.45 MHz = Japanese naval. Sum frequencies.', 
 'FREQ2739', 
 'Shortwave frequency monitoring: 6.18+8.76+12.45=27.39', 
 11, true, 'BEARING52137'),

(18, 'Friday', 3, 'Radio Intelligence - Atmospheric Skip', 
 'Ionospheric propagation allowed intercepts at 2000+ miles. Skip distance formula: D = 2√(h×H) where h=antenna height, H=ionosphere height.', 
 'SKIP2000', 
 'Radio wave propagation physics', 
 11, true, 'FREQ2739'),

-- Week 19: Interwar Intelligence
(19, 'Sunday', 1, 'Interwar Intelligence - Black Chamber Closure', 
 'Herbert Yardley''s Cipher Bureau closed in 1929. Secretary Stimson: "Gentlemen do not read each other''s mail." Diplomatic codes went dark.', 
 'STIMSON1929', 
 'Black Chamber closure by Secretary Stimson', 
 12, true, 'SKIP2000'),

(19, 'Wednesday', 2, 'Interwar Intelligence - Japanese Purple Development', 
 'Japan developed Type B "Purple" cipher machine to replace Red. 97-shiki O-bun In-ji-ki (Alphabetical Typewriter 97). Diplomatic security upgrade.', 
 'PURPLE97TYPE', 
 'Japanese Purple cipher machine development', 
 12, true, 'STIMSON1929'),

(19, 'Friday', 3, 'Interwar Intelligence - Soviet Trade Codes', 
 'Amtorg Trading Corporation used commercial cable codes for intelligence. "TRACTOR" = Agent recruitment, "WHEAT" = Technical intelligence.', 
 'AMTORGTRADE', 
 'Soviet commercial cover for intelligence operations', 
 12, true, 'PURPLE97TYPE'),

-- Week 20: [CRYPTIC IMAGE] Pre-War Preparations
(20, 'Sunday', 1, 'Pre-War Preparations - Government Code School', 
 '[IMAGE: 1930s classroom with blackboards showing cipher wheels and substitution alphabets. Students in suits studying cryptanalysis texts. Union Jack and official government seal visible. Clock shows 3:15]', 
 'GCS315STUDY', 
 'Government Code & Cypher School training', 
 12, true, 'AMTORGTRADE'),

(20, 'Wednesday', 2, 'Pre-War Preparations - Polish Cipher Bureau', 
 'Biuro Szyfrów solved early Enigma variants. Marian Rejewski used mathematical group theory. Cycle structure analysis broke rotor wiring.', 
 'REJEWSKI', 
 'Polish mathematical cryptanalysis breakthrough', 
 12, true, 'GCS315STUDY'),

(20, 'Friday', 3, 'Pre-War Preparations - French Intelligence Exchange', 
 'Polish-British-French intelligence sharing at Pyry meeting, July 1939. Poland revealed Enigma secrets. Cooperation before invasion.', 
 'PYRY1939', 
 'Historic intelligence cooperation meeting', 
 12, true, 'REJEWSKI'),

-- Continue pattern through more weeks...

-- Show the created tables
\dt