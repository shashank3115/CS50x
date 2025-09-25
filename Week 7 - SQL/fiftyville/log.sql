-- What crimes happened on July 28, 2023 at the bakery?
SELECT *
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28
  AND street = 'Humphrey Street';

-- Witness statements on July 28, 2023
SELECT *
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;

-- Cars leaving parking lot between 10:15 and 10:25
SELECT *
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28
  AND hour = 10 AND minute BETWEEN 15 AND 25
  AND activity = 'exit';

-- Withdrawals on July 28, 2023 at Leggett Street
SELECT *
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28
  AND atm_location = 'Leggett Street'
  AND transaction_type = 'withdraw';

-- Find people who used those accounts
SELECT *
FROM bank_accounts
JOIN people ON bank_accounts.person_id = people.id
WHERE account_number IN (
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2023 AND month = 7 AND day = 28
      AND atm_location = 'Leggett Street'
);

-- Cross check people with license plates leaving bakery
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND month = 7 AND day = 28
      AND hour = 10 AND minute BETWEEN 15 AND 25
);

-- Earliest flight on July 29, 2023
SELECT *
FROM flights
WHERE year = 2023 AND month = 7 AND day = 29
ORDER BY hour, minute
LIMIT 1;

-- Who was on that flight?
SELECT flights.id AS flight_id, people.name, people.phone_number, people.passport_number, people.license_plate
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29
  AND flights.id = 36;

-- Calls made by Jeremy on July 28, 2023
SELECT *
FROM phone_calls
JOIN people ON phone_calls.caller = people.phone_number
WHERE phone_calls.year = 2023 AND phone_calls.month = 7 AND phone_calls.day = 28
  AND people.name = 'Jeremy'
  AND duration < 60;
