from typing import Any, Text, Dict, List
import re
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset

# Importa il database
from database import ReservationDatabase


class ValidateRestaurantForm(FormValidationAction):
    """Validazione personalizzata per il form di prenotazione ristorante"""

    def name(self) -> Text:
        return "validate_restaurant_form"

    def validate_customer_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida il nome del cliente"""
        
        if not slot_value or len(slot_value.strip()) < 2:
            dispatcher.utter_message(text="Il nome deve contenere almeno 2 caratteri. Riprova:")
            return {"customer_name": None}
        
        # Pulisci e valida il nome completo (nome e cognome)
        clean_name = slot_value.strip()
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", clean_name):
            dispatcher.utter_message(text="Il nome può contenere solo lettere e spazi. Riprova:")
            return {"customer_name": None}
        
        # Mantieni il nome completo, non solo l'ultima parola
        return {"customer_name": clean_name.title()}

    def validate_customer_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida l'email del cliente"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_invalid_email")
            return {"customer_email": None}
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'


class ActionSubmitReservation(Action):
    """Azione per sottomettere la prenotazione"""
    
    def name(self) -> Text:
        return "action_submit_reservation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Raccoglie tutti i dati della prenotazione
        reservation_data = {
            'customer_name': tracker.get_slot("customer_name"),
            'customer_email': tracker.get_slot("customer_email"),
            'customer_phone': tracker.get_slot("customer_phone"),
            'reservation_date': tracker.get_slot("reservation_date"),
            'reservation_time': tracker.get_slot("reservation_time"),
            'number_of_guests': tracker.get_slot("number_of_guests")
        }
        
        # Simula controllo disponibilità
        reservation_date = reservation_data['reservation_date']
        reservation_time = reservation_data['reservation_time']
        
        # Lista di orari "occupati" per simulazione
        busy_slots = [
            ("20/12/2025", "20:00"),
            ("21/12/2025", "19:30"),
            ("22/12/2025", "21:00")
        ]
        
        if (reservation_date, reservation_time) in busy_slots:
            dispatcher.utter_message(response="utter_restaurant_full")
            return [SlotSet("reservation_time", None)]
        
        # Salva la prenotazione nel database
        try:
            db = ReservationDatabase()
            reservation_id = db.save_reservation(reservation_data)
            
            # Conferma prenotazione con ID
            dispatcher.utter_message(
                text=f"Perfetto {reservation_data['customer_name']}! La tua prenotazione è confermata:\n"
                     f"📋 ID Prenotazione: #{reservation_id}\n"
                     f"📅 Data: {reservation_data['reservation_date']}\n"
                     f"🕐 Ora: {reservation_data['reservation_time']}\n"
                     f"👥 Persone: {reservation_data['number_of_guests']}\n"
                     f"📧 Email: {reservation_data['customer_email']}\n"
                     f"📞 Telefono: {reservation_data['customer_phone']}\n\n"
                     f"Conserva questo ID per eventuali modifiche. Grazie per aver scelto il Ristorante Bella Vista!"
            )
            
            print(f"✅ PRENOTAZIONE SALVATA - ID: {reservation_id}")
            print(f"   Nome: {reservation_data['customer_name']}")
            print(f"   Data: {reservation_data['reservation_date']} alle {reservation_data['reservation_time']}")
            print(f"   Ospiti: {reservation_data['number_of_guests']}")
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Errore nel salvare la prenotazione: {e}")
            dispatcher.utter_message(
                text="La prenotazione è stata confermata, ma si è verificato un problema tecnico. "
                     "Contatta il ristorante per verificare."
            )
        
        return []


class ActionRestartConversation(Action):
    """Azione per riavviare la conversazione"""
    
    def name(self) -> Text:
        return "action_restart"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Conversazione riavviata. Come posso aiutarti?")
        return [AllSlotsReset()]
        
        if not re.match(email_pattern, slot_value.strip()):
            dispatcher.utter_message(response="utter_invalid_email")
            return {"customer_email": None}
        
        return {"customer_email": slot_value.strip().lower()}

    def validate_customer_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida il numero di telefono"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_invalid_phone")
            return {"customer_phone": None}
        
        # Rimuovi spazi e caratteri speciali tranne +
        clean_phone = re.sub(r'[^\d+]', '', str(slot_value).strip())
        
        # Verifica lunghezza (10-15 cifre per numeri internazionali)
        digits_only = re.sub(r'[^\d]', '', clean_phone)
        if len(digits_only) < 10 or len(digits_only) > 15:
            dispatcher.utter_message(response="utter_invalid_phone")
            return {"customer_phone": None}
        
        return {"customer_phone": clean_phone}

    def validate_reservation_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida la data di prenotazione"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_invalid_date")
            return {"reservation_date": None}
        
        try:
            # Gestisci date relative
            today = datetime.now().date()
            
            if slot_value.lower() in ["oggi", "today"]:
                return {"reservation_date": today.strftime("%d/%m/%Y")}
            elif slot_value.lower() in ["domani", "tomorrow"]:
                tomorrow = today + timedelta(days=1)
                return {"reservation_date": tomorrow.strftime("%d/%m/%Y")}
            elif slot_value.lower() in ["dopodomani"]:
                day_after = today + timedelta(days=2)
                return {"reservation_date": day_after.strftime("%d/%m/%Y")}
            
            # Prova a parsare la data nel formato gg/mm/aaaa
            date_parts = slot_value.strip().split('/')
            if len(date_parts) == 3:
                day, month, year = date_parts
                reservation_date = datetime(int(year), int(month), int(day)).date()
                
                # Verifica che la data non sia nel passato
                if reservation_date < today:
                    dispatcher.utter_message(response="utter_invalid_date")
                    return {"reservation_date": None}
                
                # Verifica che la data non sia troppo lontana (max 3 mesi)
                max_date = today + timedelta(days=90)
                if reservation_date > max_date:
                    dispatcher.utter_message(text="Possiamo accettare prenotazioni solo per i prossimi 3 mesi. Scegli una data più vicina:")
                    return {"reservation_date": None}
                
                return {"reservation_date": reservation_date.strftime("%d/%m/%Y")}
            
        except (ValueError, IndexError):
            pass
        
        dispatcher.utter_message(response="utter_invalid_date")
        return {"reservation_date": None}

    def validate_reservation_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida l'orario di prenotazione"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_invalid_time")
            return {"reservation_time": None}
        
        try:
            # Gestisci formati di tempo comuni
            time_str = slot_value.strip().lower()
            
            # Conversioni da testo
            time_conversions = {
                "sei": "18:00", "sei e mezza": "18:30",
                "sette": "19:00", "sette e mezza": "19:30",
                "otto": "20:00", "otto e mezza": "20:30",
                "nove": "21:00", "nove e mezza": "21:30",
                "dieci": "22:00", "dieci e mezza": "22:30",
                "undici": "23:00"
            }
            
            if time_str in time_conversions:
                time_str = time_conversions[time_str]
            
            # Aggiungi i due punti se mancano
            if len(time_str) == 4 and time_str.isdigit():
                time_str = time_str[:2] + ":" + time_str[2:]
            
            # Gestisci input incompleti come "21:"
            if time_str.endswith(':'):
                time_str += "00"
            
            # Prova a parsare l'orario
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            
            # Verifica che sia nell'orario di apertura (18:00 - 23:00)
            opening_time = datetime.strptime("18:00", "%H:%M").time()
            closing_time = datetime.strptime("23:00", "%H:%M").time()
            
            if not (opening_time <= time_obj <= closing_time):
                dispatcher.utter_message(response="utter_invalid_time")
                return {"reservation_time": None}
            
            return {"reservation_time": time_obj.strftime("%H:%M")}
            
        except ValueError:
            dispatcher.utter_message(response="utter_invalid_time")
            return {"reservation_time": None}

    def validate_number_of_guests(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida il numero di ospiti"""
        
        if not slot_value:
            dispatcher.utter_message(response="utter_invalid_guests")
            return {"number_of_guests": None}
        
        try:
            # Conversioni da testo a numero
            text_to_num = {
                "uno": "1", "una": "1",
                "due": "2", 
                "tre": "3",
                "quattro": "4",
                "cinque": "5",
                "sei": "6",
                "sette": "7",
                "otto": "8",
                "nove": "9",
                "dieci": "10",
                "undici": "11",
                "dodici": "12"
            }
            
            guest_str = slot_value.strip().lower()
            if guest_str in text_to_num:
                guest_str = text_to_num[guest_str]
            
            guests = int(guest_str)
            
            if guests < 1 or guests > 12:
                dispatcher.utter_message(response="utter_invalid_guests")
                return {"number_of_guests": None}
            
            return {"number_of_guests": str(guests)}
            
        except ValueError:
            dispatcher.utter_message(response="utter_invalid_guests")
            return {"number_of_guests": None}


class ActionSubmitReservation(Action):
    """Azione per sottomettere la prenotazione"""
    
    def name(self) -> Text:
        return "action_submit_reservation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simula controllo disponibilità
        reservation_date = tracker.get_slot("reservation_date")
        reservation_time = tracker.get_slot("reservation_time")
        
        # Lista di orari "occupati" per simulazione
        busy_slots = [
            ("20/12/2025", "20:00"),
            ("21/12/2025", "19:30"),
            ("22/12/2025", "21:00")
        ]
        
        if (reservation_date, reservation_time) in busy_slots:
            dispatcher.utter_message(response="utter_restaurant_full")
            return [SlotSet("reservation_time", None)]
        
        # Conferma prenotazione
        dispatcher.utter_message(response="utter_reservation_confirmed")
        
        # Qui potresti aggiungere logica per salvare nel database
        # save_reservation_to_db(tracker.slots)
        
        return []


class ActionRestartConversation(Action):
    """Azione per riavviare la conversazione"""
    
    def name(self) -> Text:
        return "action_restart"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Conversazione riavviata. Come posso aiutarti?")
        return [AllSlotsReset()]