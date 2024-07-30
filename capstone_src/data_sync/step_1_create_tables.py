# %%
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.conn_factory import getConnection as conn_factory


def _drop_facts(conn, fact_table_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {fact_table_name}")
    conn.commit()
    print("  - ", "dw.Fact_User: Table dropped")
     


def _create_dim_table(conn, table_name, columns, index_name, index_field):
    
    command = f"""
    IF EXISTS (SELECT * FROM sys.objects 
                WHERE object_id = OBJECT_ID(N'{table_name}') 
                        AND type in (N'U'))
    BEGIN
        DROP TABLE {table_name};
    END
    CREATE TABLE {table_name} (
        {columns}
    );
    
    CREATE NONCLUSTERED INDEX IDX_{index_name}_Name 
        ON {table_name}({index_field});
    """
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()

    print("  - ", f"{table_name}: Table created")


def setup_data_base_users_dim_tables():
    conn = conn_factory()

    _drop_facts(conn, "dw.Fact_User")

    _create_dim_table(conn, "dw.Dim_Platform", 
                    "Id INT PRIMARY KEY, Name NVARCHAR(250)", 
                    "Dim_platform", "Name")
    
    _create_dim_table(conn, "dw.Dim_Version_App", 
                    "Id INT PRIMARY KEY, Name NVARCHAR(250)", 
                    "Dim_Version_App", "Name")
    
    _create_dim_table(conn, "dw.Dim_Version_OS", 
                    "Id INT PRIMARY KEY, Name NVARCHAR(250)", 
                    "Dim_Version_OS", "Name")
    
    _create_dim_table(conn, "dw.Dim_Device", 
                    "Id INT PRIMARY KEY, Name NVARCHAR(250)", 
                    "Dim_Device", "Name")
    
    _create_dim_table(conn, "dw.Dim_Device_Class", 
                    "Id INT PRIMARY KEY, Name NVARCHAR(250)", 
                    "Dim_Device_Class", "Name")
    
    _create_dim_table(conn, "dw.Dim_User", 
                    "Id INT PRIMARY KEY, Username NVARCHAR(250)", 
                    "Dim_User", "Username")
    

    conn.close()


def setup_data_base_users_fact_table():
        conn = conn_factory()

        command = """
            IF EXISTS (SELECT * FROM sys.objects 
                        WHERE object_id = OBJECT_ID(N'dw.Fact_User') 
                                AND type in (N'U'))
            BEGIN
                DROP TABLE dw.Fact_User;
            END

            CREATE TABLE dw.Fact_User (
                UserId INT,
                CityId INT,
                DeviceId INT,
                PlatformId INT,
                DeviceClassId INT,
                OSVersionId INT,
                AppVersionId INT,
                Sessions INT,
                Screens INT,
                Events INT,
                Gestures INT,
                TimeInAppSeconds INT
            );

            

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_UserId
            FOREIGN KEY (UserId) REFERENCES dw.Dim_User(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_CityId
            FOREIGN KEY (CityId) REFERENCES dw.Dim_City(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_DeviceId
            FOREIGN KEY (DeviceId) REFERENCES dw.Dim_Device(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_PlatformId
            FOREIGN KEY (PlatformId) REFERENCES dw.Dim_Platform(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_DeviceClassId
            FOREIGN KEY (DeviceClassId) REFERENCES dw.Dim_Device_Class(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_OSVersionId
            FOREIGN KEY (OSVersionId) REFERENCES dw.Dim_Version_OS(Id);

            ALTER TABLE dw.Fact_User
            ADD CONSTRAINT FK_Fact_User_AppVersionId
            FOREIGN KEY (AppVersionId) REFERENCES dw.Dim_Version_App(Id);

            """
            
            # CREATE INDEX IDX_Fact_User_UserId ON dw.Fact_User(UserId);
            # CREATE INDEX IDX_Fact_User_CityId ON dw.Fact_User(CityId);
            # CREATE INDEX IDX_Fact_User_DeviceId ON dw.Fact_User(DeviceId);
            # CREATE INDEX IDX_Fact_User_PlatformId ON dw.Fact_User(PlatformId);
            # CREATE INDEX IDX_Fact_User_DeviceClassId ON dw.Fact_User(DeviceClassId);
            # CREATE INDEX IDX_Fact_User_OSVersionId ON dw.Fact_User(OSVersionId);
            # CREATE INDEX IDX_Fact_User_AppVersionId ON dw.Fact_User(AppVersionId);
            # """
        cursor = conn.cursor()

        cursor.execute(command)
        conn.commit()
        
        print("  - ", "dw.Fact_User: Table created")

        conn.close()


# %%
