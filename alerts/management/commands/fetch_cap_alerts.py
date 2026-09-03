import feedparser
import requests
import xml.etree.ElementTree as ET

from datetime import datetime
from django.utils import timezone
from email.utils import parsedate_to_datetime

from django.core.management.base import BaseCommand
from alerts.models import CAPAlerts, CAPAlertDetails

def fetch_cap_alerts():

    rss_url = "https://cap-sources.s3.amazonaws.com/bz-nms-en/rss.xml"

    feed = feedparser.parse(rss_url)

    if feed.bozo:
        raise Exception(f"Failed to parse RSS feed: {feed.bozo_exception}")

    created_count = 0
    updated_count = 0
    details_count = 0

    for entry in feed.entries:

        guid = entry.get("guid") or entry.get("id") or entry.get("link")

        if not guid:
            #print("Skipping RSS entry with no GUID or link")
            continue

        # Check whether alert already exists
        existing_alert = CAPAlerts.objects.filter(guid=guid).first()

        published_raw = entry.get("published", "")

        pubdate = None

        if published_raw:
            try:
                pubdate = parsedate_to_datetime(published_raw)
            except (TypeError, ValueError):
                print(f"Could not parse pubdate: {published_raw}")

        defaults = {
            "title":        entry.get("title", ""),
            "link":         entry.get("link", ""),
            "description":  entry.get("summary", ""),
            "author":       entry.get("author", ""),
            "category":     (entry.tags[0]["term"]
                if entry.get("tags")
                else ""
            ),
            "pubdate": pubdate,
        }

        # Only set is_published=False when creating a NEW alert
        if existing_alert is None:
            defaults["is_published"] = False

        # Create OR update RSS alert
        alert, created = CAPAlerts.objects.update_or_create(guid=guid, defaults=defaults)

        if created:
            created_count += 1
            print(f"Created alert: {alert.title}")
        else:
            updated_count += 1
            print(f"Updated alert: {alert.title}")

        # Fetch full CAP XML every time
        cap_url = entry.get("link")

        if not cap_url:
            print(f"No CAP XML URL found for: {alert.title}")
            continue

        try:
            response = requests.get(cap_url, timeout=15, headers={ "User-Agent": "WIMP3 CAP Alert Sync" } )
            response.raise_for_status()
            parse_cap_xml(response.text)
            details_count += 1

        except requests.RequestException as e:
            print(f"CAP fetch failed for {cap_url}: {e}")

        except ET.ParseError as e:
            print(f"CAP XML parse failed for {cap_url}: {e}")

        except Exception as e:
            print(f"CAP processing failed for {cap_url}: {e}")

    print(f"CAP sync complete: {created_count} created, {updated_count} updated, {details_count} CAP details processed")

def parse_cap_xml(xml_data):

    root = ET.fromstring(xml_data)

    ns = { "cap": "urn:oasis:names:tc:emergency:cap:1.2" }

    identifier = root.findtext("cap:identifier", default="", namespaces=ns)

    if not identifier:
        print("CAP XML skipped because identifier is missing")
        return

    # Make sure the matching CAPAlerts record exists
    try:
        alert = CAPAlerts.objects.get(guid=identifier)
    except CAPAlerts.DoesNotExist:
        print(f"CAP details skipped: no CAPAlerts record found for {identifier}")
        return

    # Parse expiration datetime
    expires_raw = root.findtext(".//cap:expires", "", ns)

    expires = None

    if expires_raw:
        try:
            expires = datetime.fromisoformat(expires_raw)
        except (ValueError, TypeError):
            print(f"Could not parse expiration date for {identifier}: {expires_raw}")

    # Create OR update CAP details
    details, created = CAPAlertDetails.objects.update_or_create(
        identifier = alert,
        defaults = {
            "sender":           root.findtext("cap:sender","",ns),
            "sent":             root.findtext("cap:sent","",ns),
            "status":           root.findtext("cap:status","",ns),
            "message_type":     root.findtext("cap:msgType","",ns),
            "scope":            root.findtext("cap:scope","",ns),

            # info block
            "language":         root.findtext(".//cap:language","",ns),
            "category":         root.findtext(".//cap:category","",ns),
            "event":            root.findtext(".//cap:event","",ns),
            "response_type":    root.findtext(".//cap:responseType","",ns),
            "severity":         root.findtext(".//cap:severity","",ns),
            "urgency":          root.findtext(".//cap:urgency","",ns),
            "certainty":        root.findtext(".//cap:certainty","",ns),
            "event_code_value":   root.findtext(".//cap:eventCode/cap:value","",ns),
            "event_code_value_name": root.findtext(".//cap:eventCode/cap:valueName","",ns),
            "onset":            root.findtext(".//cap:onset","",ns),
            "expires": expires,
            "sender_name":      root.findtext(".//cap:senderName","",ns),
            "headline":         root.findtext(".//cap:headline","",ns),
            "description":      root.findtext(".//cap:description","",ns),
            "instruction":      root.findtext(".//cap:instruction","",ns),
            "area_description": root.findtext(".//cap:areaDesc","",ns),
            "polygon":          root.findtext(".//cap:polygon","",ns)
        },
    )

    if created:
        print(f"Created CAP details: {identifier}")
    else:
        print(f"Updated CAP details: {identifier}")


    # Automatically unpublish expired alerts
    if expires and expires <= timezone.now():

        if alert.is_published:
            alert.is_published = False
            alert.save(update_fields=["is_published"])
            print(f"Expired alert unpublished: {alert.title} ({expires})")

class Command(BaseCommand):

    help = "Fetch and update CAP alerts from Belize NMS RSS feed"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting CAP alert synchronization...")

        try:
            fetch_cap_alerts()
            self.stdout.write(self.style.SUCCESS("CAP alerts synchronized successfully"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"CAP alert synchronization failed: {e}"))