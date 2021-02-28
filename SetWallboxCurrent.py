# Aufruf als Dienst

#data = {
#	"solaredge_current_power" : 4000,
#	"solaredge_grid_power" : -1.72,
#	"goecharger_003339_u_l1" : 215,
#	"goecharger_003339_u_l2" : 215,
#	"goecharger_003339_u_l3" : 215,
#	"goecharger_max_current" : 8
#}
 
logger.info("data: solaredge_current_power: " + str(data.get("solaredge_current_power")))
logger.info("data: solaredge_grid_power:    " + str(data.get("solaredge_grid_power")))
logger.info("data: goecharger_003339_u_l1:  " + str(data.get("goecharger_003339_u_l1")))
logger.info("data: goecharger_003339_u_l2:  " + str(data.get("goecharger_003339_u_l2")))
logger.info("data: goecharger_003339_u_l3:  " + str(data.get("goecharger_003339_u_l3")))
logger.info("data: goecharger_max_current:  " + str(data.get("goecharger_max_current")))
 
# Verfügbare Leistung der PV-Anlage in Watt
# sensor.solaredge_current_power
PvPowerGenerated = float(data.get("solaredge_current_power"))
logger.info("PvPowerGenerated: " + str(PvPowerGenerated))

# Leistung, die in das Netz eingespeist wird
# Die Einspeisung wird als negativer Wert in kW übertragen, 
# also solaredge_grid_power = -1.71 bedeutet: Es werden derzeit 1,72 kW ins Netz eingespeist
# sensor.solaredge_grid_power, in kW
PvPowerGrid = float(data.get("solaredge_grid_power")) * 1000  # in Watt
logger.info("PvPowerGrid: " + str(PvPowerGrid))

# Leistung, die in das Haus momentan bezieht (inkl. E-Auto) in Watt
# als Differenz zwischen Erzeugung und Einspeisung
# 
PvPowerConsumption = float(PvPowerGenerated + PvPowerGrid)
logger.info("PvPowerConsumption: " + str(PvPowerConsumption))

# Aktuelle Spannung an der Wallbox (V)
# goecharger_003339_u_l1/2/3
ActualWallboxVoltage1 = int(data.get("goecharger_003339_u_l1"))
ActualWallboxVoltage2 = int(data.get("goecharger_003339_u_l2"))
ActualWallboxVoltage3 = int(data.get("goecharger_003339_u_l3"))

# Aktuelle Stromstärke an der Wallbox (A)
# goecharger_max_current
ActualWallboxCurrent = int(data.get("goecharger_max_current"))
logger.info("ActualWallboxCurrent: " + str(ActualWallboxCurrent))

# Verfügbare Leistung (wenn positiv, dann kann die Ladeleistung hochgesetzt werden, wenn negativ, dann muss die Ladeleistung reduziert werden)
PvPowerAvailable = float(PvPowerGenerated - PvPowerConsumption)
logger.info("PvPowerAvailable: " + str(PvPowerAvailable))

# Aktuelle Spannung an der Wallbox (V)
ActualWallboxVoltage = float((ActualWallboxVoltage1 + ActualWallboxVoltage2 + ActualWallboxVoltage3)/3)
logger.info("ActualWallboxVoltage: " + str(ActualWallboxVoltage))
 
# Aktuelle Leistung an der Wallbox (W)
# P = U · I also Leistung (Watt) = Spannung (Volt) mal Stromstärke (Ampere)
WallboxPowerActual = float(ActualWallboxVoltage * ActualWallboxCurrent)
logger.info("WallboxPowerActual: " + str(WallboxPowerActual))

AdditionalPower = float(PvPowerAvailable - WallboxPowerActual)
AdditionalChargerCurrent = float(AdditionalPower / ActualWallboxVoltage)
NewWallboxCurrent = int(ActualWallboxCurrent + AdditionalChargerCurrent)

if NewWallboxCurrent < 0: NewWallboxCurrent = 0
if NewWallboxCurrent > 32: NewWallboxCurrent = 32

logger.info("NewWallboxCurrent: " + str(NewWallboxCurrent))

service_data = {"max_current": NewWallboxCurrent}
logger.info("service_data: max_current:  " + str(service_data.get("max_current")))
logger.info("Trying to set now")
hass.services.call("goecharger", "set_max_current", service_data, False)
logger.info("Done - Please check!")
