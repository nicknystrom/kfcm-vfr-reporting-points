# ForeFlight Content Pack

## Structure

A content pack is a ZIP file containing one or more folders:

```
my-pack/
├── layers/          # KML/GeoJSON map overlays
│   └── reporting_points.kml
├── navdata/         # Custom waypoints
│   └── waypoints.csv
└── manifest.json    # Optional metadata
```

## KML Map Layer

Place `.kml` files in the `layers/` folder. Supported elements:

- **Geometry**: Point, LineString, LinearRing, Polygon, MultiGeometry
- **Styles**: Style, StyleMap, LineStyle, PolyStyle, IconStyle
- Unsupported elements render as hash marks

## Custom Waypoints (navdata)

CSV file with no header row: `NAME,Description,Latitude,Longitude`

```
ISLAND,Feeder Fix NW 2500,44.927778,-93.568889
SOCCER,Feeder Fix SE 2300,44.739444,-93.325000
```

Use `""` for an empty description. Waypoint names are case-sensitive.

PDFs or TXT files in the same folder are associated with a waypoint when the filename starts with the exact waypoint name (e.g., `ISLAND_Chart.PDF`).

## Manifest (optional)

```json
{
  "name": "Pack Name",
  "abbreviation": "ID",
  "version": 2.0,
  "organizationName": "Org"
}
```

Supports optional `effectiveDate` and `expirationDate` fields in `YYYYMMDDThh:mm:ss` format.

## Installing via URL

Content packs can be loaded directly in ForeFlight using a link in this format:

```
https://foreflight.com/content?downloadURL=<url-to-zip>
```

Source: [ForeFlight Content Packs](https://www.foreflight.com/support/content-packs/)
