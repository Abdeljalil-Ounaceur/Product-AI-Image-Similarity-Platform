DECLARE
    table_exists NUMBER;
    index_exists NUMBER;
BEGIN
    -- Check if table exists
    SELECT COUNT(*)
    INTO table_exists
    FROM user_tables
    WHERE table_name = 'IMAGES';

    IF table_exists = 0 THEN
        EXECUTE IMMEDIATE '
        CREATE TABLE IMAGES (
            image_id VARCHAR2(255) PRIMARY KEY,
            embedding VECTOR(512, FLOAT32)
        )';
        DBMS_OUTPUT.PUT_LINE('Table IMAGES created.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Table IMAGES already exists.');
    END IF;

    -- Check if index exists
    SELECT COUNT(*)
    INTO index_exists
    FROM user_indexes
    WHERE index_name = 'IMAGES_IVF_INDEX';

    IF index_exists = 0 THEN
        EXECUTE IMMEDIATE '
        CREATE VECTOR INDEX IMAGES_IVF_INDEX ON IMAGES(EMBEDDING)
        ORGANIZATION NEIGHBOR PARTITIONS
        DISTANCE COSINE
        WITH TARGET ACCURACY 95
        PARAMETERS (type IVF, neighbor partitions 600)';
        DBMS_OUTPUT.PUT_LINE('Index IMAGES_IVF_INDEX created.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Index IMAGES_IVF_INDEX already exists.');
    END IF;

END;
/
