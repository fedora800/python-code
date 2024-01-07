
-- https://www.bluelabellabs.com/blog/how-to-setup-automatic-audit-logging-in-postgres-using-triggers-and-trigger-functions/

CREATE SEQUENCE logged_actions_event_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;


CREATE TABLE IF NOT EXISTS logged_actions
(
    event_id bigint NOT NULL DEFAULT nextval('logged_actions_event_id_seq'::regclass),
    schema_name text COLLATE pg_catalog."default" NOT NULL,
    table_name text COLLATE pg_catalog."default" NOT NULL,
    relid oid NOT NULL,
    session_user_name text COLLATE pg_catalog."default",
    action_tstamp_tx timestamp with time zone NOT NULL,
    action_tstamp_stm timestamp with time zone NOT NULL,
    action_tstamp_clk timestamp with time zone NOT NULL,
    transaction_id bigint,
    application_name text COLLATE pg_catalog."default",
    client_addr inet,
    client_port integer,
    client_query text COLLATE pg_catalog."default",
    action text COLLATE pg_catalog."default" NOT NULL,
    row_data hstore,
    changed_fields hstore,
    statement_only boolean NOT NULL,
    CONSTRAINT logged_actions_pkey PRIMARY KEY (event_id),
    CONSTRAINT logged_actions_action_check CHECK (action = ANY (ARRAY['I'::text, 'D'::text, 'U'::text, 'T'::text]))
);


CREATE INDEX logged_actions_action_idx
    ON logged_actions USING btree
    (action COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


CREATE INDEX logged_actions_action_tstamp_tx_stm_idx
    ON logged_actions USING btree
    (action_tstamp_stm ASC NULLS LAST)
    TABLESPACE pg_default;


CREATE INDEX logged_actions_relid_idx
    ON logged_actions USING btree
    (relid ASC NULLS LAST)
    TABLESPACE pg_default;


--------------------------------------------------------------------------------

CREATE FUNCTION create_log_on_modify()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF SECURITY DEFINER
    SET search_path=pg_catalog, public
AS $BODY$
DECLARE
    audit_row logged_actions;
    include_values boolean;
    log_diffs boolean;
    h_old hstore;
    h_new hstore;
    excluded_cols text[] = ARRAY[]::text[];
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'create_log_on_modify() may only run as an AFTER trigger';
    END IF;

    audit_row = ROW(
        nextval('logged_actions_event_id_seq'), -- event_id
        TG_TABLE_SCHEMA::text,                        -- schema_name
        TG_TABLE_NAME::text,                          -- table_name
        TG_RELID,                                     -- relation OID for much quicker searches
        session_user::text,                           -- session_user_name
        current_timestamp,                            -- action_tstamp_tx
        statement_timestamp(),                        -- action_tstamp_stm
        clock_timestamp(),                            -- action_tstamp_clk
        txid_current(),                               -- transaction ID
        current_setting('application_name'),          -- client application
        inet_client_addr(),                           -- client_addr
        inet_client_port(),                           -- client_port
        current_query(),                              -- top-level query or queries (if multistatement) from client
        substring(TG_OP,1,1),                         -- action
        NULL, NULL,                                   -- row_data, changed_fields
        'f'                                           -- statement_only
        );

    IF NOT TG_ARGV[0]::boolean IS DISTINCT FROM 'f'::boolean THEN
        audit_row.client_query = NULL;
    END IF;

    IF TG_ARGV[1] IS NOT NULL THEN
        excluded_cols = TG_ARGV[1]::text[];
    END IF;
    
    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(OLD.*) - excluded_cols;
        audit_row.changed_fields =  (hstore(NEW.*) - audit_row.row_data) - excluded_cols;
        IF audit_row.changed_fields = hstore('') THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(OLD.*) - excluded_cols;
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
        audit_row.row_data = hstore(NEW.*) - excluded_cols;
    ELSIF (TG_LEVEL = 'STATEMENT' AND TG_OP IN ('INSERT','UPDATE','DELETE','TRUNCATE')) THEN
        audit_row.statement_only = 't';
    ELSE
        RAISE EXCEPTION '[create_log_on_modify] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;
    INSERT INTO logged_actions VALUES (audit_row.*);
    RETURN NULL;
END;
$BODY$;


--------------------------------------------------------------------------------

CREATE TRIGGER audit_trigger_row
    AFTER INSERT OR DELETE OR UPDATE 
--    ON public."user"
    ON public."tbl_price_data_1day"
    FOR EACH ROW
    EXECUTE FUNCTION create_log_on_modify('true');





