import csv
from icalendar import Calendar


def ics_to_csv(input_ics_file, output_csv_file):
    # Open the .ics file
    with open(input_ics_file, 'r') as file:
        gcal = Calendar.from_ical(file.read())

    # Write to the CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Summary', 'Start Date', 'End Date', 'Location', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for component in gcal.walk():
            if component.name == "VEVENT": # Check if the component is an event
                summary = component.get('summary')
                start = component.get('dtstart').dt
                end = component.get('dtend').dt
                location = component.get('location')
                description = component.get('description')

                writer.writerow({
                    'Summary': summary,
                    'Start Date': start,
                    'End Date': end,
                    'Location': location,
                    'Description': description
                })


# Example usage
ics_file = 'input.ics'  # Path to the .ics file to be converted
csv_file = 'output.csv'  # Path to the output .csv file

ics_to_csv(ics_file, csv_file)
