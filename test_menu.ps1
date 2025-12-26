# Scripts rápidos para ejecutar tests
# Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Tests Unitarios - Back Minimercado" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$option = Read-Host @"
Selecciona una opción:

# CONTROLLERS - Tests de controladores
1. Ejecutar todos los tests con cobertura
2. Ejecutar solo tests de AuthController
3. Ejecutar solo tests de CajaController
4. Ejecutar solo tests de InventarioController
5. Ejecutar solo tests de VentaController

# REPOSITORIES - Tests de repositorios
6. Ejecutar solo tests de Repositories
7. Ejecutar test_caja_repository.py
8. Ejecutar test_producto_repository.py
9. Ejecutar test_usuario_repository.py
10. Ejecutar test_venta_repository.py

# UTILIDADES
11. Ver reporte de cobertura HTML
12. Instalar dependencias
13. Limpiar archivos de cobertura

Opción
"@

switch ($option) {
    # CONTROLLERS - Tests de controladores
    "1" {
        Write-Host "`n🧪 Primera corrida: Controllers (generando datos de cobertura)..." -ForegroundColor Green
        python -m pytest tests/controllers/ -v --override-ini addopts= --cov=app.controllers --cov-report=
        Write-Host "`n🧪 Segunda corrida: Repositories (acumulando cobertura + reportes finales)..." -ForegroundColor Green
        python -m pytest tests/repositories/ -v --override-ini addopts= --cov=app.repositories --cov-append --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=60
        Write-Host "`n✅ Cobertura combinada generada (solo Controllers + Repositories)!" -ForegroundColor Green
    }
    "2" {
        Write-Host "`n🧪 Ejecutando tests de AuthController..." -ForegroundColor Green
        python -m pytest tests/controllers/test_auth_controller.py -v
    }
    "3" {
        Write-Host "`n🧪 Ejecutando tests de CajaController..." -ForegroundColor Green
        python -m pytest tests/controllers/test_caja_controller.py -v
    }
    "4" {
        Write-Host "`n🧪 Ejecutando tests de InventarioController..." -ForegroundColor Green
        python -m pytest tests/controllers/test_inventario_controller.py -v
    }
    "5" {
        Write-Host "`n🧪 Ejecutando tests de VentaController..." -ForegroundColor Green
        python -m pytest tests/controllers/test_venta_controller.py -v
    }
    
    # REPOSITORIES - Tests de repositorios
    "6" {
        Write-Host "`n🧪 Ejecutando TODOS los tests de Repositories con cobertura (solo Repositories)..." -ForegroundColor Green
        python -m pytest tests/repositories/ -v --override-ini addopts= --cov=app.repositories --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=60
    }
    "7" {
        Write-Host "`n🧪 Ejecutando test_caja_repository.py..." -ForegroundColor Green
        python -m pytest tests/repositories/test_caja_repository.py -v
    }
    "8" {
        Write-Host "`n🧪 Ejecutando test_producto_repository.py..." -ForegroundColor Green
        python -m pytest tests/repositories/test_producto_repository.py -v
    }
    "9" {
        Write-Host "`n🧪 Ejecutando test_usuario_repository.py..." -ForegroundColor Green
        python -m pytest tests/repositories/test_usuario_repository.py -v
    }
    "10" {
        Write-Host "`n🧪 Ejecutando test_venta_repository.py..." -ForegroundColor Green
        python -m pytest tests/repositories/test_venta_repository.py -v
    }
    
    # UTILIDADES
    "11" {
        Write-Host "`n📊 Abriendo reporte de cobertura..." -ForegroundColor Green
        if (Test-Path "htmlcov/index.html") {
            Start-Process "htmlcov/index.html"
        } else {
            Write-Host "❌ No se encontró el reporte. Ejecuta primero los tests con cobertura." -ForegroundColor Red
        }
    }
    "12" {
        Write-Host "`n📦 Instalando dependencias..." -ForegroundColor Green
        pip install -r requirements.txt
    }
    "13" {
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
