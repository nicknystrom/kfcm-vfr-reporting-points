# GTN User Waypoint File

## File Format

CSV file named **`user.wpt`** with no header row. One waypoint per row:

| Column | Field       | Format                                                    |
|--------|-------------|-----------------------------------------------------------|
| A      | Name        | Up to 6 uppercase alphanumeric characters                 |
| B      | Comment     | Up to 25 uppercase alphanumeric characters                |
| C      | Latitude    | Decimal degrees, negative for south (up to DD.DDDDDDDDD) |
| D      | Longitude   | Decimal degrees, negative for west (up to DDD.DDDDDDDD)  |

If an imported waypoint is within 0.001 degree of an existing user waypoint, the existing waypoint and name will be reused.

### Example

```
ISLAND,FEEDER FIX NW 2500,44.927778,-93.568889
HIGHSC,FEEDER FIX NW,44.857778,-93.643889
```

## Installing on the GTN

1. Save/rename the file as `user.wpt`
2. Copy to a blank SD card (8 GB or smaller)
3. Insert SD card into GTN SD card slot
4. Power up the GTN
5. Select **Waypoint Info** > **Import Waypoints** > **OK**
6. Wait for confirmation, then power down
7. Remove SD card and re-insert supplemental database card

Source: [Garmin Aviation Support](https://support.garmin.com/en-US/aviation/faq/3mcdU37gXi88ipwjJIxJo7)
