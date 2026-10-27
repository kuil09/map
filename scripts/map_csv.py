"""Reproduce reviewed address-based My Maps CSV artifacts, including v35/v36.

Pure formatting only: no network, map actions, or embedded local paths.
Call format_places(places, ordered_ids), then csv_bytes(rows).
The formatter is reviewed for the current six pending categories.
Unsupported categories fail closed; review mappings before expanding.
"""
import re

FIELDS = ['Name', 'Address', 'Category', 'Description', 'Sources', 'Checked',
          'Location limitations', 'Record ID', 'Access and booking', 'Additional details']
LANGUAGES = ('en', 'ko', 'ja', 'zh', 'es')
CATEGORIES = {'camping': 'Camping / 캠핑', 'shopping': 'Shopping / 쇼핑',
              'landmarks': 'Landmarks & culture / 랜드마크·문화', 'food': 'Food & cafés / 음식·카페',
              'activities': 'Activities / 체험', 'hobbies': 'Games & hobbies / 게임·취미'}
SETTINGS = {'indoor': 'Indoor', 'outdoor': 'Outdoor', 'mixed': 'Indoor and outdoor'}
KINDS = {'department': 'Department store', 'mall': 'Shopping mall', 'outlet': 'Outlet mall',
         'traditional-market': 'Traditional market', 'catholic-pilgrimage': 'Catholic pilgrimage site',
         'temple': 'Buddhist temple', 'craft-history-museum': 'Craft and history museum',
         'history-museum': 'History museum', 'spa-jjimjilbang': 'Spa and jjimjilbang',
         'hot-spring-bathhouse': 'Hot-spring bathhouse', 'board-game-cafe': 'Board-game café'}


def js_string(value):
    """String conversion used by the original approved JavaScript formatter."""
    if isinstance(value, list):
        return ','.join('' if v is None else js_string(v) for v in value)
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def add(lines, label, value):
    if value is not None and value != '':
        lines.append(label + ': ' + js_string(value))


def public_wording(value):
    value = value.replace('No independently evidenced destination coordinates were adopted.',
                          'Destination coordinates are not independently verified.')
    value = re.sub(r' No (?:coordinates invented|coordinates inferred|point invented|map-center point used)\.', '', value)
    replacements = [
        ('Types require explicit facility or admission evidence. ', ''),
        ('One venue, not separate records for its general and auto sections.', 'The campground has general and auto-camping sections.'),
        ('B means bring-your-own trailer site, not rental accommodation or a universal campervan permission.', 'Own-trailer sites are not rental accommodation; campervan eligibility must be confirmed.'),
        ('No own-trailer/campervan admission inferred from the auto-camping label.', 'The auto-camping label does not establish own-trailer or campervan admission.'),
        ('(municipal announced season; registry blank)', '(municipally announced season)'),
        (' Registry major-facilities field blank.', ''),
        ('KTO partner page: 사전예약필수, 온라인예약; registry structured field blank while narrative says online.', 'Advance online reservation is required; confirm the current booking route.'),
        ('Registry: -; registered homepage absent. Current booking route unverified.', 'No current booking route or homepage confirmed. Contact the campground before travel.'),
        ('봄, 여름, 가을, 겨울; narrative says 봄, 여름, 가을 — conflict retained, not an all-year promise', 'Published seasons conflict: one listing includes winter, another lists spring, summer and autumn only. Confirm winter operation.'),
        ('Auto-camping pitches and explicit personal-trailer admission; no rental caravan, motorhome or supplied tent claim.', 'Auto-camping pitches and own-trailer admission are listed. Rental caravans, motorhome eligibility and supplied tents are unverified.'),
        ('Official named venue address copied;', 'Official named venue address;'),
        ('Source location evidence:', 'Location information:'),
        ('Overnight camping; not a day-use-only listing.', 'Overnight camping.'),
        ('Vehicle admission (source wording):', 'Published vehicle rules:'),
        ('Pets (source wording):', 'Published pet rules:'),
        ('Camping facilities (source wording):', 'Published camping facilities:'),
    ]
    for before, after in replacements:
        value = value.replace(before, after)
    return value


def format_place(p):
    assert p['address'] and p['name_en'] and p['name_ko'] and p['category'] in CATEGORIES
    for lang in LANGUAGES:
        assert isinstance(p['description'][lang], str) and isinstance(p['notes'][lang], str)
    urls = list(dict.fromkeys(u for u in [*[s['url'] for s in p['sources']],
                     p.get('operator_url'), p.get('booking_url'), p.get('coordinate_source_url')] if u))
    assert all(re.match(r'^https?://', u) for u in urls)
    access = []
    if p.get('alert'):
        add(access, 'Visit planning', 'Read the restrictions and uncertainty notes in the description before travel.')
    if p.get('booking_verification'):
        add(access, 'Reservations', 'Public information does not confirm a reservation. Account access, date-specific availability, ID verification, payment and English service have not been tested.')
    if p.get('booking_url'):
        add(access, 'Booking', p['booking_url'])
    if p.get('foreign_visitor_booking_eligibility'):
        add(access, 'Foreign-visitor booking eligibility', 'Unverified; confirm accepted ID and any Korean identity or phone requirements.')
    if p.get('live_availability'):
        add(access, 'Current availability', 'Unknown; confirm with the operator.')
    if p.get('english_support'):
        add(access, 'English assistance', 'Unverified.')
    if p.get('card_acceptance'):
        add(access, 'Card acceptance', 'Unverified.')
    if p.get('foreign_card_payment'):
        add(access, 'Overseas-card payment', 'Unverified.')
    camp = p.get('camp_type_evidence') or {}
    if camp.get('vehicle_admission_ko'):
        add(access, 'Vehicle admission (source wording)', camp['vehicle_admission_ko'])
    if camp.get('pets_ko'):
        add(access, 'Pets (source wording)', camp['pets_ko'])
    if camp.get('booking_method_ko'):
        add(access, 'Published booking method', camp['booking_method_ko'])
    status_text = {
        'temporarily_unreadable': 'The operator website could not be read; confirm current rules directly before travel.',
        'partially_readable': 'Only part of the operator information could be read; confirm current rules directly before travel.',
        'readable_with_conflicting_operational_text': 'Published operational details conflict; confirm current arrangements directly before travel.',
    }
    if p.get('operator_source_status') in status_text:
        add(access, 'Operator information', status_text[p['operator_source_status']])
    details = []
    add(details, 'Area', p.get('area'))
    add(details, 'Setting', SETTINGS.get(p.get('setting'), p.get('setting')))
    add(details, 'Venue type', KINDS.get(p.get('kind')))
    if p.get('activity_type') == 'swimming':
        add(details, 'Activity', 'Swimming')
    if p.get('cuisine'):
        add(details, 'Cuisine', p['cuisine'])
    if p.get('market_format'):
        add(details, 'Market format', p['market_format'])
    if p.get('camp_labels'):
        for lang in LANGUAGES:
            add(details, 'Camping options ' + lang.upper(), p['camp_labels'].get(lang))
    if p.get('overnight') is True:
        add(details, 'Stay', 'Overnight camping; not a day-use-only listing.')
    add(details, 'Telephone', p.get('phone'))
    add(details, 'Registered campground type', p.get('registry_type'))
    add(details, 'Published operating season', p.get('source_operation_season'))
    if p.get('source_updated'):
        add(details, 'Registry information updated', p['source_updated'])
    if camp.get('major_facilities_ko'):
        add(details, 'Camping facilities (source wording)', camp['major_facilities_ko'])
    if camp.get('note'):
        add(details, 'Camping limits', camp['note'])
    if p['id'] == 'gocamping-2226':
        add(details, 'Campground classification', 'Official registry versions differ between general and automobile camping. Both list camping pitches and personal-trailer admission; this does not establish motorhome eligibility.')
    add(details, 'Name note', p.get('name_translation_note'))
    add(details, 'Multilingual guide', 'https://humphreys-field-guide.kuil09.chatgpt.site')
    location = ['Source location evidence: ' + p['coordinate_status']]
    if p.get('coordinates'):
        coords = p['coordinates']
        add(location, 'Published general venue point', js_string(coords['lat']) + ', ' + js_string(coords['lng']) + ' (reference point only; an address-based map marker may differ).')
        if p.get('distance_label'):
            for lang in LANGUAGES:
                add(location, 'Source-point distance ' + lang.upper(), p['distance_label'].get(lang))
        add(location, 'Distance limitation', 'Straight-line distance refers to the published general venue point, not a verified entrance, driving route or Google-geocoded marker.')
    add(location, 'Address-based marker', 'The full source address is used for Google geocoding. Any placed marker is a Google address result, not an independently verified entrance, gate, parking area or accessible route.')
    add(location, 'Distance', p.get('radius_status') or p.get('radius_verification'))
    return {
        'Name': p['name_en'] + ' | ' + p['name_ko'],
        'Address': p['address'], 'Category': CATEGORIES[p['category']],
        'Description': '\n\n'.join(lang.upper() + ': ' + p['description'][lang] + '\n' + p['notes'][lang] for lang in LANGUAGES),
        'Sources': '\n'.join(urls), 'Checked': p['checked'],
        'Location limitations': public_wording('\n'.join(location)),
        'Record ID': p['id'], 'Access and booking': public_wording('\n'.join(access)),
        'Additional details': public_wording('\n'.join(details)),
    }


def format_places(places, ordered_ids):
    """Select exact unique IDs in caller order; reject absent/duplicate IDs."""
    by_id = {p['id']: p for p in places}
    if len(by_id) != len(places):
        raise ValueError('Duplicate IDs in places')
    if len(set(ordered_ids)) != len(ordered_ids):
        raise ValueError('Duplicate IDs in requested order')
    return [format_place(by_id[ident]) for ident in ordered_ids]


def csv_bytes(rows, *, include_bom=False):
    """UTF-8 without BOM, quoted fields, doubled quotes and CRLF records.

    Use include_bom=True only to reproduce historical BOM-bearing artifacts.
    Cell contents, including any embedded U+FEFF characters, are preserved.
    """
    matrix = [FIELDS, *[[row[field] for field in FIELDS] for row in rows]]
    return (('\ufeff' if include_bom else '') + '\r\n'.join(
        ','.join('"' + str(value).replace('"', '""') + '"' for value in row)
        for row in matrix) + '\r\n').encode('utf-8')

