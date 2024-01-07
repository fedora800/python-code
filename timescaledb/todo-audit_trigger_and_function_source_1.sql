
-- https://medium.com/israeli-tech-radar/postgresql-trigger-based-audit-log-fd9d9d5e412c



--------------------------------------------------------------------------------
-- table definition

CREATE TABLE IF NOT EXISTS audit_log (
    id serial PRIMARY KEY,
    table_name TEXT,
    record_id TEXT,
    operation_type TEXT,
    changed_at TIMESTAMP DEFAULT now(),
    changed_by TEXT,
    original_values jsonb,
    new_values jsonb,
);

/*
    id: a serial key of the entry.
    table_name: the name of the table in which the update occurred.
    record_id: the id of the entry in the changed table.
    operation_type: INSERT, UPDATE, or DELETE.
    changed_at: time of the update.
    changed_by: which user made the update (not as trivial as it seems, but we will get to it).
    original_values: a json object that holds the changed key with the original value.
    new_values: a json object that holds the changed key with the new value.
*/


--------------------------------------------------------------------------------
-- function to map to the trigger

CREATE OR REPLACE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
DECLARE
    new_data jsonb;
    old_data jsonb;
    key text;
    new_values jsonb;
    old_values jsonb;
    user_id text;
BEGIN

    user_id := current_setting('audit.user_id', true);

    IF user_id IS NULL THEN
        user_id := current_user;
    END IF;

    new_values := '{}';
    old_values := '{}';

    IF TG_OP = 'INSERT' THEN
        new_data := to_jsonb(NEW);
        new_values := new_data;

    ELSIF TG_OP = 'UPDATE' THEN
        new_data := to_jsonb(NEW);
        old_data := to_jsonb(OLD);

        FOR key IN SELECT jsonb_object_keys(new_data) INTERSECT SELECT jsonb_object_keys(old_data)
        LOOP
            IF new_data ->> key != old_data ->> key THEN
                new_values := new_values || jsonb_build_object(key, new_data ->> key);
                old_values := old_values || jsonb_build_object(key, old_data ->> key);
            END IF;
        END LOOP;

    ELSIF TG_OP = 'DELETE' THEN
        old_data := to_jsonb(OLD);
        old_values := old_data;

        FOR key IN SELECT jsonb_object_keys(old_data)
        LOOP
            old_values := old_values || jsonb_build_object(key, old_data ->> key);
        END LOOP;

    END IF;

    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, operation_type, changed_by, original_values, new_values)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, user_id, old_values, new_values);

        RETURN NEW;
    ELSE
        INSERT INTO audit_log (table_name, record_id, operation_type, changed_by, original_values, new_values)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, user_id, old_values, new_values);

        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;


--------------------------------------------------------------------------------
-- create the trigger
-- note that it looks like we will have to ADD TRIGGER TO EACH AND EVERY TABLE we need the audit for

CREATE TRIGGER audit_log_trigger
    BEFORE INSERT OR UPDATE OR DELETE 
 ON public.case_studies
    FOR EACH ROW
    EXECUTE FUNCTION audit_trigger(); 


CREATE TRIGGER audit_log_trigger
    BEFORE INSERT OR UPDATE OR DELETE 
 ON public.series
    FOR EACH ROW
    EXECUTE FUNCTION audit_trigger();


CREATE TRIGGER audit_log_trigger
    BEFORE INSERT OR UPDATE OR DELETE 
 ON public.images
    FOR EACH ROW
    EXECUTE FUNCTION audit_trigger();








