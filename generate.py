#!/usr/bin/env python3
"""Generate ForeFlight content pack and Garmin GTN waypoints from KML."""

import os
import re
import xml.etree.ElementTree as ET

KML_FILE = "KFCM VFR Reporting Points.kml"
NS = {"kml": "http://www.opengis.net/kml/2.2"}

CONTENT_PACK_NAVDATA = "foreflight-content-pack/navdata"
GTN_DIR = "garmin-gtn"


def parse_kml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    waypoints = []

    for folder in root.findall(".//kml:Folder", NS):
        folder_name = folder.find("kml:name", NS).text
        if "Feeder" in folder_name:
            fix_type = "Feeder"
        elif "Inside" in folder_name:
            fix_type = "Inside"
        else:
            continue

        for pm in folder.findall("kml:Placemark", NS):
            point = pm.find("kml:Point", NS)
            if point is None:
                continue
            coords_text = point.find("kml:coordinates", NS).text.strip()
            lon, lat, _alt = coords_text.split(",")

            name = pm.find("kml:name", NS).text
            desc = pm.find("kml:description", NS).text or ""

            # Direction: text before first " - "
            direction = desc.split(" - ")[0].strip() if " - " in desc else ""

            # Altitude: e.g. 2500' MSL
            alt_match = re.search(r"(\d+)' MSL", desc)
            altitude = alt_match.group(1) if alt_match else ""

            # 6-char GTN code: uppercase, strip non-alphanumeric, first 6
            code = re.sub(r"[^A-Z0-9]", "", name.upper())[:6]

            waypoints.append({
                "name": name,
                "code": code,
                "fix_type": fix_type,
                "direction": direction,
                "altitude": altitude,
                "lat": lat.strip(),
                "lon": lon.strip(),
            })

    return waypoints


def gtn_comment(wp):
    name_upper = wp["name"].upper()
    fix_word = wp["fix_type"].upper()
    parts = [name_upper, fix_word, wp["direction"]]
    if wp["altitude"]:
        parts.append(wp["altitude"])
    comment = " ".join(parts)
    if len(comment) > 25:
        abbrev = {"FEEDER": "FDR", "INSIDE": "INSD"}
        parts[1] = abbrev.get(fix_word, fix_word)
        comment = " ".join(parts)
    return comment[:25]


def write_foreflight_kml(src_path, dest_path, waypoints):
    """Write a copy of the KML with placemark names replaced by 6-char codes."""
    tree = ET.parse(src_path)
    root = tree.getroot()

    # Build lookup: (lat, lon) -> code for Point placemarks
    code_by_coords = {}
    for wp in waypoints:
        key = (wp["lat"], wp["lon"])
        code_by_coords[key] = wp["code"]

    for pm in root.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        point = pm.find("{http://www.opengis.net/kml/2.2}Point")
        if point is None:
            continue
        coords_text = point.find("{http://www.opengis.net/kml/2.2}coordinates").text.strip()
        lon, lat, _alt = coords_text.split(",")
        key = (lat.strip(), lon.strip())
        if key in code_by_coords:
            name_el = pm.find("{http://www.opengis.net/kml/2.2}name")
            name_el.text = code_by_coords[key]

    ET.register_namespace("", "http://www.opengis.net/kml/2.2")
    tree.write(dest_path, xml_declaration=True, encoding="UTF-8")


def main():
    waypoints = parse_kml(KML_FILE)

    # Create output directories
    os.makedirs(CONTENT_PACK_NAVDATA, exist_ok=True)
    os.makedirs(GTN_DIR, exist_ok=True)

    # Write transformed KML to content pack navdata
    kml_dest = os.path.join(CONTENT_PACK_NAVDATA, "KFCM VFR Waypoints.kml")
    write_foreflight_kml(KML_FILE, kml_dest, waypoints)

    # Write Garmin GTN user.wpt
    with open(os.path.join(GTN_DIR, "user.wpt"), "w") as f:
        for wp in waypoints:
            comment = gtn_comment(wp)
            f.write(f"{wp['code']},{comment},{wp['lat']},{wp['lon']}\n")

    print(f"Generated {len(waypoints)} waypoints")
    print(f"  {kml_dest}")
    print(f"  {GTN_DIR}/user.wpt")


if __name__ == "__main__":
    main()
