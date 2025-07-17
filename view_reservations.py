#!/usr/bin/env python3
"""
Script per visualizzare e gestire le prenotazioni del ristorante
"""

from database import ReservationDatabase
import sys
from datetime import datetime

def main():
    db = ReservationDatabase()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "view" or command == "list":
            db.print_all_reservations()
        
        elif command == "today":
            today = datetime.now().strftime("%d/%m/%Y")
            reservations = db.get_reservations_by_date(today)
            
            if not reservations:
                print(f"📋 Nessuna prenotazione per oggi ({today})")
            else:
                print(f"\n📋 PRENOTAZIONI PER OGGI ({today})")
                print("="*50)
                for res in reservations:
                    print(f"🕐 {res['reservation_time']} - {res['customer_name']} ({res['number_of_guests']} persone)")
                    print(f"   📧 {res['customer_email']} | 📞 {res['customer_phone']}")
                    print("-" * 30)
        
        elif command == "export":
            from database import export_to_csv
            export_to_csv()
        
        elif command == "help":
            print_help()
        
        else:
            print(f"❌ Comando sconosciuto: {command}")
            print_help()
    
    else:
        # Mostra menu interattivo
        interactive_menu(db)

def interactive_menu(db):
    """Menu interattivo per gestire le prenotazioni"""
    while True:
        print("\n" + "="*50)
        print("🍽️  GESTIONE PRENOTAZIONI RISTORANTE")
        print("="*50)
        print("1. Visualizza tutte le prenotazioni")
        print("2. Prenotazioni di oggi")
        print("3. Prenotazioni per data specifica")
        print("4. Esporta in CSV")
        print("5. Cancella prenotazione")
        print("6. Statistiche")
        print("0. Esci")
        print("-"*50)
        
        choice = input("Scegli un'opzione (0-6): ").strip()
        
        if choice == "1":
            db.print_all_reservations()
        
        elif choice == "2":
            today = datetime.now().strftime("%d/%m/%Y")
            show_reservations_by_date(db, today)
        
        elif choice == "3":
            date = input("Inserisci la data (gg/mm/aaaa): ").strip()
            show_reservations_by_date(db, date)
        
        elif choice == "4":
            from database import export_to_csv
            filename = input("Nome file (default: reservations.csv): ").strip()
            if not filename:
                filename = "reservations.csv"
            export_to_csv(filename)
        
        elif choice == "5":
            cancel_reservation(db)
        
        elif choice == "6":
            show_statistics(db)
        
        elif choice == "0":
            print("👋 Arrivederci!")
            break
        
        else:
            print("❌ Opzione non valida!")

def show_reservations_by_date(db, date):
    """Mostra prenotazioni per una data specifica"""
    reservations = db.get_reservations_by_date(date)
    
    if not reservations:
        print(f"📋 Nessuna prenotazione per il {date}")
        return
    
    print(f"\n📋 PRENOTAZIONI PER IL {date}")
    print("="*60)
    
    for res in reservations:
        print(f"🕐 {res['reservation_time']} - {res['customer_name']} ({res['number_of_guests']} persone)")
        print(f"   📧 {res['customer_email']} | 📞 {res['customer_phone']}")
        print(f"   📋 ID: #{res['id']} | Status: {res['status']}")
        print("-" * 40)

def cancel_reservation(db):
    """Cancella una prenotazione"""
    try:
        reservation_id = int(input("Inserisci l'ID della prenotazione da cancellare: ").strip())
        
        # Mostra la prenotazione prima di cancellarla
        reservations = db.get_all_reservations()
        reservation = next((r for r in reservations if r['id'] == reservation_id), None)
        
        if not reservation:
            print(f"❌ Prenotazione con ID #{reservation_id} non trovata!")
            return
        
        print(f"\n📋 Prenotazione da cancellare:")
        print(f"   👤 {reservation['customer_name']}")
        print(f"   📅 {reservation['reservation_date']} alle {reservation['reservation_time']}")
        print(f"   👥 {reservation['number_of_guests']} persone")
        
        confirm = input("\nSei sicuro di voler cancellare questa prenotazione? (s/N): ").strip().lower()
        
        if confirm == 's' or confirm == 'si':
            db.delete_reservation(reservation_id)
            print(f"✅ Prenotazione #{reservation_id} cancellata con successo!")
        else:
            print("❌ Cancellazione annullata.")
            
    except ValueError:
        print("❌ ID non valido!")
    except Exception as e:
        print(f"❌ Errore: {e}")

def show_statistics(db):
    """Mostra statistiche delle prenotazioni"""
    reservations = db.get_all_reservations()
    
    if not reservations:
        print("📊 Nessuna prenotazione per calcolare le statistiche.")
        return
    
    # Calcola statistiche
    total_reservations = len(reservations)
    total_guests = sum(int(r['number_of_guests']) for r in reservations)
    avg_guests = total_guests / total_reservations if total_reservations > 0 else 0
    
    # Gruppo per data
    dates = {}
    for res in reservations:
        date = res['reservation_date']
        if date not in dates:
            dates[date] = 0
        dates[date] += 1
    
    # Gruppo per orario
    times = {}
    for res in reservations:
        time = res['reservation_time']
        if time not in times:
            times[time] = 0
        times[time] += 1
    
    print("\n📊 STATISTICHE PRENOTAZIONI")
    print("="*40)
    print(f"📋 Totale prenotazioni: {total_reservations}")
    print(f"👥 Totale ospiti: {total_guests}")
    print(f"📈 Media ospiti per prenotazione: {avg_guests:.1f}")
    
    print(f"\n📅 Giorni più richiesti:")
    for date, count in sorted(dates.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {date}: {count} prenotazioni")
    
    print(f"\n🕐 Orari più richiesti:")
    for time, count in sorted(times.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {time}: {count} prenotazioni")

def print_help():
    """Stampa l'aiuto"""
    print("""
📋 COMANDI DISPONIBILI:
    python view_reservations.py view       - Visualizza tutte le prenotazioni
    python view_reservations.py today      - Prenotazioni di oggi
    python view_reservations.py export     - Esporta in CSV
    python view_reservations.py help       - Mostra questo aiuto
    python view_reservations.py            - Menu interattivo
    """)

if __name__ == "__main__":
    main()