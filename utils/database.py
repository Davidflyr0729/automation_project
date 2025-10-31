import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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
        
        # NUEVA TABLA: Caso 6 - Redirecciones Header
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS case6_redirects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                browser TEXT NOT NULL,
                language TEXT NOT NULL,
                from_url TEXT NOT NULL,
                to_url TEXT NOT NULL,
                redirect_success BOOLEAN NOT NULL,
                load_time_seconds REAL,
                page_title TEXT,
                execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                additional_notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Base de datos verificada en: {self.db_path}")
    
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
        logger.info(f"✅ Resultado guardado: Caso {test_case_number} - {browser} - {language} - {status}")
    
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
    
    # NUEVO MÉTODO: Guardar datos específicos del Caso 6
    def save_case6_redirect(self, test_name, browser, language, from_url, to_url, 
                           redirect_success, load_time_seconds=None, page_title=None, additional_notes=""):
        """Guardar datos específicos de redirecciones del Caso 6"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO case6_redirects 
            (test_name, browser, language, from_url, to_url, redirect_success, 
             load_time_seconds, page_title, additional_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (test_name, browser, language, from_url, to_url, redirect_success, 
              load_time_seconds, page_title, additional_notes))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Redirección Caso 6 guardada: {test_name} - {browser} - {language}")
    
    # NUEVO MÉTODO: Obtener redirecciones del Caso 6
    def get_case6_redirects(self, browser=None, language=None):
        """Obtener redirecciones del Caso 6 con filtros opcionales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM case6_redirects"
        params = []
        
        conditions = []
        if browser:
            conditions.append("browser = ?")
            params.append(browser)
        if language:
            conditions.append("language = ?")
            params.append(language)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY execution_time DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
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
    
    # NUEVO MÉTODO: Estadísticas específicas del Caso 6
    def get_case6_stats(self):
        """Obtener estadísticas específicas del Caso 6"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Estadísticas por navegador
        cursor.execute('''
            SELECT browser, 
                   COUNT(*) as total_redirects,
                   SUM(CASE WHEN redirect_success = 1 THEN 1 ELSE 0 END) as successful_redirects,
                   AVG(load_time_seconds) as avg_load_time
            FROM case6_redirects 
            GROUP BY browser
        ''')
        browser_stats = cursor.fetchall()
        
        # Estadísticas por idioma
        cursor.execute('''
            SELECT language, 
                   COUNT(*) as total_redirects,
                   SUM(CASE WHEN redirect_success = 1 THEN 1 ELSE 0 END) as successful_redirects
            FROM case6_redirects 
            GROUP BY language
        ''')
        language_stats = cursor.fetchall()
        
        # Estadísticas por test
        cursor.execute('''
            SELECT test_name, 
                   COUNT(*) as total_redirects,
                   SUM(CASE WHEN redirect_success = 1 THEN 1 ELSE 0 END) as successful_redirects
            FROM case6_redirects 
            GROUP BY test_name
        ''')
        test_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'browser_stats': browser_stats,
            'language_stats': language_stats,
            'test_stats': test_stats
        }
    
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
        
        # NUEVO: Estadísticas del Caso 6
        case6_stats = self.get_case6_stats()
        if case6_stats['browser_stats']:
            print(f"\n🎯 CASO 6 - REDIRECCIONES HEADER:")
            
            print("   📊 Por Navegador:")
            for stat in case6_stats['browser_stats']:
                browser, total, success, avg_time = stat
                success_rate = (success / total * 100) if total > 0 else 0
                avg_time_str = f"{avg_time:.2f}s" if avg_time else "N/A"
                print(f"     {browser:<8}: {success}/{total} éxitos ({success_rate:.1f}%) - Tiempo: {avg_time_str}")
            
            print("   🌐 Por Idioma:")
            for stat in case6_stats['language_stats']:
                language, total, success = stat
                success_rate = (success / total * 100) if total > 0 else 0
                print(f"     {language:<10}: {success}/{total} éxitos ({success_rate:.1f}%)")
        
        if results:
            print(f"\n📝 ÚLTIMOS 4 REGISTROS:")
            for row in results[:4]:
                status_icon = "✅" if row[5] == "PASS" else "❌"
                print(f"   {status_icon} Caso {row[1]} - {row[3]:<8} - {row[4]:<10} - {row[6]}")

    # NUEVO MÉTODO: Limpiar datos antiguos (opcional)
    def cleanup_old_data(self, days_old=30):
        """Eliminar datos más antiguos que X días"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = f"datetime('now', '-{days_old} days')"
        
        # Eliminar de test_results
        cursor.execute(f'DELETE FROM test_results WHERE execution_time < {cutoff_date}')
        deleted_results = cursor.rowcount
        
        # Eliminar de case6_redirects
        cursor.execute(f'DELETE FROM case6_redirects WHERE execution_time < {cutoff_date}')
        deleted_redirects = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"🧹 Cleanup completado: {deleted_results} resultados, {deleted_redirects} redirecciones eliminadas")
        return deleted_results + deleted_redirects