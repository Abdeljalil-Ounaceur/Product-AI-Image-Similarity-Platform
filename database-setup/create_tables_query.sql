DECLARE
    table_exists NUMBER;
BEGIN
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
END;
/
