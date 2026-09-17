import csv
from django.utils.timezone import now
from User.models import Contact

def export_contacts_to_csv(user, response):
    writer = csv.writer(response)
    writer.writerow([
        'First Name', 'Last Name', 'Display Name', 'Email', 
        'Phone', 'Company', 'Job Title', 'Address'
    ])
    
    contacts = Contact.objects.filter(user=user)
    for contact in contacts:
        writer.writerow([
            contact.first_name or '',
            contact.last_name or '',
            contact.name or '',
            contact.email or '',
            contact.phone_number or '',
            contact.company or '',
            contact.job_title or '',
            contact.address or ''
        ])
    return response

def import_contacts_from_csv(user, csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    contacts_to_create = []
    for row in reader:
        # Map CSV columns (robust handling for different column names)
        first_name = row.get('First Name', row.get('first_name', ''))
        last_name = row.get('Last Name', row.get('last_name', ''))
        name = row.get('Display Name', row.get('name', f"{first_name} {last_name}".strip()))
        
        email = row.get('Email', row.get('email', ''))
        phone = row.get('Phone', row.get('phone_number', ''))
        company = row.get('Company', row.get('company', ''))
        job_title = row.get('Job Title', row.get('job_title', ''))
        address = row.get('Address', row.get('address', ''))
        
        if not name and not phone:
            continue # Skip empty rows
            
        contacts_to_create.append(Contact(
            user=user,
            name=name or 'Unknown',
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone,
            company=company,
            job_title=job_title,
            address=address
        ))
        
    if contacts_to_create:
        Contact.objects.bulk_create(contacts_to_create)
    
    return len(contacts_to_create)
