# Mennekes Amtron Wallbox
With this Python module you can read and write modbus registers from MENNEKES AMTRON Xtra/Premium wallboxes.
Tested on my MENNEKES AMTRON Xtra wallbox.

Should work for AMTRON Premium devices as well.

Implements registers from the [MENNEKES ATROM MODBUS-TCP description](https://update.mennekes.de/hcc3/1.13/Description%20Modbus_AMTRON%20HCC3_v01_2021-06-25_en.pdf).

## Setup

Clone git and call:
```bash
pip install .
```

## Usage
```python
from amtronwallbox.amtronwallbox import MennekesAmtronWallbox

#ip and port for modbus host
amtron = MennekesAmtronWallbox('IP',502)

#update and show all values provided by register map for modbus server
amtron.print_all_data()
> {
    'internal_temp': 12,
    'external_temp': 13,
    'cp_state': 1,
    'pp_state': 4,
    'hcc3_error_code': 0,
    'state': 0,
    'operation_mode': 1,
    'connector_type': 2,
    'no_of_phases': 3,
    'rated_current': 32,
    'installation_current': 16,
    'serial_number': 0000000000,
    'charging_session_meter_count': 11779,
    'actual_power_consumption': 0,
    'wallbox_name': 'AMTRON',
    'max_current_t1': 16,
    'start_hour_t1': 4,
    'start_minute_t1': 30
}
```
