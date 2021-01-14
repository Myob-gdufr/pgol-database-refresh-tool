import unittest
from rdsbackup.Log import Log, LogLevel, GlobalLog
from rdsbackup.RdsServer import RdsServer

# noinspection SpellCheckingInspection
class TestRdsServer(unittest.TestCase):
    def setUp(self):
        self.__log = Log(self.__class__, LogLevel.TRACE)

    def test_regex_prod(self):
        source = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))
        expected = list(map(lambda x: {'db': x}, [
            "PG1000NZ"
        ]))

        #  Test
        results = list(filter(RdsServer.db_filter([RdsServer.DbFilter.PROD]), source))

        #  Verify
        self.assertEqual(expected, results)

    def test_regex_test(self):
        source = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))
        expected = list(map(lambda x: {'db': x}, [
            "PG1000NZ_Test", "PG1000NZ_Test2"
        ]))

        #  Test
        results = list(filter(RdsServer.db_filter([RdsServer.DbFilter.TEST]), source))

        #  Verify
        self.assertEqual(expected, results)

    def test_regex_sites(self):
        source = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))
        expected = list(map(lambda x: {'db': x}, [
            "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614"
        ]))

        #  Test
        results = list(filter(RdsServer.db_filter([RdsServer.DbFilter.PG_SITE]), source))

        #  Verify
        self.assertEqual(expected, results)

    def test_regex_system(self):
        source = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))
        expected = list(map(lambda x: {'db': x}, [
            "master", "audit", "tempdb"
        ]))

        #  Test
        results = list(filter(RdsServer.db_filter([RdsServer.DbFilter.MSSQL_SYSTEM]), source))

        #  Verify
        self.assertEqual(expected, results)

    def test_regex_all(self):
        source = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))
        expected = list(map(lambda x: {'db': x}, [
            "master", "audit", "PG1000NZ", "PG1000NZ_Test", "PG1000NZ_Test2",
            "PG1000AU_Historic", "PG1000AU_Historic_20180614",
            "tempdb"
        ]))

        #  Test
        results = list(filter(RdsServer.db_filter([RdsServer.DbFilter.ALL]), source))

        #  Verify
        self.assertEqual(expected, results)


if __name__ == '__main__':
    unittest.main()
