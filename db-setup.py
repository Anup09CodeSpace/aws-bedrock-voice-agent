import boto3
import datetime 
import time 
from decimal import Decimal 

def setup_demo_data(): 
 # Initialize DynamoDB resource 
 # Make sure your AWS credentials are set in your environment 
 dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 

 # --- 1. Define Table Schemas --- 
 tables = { 
 'Hotel_Guests': { 
 'KeySchema': [{'AttributeName': 'guestName', 'KeyType': 'HASH'}], 
 'AttributeDefinitions': [{'AttributeName': 'guestName', 'AttributeType': 'S'}] 
 }, 
 'Hotel_Reservations': { 
 'KeySchema': [{'AttributeName': 'reservationId', 'KeyType': 'HASH'}], 
 'AttributeDefinitions': [{'AttributeName': 'reservationId', 'AttributeType': 'S'}] 
 } 
 } 

 # --- 2. Delete Old Tables & Create New Ones --- 
 print("--- Resetting Database ---") 
 for table_name, schema in tables.items(): 
  table = dynamodb.Table(table_name) 
  # Delete if exists 
  try: 
   print(f"Deleting old table: {table_name}...") 
   table.delete() 
   table.wait_until_not_exists() 
   print(f"Deleted {table_name}.") 
  except Exception as e: 
   # Verify if error is just "ResourceNotFoundException" (which is fine) 
   if "ResourceNotFoundException" in str(e): 
    pass 
   else: 
    print(f"Warning deleting {table_name}: {e}") 

  # Create new 
  print(f"Creating new table: {table_name}...") 
  try: 
   dynamodb.create_table( 
    TableName=table_name, 
    KeySchema=schema['KeySchema'], 
    AttributeDefinitions=schema['AttributeDefinitions'], 
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5} 
   ) 
   # Refresh table reference and wait for it to exist 
   table = dynamodb.Table(table_name) 
   table.wait_until_exists() 
   print(f"Ready: {table_name}") 
  except Exception as e: 
   print(f"Error creating {table_name}: {e}") 
   return 

 # --- 3. Seed Guest Data --- 
 print("\n--- Seeding Hotel Guests ---") 
 guests = dynamodb.Table('Hotel_Guests') 

 # Guest 1: Upcoming stay, Gold member, no issues 
 guests.put_item(Item={ 
  'guestName': 'Anna Smith', 
  'dob': '1991-06-05', 
  'loyaltyTier': 'Gold', 
  'phoneNumber': '+1-555-111-2222', 
  'email': 'anna.smith@example.com', 
  'preferredLanguage': 'en-US', 
  'preferredBedType': 'King', 
  'preferredView': 'Sea', 
  'vipFlag': True 
 }) 

 # Guest 2: Has a reservation with an outstanding balance and special requests 
 guests.put_item(Item={ 
  'guestName': 'Mark Johnson', 
  'dob': '1985-01-21', 
  'loyaltyTier': 'Standard', 
  'phoneNumber': '+1-555-333-4444', 
  'email': 'mark.johnson@example.com', 
  'preferredLanguage': 'en-US', 
  'preferredBedType': 'Queen', 
  'preferredView': 'City', 
  'vipFlag': False 
 }) 

 # --- Added Guests (extra demo data) --- 
 guests.put_item(Item={ 
  'guestName': 'Priya Nair', 
  'dob': '1993-11-12', 
  'loyaltyTier': 'Platinum', 
  'phoneNumber': '+1-555-777-1212', 
  'email': 'priya.nair@example.com', 
  'preferredLanguage': 'en-CA', 
  'preferredBedType': 'King', 
  'preferredView': 'Sea', 
  'vipFlag': True 
 }) 

 guests.put_item(Item={ 
  'guestName': 'Carlos Mendes', 
  'dob': '1979-04-03', 
  'loyaltyTier': 'Gold', 
  'phoneNumber': '+1-555-888-3434', 
  'email': 'carlos.mendes@example.com', 
  'preferredLanguage': 'pt-BR', 
  'preferredBedType': 'Queen', 
  'preferredView': 'City', 
  'vipFlag': False 
 }) 

 guests.put_item(Item={ 
  'guestName': 'Emily Chen', 
  'dob': '1990-09-28', 
  'loyaltyTier': 'Standard', 
  'phoneNumber': '+1-555-999-5656', 
  'email': 'emily.chen@example.com', 
  'preferredLanguage': 'en-US', 
  'preferredBedType': 'Twin', 
  'preferredView': 'Garden', 
  'vipFlag': False 
 }) 

 guests.put_item(Item={ 
  'guestName': 'David Brown', 
  'dob': '1988-02-14', 
  'loyaltyTier': 'Silver', 
  'phoneNumber': '+1-555-222-7878', 
  'email': 'david.brown@example.com', 
  'preferredLanguage': 'en-US', 
  'preferredBedType': 'King', 
  'preferredView': 'City', 
  'vipFlag': False 
 }) 

 guests.put_item(Item={ 
  'guestName': 'Sophia Rossi', 
  'dob': '1995-07-19', 
  'loyaltyTier': 'Gold', 
  'phoneNumber': '+1-555-444-9090', 
  'email': 'sophia.rossi@example.com', 
  'preferredLanguage': 'it-IT', 
  'preferredBedType': 'Queen', 
  'preferredView': 'Sea', 
  'vipFlag': True 
 }) 

 print("Guests seeded: Anna Smith (Gold), Mark Johnson (Standard)") 

 # --- 4. Seed Reservation Data --- 
 print("\n--- Seeding Hotel Reservations ---") 
 reservations = dynamodb.Table('Hotel_Reservations') 
 today = datetime.date.today() 
 tomorrow = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d') 
 day_after = (today + datetime.timedelta(days=2)).strftime('%Y-%m-%d') 
 next_week = (today + datetime.timedelta(days=7)).strftime('%Y-%m-%d') 
 next_week_plus_two = (today + datetime.timedelta(days=9)).strftime('%Y-%m-%d') 

 # Reservation 1: Anna - upcoming confirmed reservation, fully paid 
 reservations.put_item(Item={ 
  'reservationId': 'RES-1001', 
  'guestName': 'Anna Smith', 
  'roomNumber': '1205', 
  'roomType': 'King Deluxe', 
  'checkInDate': tomorrow, 
  'checkOutDate': day_after, 
  'status': 'Confirmed', # other possibilities: CheckedIn, CheckedOut, Cancelled, NoShow 
  'paymentStatus': 'Paid', # Paid  DepositPaid  Unpaid  Partial 
  'balanceDue': Decimal('0.00'), 
  'bookingChannel': 'Hotel Website', 
  'specialRequests': ['High floor', 'Late check-out'], 
  'eligibleForLateCheckout': True, 
  'allowVoiceAgentChanges': True 
 }) 

 # Reservation 2: Mark - confirmed, with outstanding balance and airport pickup 
 reservations.put_item(Item={ 
  'reservationId': 'RES-2001', 
  'guestName': 'Mark Johnson', 
  'roomNumber': '0803', 
  'roomType': 'Queen Standard', 
  'checkInDate': next_week, 
  'checkOutDate': next_week_plus_two, 
  'status': 'Confirmed', 
  'paymentStatus': 'DepositPaid', 
  'balanceDue': Decimal('240.50'), 
  'bookingChannel': 'Booking.com', 
  'specialRequests': ['Airport pickup', 'Feather-free pillows'], 
  'eligibleForLateCheckout': False, 
  'allowVoiceAgentChanges': True 
 }) 

 # Reservation 3: Mark - past stay, already checked out (for “previous stays” queries) 
 reservations.put_item(Item={ 
  'reservationId': 'RES-1999', 
  'guestName': 'Mark Johnson', 
  'roomNumber': '0502', 
  'roomType': 'Queen Standard', 
  'checkInDate': (today - datetime.timedelta(days=10)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), 
  'status': 'CheckedOut', 
  'paymentStatus': 'Paid', 
  'balanceDue': Decimal('0.00'), 
  'bookingChannel': 'Hotel Website', 
  'specialRequests': ['Early check-in'], 
  'eligibleForLateCheckout': False, 
  'allowVoiceAgentChanges': False # historical, don’t modify 
 }) 

 # --- Added Reservations (extra demo data) --- 
 reservations.put_item(Item={ 
  'reservationId': 'RES-3001', 
  'guestName': 'Priya Nair', 
  'roomNumber': '1508', 
  'roomType': 'King Executive', 
  'checkInDate': (today + datetime.timedelta(days=3)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today + datetime.timedelta(days=6)).strftime('%Y-%m-%d'), 
  'status': 'Confirmed', 
  'paymentStatus': 'Paid', 
  'balanceDue': Decimal('0.00'), 
  'bookingChannel': 'Hotel Website', 
  'specialRequests': ['Quiet room', 'Extra towels'], 
  'eligibleForLateCheckout': True, 
  'allowVoiceAgentChanges': True 
 }) 

 reservations.put_item(Item={ 
  'reservationId': 'RES-3002', 
  'guestName': 'Priya Nair', 
  'roomNumber': '1508', 
  'roomType': 'King Executive', 
  'checkInDate': (today - datetime.timedelta(days=35)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today - datetime.timedelta(days=32)).strftime('%Y-%m-%d'), 
  'status': 'CheckedOut', 
  'paymentStatus': 'Paid', 
  'balanceDue': Decimal('0.00'), 
  'bookingChannel': 'Amex Travel', 
  'specialRequests': ['Late arrival'], 
  'eligibleForLateCheckout': True, 
  'allowVoiceAgentChanges': False 
 }) 

 reservations.put_item(Item={ 
  'reservationId': 'RES-4001', 
  'guestName': 'Carlos Mendes', 
  'roomNumber': '0911', 
  'roomType': 'Queen Standard', 
  'checkInDate': (today + datetime.timedelta(days=5)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today + datetime.timedelta(days=8)).strftime('%Y-%m-%d'), 
  'status': 'Confirmed', 
  'paymentStatus': 'Partial', 
  'balanceDue': Decimal('110.00'), 
  'bookingChannel': 'Expedia', 
  'specialRequests': ['Feather-free pillows'], 
  'eligibleForLateCheckout': False, 
  'allowVoiceAgentChanges': True 
 }) 

 reservations.put_item(Item={ 
  'reservationId': 'RES-5001', 
  'guestName': 'Emily Chen', 
  'roomNumber': '0706', 
  'roomType': 'Twin Standard', 
  'checkInDate': (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today + datetime.timedelta(days=4)).strftime('%Y-%m-%d'), 
  'status': 'Cancelled', 
  'paymentStatus': 'Unpaid', 
  'balanceDue': Decimal('0.00'), 
  'bookingChannel': 'Hotel Website', 
  'specialRequests': ['Near elevator'], 
  'eligibleForLateCheckout': False, 
  'allowVoiceAgentChanges': True 
 }) 

 reservations.put_item(Item={ 
  'reservationId': 'RES-6001', 
  'guestName': 'David Brown', 
  'roomNumber': '0304', 
  'roomType': 'King Standard', 
  'checkInDate': (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today + datetime.timedelta(days=2)).strftime('%Y-%m-%d'), 
  'status': 'CheckedIn', 
  'paymentStatus': 'DepositPaid', 
  'balanceDue': Decimal('180.75'), 
  'bookingChannel': 'Corporate', 
  'specialRequests': ['Late check-out'], 
  'eligibleForLateCheckout': True, 
  'allowVoiceAgentChanges': True 
 }) 

 reservations.put_item(Item={ 
  'reservationId': 'RES-7001', 
  'guestName': 'Sophia Rossi', 
  'roomNumber': '1402', 
  'roomType': 'Queen Deluxe', 
  'checkInDate': (today - datetime.timedelta(days=12)).strftime('%Y-%m-%d'), 
  'checkOutDate': (today - datetime.timedelta(days=9)).strftime('%Y-%m-%d'), 
  'status': 'NoShow', 
  'paymentStatus': 'Unpaid', 
  'balanceDue': Decimal('75.00'), 
  'bookingChannel': 'Booking.com', 
  'specialRequests': ['High floor'], 
  'eligibleForLateCheckout': False, 
  'allowVoiceAgentChanges': False 
 }) 

 print("Reservations seeded:") 
 print(" - RES-1001 (Anna, upcoming, fully paid)") 
 print(" - RES-2001 (Mark, upcoming, balance due)") 
 print(" - RES-1999 (Mark, past stay, checked out)") 
 print("\n--- Setup Complete ---") 

if __name__ == '__main__': 
 setup_demo_data()