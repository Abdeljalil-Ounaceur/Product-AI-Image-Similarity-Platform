BEGIN
    -- Switch to FREEPDB1 container
    EXECUTE IMMEDIATE 'ALTER SESSION SET CONTAINER = FREEPDB1';

    -- Create USERS tablespace if it doesn't exist
    BEGIN
        EXECUTE IMMEDIATE '
        CREATE TABLESPACE USERS
        DATAFILE ''/opt/oracle/oradata/FREE/FREEPDB1/users01.dbf''
        SIZE 100M
        AUTOEXTEND ON
        NEXT 10M
        MAXSIZE UNLIMITED';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -1543 THEN  -- Ignore tablespace already exists error
                RAISE;
            END IF;
    END;

    -- Create user db_user with password and unlimited quota on USERS tablespace
    BEGIN
        EXECUTE IMMEDIATE 'CREATE USER db_user IDENTIFIED BY password DEFAULT TABLESPACE USERS QUOTA UNLIMITED ON USERS';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -1920 THEN  -- Ignore user already exists error
                RAISE;
            END IF;
    END;

    -- Grant privileges to db_user
    EXECUTE IMMEDIATE 'GRANT CONNECT, RESOURCE TO db_user';

    -- Create tables owned by db_user if they do not exist
    BEGIN
        EXECUTE IMMEDIATE '
        CREATE TABLE db_user.PRODUCT_IMAGE_EMBEDDINGS (
            image_id VARCHAR2(255) PRIMARY KEY,
            embedding VECTOR(512, FLOAT32)
        )';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -955 THEN -- name is already used by an existing object
                RAISE;
            END IF;
    END;

    BEGIN
        EXECUTE IMMEDIATE '
        CREATE TABLE db_user.USER_UPLOADED_IMAGE_EMBEDDINGS (
            image_id VARCHAR2(255) PRIMARY KEY,
            embedding VECTOR(512, FLOAT32)
        )';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -955 THEN -- name is already used by an existing object
                RAISE;
            END IF;
    END;

    -- Create vector index on db_user.PRODUCT_IMAGE_EMBEDDINGS if it does not exist
    BEGIN
        EXECUTE IMMEDIATE '
        CREATE VECTOR INDEX db_user.PRODUCT_IMAGE_IVF_INDEX ON db_user.PRODUCT_IMAGE_EMBEDDINGS(embedding)
        ORGANIZATION NEIGHBOR PARTITIONS
        DISTANCE COSINE
        WITH TARGET ACCURACY 95
        PARAMETERS (type IVF, neighbor partitions 600)';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -955 THEN -- name is already used by an existing object
                RAISE;
            END IF;
    END;

END;
/
