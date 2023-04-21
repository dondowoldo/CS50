-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description
    FROM crime_scene_reports
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND street = "Humphrey Street";
    -- Check for Crime scene on the day of the robbery.

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

SELECT activity, minute, license_plate
    FROM bakery_security_logs
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND minute < 25
    AND minute > 15;

SELECT license_plate
    FROM bakery_security_logs
    WHERE license_plate IN
        (SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND activity = "entrance"
            AND minute <= 15)
    AND license_plate IN
        (SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND activity = "exit"
            AND minute > 15);

    -- Recovered possible license plates of cars entering parking lot before robbery and leaving after

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
            WHERE license_plate IN
                (SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND activity = "entrance"
                    AND minute <= 15)
    AND license_plate IN
        (SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND activity = "exit"
            AND minute > 15));
    -- Cross reference people withdrawing cash from ATM at Leggett street and license plates present at the bakery parking lot during the robbery and look for a match.

    -- Number 1 suspect currently "Luca"
     -- | name |  phone_number  | passport_number |
    --  +------+----------------+-----------------+
    --  | Luca | (389) 555-5198 | 8496433585      |

    SELECT id, full_name, abbreviation
        FROM airports
        WHERE full_name
        LIKE "Fiftyville%";

        --+----+-----------------------------+--------------+
        --| id |          full_name          | abbreviation |
        --+----+-----------------------------+--------------+
        --| 8  | Fiftyville Regional Airport | CSF          |
        --+----+-----------------------------+--------------+

        -- Check for ID of local airport and look for flights leaving Fiftyville tomorrow that Luca might be on.

    SELECT flight_id, seat
    FROM passengers
    WHERE flight_id IN
        (SELECT id
            FROM flights
            WHERE origin_airport_id = 8
            AND year = 2021
            AND month = 7
            AND day = 29)
            AND passport_number = 8496433585;

        -- Luca on flight ID 36 - seat 7B

    SELECT id, destination_airport_id, hour, minute
        FROM flights
        WHERE origin_airport_id = 8
        AND year = 2021
        AND month = 7
        AND day = 29
        ORDER BY hour, minute ASC;

        -- Check for earliest flights leaving fiftyville on 29th in connection to Raymond's interview
        SELECT abbreviation, full_name, city
            FROM airports
            WHERE id = 4;

        -- Luca on the flight ID 36 Going from Fiftyville to LaGuardia A. in New York leaving at 8:20
            -- Very likely Luca is the thief !!

        -- NOW LOOKING FOR ACCOMPLICE
            -- Check phone calls according to the Raymond's interview

    SELECT *
        FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration <= 60
        AND (caller = "(389) 555-5198"
            OR receiver = "(389) 555-5198");

        -- Checking for phone calls involving Luca on the day of the robbery that were 1 minute or less.
        -- Luca received the call from "(609) 555-5876"   // id of the call = 234

        -- Check the details of the person that Luca was on call with.

    SELECT *
        FROM people
        WHERE phone_number = "(609) 555-5876";

    -- Possible accomplice : Kathryn
       -- +--------+---------+----------------+-----------------+---------------+
       -- |   id   |  name   |  phone_number  | passport_number | license_plate |
       -- +--------+---------+----------------+-----------------+---------------+
       -- | 561160 | Kathryn | (609) 555-5876 | 6121106406      | 4ZY7I8T       |
       -- +--------+---------+----------------+-----------------+---------------+

    -- Check if Kathryn is on any flight and if so, check id of that flight and retrieve information.
    SELECT *
        FROM flights
        WHERE id =
            (SELECT flight_id
                FROM passengers
                WHERE passport_number = 6121106406);

    SELECT *
        FROM airports
        WHERE id = 34;


    -- Kathryn on flight 28/7/2021 leaving Fiftyville at 17:20 and going to Dallas International APT in Dallas




