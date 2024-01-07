
/*
--------------------------------------------------------------------------------

-- F01 - fnc_calculate_sma


-- TR01 - trg_update_sma

--------------------------------------------------------------------------------
*/


--------------------------------------------------------------------------------

-- F01 - fnc_calculate_sma
-- Create a function to calculate the sma50 
DROP FUNCTION IF EXISTS fnc_calculate_sma() CASCADE;
CREATE OR REPLACE FUNCTION fnc_calculate_sma()
RETURNS TRIGGER AS $$
DECLARE
    avg_close NUMERIC(10, 2) := 0;
    row_count INT;
BEGIN
    SELECT COUNT(*) INTO row_count
    FROM tbl_price_data_1day t
    WHERE t.pd_symbol = NEW.pd_symbol;

    -- Check if there are at least 50 rows for the given pd_symbol
    IF row_count >= 50 THEN
        SELECT AVG(close) INTO avg_close
        FROM (
            SELECT close
            FROM tbl_price_data_1day t
            WHERE t.pd_symbol = NEW.pd_symbol
            ORDER BY t.pd_time DESC
            LIMIT 50
        ) subquery;
    END IF;

    -- Assign the calculated moving average or another appropriate default value
    NEW.sma_50 := COALESCE(avg_close, NULL);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- TR01 - trg_update_sma
-- Create a trigger to run the function on INSERT
DROP TRIGGER IF EXISTS trg_update_sma ON tbl_price_data_1day CASCADE;
CREATE TRIGGER trg_update_sma
BEFORE INSERT ON tbl_price_data_1day
FOR EACH ROW
EXECUTE FUNCTION fnc_calculate_sma();


--------------------------------------------------------------------------------


