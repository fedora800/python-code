
/*
--------------------------------------------------------------------------------

-- F01 - fnc_calculate_sma
-- F02 - fnc_calculate_ema
-- F03 - fnc_calculate_rsi


-- TR01 - trg_update_sma
-- TR02 - trg_update_ema
-- TR03 - trg_update_rsi

--------------------------------------------------------------------------------
*/


--------------------------------------------------------------------------------

-- F01 - fnc_calculate_sma
-- Create a function to calculate the sma50 
/* -- original - works ----
DROP FUNCTION IF EXISTS fnc_calculate_sma() CASCADE;
CREATE OR REPLACE FUNCTION fnc_calculate_sma()
RETURNS TRIGGER AS $$
DECLARE
    avg_close_50rows  NUMERIC(10, 2) := 0;
    row_count INT;
BEGIN
    SELECT COUNT(*) INTO row_count
    FROM tbl_price_data_1day t
    WHERE t.pd_symbol = NEW.pd_symbol;

    -- Check if there are at least 50 rows for the given pd_symbol
    IF row_count >= 50 THEN
        SELECT AVG(close) INTO avg_close_50rows
        FROM (
            SELECT close
            FROM tbl_price_data_1day t
            WHERE t.pd_symbol = NEW.pd_symbol
            ORDER BY t.pd_time DESC
            LIMIT 50
        ) subquery;
    END IF;

    -- Assign the calculated moving average or another appropriate default value
    NEW.sma_50 := COALESCE(avg_close_50rows, NULL);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
*/

DROP FUNCTION IF EXISTS fnc_calculate_sma() CASCADE;
CREATE OR REPLACE FUNCTION fnc_calculate_sma()
RETURNS TRIGGER AS $$
DECLARE
    avg_close_50rows  NUMERIC(10, 2);
    avg_close_200rows NUMERIC(10, 2);
    row_count INT;
BEGIN
    SELECT COUNT(*) INTO row_count
    FROM tbl_price_data_1day t
    WHERE t.pd_symbol = NEW.pd_symbol;

    -- below prints too much, every row insert, so commented out for now
    -- RAISE NOTICE 'Row count for % : %', NEW.pd_symbol, row_count;  -- Debugging output, check the PostgreSQL log or use a tool like PgAdmin to view the log messages
--    RAISE LOG 'This is an informational message';
--    RAISE WARNING 'Something unexpected happened';
--    RAISE EXCEPTION 'An unexpected error';

    IF row_count >= 50 THEN
        SELECT AVG(close) INTO avg_close_50rows
        FROM (
            SELECT close
            FROM tbl_price_data_1day t
            WHERE t.pd_symbol = NEW.pd_symbol
            ORDER BY t.pd_time DESC
            LIMIT 50
        ) subquery;
        --RAISE NOTICE 'Avg 50 rows: %', avg_close_50rows;  -- Debugging output
    END IF;
    IF row_count >= 200 THEN
        SELECT AVG(close) INTO avg_close_200rows
        FROM (
            SELECT close
            FROM tbl_price_data_1day t
            WHERE t.pd_symbol = NEW.pd_symbol
            ORDER BY t.pd_time DESC
            LIMIT 200
        ) subquery;
        --RAISE NOTICE 'Avg 200 rows: %', avg_close_200rows;  -- Debugging output
    END IF;

    -- Assign the calculated moving average or another appropriate default value
    NEW.sma_50 := COALESCE(avg_close_50rows, NULL);
    NEW.sma_200 := COALESCE(avg_close_200rows, NULL);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- F02 - fnc_calculate_ema
-- Create a function to calculate the ema13
CREATE OR REPLACE FUNCTION fnc_calculate_ema_13()
RETURNS TRIGGER AS $$
DECLARE
    close_price NUMERIC(10, 2);
    ema_yesterday NUMERIC(10, 2);
    smoothing_factor NUMERIC(10, 2) := 2.0 / (13.0 + 1.0); -- 13-day EMA
BEGIN
    -- Get the closing price of the current row
    close_price := NEW.close;

    -- Get the EMA value from the previous day
    SELECT ema_13 INTO ema_yesterday
    FROM tbl_price_data_1day
    WHERE pd_symbol = NEW.pd_symbol
    ORDER BY pd_time DESC
    LIMIT 1;

    -- If there is no previous EMA value, set it to the closing price
    IF ema_yesterday IS NULL THEN
        NEW.ema_13 := close_price;
    ELSE
        -- Calculate the new EMA using the smoothing factor
        NEW.ema_13 := (close_price - ema_yesterday) * smoothing_factor + ema_yesterday;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



-- F03 - fnc_calculate_rsi
-- Create a function to calculate the rsi14
CREATE OR REPLACE FUNCTION fnc_calculate_rsi()
RETURNS TRIGGER AS $$
DECLARE
    avg_gain NUMERIC(10, 2);
    avg_loss NUMERIC(10, 2);
    rs       NUMERIC(10, 2);
BEGIN
    -- Calculate gains and losses for the last 14 periods
    SELECT
        COALESCE(AVG(gain), 0),
        COALESCE(-AVG(loss), 0)
    INTO avg_gain, avg_loss
    FROM (
        SELECT
            CASE WHEN close > LAG(close) OVER w THEN close - LAG(close) OVER w ELSE 0 END AS gain,
            CASE WHEN close < LAG(close) OVER w THEN LAG(close) OVER w - close ELSE 0 END AS loss
        FROM tbl_price_data_1day
        WHERE pd_symbol = NEW.pd_symbol
        WINDOW w AS (PARTITION BY pd_symbol ORDER BY pd_time DESC ROWS BETWEEN 14 PRECEDING AND CURRENT ROW)
        LIMIT 14
    ) subquery;

    -- Calculate Relative Strength (RS) and RSI
    rs := CASE WHEN avg_loss = 0 THEN
                CASE WHEN avg_gain = 0 THEN 0 ELSE 100 END
             ELSE
                100 - (100 / (1 + avg_gain / avg_loss))
          END;

    -- Update RSI_14 column
    NEW.rsi_14 := rs;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


--------------------------------------------------------------------------------

-- TR01 - trg_update_sma
-- Create a trigger to run the function on INSERT
DROP TRIGGER IF EXISTS trg_update_sma ON tbl_price_data_1day CASCADE;
CREATE TRIGGER trg_update_sma
BEFORE INSERT ON tbl_price_data_1day
FOR EACH ROW
EXECUTE FUNCTION fnc_calculate_sma();


-- TR02 - trg_update_ema
-- Create a trigger to run the function on INSERT
CREATE TRIGGER trg_update_ema_13
BEFORE INSERT ON tbl_price_data_1day
FOR EACH ROW
EXECUTE FUNCTION fnc_calculate_ema_13();


-- TR03 - trg_update_rsi


--------------------------------------------------------------------------------


