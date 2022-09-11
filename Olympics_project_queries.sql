-- The objective of this project is to analyze and visualize data about Olympic games.
-- The dataset contains information about all historical Olympic Games events, including all the games from Athens 1896 to Beijing 2022.
-- Specifically, I will be analyzing data bout more than 21,000 medals, 162,000 results, 74,000 athletes,
-- and 53 hosts of the Summer and Winter Olympic Games.
-- Some of data is corrupted and it may not fully represent actual numbers of particular medal counts etc. but
-- since the purpose of this project is to practice data analysis and visualisation, I will not try to verify all of it.


-- Firstly, I have to create appropriate tables for my data.

CREATE TABLE olympic_athletes
(
	athlete_full_name VARCHAR(100),
	games_participations SMALLINT,
	first_game VARCHAR(50),
	athlete_year_birth VARCHAR(25),
	athlete_medals VARCHAR(200)
);

--

CREATE TABLE olympic_medals
(
	discipline VARCHAR(100),
	event_name VARCHAR(100),
	event_title VARCHAR(200),
	event_gender VARCHAR(50),
	medal_type VARCHAR(50),
	participant_type VARCHAR(50),
	participant_title VARCHAR(50),
	athlete_full_name VARCHAR(100),
	country_name VARCHAR(50)
);

--

CREATE TABLE olympic_hosts
(
	event_name VARCHAR(100),
	game_end_date DATE,
	game_start_date DATE,
	game_location VARCHAR(100),
	event_name_fixed VARCHAR(100),
	game_season VARCHAR(50),
	game_year VARCHAR(25)
);

--

CREATE TABLE olympic_results
(
	discipline VARCHAR(100),
	event_title VARCHAR(200),
	event_name VARCHAR(100),
	participant_type VARCHAR(50),
	medal_type VARCHAR(50),
	rank_position VARCHAR(50),
	country_name VARCHAR(50),
	country_code VARCHAR(25),
	country_3_letter_code VARCHAR(25),
	athlete_full_name VARCHAR(100)
);


-- Some events have missing information about athletes full name in the case when it was represented by a team, not the specific athlete.
-- I will update the athlete_full_name column and insert strings in the form of 'Team of...', when there are null values in the column.

UPDATE olympic_results
SET athlete_full_name = CONCAT('Team of', ' ', country_name)
WHERE participant_type = 'GameTeam' AND athlete_full_name IS NULL;

	
-- For my visualisation, I intend to extract information about all the participating countries and olympic regions and their respective medal counts,
-- grouped by medal type.
-- That information is stored in the olympic_results table, so the main SQL functions I will use are self-join, sub-query and Common Table Expressions. 

WITH cte AS (
SELECT 
	country.country_name, 
	gold.total_amount_of_gold_medals, 
	silver.total_amount_of_silver_medals, 
	bronze.total_amount_of_bronze_medals 
FROM
		(SELECT DISTINCT(country_name)
			FROM olympic_results) country
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_gold_medals
			FROM olympic_results
			WHERE medal_type = 'GOLD'
			GROUP BY country_name) gold
	ON country.country_name = gold.country_name
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_silver_medals
			FROM olympic_results
			WHERE medal_type = 'SILVER'
			GROUP BY country_name) silver
	ON gold.country_name = silver.country_name
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_bronze_medals
			FROM olympic_results
			WHERE medal_type = 'BRONZE'
			GROUP BY country_name) bronze
	ON gold.country_name = bronze.country_name)
SELECT 
	country_name,
	COALESCE(total_amount_of_gold_medals, 0) AS gold_medals,
	COALESCE(total_amount_of_silver_medals, 0) AS silver_medals,
	COALESCE(total_amount_of_bronze_medals, 0) AS bronze_medals
FROM cte
ORDER BY gold_medals DESC, silver_medals DESC, bronze_medals DESC;



-- My dataset contains 238 different countries or participating regions. Tableau maps recognize 250 different countries,
-- but the dataset used consists of regions like Soviet Union or Federal Republic of Germany.
-- I have to manually verify and adjust country names in Excel, so that they would get easly uploaded into Tableau maps.

-- For the actual map, I will exclude several countries/ regions/ teams from the official list, like:
-- Australasia
-- Bohemia
-- Czechoslovakia
-- Sovier Union etc.



-- Now I will crate a table, based on the previous query result, that will consist of all the countries and their medal count.

CREATE TABLE olympic_countries_and_medals
AS WITH cte AS (
SELECT 
	country.country_name, 
	gold.total_amount_of_gold_medals, 
	silver.total_amount_of_silver_medals, 
	bronze.total_amount_of_bronze_medals 
FROM
		(SELECT DISTINCT(country_name)
			FROM olympic_results) country
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_gold_medals
			FROM olympic_results
			WHERE medal_type = 'GOLD'
			GROUP BY country_name) gold
	ON country.country_name = gold.country_name
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_silver_medals
			FROM olympic_results
			WHERE medal_type = 'SILVER'
			GROUP BY country_name) silver
	ON gold.country_name = silver.country_name
	LEFT JOIN
		(SELECT country_name, COUNT(medal_type) AS total_amount_of_bronze_medals
			FROM olympic_results
			WHERE medal_type = 'BRONZE'
			GROUP BY country_name) bronze
	ON gold.country_name = bronze.country_name)
SELECT 
	country_name,
	COALESCE(total_amount_of_gold_medals, 0) AS gold_medals,
	COALESCE(total_amount_of_silver_medals, 0) AS silver_medals,
	COALESCE(total_amount_of_bronze_medals, 0) AS bronze_medals
FROM cte
ORDER BY gold_medals DESC, silver_medals DESC, bronze_medals DESC;



-- Now, I will change the existing names of the countries in the olympic_countries_and_medals table to names that I assigned in Excel,
-- that comply with Tableau notation.


UPDATE olympic_countries_and_medals
SET country_name = 'The Bahamas'
WHERE country_name = 'Bahamas';

UPDATE olympic_countries_and_medals
SET country_name = 'Brunei Darussalam'
WHERE country_name = 'Brunei';

UPDATE olympic_countries_and_medals
SET country_name = 'Taiwan'
WHERE country_name = 'Chinese Taipei';

UPDATE olympic_countries_and_medals
SET country_name = 'Czechia'
WHERE country_name = 'Czech Republic';

UPDATE olympic_countries_and_medals
SET country_name = 'North Korea'
WHERE country_name = 'Democratic People''s Republic of Korea';

UPDATE olympic_countries_and_medals
SET country_name = 'Democratic Republic of Congo'
WHERE country_name = 'Democratic Republic of the Congo';

UPDATE olympic_countries_and_medals
SET country_name = 'Timor Leste'
WHERE country_name = 'Democratic Republic of Timor-Leste';

UPDATE olympic_countries_and_medals
SET country_name = 'Fiji Islands'
WHERE country_name = 'Fiji';

UPDATE olympic_countries_and_medals
SET country_name = 'United Kingdom'
WHERE country_name = 'Great Britain';

UPDATE olympic_countries_and_medals
SET country_name = 'Hong Kong SAR'
WHERE country_name = 'Hong Kong, China';

UPDATE olympic_countries_and_medals
SET country_name = 'Iran'
WHERE country_name = 'Islamic Republic of Iran';

UPDATE olympic_countries_and_medals
SET country_name = 'Côte-d''Ivoire'
WHERE country_name = 'Ivory Coast';

UPDATE olympic_countries_and_medals
SET country_name = 'Laos'
WHERE country_name = 'Lao People''s Democratic Republic';

UPDATE olympic_countries_and_medals
SET country_name = 'Palestinian Territories'
WHERE country_name = 'Palestine';

UPDATE olympic_countries_and_medals
SET country_name = 'China'
WHERE country_name = 'People''s Republic of China';

UPDATE olympic_countries_and_medals
SET country_name = 'South Korea'
WHERE country_name = 'Republic of Korea';

UPDATE olympic_countries_and_medals
SET country_name = 'Moldova'
WHERE country_name = 'Republic of Moldova';

UPDATE olympic_countries_and_medals
SET country_name = 'Russia'
WHERE country_name = 'Russian Federation';

UPDATE olympic_countries_and_medals
SET country_name = 'Syria'
WHERE country_name = 'Syrian Arab Republic';

UPDATE olympic_countries_and_medals
SET country_name = 'Tanzania'
WHERE country_name = 'United Republic of Tanzania';

UPDATE olympic_countries_and_medals
SET country_name = 'United States'
WHERE country_name = 'United States of America';

UPDATE olympic_countries_and_medals
SET country_name = 'Virgin Islands'
WHERE country_name = 'US Virgin Islands';

UPDATE olympic_countries_and_medals
SET country_name = 'Viet Nam'
WHERE country_name = 'Vietnam';

UPDATE olympic_countries_and_medals
SET country_name = 'British Virgin Islands'
WHERE country_name = 'Virgin Islands, British';

UPDATE olympic_countries_and_medals
SET country_name = 'British Virgin Islands'
WHERE country_name = 'Virgin Islands, British';

----------------------


-- Now that all country names have been changed, I will select information about the countries that match with Tableau notation.

SELECT * FROM olympic_countries_and_medals
WHERE country_name IN(
'Afghanistan',
'Albania',
'Algeria',
'American Samoa',
'Andorra',
'Angola',
'Antigua and Barbuda',
'Argentina',
'Armenia',
'Aruba',
'Australia',
'Austria',
'Azerbaijan',
'The Bahamas',
'Bahrain',
'Bangladesh',
'Barbados',
'Belarus',
'Belgium',
'Belize',
'Benin',
'Bermuda',
'Bhutan',
'Bolivia',
'Bosnia and Herzegovina',
'Botswana',
'Brazil',
'British Virgin Islands',
'Brunei Darussalam',
'Bulgaria',
'Burkina Faso',
'Burundi',
'Cambodia',
'Cameroon',
'Canada',
'Cape Verde',
'Cayman Islands',
'Central African Republic',
'Chad',
'Chile',
'Taiwan',
'Colombia',
'Comoros',
'Congo',
'Cook Islands',
'Costa Rica',
'Croatia',
'Cuba',
'Cyprus',
'Czechia',
'North Korea',
'Democratic Republic of Congo',
'Timor Leste',
'Denmark',
'Djibouti',
'Dominica',
'Dominican Republic',
'Ecuador',
'Egypt',
'El Salvador',
'Equatorial Guinea',
'Eritrea',
'Estonia',
'Eswatini',
'Ethiopia',
'Federated States of Micronesia',
'Fiji Islands',
'Finland',
'France',
'Gabon',
'Gambia',
'Georgia',
'Germany',
'Ghana',
'United Kingdom',
'Greece',
'Grenada',
'Guam',
'Guatemala',
'Guinea',
'Guinea-Bissau',
'Guyana',
'Haiti',
'Honduras',
'Hong Kong SAR',
'Hungary',
'Iceland',
'India',
'Indonesia',
'Iraq',
'Ireland',
'Iran',
'Israel',
'Italy',
'Côte-d''Ivoire',
'Jamaica',
'Japan',
'Jordan',
'Kazakhstan',
'Kenya',
'Kiribati',
'Kosovo',
'Kuwait',
'Kyrgyzstan',
'Laos',
'Latvia',
'Lebanon',
'Lesotho',
'Liberia',
'Libya',
'Liechtenstein',
'Lithuania',
'Luxembourg',
'Madagascar',
'Malawi',
'Malaysia',
'Maldives',
'Mali',
'Malta',
'Marshall Islands',
'Mauritania',
'Mauritius',
'Mexico',
'Monaco',
'Mongolia',
'Montenegro',
'Morocco',
'Mozambique',
'Myanmar',
'Namibia',
'Nauru',
'Nepal',
'Netherlands',
'New Zealand',
'Nicaragua',
'Niger',
'Nigeria',
'North Macedonia',
'Norway',
'Oman',
'Pakistan',
'Palau',
'Palestinian Territories',
'Panama',
'Papua New Guinea',
'Paraguay',
'China',
'Peru',
'Philippines',
'Poland',
'Portugal',
'Puerto Rico',
'Qatar',
'South Korea',
'Moldova',
'Romania',
'Russia',
'Rwanda',
'Saint Kitts and Nevis',
'Saint Lucia',
'Saint Vincent and the Grenadines',
'Samoa',
'San Marino',
'Sao Tome and Principe',
'Saudi Arabia',
'Senegal',
'Serbia',
'Seychelles',
'Sierra Leone',
'Singapore',
'Slovakia',
'Slovenia',
'Solomon Islands',
'Somalia',
'South Africa',
'South Sudan',
'Spain',
'Sri Lanka',
'Sudan',
'Suriname',
'Sweden',
'Switzerland',
'Syria',
'Tajikistan',
'Thailand',
'Togo',
'Tonga',
'Trinidad and Tobago',
'Tunisia',
'Turkey',
'Turkmenistan',
'Tuvalu',
'Uganda',
'Ukraine',
'United Arab Emirates',
'Tanzania',
'United States',
'Uruguay',
'Uzbekistan',
'Vanuatu',
'Venezuela',
'Viet Nam',
'British Virgin Islands',
'Virgin Islands',
'Yemen',
'Zambia',
'Zimbabwe')
ORDER BY gold_medals DESC, silver_medals DESC, bronze_medals DESC;

-----------

-- Now I am interested in analyzing countries and their medal count by each olympic discipline.
-- Having that information I will be able to study which countries are the best in each discipline.
-- I will use the UNION function with some simple filters.

SELECT country_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'GOLD'
		GROUP BY discipline, medal_type, country_name
UNION ALL
	SELECT country_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'SILVER'
		GROUP BY discipline, medal_type, country_name
UNION ALL
	SELECT country_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'BRONZE'
		GROUP BY discipline, medal_type, country_name
ORDER BY country_name, discipline, medal_type

--------------

-- Lastly, I am interested in extracting information about medalists with the highest number of medals in each discipline.
-- I will be able to combine that information with the previous query result and use same discipline filter in Tableau,
-- so that when the user chooses a particular sport, he will not only receive information about leading countries in the sport,
-- but also about the most accomplished medalists and their nationality.


SELECT athlete_full_name, country_name, event_title, event_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'GOLD'
		GROUP BY athlete_full_name, medal_type, country_name, event_title, event_name, discipline
UNION ALL
	SELECT athlete_full_name, country_name, event_title, event_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'SILVER'
		GROUP BY athlete_full_name, medal_type, country_name, event_title, event_name, discipline
UNION ALL
	SELECT athlete_full_name, country_name, event_title, event_name, discipline, COUNT(medal_type), medal_type
		FROM olympic_medals
		WHERE medal_type = 'BRONZE'
		GROUP BY athlete_full_name, medal_type, country_name, event_title, event_name, discipline
ORDER BY athlete_full_name, discipline, medal_type;