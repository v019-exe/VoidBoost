import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Union, List
import ctypes
from ctypes import wintypes

class TempRemover:
    def __init__(self):
        self.logger = self._setup_logger()
        self.protected_files = {
            'temp': ['desktop.ini', 'thumbs.db'],
            'prefetch': ['layout.ini']
        }

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger('TempRemover')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @staticmethod
    def ejecutar_como_admin():
        """
        Reinicia el script con privilegios de administrador si no los tiene.
        """
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                return True
            else:
                # Reiniciar el script con privilegios de administrador
                ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable,
                    " ".join(sys.argv),
                    None,
                    1  # SW_SHOWNORMAL
                )
                sys.exit()
        except Exception as e:
            print(f"Error al solicitar privilegios de administrador: {e}")
            return False

    def archivo_en_uso(self, file_path: Union[str, Path]) -> bool:
        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path, 'rb', buffering=0) as f:
                msvcrt = ctypes.cdll.msvcrt
                file_handle = msvcrt.get_osfhandle(f.fileno())
                result = ctypes.windll.kernel32.LockFile(file_handle, 0, 0, 0, 0)
                if result == 0:
                    return True
                ctypes.windll.kernel32.UnlockFile(file_handle, 0, 0, 0, 0)
                return False
        except (IOError, OSError, AttributeError):
            return True

    def _safe_remove(self, path: Union[str, Path], folder_type: str = 'temp') -> bool:
        path = Path(path)

        if path.name.lower() in self.protected_files.get(folder_type, []):
            self.logger.debug(f"Archivo protegido: {path}")
            return False

        if not path.exists():
            return True

        try:
            if path.is_file():
                if self.archivo_en_uso(path):
                    self.logger.debug(f"Archivo en uso: {path}")
                    return False

                path.unlink(missing_ok=True)
                self.logger.info(f"Archivo eliminado: {path}")
                return True

            elif path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
                self.logger.info(f"Carpeta eliminada: {path}")
                return True

        except Exception as e:
            self.logger.error(f"Error al eliminar {path}: {str(e)}")
            return False

    def limpiar_temp(self) -> None:
        temp_paths = [
            os.getenv('TEMP'),
            os.getenv('TMP'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Temp')
        ]

        for temp_path in temp_paths:
            if temp_path and os.path.exists(temp_path):
                self.logger.info(f"Limpiando carpeta temporal: {temp_path}")
                for item in Path(temp_path).iterdir():
                    self._safe_remove(item, 'temp')
            else:
                self.logger.warning(f"No se encuentra la carpeta temporal: {temp_path}")

    def limpiar_prefetch(self) -> None:
        """
        Limpia la carpeta Prefetch de Windows con administrador
        """
        prefetch_path = Path(r'C:\Windows\Prefetch')

        if not prefetch_path.exists():
            self.logger.warning("No se encuentra la carpeta Prefetch")
            return

        if not ctypes.windll.shell32.IsUserAnAdmin():
            self.logger.warning("Se requieren privilegios de administrador para Prefetch")
            self.ejecutar_como_admin()
            return

        self.logger.info("Limpiando carpeta Prefetch")
        for item in prefetch_path.iterdir():
            self._safe_remove(item, 'prefetch')

    def limpiar_carpetas_vacias(self, folder_path: Union[str, Path]) -> None:
        folder_path = Path(folder_path)

        if not folder_path.exists():
            self.logger.warning(f"La carpeta no existe: {folder_path}")
            return

        try:
            for path in sorted(folder_path.rglob('*'), reverse=True):
                if path.is_dir():
                    try:
                        path.rmdir()
                        self.logger.info(f"Carpeta vacía eliminada: {path}")
                    except OSError:
                        continue
        except Exception as e:
            self.logger.error(f"Error al limpiar carpetas vacías: {str(e)}")