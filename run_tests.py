# Script para ejecutar tests con cobertura
# Ejecutar: python run_tests.py

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*80}")
    print(f"  {description}")
    print(f"{'='*80}\n")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error al ejecutar: {description}")
        return False
    else:
        print(f"\n✅ {description} completado exitosamente")
        return True

def main():
    print("🧪 Iniciando ejecución de pruebas unitarias")
    print("📁 Proyecto: Back Minimercado - Controllers, Repositories y Services")
    
    # Verificar que pytest está instalado
    try:
        import pytest
        print("✅ pytest encontrado")
    except ImportError:
        print("❌ pytest no está instalado")
        print("Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    # Ejecutar tests con cobertura acumulada (controllers + repositories + services)
    commands = [
        # PRIMERA ejecución: Controllers generan datos de cobertura (sin reportes)
        (
            "python -m pytest tests/controllers/ -v --override-ini addopts= --cov=app.controllers --cov-report=",
            "Primera ejecución: Controllers (generando datos de cobertura)"
        ),
        # SEGUNDA ejecución: Repositories acumulan cobertura (sin reportes)
        (
            "python -m pytest tests/repositories/ -v --override-ini addopts= --cov=app.repositories --cov-append --cov-report=",
            "Segunda ejecución: Repositories (acumulando cobertura)"
        ),
        # TERCERA ejecución: Services acumulan cobertura + generan reportes finales
        (
            "python -m pytest tests/services/ -v --override-ini addopts= --cov=app.services --cov-append --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=60",
            "Tercera ejecución: Services (acumulando cobertura + reportes finales)"
        ),
    ]
    
    all_success = True
    for command, description in commands:
        if not run_command(command, description):
            all_success = False
    
    # Resumen final
    print(f"\n{'='*80}")
    print("  RESUMEN DE EJECUCIÓN")
    print(f"{'='*80}\n")
    
    if all_success:
        print("✅ Todos los tests pasaron exitosamente")
        print("📊 Reporte de cobertura generado en: htmlcov/index.html")
        print("📄 Reporte XML generado en: coverage.xml")
        print("\n💡 Para ver el reporte HTML, abre: htmlcov/index.html")
    else:
        print("❌ Algunos tests fallaron o la cobertura es menor al 60%")
        print("🔍 Revisa los mensajes de error anteriores")
        sys.exit(1)

if __name__ == "__main__":
    main()
