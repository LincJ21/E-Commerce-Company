import psycopg2
from psycopg2 import Error

# Definir las consultas SQL en el orden correcto
sql_queries = [
    '''
    CREATE TABLE Tipo_Producto (
        Id_Compra SERIAL PRIMARY KEY,
        Nombre VARCHAR(100),
        Descripcion TEXT
    );
    ''',
    '''
    CREATE TABLE Ubicacion (
        Id_Ubicacion SERIAL PRIMARY KEY,
        Almacen VARCHAR(50),
        Sucursal VARCHAR(50),
        Estante VARCHAR(50)
    );
    ''',
    '''
    CREATE TABLE Cliente (
        Id_Cliente SERIAL PRIMARY KEY,
        Nombre VARCHAR(100),
        Email VARCHAR(100) UNIQUE,
        Fecha_Registro DATE,
        Id_H_Compras INT
    );
    ''',
    '''
    CREATE TABLE Direccion (
        Id_Direccion SERIAL PRIMARY KEY,
        Ciudad VARCHAR(100),
        Codigo_Postal VARCHAR(10),
        Barrio VARCHAR(100),
        Detalle_Adicional TEXT
    );
    ''',
    '''
    CREATE TABLE Pago (
        Id_Pago SERIAL PRIMARY KEY,
        Fecha_Pago DATE,
        Metodo_Pago VARCHAR(50),
        Estado_Pago VARCHAR(50)
    );
    ''',
    '''
    CREATE TABLE Producto (
        Id_Producto SERIAL PRIMARY KEY,
        Nombre VARCHAR(100),
        Precio DECIMAL(10, 2),
        Imagen_URL TEXT,
        Id_T_Producto INT REFERENCES Tipo_Producto(Id_Compra)
    );
    ''',
    '''
    CREATE TABLE Detalle_Producto (
        Id_Detalle SERIAL PRIMARY KEY,
        Id_Producto INT REFERENCES Producto(Id_Producto),
        Cantidad INT,
        Precio DECIMAL(10, 2)
    );
    ''',
    '''
    CREATE TABLE Pedido (
        Id_Pedido SERIAL PRIMARY KEY,
        Fecha_Creacion DATE,
        Estado VARCHAR(50),
        Id_Cliente INT REFERENCES Cliente(Id_Cliente),
        Id_Detalle INT REFERENCES Detalle_Producto(Id_Detalle)
    );
    ''',
    '''
    CREATE TABLE Compra (
        Id_Compra SERIAL PRIMARY KEY,
        Id_Pago INT REFERENCES Pago(Id_Pago),
        Id_Pedido INT REFERENCES Pedido(Id_Pedido)
    );
    ''',
    '''
    CREATE TABLE Historial_Compras (
        Id_H_Compras SERIAL PRIMARY KEY,
        Id_Compra INT REFERENCES Compra(Id_Compra),
        Estado_Compra VARCHAR(50),
        Descripcion TEXT
    );
    ''',
    '''
    CREATE TABLE Inventario (
        Id_Inventario SERIAL PRIMARY KEY,
        Id_Producto INT REFERENCES Producto(Id_Producto),
        Cantidad_Disponible INT,
        Ubicacion INT REFERENCES Ubicacion(Id_Ubicacion)
    );
    ''',
    '''
    CREATE TABLE C_D (
        Id_Compra INT REFERENCES Compra(Id_Compra),
        Id_Cliente INT REFERENCES Cliente(Id_Cliente),
        Id_Direccion INT REFERENCES Direccion(Id_Direccion),
        PRIMARY KEY (Id_Compra, Id_Cliente, Id_Direccion)
    );
    '''
]

try:
    # Establecer la conexión
    connection = psycopg2.connect(
        dbname="railway",                  # Nombre de la base de datos
        user="postgres",                   # Usuario
        password="SKLYjqmQgbHpHWWxGHIEukBxFpPLipLQ",  # Contraseña
        host="junction.proxy.rlwy.net",    # Dominio proxy para conexiones externas
        port="22062",                      # Puerto del proxy
        sslmode="require"                  # Modo SSL
    )

    # Crear un cursor
    cursor = connection.cursor()
    
    # Ejecutar cada consulta SQL
    for query in sql_queries:
        cursor.execute(query)
    
    # Confirmar cambios
    connection.commit()
    print("Tablas creadas exitosamente en la base de datos")

except psycopg2.Error as error:
    print("Error al conectar o crear las tablas en la base de datos:", error)

finally:
    # Cerrar el cursor y la conexión
    if cursor:
        cursor.close()
    if connection:
        connection.close()
