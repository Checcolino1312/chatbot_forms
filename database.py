import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any

class ReservationDatabase:
    """Gestisce le prenotazioni in un database SQLite"""
    
    def __init__(self, db_path: str = "reservations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Crea la tabella se non esiste"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                reservation_time TEXT NOT NULL,
                number_of_guests INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'confirmed'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_reservation(self, reservation_data: Dict[str, Any]) -> int:
        """Salva una prenotazione nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reservations 
            (customer_name, customer_email, customer_phone, 
             reservation_date, reservation_time, number_of_guests)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            reservation_data.get('customer_name'),
            reservation_data.get('customer_email'),
            reservation_data.get('customer_phone'),
            reservation_data.get('reservation_date'),
            reservation_data.get('reservation_time'),
            int(reservation_data.get('number_of_guests', 1))
        ))
        
        reservation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return reservation_id
    
    def get_all_reservations(self) -> List[Dict[str, Any]]:
        """Recupera tutte le prenotazioni"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM reservations 
            ORDER BY reservation_date, reservation_time
        ''')
        
        columns = [description[0] for description in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results
    
    def get_reservations_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Recupera prenotazioni per una data specifica"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM reservations 
            WHERE reservation_date = ? 
            ORDER BY reservation_time
        ''', (date,))
        
        columns = [description[0] for description in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return results
    
    def update_reservation_status(self, reservation_id: int, status: str):
        """Aggiorna lo status di una prenotazione"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE reservations 
            SET status = ? 
            WHERE id = ?
        ''', (status, reservation_id))
        
        conn.commit()
        conn.close()
    
    def delete_reservation(self, reservation_id: int):
        """Cancella una prenotazione"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
        
        conn.commit()
        conn.close()
    
    def print_all_reservations(self):
        """Stampa tutte le prenotazioni in formato leggibile"""
        reservations = self.get_all_reservations()
        
        if not reservations:
            print("📋 Nessuna prenotazione trovata.")
            return
        
        print("\n" + "="*80)
        print("📋 PRENOTAZIONI RISTORANTE BELLA VISTA")
        print("="*80)
        
        for reservation in reservations:
            print(f"""
📅 Prenotazione #{reservation['id']}
👤 Nome: {reservation['customer_name']}
📧 Email: {reservation['customer_email']}
📞 Telefono: {reservation['customer_phone']}
📅 Data: {reservation['reservation_date']}
🕐 Ora: {reservation['reservation_time']}
👥 Ospiti: {reservation['number_of_guests']}
📝 Status: {reservation['status']}
⏰ Creata: {reservation['created_at']}
{'-'*50}""")


# Funzione helper per visualizzare le prenotazioni
def view_reservations():
    """Visualizza tutte le prenotazioni"""
    db = ReservationDatabase()
    db.print_all_reservations()


# Funzione helper per esportare in CSV
def export_to_csv(filename: str = "reservations.csv"):
    """Esporta le prenotazioni in CSV"""
    import csv
    
    db = ReservationDatabase()
    reservations = db.get_all_reservations()
    
    if not reservations:
        print("Nessuna prenotazione da esportare.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = reservations[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(reservations)
    
    print(f"✅ Prenotazioni esportate in {filename}")


if __name__ == "__main__":
    # Test del database
    db = ReservationDatabase()
    
    # Esempio di prenotazione
    sample_reservation = {
        'customer_name': 'Mario Rossi',
        'customer_email': 'mario.rossi@email.com',
        'customer_phone': '3401234567',
        'reservation_date': '20/12/2025',
        'reservation_time': '20:00',
        'number_of_guests': '2'
    }
    
    # Salva la prenotazione di esempio
    reservation_id = db.save_reservation(sample_reservation)
    print(f"✅ Prenotazione salvata con ID: {reservation_id}")
    
    # Mostra tutte le prenotazioni
    db.print_all_reservations()