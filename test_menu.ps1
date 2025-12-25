# Scripts rápidos para ejecutar tests
# Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Tests Unitarios - Back Minimercado" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$option = Read-Host @"
Selecciona una opción:
1. Ejecutar todos los tests con cobertura
2. Ejecutar solo tests de AuthController
3. Ejecutar solo tests de CajaController
4. Ejecutar solo tests de InventarioController
5. Ejecutar solo tests de VentaController
6. Ver reporte de cobertura HTML
7. Instalar dependencias
8. Limpiar archivos de cobertura

Opción
"@

switch ($option) {
    "1" {
        Write-Host "`n🧪 Ejecutando todos los tests..." -ForegroundColor Green
        pytest tests/controllers/ -v --cov=app/controllers --cov-report=html --cov-report=term-missing
    }
    "2" {
        Write-Host "`n🧪 Ejecutando tests de AuthController..." -ForegroundColor Green
        pytest tests/controllers/test_auth_controller.py -v
    }
    "3" {
        Write-Host "`n🧪 Ejecutando tests de CajaController..." -ForegroundColor Green
        pytest tests/controllers/test_caja_controller.py -v
    }
    "4" {
        Write-Host "`n🧪 Ejecutando tests de InventarioController..." -ForegroundColor Green
        pytest tests/controllers/test_inventario_controller.py -v
    }
    "5" {
        Write-Host "`n🧪 Ejecutando tests de VentaController..." -ForegroundColor Green
        pytest tests/controllers/test_venta_controller.py -v
    }
    "6" {
        Write-Host "`n📊 Abriendo reporte de cobertura..." -ForegroundColor Green
        if (Test-Path "htmlcov/index.html") {
            Start-Process "htmlcov/index.html"
        } else {
            Write-Host "❌ No se encontró el reporte. Ejecuta primero los tests con cobertura." -ForegroundColor Red
        }
    }
    "7" {
        Write-Host "`n📦 Instalando dependencias..." -ForegroundColor Green
        pip install -r requirements.txt
    }
    "8" {
        Write-Host "`n🧹 Limpiando archivos de cobertura..." -ForegroundColor Green
        Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
        Remove-Item -Force .coverage -ErrorAction SilentlyContinue
        Remove-Item -Force coverage.xml -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
        Write-Host "✅ Limpieza completada" -ForegroundColor Green
    }
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
    }
}

Write-Host "`n"
