import psycopg2
from psycopg2 import Error

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

    # Comandos para eliminar las tablas si existen
    drop_table_queries = [
        "DROP TABLE IF EXISTS producto02 CASCADE;",
        "DROP TABLE IF EXISTS Tipo_Producto02 CASCADE;"
    ]
    for query in drop_table_queries:
        cursor.execute(query)

    # Comando para crear la tabla Tipo_Producto02
    create_table_tipo_producto_query = """
    CREATE TABLE Tipo_Producto02 (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        descripcion TEXT
    );
    """
    cursor.execute(create_table_tipo_producto_query)

    # Insertar tipos de productos tecnológicos en Tipo_Producto02
    insert_tipo_producto_query = """
    INSERT INTO Tipo_Producto02 (id, nombre, descripcion) VALUES
    (1, 'Laptop', 'Computadoras portátiles para uso personal o profesional'),
    (2, 'Smartphone', 'Teléfonos inteligentes con capacidad de conexión a internet'),
    (3, 'Tablet', 'Dispositivos táctiles ideales para trabajo y entretenimiento'),
    (4, 'Accesorios', 'Periféricos y complementos para dispositivos tecnológicos'),
    (5, 'Monitor', 'Pantallas para ordenadores y otras aplicaciones');
    """
    cursor.execute(insert_tipo_producto_query)

    # Comando para crear la tabla producto02
    create_table_producto_query = """
    CREATE TABLE producto02 (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        local_kw VARCHAR(255) NOT NULL,
        id_t_producto INTEGER NOT NULL,
        imagen_url TEXT,
        precio FLOAT,
        descripcion TEXT,
        FOREIGN KEY (id_t_producto) REFERENCES Tipo_Producto02 (id)
    );
    """
    cursor.execute(create_table_producto_query)

    # Insertar 10 productos tecnológicos en producto02
    insert_productos_query = """
    INSERT INTO producto02 (id, nombre, local_kw, id_t_producto, imagen_url, precio, descripcion) VALUES
    (1, 'MacBook Air M2', 'macbook-air-m2', 1, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mb-air-m2-gold-select-202206_GEO_EMEA_LANG_EN?wid=940&hei=1112&fmt=jpeg&qlt=95&.v=1655321289604', 1199.99, 'Laptop ligera y potente con chip M2 de Apple'),
    (2, 'Dell XPS 13', 'dell-xps-13', 1, 'https://www.dell.com/sites/csimages/App-Merchandizing_Images/all/xps-13-laptop-9320-category-page.png', 999.99, 'Laptop de alta gama con pantalla InfinityEdge'),
    (3, 'iPhone 14 Pro', 'iphone-14-pro', 2, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-14-pro-max-deeppurple-select_FMT_WHH?wid=470&hei=556&fmt=png-alpha&.v=1660753619946', 1099.99, 'Teléfono inteligente con cámara avanzada y pantalla ProMotion'),
    (4, 'Samsung Galaxy S23', 'samsung-galaxy-s23', 2, 'https://image-us.samsung.com/SamsungUS/home/mobile/phones/pdp/SM-S916UZKEXAA/Gallery1/MOCK01/PDP-Gallery-S23-B1_PhantomBlack-1600x1200.jpg', 799.99, 'Teléfono inteligente con pantalla AMOLED y cámara de alta resolución'),
    (5, 'iPad Pro 11', 'ipad-pro-11', 3, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-11-select-202212-202303_GEO_EMEA_LANG_EN?wid=470&hei=556&fmt=png-alpha&.v=1678406016774', 899.99, 'Tablet potente con pantalla Liquid Retina y chip M1'),
    (6, 'Samsung Galaxy Tab S9', 'samsung-galaxy-tab-s9', 3, 'https://image-us.samsung.com/us/smartphones/galaxy-tab-s/galaxy-tab-s9-ultra/product/images/SM-X910NZAEXAR_001_Front_PhantomGraphite.webp', 749.99, 'Tablet con pantalla AMOLED y S Pen incluido'),
    (7, 'Teclado Mecánico Logitech', 'teclado-mecanico-logitech', 4, 'https://resource.logitechg.com/w_800,c_limit,q_auto:best,f_auto,dpr_1.0/d_transparent.gif/content/dam/gaming/en/products/pro-keyboard/pro-x-keyboard.png?v=1', 129.99, 'Teclado mecánico con switches intercambiables'),
    (8, 'Auriculares Sony WH-1000XM5', 'auriculares-sony-wh-1000xm5', 4, 'https://m.media-amazon.com/images/I/41IA6CSwPzL._AC_UY327_FMwebp_QL65_.jpg', 349.99, 'Auriculares inalámbricos con cancelación de ruido activa'),
    (9, 'Monitor LG UltraGear 27"', 'monitor-lg-ultragear-27', 5, 'https://www.lg.com/uk/images/monitors/md07508486/gallery/D-1.jpg', 499.99, 'Monitor gaming con alta tasa de refresco y resolución QHD'),
    (10, 'Monitor Dell UltraSharp 32"', 'monitor-dell-ultrasharp-32', 5, 'https://www.dell.com/sites/csimages/Video_Imagery/all/ultrasharp-32.jpg', 1299.99, 'Monitor profesional con resolución 4K y amplia gama de colores');
    """
    cursor.execute(insert_productos_query)

    # Confirmar los cambios
    connection.commit()

    print("Tablas creadas, columnas añadidas y datos insertados exitosamente")

except (Exception, Error) as error:
    print("Error al conectar a PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexión a PostgreSQL cerrada")