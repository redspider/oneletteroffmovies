CREATE TABLE entries (
    id BIGINT PRIMARY KEY,
    dated TIMESTAMP,
    author_id TEXT,
    author_name TEXT,
    profile_image TEXT,
    qmovie TEXT,
    movie TEXT
);

CREATE TABLE movies (
    qname TEXT PRIMARY KEY,
    best BIGINT REFERENCES entries(id),
    count INT
);

CREATE OR REPLACE FUNCTION add_movie(v_id BIGINT, v_author_id TEXT, v_author_name TEXT, v_profile_image TEXT, v_movie TEXT, v_qname TEXT) RETURNS VOID AS
$$
BEGIN
    BEGIN
        INSERT INTO entries (id, dated, author_id, author_name, profile_image, qmovie, movie) VALUES (v_id, NOW(), v_author_id, v_author_name, v_profile_image, v_movie, v_qname);
        PERFORM update_movies(v_qname, v_id);
        RETURN;
    EXCEPTION WHEN unique_violation THEN
        -- Ignore
    END;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_movies (v_qname TEXT, v_id BIGINT) RETURNS VOID AS
$$
BEGIN
    LOOP
        UPDATE movies SET count = count + 1 WHERE qname = v_qname;
        
        IF found THEN
            RETURN;
        END IF;
        BEGIN
            INSERT INTO movies (qname, best, count) VALUES (v_qname, v_id, 1);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Loop again
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

    
