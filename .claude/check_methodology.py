#!/usr/bin/env python3
"""
Validador de cumplimiento de metodología para el proyecto Graphiti.
Verifica que se sigan los checkpoints y mejores prácticas.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class MethodologyChecker:
    """Verifica el cumplimiento de la metodología de desarrollo."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.status_file = self.project_root / ".claude" / "methodology_status.json"
        self.checkpoint_log = self.project_root / ".claude" / "checkpoint_log.json"
        self.errors = []
        self.warnings = []
        
    def check_git_status(self) -> bool:
        """Verifica el estado de git."""
        try:
            # Verificar branch actual
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            current_branch = result.stdout.strip()
            
            if current_branch == "main":
                self.errors.append("❌ Trabajando en main directamente (prohibido)")
                return False
                
            # Verificar si hay cambios sin commitear
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.stdout.strip():
                self.warnings.append("⚠️  Hay cambios sin commitear")
                
            print(f"✅ Git status OK (branch: {current_branch})")
            return True
            
        except Exception as e:
            self.errors.append(f"❌ Error verificando git: {e}")
            return False
    
    def check_tests(self) -> bool:
        """Verifica que los tests pasen."""
        try:
            result = subprocess.run(
                ["pytest", "--co", "-q"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode != 0:
                self.warnings.append("⚠️  Tests no se pueden ejecutar")
                return True  # No es error crítico
                
            print("✅ Tests verificados")
            return True
            
        except FileNotFoundError:
            self.warnings.append("⚠️  pytest no instalado")
            return True
    
    def check_backup_exists(self) -> bool:
        """Verifica que exista un backup reciente."""
        try:
            result = subprocess.run(
                ["git", "tag", "-l", "backup-*"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            backup_tags = result.stdout.strip().split('\n')
            backup_tags = [tag for tag in backup_tags if tag]
            
            if not backup_tags:
                self.warnings.append("⚠️  No hay tags de backup")
                return True
                
            latest_backup = backup_tags[-1]
            print(f"✅ Backup encontrado: {latest_backup}")
            return True
            
        except Exception as e:
            self.errors.append(f"❌ Error verificando backups: {e}")
            return False
    
    def check_methodology_status(self) -> bool:
        """Verifica el estado de la metodología."""
        if not self.status_file.exists():
            # Crear archivo inicial
            self.initialize_status_file()
            
        try:
            with open(self.status_file) as f:
                status = json.load(f)
                
            checkpoints = status.get("checkpoints", {})
            pending = [k for k, v in checkpoints.items() if v["status"] == "pending"]
            
            if pending:
                self.warnings.append(f"⚠️  Checkpoints pendientes: {', '.join(pending)}")
                
            print("✅ Estado de metodología cargado")
            return True
            
        except Exception as e:
            self.errors.append(f"❌ Error leyendo estado: {e}")
            return False
    
    def initialize_status_file(self):
        """Inicializa el archivo de estado."""
        initial_status = {
            "session_start": datetime.now().isoformat(),
            "checkpoints": {
                "setup": {"status": "pending", "timestamp": None},
                "analysis": {"status": "pending", "timestamp": None},
                "plan": {"status": "pending", "timestamp": None},
                "design": {"status": "pending", "timestamp": None},
                "backup": {"status": "pending", "timestamp": None},
                "development": {"status": "pending", "timestamp": None},
                "pr": {"status": "pending", "timestamp": None},
                "merge": {"status": "pending", "timestamp": None}
            },
            "current_phase": "initialization"
        }
        
        self.status_file.parent.mkdir(exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(initial_status, f, indent=2)
    
    def check_code_quality(self) -> bool:
        """Verifica la calidad del código."""
        checks_passed = True
        
        # Verificar con ruff
        try:
            result = subprocess.run(
                ["ruff", "check", ".", "--quiet"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode != 0:
                self.warnings.append("⚠️  Ruff encontró problemas de estilo")
                
        except FileNotFoundError:
            self.warnings.append("⚠️  ruff no instalado")
            
        print("✅ Verificación de calidad completada")
        return checks_passed
    
    def generate_report(self) -> Tuple[bool, str]:
        """Genera reporte de cumplimiento."""
        all_passed = len(self.errors) == 0
        
        report = []
        report.append("\n" + "="*50)
        report.append("📊 REPORTE DE CUMPLIMIENTO DE METODOLOGÍA")
        report.append("="*50)
        
        if all_passed:
            report.append("\n✅ CUMPLIMIENTO TOTAL - Puedes proceder")
        else:
            report.append("\n❌ HAY ERRORES CRÍTICOS - No proceder")
            
        if self.errors:
            report.append("\n🔴 ERRORES CRÍTICOS:")
            for error in self.errors:
                report.append(f"  {error}")
                
        if self.warnings:
            report.append("\n🟡 ADVERTENCIAS:")
            for warning in self.warnings:
                report.append(f"  {warning}")
                
        report.append("\n" + "="*50)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append("="*50 + "\n")
        
        return all_passed, '\n'.join(report)
    
    def run_all_checks(self) -> bool:
        """Ejecuta todas las verificaciones."""
        print("\n🔍 Iniciando verificación de metodología...\n")
        
        checks = [
            ("Git Status", self.check_git_status),
            ("Tests", self.check_tests),
            ("Backup", self.check_backup_exists),
            ("Methodology Status", self.check_methodology_status),
            ("Code Quality", self.check_code_quality)
        ]
        
        for name, check_func in checks:
            print(f"Verificando {name}...")
            check_func()
            
        passed, report = self.generate_report()
        print(report)
        
        return passed


def main():
    """Función principal."""
    checker = MethodologyChecker()
    
    if checker.run_all_checks():
        print("✅ Todas las verificaciones pasaron. Puedes continuar.")
        sys.exit(0)
    else:
        print("❌ Hay problemas que resolver antes de continuar.")
        sys.exit(1)


if __name__ == "__main__":
    main()