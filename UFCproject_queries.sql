
-- The data about around 4800 UFC events was cleaned and adjusted in Excel. I discarded all rows that had missing values which were needed in further exploration.
-- Some data had to be adjusted with the help of "text to columns", "search and replace" and other Excel tools.
-- Cleaned dataset contains large amount of information about 2614 UFC event.


-- Creating table that will store information about fights as an event.

CREATE TABLE fight_specs
(
	fight_id SMALLSERIAL PRIMARY KEY,
	r_odds SMALLINT,
	b_odds SMALLINT,
	fight_date DATE,
	city_fight VARCHAR(50),
	state_fight VARCHAR(50),
	country_fight VARCHAR(50),
	winner VARCHAR(50),
	title_bout VARCHAR(50),
	weight_class VARCHAR(50),
	no_of_rounds SMALLINT,
	empty_arena SMALLINT,
	finish VARCHAR(50),
	finish_details VARCHAR(50),
	finish_round SMALLINT,
	r_dec_odds SMALLINT,
	r_sub_odds SMALLINT,
	r_ko_odds SMALLINT,
	b_dec_odds SMALLINT,
	b_sub_odds SMALLINT,
	b_ko_odds SMALLINT
);

-- Creating table that will store information about fighters and their statistics.

CREATE TABLE fighters_spec
(
	fight_id SMALLSERIAL,
	R_fighter VARCHAR(50),
	B_fighter VARCHAR(50),
	Gender VARCHAR(50),
	B_current_lose_streak SMALLINT,
	B_current_win_streak SMALLINT,
	B_avg_sig_str_landed DECIMAL,
	B_avg_sig_str_pct DECIMAL,
	B_avg_sub_att DECIMAL,
	B_avg_td_landed DECIMAL,
	B_avg_td_pct DECIMAL,
	B_longest_win_streak SMALLINT,
	B_losses SMALLINT,
	B_total_title_bouts SMALLINT,
	B_win_by_decision_majority SMALLINT,
	B_win_by_decision_split SMALLINT,
	B_win_by_decision_unanimous SMALLINT,
	B_win_by_ko_tko SMALLINT,
	B_win_by_submission SMALLINT,
	B_win_by_tko_doctor_stoppage SMALLINT,
	B_wins SMALLINT,
	B_stance VARCHAR(50),
	B_height_cms DECIMAL,
	B_weight_lbs DECIMAL,
	B_age SMALLINT,
	R_current_lose_streak SMALLINT,
	R_current_win_streak SMALLINT,
	R_avg_sig_str_landed DECIMAL,
	R_avg_sig_str_pct DECIMAL,
	R_avg_sub_att DECIMAL,
	R_avg_td_landed DECIMAL,
	R_avg_td_pct DECIMAL,
	R_longest_win_streak SMALLINT,
	R_losses SMALLINT,
	R_total_title_bouts SMALLINT,
	R_win_by_decision_majority SMALLINT,
	R_win_by_decision_split SMALLINT,
	R_win_by_decision_unanimous SMALLINT,
	R_win_by_ko_tko SMALLINT,
	R_win_by_submission SMALLINT,
	R_win_by_tko_doctor_stoppage SMALLINT,
	R_wins SMALLINT,
	R_stance VARCHAR(50),
	R_height_cms DECIMAL,
	R_weight_lbs DECIMAL,
	R_age SMALLINT
);

----------------------------

-- 1. Creating a SELECT statement that groups all the fights into weight class categories.
-- By doing so I am able to extract information about the percentage of fights getting finished by a knockout or a submission in each weight category.
-- Information about the average number of rounds per weight category provides similar information.


WITH cte AS
(
	SELECT
	SUM(CASE finish
				 WHEN 'U-DEC' THEN 1
				 ELSE 0
				 END) AS unanimous_decision_count,
	SUM(CASE finish
		 		WHEN 'M-DEC' THEN 1
		 		ELSE 0
		 		END) AS majority_decision_count,
	SUM(CASE finish
				WHEN 'S-DEC' THEN 1
				ELSE 0
				END) AS split_decision_count,
	SUM(CASE finish
				WHEN 'KO/TKO' THEN 1
				ELSE 0
				END) AS ko_tko_count,
	SUM(CASE finish
				WHEN 'SUB' THEN 1
				ELSE 0
				END) AS submission_count,
				ROUND(AVG(finish_round), 3) AS average_number_of_rounds,
				weight_class
				FROM fight_specs
				WHERE weight_class IN ('Heavyweight',
						   'Light Heavyweight',
						   'Middleweight',
						   'Welterweight',
						   'Lightweight',
						   'Featherweight',
						   'Bantamweight',
						   'Women''s Bantamweight',
						   'Women''s Strawweight',
						   'Women''s Flyweight')
	GROUP BY weight_class)
SELECT weight_class, unanimous_decision_count, majority_decision_count, split_decision_count, ko_tko_count, submission_count,
				unanimous_decision_count + majority_decision_count + split_decision_count + ko_tko_count + submission_count AS sum_of_finishes,
				ROUND(ko_tko_count / CAST(unanimous_decision_count + majority_decision_count + split_decision_count + ko_tko_count + submission_count AS NUMERIC), 3) * 100 AS percentage_of_knockouts,
				ROUND(submission_count / CAST(unanimous_decision_count + majority_decision_count + split_decision_count + ko_tko_count + submission_count AS NUMERIC), 3) * 100 AS percentage_of_submissions,
				ROUND(CAST(ko_tko_count + submission_count AS NUMERIC) / CAST(unanimous_decision_count + majority_decision_count + split_decision_count + ko_tko_count + submission_count AS NUMERIC), 3) * 100 AS percentage_of_finishes,
				average_number_of_rounds
FROM cte;



----------------------------

-- 2. The data is organised by each UFC event and each row contains information about two fighters: fighter R (red corner) and fighter B (blue corner).
-- I create a SELECT statement, using functions such as CTE and UNION, in order to extract all the information specific to each fighter.
-- In order to extract valuable information, I decided to limit the fighters range to fighters that had not less than 10 fights in my dataset, 
-- their average submission attempts per 15 minutes is higher than 0.2, their average takedown accuracy is higher than 10%
-- and their average significant striking accuracy is higher than 10%.
-- Using this data I am able to analyse who are the best 10 fighters in my dataset, by striking and grappling department.
 

WITH cte AS
(
SELECT r_fighter, r_avg_sig_str_pct, r_avg_td_pct, r_avg_sub_att
FROM fighters_spec
WHERE r_fighter != b_fighter
UNION ALL
SELECT b_fighter, b_avg_sig_str_pct, b_avg_td_pct, b_avg_sub_att
FROM fighters_spec
WHERE b_fighter != r_fighter)
SELECT r_fighter AS fighter, COUNT(r_fighter) AS fighters_fights, AVG(r_avg_sig_str_pct) AS average_significant_striking_accuracy,
		AVG(r_avg_td_pct) AS average_takedown_accuracy,
		AVG(r_avg_sub_att) AS average_submission_attacks_per_15_minutes
FROM cte
GROUP BY r_fighter
HAVING COUNT(r_fighter) >= 10 AND AVG(r_avg_sub_att) > 0.2 AND AVG(r_avg_td_pct) > 0.1 AND AVG(r_avg_sig_str_pct) > 0.1
ORDER BY AVG(r_avg_td_pct) DESC
LIMIT 10;

----------------------------



-- 3. Lastly, I am interested in extracting the information about where did all the fights take place. Using this data I am able to decide which country held the highest amount of UFC events.

SELECT country_fight, COUNT(country_fight) AS number_of_fights
FROM fight_specs
GROUP BY country_fight
ORDER BY number_of_fights DESC;