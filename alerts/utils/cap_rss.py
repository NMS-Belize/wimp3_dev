import feedparser, requests
import xml.etree.ElementTree as ET
from datetime import datetime

from alerts.models import CAPAlerts, CAPAlertDetails

def fetch_cap_alerts():
    
    # RSS feed URL
    rss_url = "https://cap-sources.s3.amazonaws.com/bz-nms-en/rss.xml"
    
    feed = feedparser.parse(rss_url)
    
    if feed.bozo:
        raise Exception(f"Failed to parse RSS feed: {feed.bozo_exception}")

    for entry in feed.entries:
        # ---- Store RSS summary ----
        alert, created = CAPAlerts.objects.get_or_create(
            guid = entry.get("guid"),
            defaults={
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "description": entry.get("summary", ""),
                "author": entry.get("author", ""),
                "category": entry.tags[0]["term"] if entry.get("tags") else "",
                "pubdate": entry.get("published", ""),
                "is_published": False,
            },
        )
        pass

        if not created:
            continue  # already processed

        # ---- Fetch full CAP XML ----
        try:
            cap_xml = requests.get(entry.link, timeout=10).text
            parse_cap_xml(cap_xml)
        except Exception as e:
            print(f"CAP fetch failed: {e}")

def parse_cap_xml(xml_data):
    
    root = ET.fromstring(xml_data)

    ns = {"cap": "urn:oasis:names:tc:emergency:cap:1.2"}

    identifier = root.findtext("cap:identifier", default="", namespaces=ns)

    CAPAlertDetails.objects.update_or_create(
        identifier=identifier,
        defaults={
            "sender": root.findtext("cap:sender", "", ns),
            "sent": root.findtext("cap:sent", "", ns),
            "status": root.findtext("cap:status", "", ns),
            "message_type": root.findtext("cap:msgType", "", ns),
            "scope": root.findtext("cap:scope", "", ns),
            "language": root.findtext("cap:language", "", ns),

            # info block
            "category": root.findtext(".//cap:category", "", ns),
            "event": root.findtext(".//cap:event", "", ns),
            "response_type": root.findtext(".//cap:responseType", "", ns),
            "severity": root.findtext(".//cap:severity", "", ns),
            "certainty": root.findtext(".//cap:certainty", "", ns),

            "event_code": root.findtext(".//cap:eventCode/cap:value", "", ns),
            "value_name": root.findtext(".//cap:eventCode/cap:valueName", "", ns),

            "onset": root.findtext(".//cap:onset", "", ns),
            "expires": root.findtext(".//cap:expires", "", ns),

            "sender_name": root.findtext(".//cap:senderName", "", ns),
            "headline": root.findtext(".//cap:headline", "", ns),
            "description": root.findtext(".//cap:description", "", ns),
            "instruction": root.findtext(".//cap:instruction", "", ns),

            "area": root.findtext(".//cap:areaDesc", "", ns),
            "area_description": root.findtext(".//cap:areaDesc", "", ns),
            "polygon": root.findtext(".//cap:polygon", "", ns),
        },
    )