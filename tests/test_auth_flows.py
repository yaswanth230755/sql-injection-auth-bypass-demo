import tempfile
import unittest
from pathlib import Path

import sql_injection_demo.app as app_module
import sql_injection_demo.auth_secure as secure_module
import sql_injection_demo.auth_vulnerable as vulnerable_module
import sql_injection_demo.database as database_module
import sql_injection_demo.logger as logger_module


class AuthFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.test_db = self.temp_path / "users_test.db"
        self.test_log = self.temp_path / "auth_test.log"

        self.original_db_database = database_module.DB
        self.original_db_secure = secure_module.DB
        self.original_db_vulnerable = vulnerable_module.DB
        self.original_db_logger = logger_module.DB
        self.original_logfile_logger = logger_module.LOGFILE

        database_module.DB = str(self.test_db)
        secure_module.DB = str(self.test_db)
        vulnerable_module.DB = str(self.test_db)
        logger_module.DB = str(self.test_db)
        logger_module.LOGFILE = str(self.test_log)

        database_module.init_db()
        self.client = app_module.app.test_client()

    def tearDown(self):
        database_module.DB = self.original_db_database
        secure_module.DB = self.original_db_secure
        vulnerable_module.DB = self.original_db_vulnerable
        logger_module.DB = self.original_db_logger
        logger_module.LOGFILE = self.original_logfile_logger
        self.temp_dir.cleanup()

    def test_index_route_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_vulnerable_login_allows_sql_injection_bypass(self):
        response = self.client.post(
            "/login_vuln",
            data={"username": "' OR '1'='1' --", "password": "anything"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ATTACK SUCCESSFUL", response.data)
        self.assertIn(b"Module mode: VULNERABLE", response.data)

    def test_secure_login_blocks_sql_injection_payload(self):
        response = self.client.post(
            "/login_safe",
            data={"username": "' OR '1'='1' --", "password": "anything"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MITIGATION ACTIVE", response.data)
        self.assertIn(b"Module mode: SECURE", response.data)

    def test_secure_login_locks_account_after_repeated_failures(self):
        for _ in range(5):
            self.client.post(
                "/login_safe",
                data={"username": "admin", "password": "wrong-password"},
            )

        locked_response = self.client.post(
            "/login_safe",
            data={"username": "admin", "password": "adminpass123"},
        )
        self.assertEqual(locked_response.status_code, 200)
        self.assertIn(b"Account temporarily locked", locked_response.data)

    def test_secure_login_writes_audit_log_entry(self):
        self.client.post(
            "/login_safe",
            data={"username": "admin", "password": "wrong-password"},
        )

        self.assertTrue(self.test_log.exists())
        log_contents = self.test_log.read_text(encoding="utf-8")
        self.assertIn("LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_1", log_contents)


if __name__ == "__main__":
    unittest.main()
