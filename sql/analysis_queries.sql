-- IBM Applied Data Science Capstone: EDA with SQL (SPACEXTBL)
-- Execute against the IBM SQL lab dataset. Schema/table casing may vary by DB engine.

-- TASK 1: Unique launch sites
SELECT DISTINCT launch_site FROM SPACEXTBL ORDER BY launch_site;
-- Result: CCAFS LC-40; CCAFS SLC-40; KSC LC-39A; VAFB SLC-4E

-- TASK 2: First five rows for launch sites beginning CCA
SELECT * FROM SPACEXTBL WHERE launch_site LIKE 'CCA%' LIMIT 5;
-- Result dates: 2010-06-04, 2010-12-08, 2012-05-22, 2012-10-08, 2013-03-01

-- TASK 3: Total payload mass for NASA (CRS)
SELECT SUM(payload_mass__kg_) AS total_payload_mass_kg FROM SPACEXTBL WHERE customer = 'NASA (CRS)';
-- Result: 45,596 kg

-- TASK 4: Average payload mass for F9 v1.1
SELECT AVG(payload_mass__kg_) AS average_payload_mass_kg FROM SPACEXTBL WHERE booster_version LIKE 'F9 v1.1%';
-- Result: 2,534 kg (IBM course notebook snapshot)

-- TASK 5: First successful ground-pad landing date
SELECT MIN(date) AS first_successful_ground_pad_landing FROM SPACEXTBL WHERE landing__outcome = 'Success (ground pad)';
-- Result: 2015-12-22

-- TASK 6: Successful drone-ship landing boosters, payload 4,000–6,000 kg
SELECT booster_version FROM SPACEXTBL WHERE landing__outcome = 'Success (drone ship)' AND payload_mass__kg_ BETWEEN 4000 AND 6000;
-- Result: F9 FT B1022; F9 FT B1026; F9 FT B1021.2; F9 FT B1031.2

-- TASK 7: Success/failure landing outcome counts in the course notebook
SELECT 'Success' AS outcome, COUNT(*) AS count FROM SPACEXTBL WHERE landing__outcome LIKE 'Success%'
UNION ALL SELECT 'Failure' AS outcome, COUNT(*) AS count FROM SPACEXTBL WHERE landing__outcome NOT LIKE 'Success%'
UNION ALL SELECT '(All)' AS outcome, COUNT(*) AS count FROM SPACEXTBL;
-- Result: Success 61; Failure 40; All 101

-- TASK 8: Booster versions with maximum payload mass
SELECT DISTINCT booster_version FROM SPACEXTBL WHERE payload_mass__kg_ = (SELECT MAX(payload_mass__kg_) FROM SPACEXTBL);
-- Result: 12 booster records; maximum payload mass is 15,600 kg.

-- TASK 9: Failed drone-ship landing attempts in 2015
SELECT booster_version, launch_site, landing__outcome FROM SPACEXTBL
WHERE landing__outcome = 'Failure (drone ship)' AND EXTRACT(YEAR FROM date) = 2015;
-- Result: F9 v1.1 B1012 and F9 v1.1 B1015, both CCAFS LC-40.

-- TASK 10: Rank landing outcomes between 2010-06-04 and 2017-03-20
SELECT landing__outcome, COUNT(*) AS count FROM SPACEXTBL
WHERE date BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY landing__outcome ORDER BY count DESC;
-- Result: No attempt 10; Failure (drone ship) 5; Success (drone ship) 5;
-- Controlled (ocean) 3; Success (ground pad) 3; Failure (parachute) 2;
-- Uncontrolled (ocean) 2; Precluded (drone ship) 1.
