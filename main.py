from modules import PlanCreator
from modules import TempRemover
import os
import sys
import ctypes

def comprobar_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not comprobar_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv))

def main():
    pregunta1 = input("Quieres crear un plan de energía? (s/n): ")
    if pregunta1.lower() == "s":
        nombre_plan = input("Introduce el nombre del plan: ")
        tipo_plan = input("Que tipo de plan de energía quieres (bajo, medio, alto): ")

        if tipo_plan == "bajo":
            plan_creator = PlanCreator("bajo", nombre_plan)
            plan_creator.crear_plan_energia()

        if tipo_plan == "medio":
            plan_creator = PlanCreator("medio", nombre_plan)
            plan_creator.crear_plan_energia()

        if tipo_plan == "alto":
            plan_creator = PlanCreator("alto", nombre_plan)
            plan_creator.crear_plan_energia()


    pregunta2 = input("Quieres limpiar los archivos temporales? (s/n): ")

    if pregunta2.lower() == "s":
        cleaner = TempRemover()
        try:
            cleaner.limpiar_temp()
            cleaner.limpiar_prefetch()
            cleaner.limpiar_carpetas_vacias(os.getenv('TEMP'))
        except Exception as e:
            cleaner.logger.error(f"Error durante la limpieza: {str(e)}")



if __name__ == "__main__":
    main()

