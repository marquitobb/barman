from .database import get_connection

def get_all_motors():
    """Obtiene todos los motores y sus contenidos"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motors")
        columns = [column[0] for column in cursor.description]
        motors = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return motors

def get_motor_by_device(device):
    """Obtiene un motor por su dispositivo (relay_one, relay_two, etc.)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM motors WHERE device = ?", (device,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

def update_motor_content(device, content):
    """Actualiza el contenido de un motor"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE motors SET content = ? WHERE device = ?", (content, device))
        conn.commit()
        return cursor.rowcount > 0

def update_motor_level(device, amount_used):
    """Actualiza el nivel actual de un motor después de usar cierta cantidad"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE motors SET current_level = current_level - ? WHERE device = ? AND current_level >= ?",
            (amount_used, device, amount_used)
        )
        conn.commit()
        return cursor.rowcount > 0

def reset_motor_level(device):
    """Rellena un motor a su capacidad máxima"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE motors SET current_level = capacity WHERE device = ?", (device,))
        conn.commit()
        return cursor.rowcount > 0