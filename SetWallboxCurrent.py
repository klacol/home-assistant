# Aufruf als Dienst

data = {
	"solaredge_current_power" : 4000,
	"solaredge_grid_power" : -1.42,
	"goecharger_003339_u_l1" : 215,
	"goecharger_003339_u_l2" : 215,
	"goecharger_003339_u_l3" : 215,
	"goecharger_max_current" : 8
}
 
 
# Verfügbare Leistung der PV-Anlage in Watt
# sensor.solaredge_current_power
PvPowerGenerated = data.get("solaredge_current_power")

# Leistung, die in das Netz eingespeist wird
# Die Einspeisung wird als negativer Wert in kW übertragen, 
# also solaredge_grid_power = -1,430 bedeutet: Es werden derzeit 1,430 kW ins Netz eingespeist
# sensor.solaredge_grid_power, in kW
PvPowerGrid = data.get("solaredge_grid_power") * 1000  # in Watt

# Leistung, die in das Haus momentan bezieht (inkl. E-Auto) in Watt
# als Differenz zwischen Erzeugung und Einspeisung
# 
PvPowerConsumption = PvPowerGenerated + PvPowerGrid

# Aktuelle Spannung an der Wallbox (V)
# goecharger_003339_u_l1/2/3
ActualWallboxVoltage1 = data.get("goecharger_003339_u_l1")
ActualWallboxVoltage2 = data.get("goecharger_003339_u_l2")
ActualWallboxVoltage3 = data.get("goecharger_003339_u_l3")

# Aktuelle Stromstärke an der Wallbox (A)
# goecharger_max_current
ActualWallboxCurrent = data.get("goecharger_max_current")

# Verfügbare Leistung (wenn positiv, dann kann die Ladeleistung hochgesetzt werden, wenn negativ, dann muss die Ladeleistung reduziert werden)
PvPowerAvailable = PvPowerGenerated - PvPowerConsumption

# Aktuelle Spannung an der Wallbox (V)
ActualWallboxVoltage = (ActualWallboxVoltage1 + ActualWallboxVoltage2 + ActualWallboxVoltage3)/3
 
# Aktuelle Leistung an der Wallbox (W)
# P = U · I also Leistung (Watt) = Spannung (Volt) mal Stromstärke (Ampere)
WallboxPowerActual = ActualWallboxVoltage * ActualWallboxCurrent

AdditionalPower = PvPowerAvailable - WallboxPowerActual
AdditionalChargerCurrent = AdditionalPower / ActualWallboxVoltage
NewWallboxCurrent = int(ActualWallboxCurrent + AdditionalChargerCurrent)

if NewWallboxCurrent < 0: NewWallboxCurrent = 0
if NewWallboxCurrent > 32: NewWallboxCurrent = 32

print ("NewWallboxCurrent: ", NewWallboxCurrent, "Ampere")
#logger.info("NewWallboxCurrent", NewWallboxCurrent)
#hass.bus.fire(name, {"wow": "from a Python script!"})
