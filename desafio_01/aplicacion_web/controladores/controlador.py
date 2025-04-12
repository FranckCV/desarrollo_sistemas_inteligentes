from controladores.bd import obtener_conexion

def obtener_persona_por_img(img):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT per.id , per.nombre FROM persona per left join foto ft on ft.personaid = per.id WHERE nom_archivo = %s", 
            (str(img),))
        rpta = cursor.fetchone()
    conexion.close()
    return rpta


def obtener_imgs_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT nom_archivo FROM foto WHERE personaid = %s ", 
            (id,))
        rpta = cursor.fetchall()
    conexion.close()
    return [r[0] for r in rpta]


def obtener_img_principal_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT nom_archivo FROM foto WHERE personaid = %s and principal = 1", 
            (id,))
        rpta = cursor.fetchone()
    conexion.close()
    return rpta[0]


def insertar_foto(nombre , personaid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO foto (nom_archivo, principal , personaid)
            VALUES (%s, 0 , %s)
        """, (nombre, personaid ))
        rpta_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return rpta_id


def insertar_persona(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO persona (nombre)
            VALUES (%s)
        """, (nombre))
        rpta_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return rpta_id







# def insertar_empresa(nombre, razonsocial, ruc, estado):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("""
#             INSERT INTO empresa (nombre, razonsocial, ruc, estado, fechacreacion)
#             VALUES (%s, %s, %s, %s, NOW())
#         """, (nombre, razonsocial, ruc, estado))
#         empresa_id = cursor.lastrowid
#     conexion.commit()
#     conexion.close()
#     return empresa_id


# def obtener_empresas():
#     conexion = obtener_conexion()
#     empresas = []
#     with conexion.cursor() as cursor:
#         cursor.execute("SELECT id, nombre, razonsocial, ruc, estado FROM empresa")
#         empresas = cursor.fetchall()
#     conexion.close()
#     return empresas


# def eliminar_empresa(id):
#     conexion = obtener_conexion()
#     try:
#         with conexion.cursor() as cursor:
#             conexion.begin()
#             cursor.execute("DELETE FROM cuota WHERE empresaid = %s", (id,))
#             cursor.execute("DELETE FROM empresa WHERE id = %s", (id,))
#         conexion.commit()
#     except Exception as e:
#         conexion.rollback()
#         print(f"Error: {e}")
#     finally:
#         conexion.close()

# def obtener_empresa_por_id(id):
#     conexion = obtener_conexion()
#     empresa = None
#     with conexion.cursor() as cursor:
#         cursor.execute(
#             "SELECT id, nombre, razonsocial, ruc, estado, fechacreacion, fechaactualizacion FROM empresa WHERE id = %s", (id,))
#         empresa = cursor.fetchone()
#     conexion.close()
#     return empresa

# def tiene_sucursales(idempresa):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#         SELECT 
#             e.id, 
#             COUNT(DISTINCT s.id) AS sucursales_count
#         FROM empresa e
#         LEFT JOIN sucursal s ON s.empresaid = e.id
#         LEFT JOIN postulante po ON po.sucursalid = s.id
#         WHERE e.id = %s
#         GROUP BY e.id;
#         '''
#         cursor.execute(sql, (idempresa,))
#         empresas = cursor.fetchone()
#     conexion.close()
#     return empresas

# def actualizar_empresa(nombre, razonsocial, ruc, estado, id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         cursor.execute("""
#             UPDATE empresa
#             SET nombre = %s, razonsocial = %s, ruc = %s, estado = %s, fechaactualizacion = NOW()
#             WHERE id = %s
#         """, (nombre, razonsocial, ruc, estado, id))
#     conexion.commit()
#     conexion.close()

# def actualizar_empresa_y_cuota(nombre, razonsocial, ruc, estado, id, cantidad, momentocobro, empresaid):
#     conexion = obtener_conexion()
#     try:
#         with conexion.cursor() as cursor:
#             conexion.begin()
            
#             cursor.execute("""
#                 UPDATE empresa
#                 SET nombre = %s, razonsocial = %s, ruc = %s, estado = %s, fechaactualizacion = NOW()
#                 WHERE id = %s
#             """, (nombre, razonsocial, ruc, estado, id))
            
#             cursor.execute("""
#                 UPDATE cuota
#                 SET cantidad = %s, momentocobro = %s
#                 WHERE empresaid = %s
#             """, (cantidad, momentocobro, empresaid))
        
#         conexion.commit()
#     except Exception as e:
#         conexion.rollback()
#         print(f"Error: {e}")
#     finally:
#         conexion.close()

# def obtener_empresas_2():
#     conexion = obtener_conexion()
#     empresas = []
#     with conexion.cursor() as cursor:
#         sql = '''
#         SELECT 
#             e.id, 
#             e.nombre, 
#             e.razonsocial, 
#             e.ruc,
#             e.estado,
#             COUNT(CASE WHEN po.estado = 'N' THEN po.id END) AS postulantes_count,
#             COUNT(DISTINCT s.id) AS sucursales_count,
#             c.id,
#             c.cantidad,
#             c.avancecuota
#         FROM empresa e
#         LEFT JOIN sucursal s ON s.empresaid = e.id
#         LEFT JOIN postulante po ON po.sucursalid = s.id
#         LEFT JOIN cuota c ON c.empresaid = e.id
#         GROUP BY e.id, e.nombre, e.razonsocial, e.ruc, e.estado, c.cantidad, c.avancecuota;
#         '''
#         cursor.execute(sql)
#         empresas = cursor.fetchall()
#     conexion.close()
#     return empresas


# def obtener_empresas_3():
#     conexion = obtener_conexion()
#     empresas = []
#     with conexion.cursor() as cursor:
#         sql = '''
#         SELECT 
#             e.id, 
#             e.nombre, 
#             COUNT(CASE WHEN po.estado = 'N' THEN po.id END) AS postulantes_count
#         FROM empresa e
#         LEFT JOIN sucursal s ON s.empresaid = e.id
#         LEFT JOIN postulante po ON po.sucursalid = s.id
#         LEFT JOIN cuota c ON c.empresaid = e.id
#         GROUP BY e.id, e.nombre, e.razonsocial, e.ruc, e.estado, c.cantidad, c.avancecuota;
#         '''
#         cursor.execute(sql)
#         empresas = cursor.fetchall()
#     conexion.close()
#     return empresas



# def transaccion_empresa_y_cuota(nombre, razonsocial, ruc, estado, cantidad, momentocobro, avancecuota):
#     conexion = obtener_conexion()
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO empresa (nombre, razonsocial, ruc, estado, fechacreacion)
#                 VALUES (%s, %s, %s, %s, NOW())
#             """, (nombre, razonsocial, ruc, estado))
#             empresa_id = cursor.lastrowid

#             cursor.execute("""
#                 INSERT INTO cuota (cantidad, momentocobro, avancecuota, empresaid, totalpostulantes)
#                 VALUES (%s, %s, %s, %s, 0)
#             """, (cantidad, momentocobro, avancecuota, empresa_id))
#             cuota_id = cursor.lastrowid

#             cursor.execute("""
#                 INSERT INTO rango (tanda, inicio, final, estado, cuotaid)
#                 VALUES (1, 1, %s, 'A', %s)
#             """, (cantidad, cuota_id))

#         conexion.commit()
#     except Exception as e:
#         conexion.rollback()
#         raise e
#     finally:
#         conexion.close()

#     return empresa_id




# def insert_empresa_cuota_rango(nombre, razonsocial, ruc, estado, cantidad, momentocobro, avancecuota):
#     conexion = obtener_conexion()
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO empresa (nombre, razonsocial, ruc, estado, fechacreacion)
#                 VALUES (%s, %s, %s, %s, NOW())
#             """, (nombre, razonsocial, ruc, estado))
#             empresa_id = cursor.lastrowid

#             cursor.execute("""
#                 INSERT INTO cuota (cantidad, momentocobro, avancecuota, empresaid, totalpostulantes)
#                 VALUES (%s, %s, %s, %s, 0)
#             """, (cantidad, momentocobro, avancecuota, empresa_id))
#             cuota_id = cursor.lastrowid

#             cursor.execute("""
#                 INSERT INTO rango (tanda, inicio, final, estado, cuotaid)
#                 VALUES (1, 1, %s, 'A', %s)
#             """, (cantidad, cuota_id))

#         conexion.commit()
#     except Exception as e:
#         conexion.rollback()
#         raise e
#     finally:
#         conexion.close()

#     return empresa_id