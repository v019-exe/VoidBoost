import subprocess
import re

class PlanCreator:
    def __init__(self, tipo, name):
        self.type = tipo
        self.name = name

    @staticmethod
    def obtener_powerplans():
        result = subprocess.run(["powercfg", "/l"], capture_output=True, text=True, shell=True)
        output = result.stdout.strip()

        plans = {}
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("GUID de plan de energ¡a:"):
                match = re.match(r"GUID de plan de energ¡a:\s*([a-fA-F0-9\-]{36})\s*\((.*?)\)", line)
                if match:
                    plan_id = match.group(1)
                    plan_name = match.group(2)
                    plans[plan_id] = plan_name
        return plans

    def crear_plan_energia(self):
        tipo = self.type
        planes = PlanCreator.obtener_powerplans()

        for id, nombre in planes.items():
            if tipo == "alto" and "Alto rendimiento" in nombre:
                subprocess.run(["powercfg", "/changename", id, self.name], shell=True)
                subprocess.run(["powercfg", "/setactive", id], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "0"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "0"], shell=True)
                print(f"Configuraciones de alto rendimiento aplicadas al plan con ID: {id}")
                print(f"Nombre del plan actualizado a: {self.name}")
                break

            if tipo == "bajo" and "Ahorro de energía" in nombre:
                subprocess.run(["powercfg", "/changename", id, self.name], shell=True)
                subprocess.run(["powercfg", "/setactive", id], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "5"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "5"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "15"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "15"], shell=True)
                print(f"Configuraciones de ahorro de energía aplicadas al plan con ID: {id}")
                print(f"Nombre del plan actualizado a: {self.name}")
                break

            if tipo == "medio" and "Equilibrado" in nombre:
                subprocess.run(["powercfg", "/changename", id, self.name], shell=True)
                subprocess.run(["powercfg", "/setactive", id], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "MONITORIDLE", "10"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "15"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_DISK", "DISKIDLE", "15"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "15"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "STANDBYIDLE", "15"], shell=True)
                subprocess.run(["powercfg", "/SETACVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "30"], shell=True)
                subprocess.run(["powercfg", "/SETDCVALUEINDEX", id, "SUB_SLEEP", "HIBERNATEIDLE", "30"], shell=True)
                print(f"Configuraciones de energía equilibrada aplicadas al plan con ID: {id}")
                print(f"Nombre del plan actualizado a: {self.name}")
                break
