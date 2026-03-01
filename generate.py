#!/usr/bin/env python3
"""Generate ForeFlight content pack and Garmin GTN waypoints from KML."""

import os
import re
import shutil
import xml.etree.ElementTree as ET

KML_FILE = "KFCM VFR Reporting Points.kml"
NS = {"kml": "http://www.opengis.net/kml/2.2"}

CONTENT_PACK_LAYERS = "foreflight-content-pack/layers"
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


def foreflight_description(wp):
    desc = f"{wp['name']} - {wp['fix_type']} Fix {wp['direction']}"
    if wp["altitude"]:
        desc += f" {wp['altitude']}"
    return desc


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


def main():
    waypoints = parse_kml(KML_FILE)

    # Create output directories
    os.makedirs(CONTENT_PACK_LAYERS, exist_ok=True)
    os.makedirs(CONTENT_PACK_NAVDATA, exist_ok=True)
    os.makedirs(GTN_DIR, exist_ok=True)

    # Copy KML to content pack layers
    shutil.copy2(KML_FILE, os.path.join(CONTENT_PACK_LAYERS, "FCM Fix Map.kml"))

    # Write ForeFlight waypoints CSV
    with open(os.path.join(CONTENT_PACK_NAVDATA, "FCM Fix Wpts.csv"), "w") as f:
        for wp in waypoints:
            desc = foreflight_description(wp)
            f.write(f"{wp['code']},{desc},{wp['lat']},{wp['lon']}\n")

    # Write Garmin GTN user.wpt
    with open(os.path.join(GTN_DIR, "user.wpt"), "w") as f:
        for wp in waypoints:
            comment = gtn_comment(wp)
            f.write(f"{wp['code']},{comment},{wp['lat']},{wp['lon']}\n")

    print(f"Generated {len(waypoints)} waypoints")
    print(f"  {CONTENT_PACK_NAVDATA}/FCM Fix Wpts.csv")
    print(f"  {GTN_DIR}/user.wpt")
    print(f"  {CONTENT_PACK_LAYERS}/FCM Fix Map.kml")


if __name__ == "__main__":
    main()
