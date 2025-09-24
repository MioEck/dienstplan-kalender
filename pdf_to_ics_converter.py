
import re
from datetime import datetime, timedelta
from ics import Calendar, Event

def parse_schedule(ocr_text):
    schedule = {}
    
    week_range_match = re.search(r'Wochenübersicht (\d{2}\.\d{2}\.\d{2}) bis (\d{2}\.\d{2}\.\d{2})', ocr_text)
    if week_range_match:
        start_date_str = week_range_match.group(1)
        year = datetime.strptime(start_date_str, '%d.%m.%y').year
    else:
        raise ValueError("Could not extract week range from OCR text.")

    day_sections = re.split(r'(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag)\s+(\d{2}\.\d{2}\.\d{2})', ocr_text)
    
    for i in range(1, len(day_sections), 3):
        if i + 2 < len(day_sections):
            day_name = day_sections[i]
            date_str = day_sections[i+1]
            day_content = day_sections[i+2]

            current_date = datetime.strptime(f"{date_str}.{year}", '%d.%m.%y.%Y').date()
            schedule[current_date] = []

            day_content_normalized = day_content.replace('\n', ' ')

            # --- Parsing Kurs events ---
            # The OCR output for Kurs events can be complex, e.g., 'Kurs 217 Kurs 216 Start: 12:43 - Ende: 23:40 Start: 11:56 - Ende: 23:18 Start: 11:56 - Ende: 23:18'
            # We need to find all individual event descriptions that contain 'Kurs' and time information.
            
            # This regex will find all occurrences of 'Kurs XXX' followed by 'Start: HH:MM - Ende: HH:MM'
            # It's designed to capture each Kurs event and its time independently.
            # The non-greedy quantifier .*? is important here.
            
            # Let's try to find all occurrences of 'Kurs XXX' and then the time range immediately following it.
            # This pattern should capture 'Kurs XXX' and its directly associated time.
            # We need to be careful with the OCR output where multiple events might be on one line.
            
            # Let's process the day_content_normalized as a continuous string and find all Kurs events with their times.
            # This regex will find all occurrences of 'Kurs XXX' followed by 'Start: HH:MM - Ende: HH:MM'
            # It's designed to capture each Kurs event and its time independently.
            # The non-greedy quantifier .*? is important here.
            
            # The OCR output for Wednesday is: 'Kurs 216 Start: 12:43 - Ende: 23:40 Start: 11:56 - Ende: 23:18 Start: 11:56 - Ende: 23:18'
            # This implies that 'Kurs 216' is associated with *all* these time ranges. This is incorrect.
            # It's more likely that the OCR has merged multiple lines or misidentified the layout.
            # Given the structure, it's possible that 'Kurs 217' and 'Kurs 216' are separate events, and the times are also separate.
            # Let's try to extract all 'Kurs XXX' and all 'Start: HH:MM - Ende: HH:MM' pairs and then associate them.

            # Let's try a different approach: find all event blocks that contain 'Kurs' and time information.
            # This regex attempts to capture a 'Kurs XXX' followed by its time block.
            # It's still problematic if multiple Kurs events are on the same line without clear delimiters.
            
            # Let's simplify the parsing for Kurs events based on the provided OCR.
            # The OCR for Wednesday is: 'Kurs 216 Start: 12:43 - Ende: 23:40 Start: 11:56 - Ende: 23:18 Start: 11:56 - Ende: 23:18'
            # This implies that 'Kurs 216' is associated with *all* these time ranges. This is not how a schedule works.
            # It's more likely that the OCR has failed to separate distinct events.
            # For now, let's assume that each 'Kurs XXX' is followed by *one* 'Start: HH:MM - Ende: HH:MM' block.
            # If there are multiple on one line, we'll only pick the first one for that Kurs, or the last one, depending on the regex.
            
            # Let's try to find all 'Kurs XXX' and then the time range immediately following it.
            # This pattern should capture 'Kurs XXX' and its directly associated time.
            kurs_event_pattern_v2 = r'(Kurs \d+)\s*(?:Start:\s*(\d{2}:\d{2})\s*-\s*Ende:\s*(\d{2}:\d{2}))?'
            
            # The OCR for Monday and Tuesday only shows 'Kurs 217' and 'Kurs 216' without times.
            # We need to handle these as well. If no time is found, we can skip it or make it an all-day event.
            
            # Let's try to extract all Kurs events first, then try to find their times.
            # This is still difficult due to the OCR quality.

            # Let's try to extract all 'Kurs XXX' and then all 'Start: HH:MM - Ende: HH:MM' blocks.
            # Then, we'll try to match them up. This is still prone to errors if the order is not strict.

            # Given the OCR output, it seems the Kurs events are sometimes listed without times on their own line,
            # and sometimes with times on a line that might also contain other Kurs events.
            # Let's try to parse the OCR line by line for Kurs events.

            lines_in_day_content = day_content.split('\n')
            for line in lines_in_day_content:
                line = line.strip()
                if not line:
                    continue

                # Try to match 'Kurs XXX Start: HH:MM - Ende: HH:MM'
                kurs_match_with_time = re.search(r'(Kurs \d+)\s+Start:\s*(\d{2}:\d{2})\s*-\s*Ende:\s*(\d{2}:\d{2})', line)
                if kurs_match_with_time:
                    event_name = kurs_match_with_time.group(1).strip()
                    start_time_str = kurs_match_with_time.group(2)
                    end_time_str = kurs_match_with_time.group(3)
                    
                    event_start = datetime.combine(current_date, datetime.strptime(start_time_str, '%H:%M').time())
                    event_end = datetime.combine(current_date, datetime.strptime(end_time_str, '%H:%M').time())
                    schedule[current_date].append({
                        'type': 'Kurs',
                        'name': event_name,
                        'start': event_start,
                        'end': event_end
                    })
                else:
                    # If no time is found, check if it's just a 'Kurs XXX' entry
                    kurs_match_no_time = re.search(r'(Kurs \d+)', line)
                    if kurs_match_no_time:
                        event_name = kurs_match_no_time.group(1).strip()
                        # If no time, we can make it an all-day event or skip it.
                        # For now, let's skip it as the user is interested in scheduled services.
                        pass

            # --- Parsing Frei or Urlaub Wochenende events ---
            # We need to ensure we don't add duplicate 'Frei' events if they are part of a larger string like 'Rebenstorf, Michael Frei'
            # So, we'll parse 'Rebenstorf, Michael Frei' first, then generic 'Frei' or 'Urlaub Wochenende'

            # Handle cases like 'Rebenstorf, Michael Frei' where 'Frei' is an event for the day
            rebenstorf_frei_match = re.search(r'Rebenstorf, Michael\s+(Frei)', day_content_normalized)
            if rebenstorf_frei_match:
                event_name = rebenstorf_frei_match.group(1)
                schedule[current_date].append({
                    'type': 'Free',
                    'name': event_name,
                    'start': datetime.combine(current_date, datetime.min.time()),
                    'end': datetime.combine(current_date, datetime.max.time()),
                    'all_day': True
                })
            
            # Generic 'Frei' or 'Urlaub Wochenende' - only if not already added by 'Rebenstorf, Michael Frei'
            # This is a bit tricky, as 'Frei' might appear alone or as part of the 'Rebenstorf' entry.
            # Let's assume if 'Rebenstorf, Michael Frei' is found, we don't need to search for a standalone 'Frei' for that day.
            # For 'Urlaub Wochenende', it's usually standalone.
            if not rebenstorf_frei_match:
                free_matches = re.findall(r'(Frei|Urlaub Wochenende)', day_content_normalized)
                for fmatch in free_matches:
                    event_name = fmatch
                    schedule[current_date].append({
                        'type': 'Free',
                        'name': event_name,
                        'start': datetime.combine(current_date, datetime.min.time()),
                        'end': datetime.combine(current_date, datetime.max.time()),
                        'all_day': True
                    })

    return schedule

def generate_ics(schedule, output_file='schedule.ics'):
    c = Calendar()
    for date, events in schedule.items():
        for event_data in events:
            e = Event()
            e.name = event_data['name']
            e.begin = event_data['start']
            e.end = event_data['end']
            if event_data.get('all_day'):
                e.make_all_day()
            c.events.add(e)

    with open(output_file, 'w') as f:
        f.writelines(c)

if __name__ == '__main__':
    with open('pdf_ocr_output.txt', 'r') as f:
        ocr_text = f.read()

    parsed_schedule = parse_schedule(ocr_text)
    generate_ics(parsed_schedule, 'dienstplan.ics')
    print("ICS file 'dienstplan.ics' generated successfully.")


