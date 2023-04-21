-- Keep a log of any SQL queries you execute as you solve the mystery.

 -- Check for Crime scene on the day of the robbery.
SELECT description
    FROM crime_scene_reports
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND street = "Humphrey Street";

    -- Theft happened at 10:15 in Humphrey Street bakery.
    -- 3 witnesses interviewed on the same day. Bakery mentioned in every transcript

SELECT name, transcript
    FROM interviews
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND transcript LIKE "%bakery%";
    -- Wittnesses--

    -- Ruth : within 10 mins of theft -> thief into car in bakery parking and drove away.
    -- Eugene : Possibly knows the thief. Saw thief before arrival to bakery withdrawing cash from ATM on Leggett Street.
    -- Raymond : Thief called someone as leaving the bakery. Max 1 minute call. Thief mentioned taking earliest flight of Fiftyville next day 29th. Person on the phone to buy the ticket.

    -- CONCLUSIONS-- // 1. Check security footage for car // 2. check atm transactions on Legget Street // 3. Check flight schedule from fiftyville


    -- Recovered possible license plates of cars leaving parking lot after the robbery within 10 minutes as Ruth mentioned in her statement

SELECT license_plate
    FROM bakery_security_logs
    WHERE license_plate IN
        (SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND activity = "exit"
            AND minute >= 15
            AND minute <= 25);


 -- Cross reference people withdrawing cash from ATM at Leggett street and license plates present at the bakery parking lot during the robbery and look for a match.

SELECT name, phone_number, passport_number
    FROM people
    WHERE id IN
        (SELECT person_id
            FROM bank_accounts
            WHERE account_number IN
                (SELECT account_number
                    FROM atm_transactions
                    WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND atm_location = "Leggett Street"
                    AND transaction_type = "withdraw"))
                    AND license_plate IN
                        (SELECT license_plate
                            FROM bakery_security_logs
                            WHERE year = 2021 AND month = 7
                            AND day = 28 AND activity = "exit"
                            AND minute >= 15
                            AND minute <= 25);

        --+-------+----------------+-----------------+
        --| name  |  phone_number  | passport_number |
        --+-------+----------------+-----------------+
        --| Iman  | (829) 555-5269 | 7049073643      |
        --| Luca  | (389) 555-5198 | 8496433585      |
        --| Diana | (770) 555-1861 | 3592750733      |
        --| Bruce | (367) 555-5533 | 5773159633      |
        --+-------+----------------+-----------------+


    -- Cross referencing results of previous search with the information that the thief has called someone for less than a minute.
SELECT *
    FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration <= 60
    AND caller IN
        (SELECT phone_number
            FROM people
            WHERE id IN
                (SELECT person_id
                    FROM bank_accounts
                    WHERE account_number IN
                        (SELECT account_number
                            FROM atm_transactions
                            WHERE year = 2021
                            AND month = 7
                            AND day = 28
                            AND atm_location = "Leggett Street"
                            AND transaction_type = "withdraw"))
                            AND license_plate IN
                                (SELECT license_plate
                                    FROM bakery_security_logs
                                    WHERE year = 2021 AND month = 7
                                    AND day = 28 AND activity = "exit"
                                    AND minute >= 15
                                    AND minute <= 25));


        --+-----+----------------+----------------+------+-------+-----+----------+
        --| id  |     caller     |    receiver    | year | month | day | duration |
        --+-----+----------------+----------------+------+-------+-----+----------+
        --| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
        --| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
        --+-----+----------------+----------------+------+-------+-----+----------+

            -- Narrowed down to 2 suspects. Retrieving full information on them

SELECT * FROM people
    WHERE phone_number IN
        (SELECT caller FROM phone_calls
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND duration <= 60
            AND caller IN
                (SELECT phone_number
                    FROM people
                    WHERE id IN
                        (SELECT person_id
                            FROM bank_accounts
                            WHERE account_number IN
                                (SELECT account_number
                                    FROM atm_transactions
                                    WHERE year = 2021
                                    AND month = 7
                                    AND day = 28
                                    AND atm_location = "Leggett Street"
                                    AND transaction_type = "withdraw"))
                                    AND license_plate IN
                                        (SELECT license_plate
                                            FROM bakery_security_logs
                                            WHERE year = 2021 AND month = 7
                                            AND day = 28 AND activity = "exit"
                                            AND minute >= 15
                                            AND minute <= 25)));


        --+--------+-------+----------------+-----------------+---------------+
        --|   id   | name  |  phone_number  | passport_number | license_plate |
        --+--------+-------+----------------+-----------------+---------------+
        --| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
        --| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
        --+--------+-------+----------------+-----------------+---------------+



        -- Checking for APT id, APT abb and full name of FiftyVille

SELECT id, full_name, abbreviation
    FROM airports
    WHERE full_name
    LIKE "Fiftyville%";

        --+----+-----------------------------+--------------+
        --| id |          full_name          | abbreviation |
        --+----+-----------------------------+--------------+
        --| 8  | Fiftyville Regional Airport | CSF          |
        --+----+-----------------------------+--------------+



        -- Check for earliest flights leaving fiftyville on 29th in connection to Raymond's interview

SELECT id, destination_airport_id, hour, minute
    FROM flights
    WHERE origin_airport_id = 8
    AND year = 2021
    AND month = 7
    AND day = 29
    ORDER BY hour, minute ASC LIMIT 1;

            --+----+------------------------+------+--------+
            --| id | destination_airport_id | hour | minute |
            --+----+------------------------+------+--------+
            --| 36 | 4                      | 8    | 20     |
            --| 43 | 1                      | 9    | 30     |
            --| 23 | 11                     | 12   | 15     |
            --| 53 | 9                      | 15   | 20     |
            --| 18 | 6                      | 16   | 0      |
            --+----+------------------------+------+--------+

SELECT abbreviation, full_name, city
    FROM airports
    WHERE id = 4;

    -- Earliest flight heading to LGA (LaGuardia Airport) in New York City


    -- Check if any of the suspects (Diana or Bruce) is on the flight.

SELECT name
    FROM people
    WHERE passport_number IN (
        SELECT passport_number
            FROM people
            WHERE phone_number IN
                (SELECT caller FROM phone_calls
                    WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND duration <= 60
                    AND caller IN
                        (SELECT phone_number
                            FROM people
                            WHERE id IN
                                (SELECT person_id
                                    FROM bank_accounts
                                    WHERE account_number IN
                                        (SELECT account_number
                                            FROM atm_transactions
                                            WHERE year = 2021
                                            AND month = 7
                                            AND day = 28
                                            AND atm_location = "Leggett Street"
                                            AND transaction_type = "withdraw"))
                                            AND license_plate IN
                                                (SELECT license_plate
                                                    FROM bakery_security_logs
                                                    WHERE year = 2021 AND month = 7
                                                    AND day = 28 AND activity = "exit"
                                                    AND minute >= 15
                                                    AND minute <= 25))))
    AND passport_number IN (
        SELECT passport_number
            FROM passengers
            WHERE flight_id = (
                SELECT id
                    FROM flights
                    WHERE origin_airport_id = 8
                    AND year = 2021
                    AND month = 7
                    AND day = 29
                    ORDER BY hour, minute ASC LIMIT 1));

             -- Selection narrowed down to Bruce only therefore He must be the thief !
                        --+--------+
                        --|  name  |
                        --+--------+
                        --| Bruce  |
                        --+--------+

            -- Check who was Bruce talking to to determine who the complice was.

SELECT name FROM people
    WHERE phone_number = (
        SELECT receiver
            FROM phone_calls
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND duration <= 60
            AND caller = "(367) 555-5533");

                --+-------+
                --| name  |
                --+-------+
                --| Robin |
                --+-------+

            -- Accomplice was Robin !