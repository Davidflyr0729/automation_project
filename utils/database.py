import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """Manejador mejorado de base de datos SQLite"""
    
    def __init__(self, db_path="data/test_results.db"):
        self.db_path = db_path
        self._create_database()
    
    def _create_database(self):
        """Crear la base de datos con estructura mejorada"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla principal de resultados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_case_number INTEGER NOT NULL,
                test_case_name TEXT NOT NULL,
                browser TEXT NOT NULL,
                language TEXT NOT NULL,
                status TEXT NOT NULL,
                execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT,
                screenshot_path TEXT,
                additional_info TEXT
            )
        ''')
        
        # Tabla para estadísticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_case_number INTEGER NOT NULL,
                browser TEXT NOT NULL,
                total_tests INTEGER DEFAULT 0,
                passed_tests INTEGER DEFAULT 0,
                failed_tests INTEGER DEFAULT 0,
                last_execution DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(test_case_number, browser)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Base de datos verificada en: {self.db_path}")
    
    def save_test_result(self, test_case_number, test_case_name, browser, language, status, 
                        url="", screenshot_path="", additional_info=""):
        """Guardar resultado de test con estructura mejorada"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insertar resultado
        cursor.execute('''
            INSERT INTO test_results 
            (test_case_number, test_case_name, browser, language, status, url, screenshot_path, additional_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (test_case_number, test_case_name, browser, language, status, url, screenshot_path, additional_info))
        
        # Actualizar estadísticas
        self._update_stats(cursor, test_case_number, browser, status)
        
        conn.commit()
        conn.close()
        print(f"✅ Resultado guardado: Caso {test_case_number} - {browser} - {language} - {status}")
    
    def _update_stats(self, cursor, test_case_number, browser, status):
        """Actualizar estadísticas del test case"""
        # Verificar si ya existe estadística para este caso y navegador
        cursor.execute('''
            SELECT total_tests, passed_tests, failed_tests 
            FROM test_stats 
            WHERE test_case_number = ? AND browser = ?
        ''', (test_case_number, browser))
        
        result = cursor.fetchone()
        
        if result:
            # Actualizar estadística existente
            total, passed, failed = result
            total += 1
            passed += 1 if status == "PASS" else 0
            failed += 1 if status == "FAIL" else 0
            
            cursor.execute('''
                UPDATE test_stats 
                SET total_tests = ?, passed_tests = ?, failed_tests = ?, last_execution = CURRENT_TIMESTAMP
                WHERE test_case_number = ? AND browser = ?
            ''', (total, passed, failed, test_case_number, browser))
        else:
            # Crear nueva estadística
            passed = 1 if status == "PASS" else 0
            failed = 1 if status == "FAIL" else 0
            
            cursor.execute('''
                INSERT INTO test_stats 
                (test_case_number, browser, total_tests, passed_tests, failed_tests)
                VALUES (?, ?, 1, ?, ?)
            ''', (test_case_number, browser, passed, failed))
    
    def get_test_results(self, test_case_number=None, browser=None):
        """Obtener resultados filtrados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM test_results"
        params = []
        
        if test_case_number and browser:
            query += " WHERE test_case_number = ? AND browser = ?"
            params = [test_case_number, browser]
        elif test_case_number:
            query += " WHERE test_case_number = ?"
            params = [test_case_number]
        elif browser:
            query += " WHERE browser = ?"
            params = [browser]
            
        query += " ORDER BY execution_time DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_test_stats(self, test_case_number=None):
        """Obtener estadísticas de tests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if test_case_number:
            cursor.execute('''
                SELECT * FROM test_stats WHERE test_case_number = ? ORDER BY last_execution DESC
            ''', (test_case_number,))
        else:
            cursor.execute('SELECT * FROM test_stats ORDER BY last_execution DESC')
        
        stats = cursor.fetchall()
        conn.close()
        return stats
    
    def print_database_summary(self):
        """Imprimir resumen completo de la base de datos"""
        print("\n📊 RESUMEN BASE DE DATOS:")
        print("=" * 50)
        
        # Estadísticas generales
        stats = self.get_test_stats()
        results = self.get_test_results()
        
        print(f"📈 Total de registros: {len(results)}")
        print(f"📋 Total de estadísticas: {len(stats)}")
        
        if stats:
            print("\n🔍 ESTADÍSTICAS POR CASO Y NAVEGADOR:")
            for stat in stats:
                case_num, browser, total, passed, failed, last_exec = stat[1], stat[2], stat[3], stat[4], stat[5], stat[6]
                success_rate = (passed / total * 100) if total > 0 else 0
                print(f"   Caso {case_num} - {browser:<8}: {passed}/{total} éxitos ({success_rate:.1f}%) - {last_exec}")
        
        if results:
            print(f"\n📝 ÚLTIMOS 4 REGISTROS:")
            for row in results[:4]:
                status_icon = "✅" if row[5] == "PASS" else "❌"
                print(f"   {status_icon} Caso {row[1]} - {row[3]:<8} - {row[4]:<10} - {row[6]}")