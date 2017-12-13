"""
MIT License

Copyright (c) 2017 Formstack

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pymysql

from checks import AgentCheck
from contextlib import closing, contextmanager


class AirflowDagCheck(AgentCheck):
    SERVICE_CHECK_NAME = 'airflow_dag.can_connect'
    DAG_CHECK_NAME = 'airflow_dag.run_status'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

        self.table = None

    def check(self, instance):
        collected_metrics = None

        host, user, password, database, table, port = self._get_config(instance)

        self.table = table

        if not host or not user:
            raise Exception("mysql_host and mysql_user are required")

        with self._connect(host, user, password, port, database) as db:
            try:
                collected_metrics = self._collect_dag_metrics(db)
            except Exception:
                self.log_exception(Exception.message)

        if collected_metrics == None:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL)

        for metric in collected_metrics:
            dag_check_tags = [
                'dag_id:%s' % metric['dag_id'],
            ]

            if metric['state'] == 'failed':
                self.service_check(self.DAG_CHECK_NAME, AgentCheck.CRITICAL, tags=dag_check_tags)
            elif metric['state'] == 'success':
                self.service_check(self.DAG_CHECK_NAME, AgentCheck.OK, tags=dag_check_tags)

    def _get_config(self, instance):
        host = instance.get('mysql_host', '')
        user = instance.get('mysql_user', '')
        password = instance.get('mysql_password', '')
        database = instance.get('mysql_database', '')
        table = instance.get('mysql_table', '')
        port = instance.get('mysql_port', 3306)

        return (
            host,
            user,
            password,
            database,
            table,
            port
        )

    @contextmanager
    def _connect(self, host, user, password, port, database):
        self.service_check_tags = [
            'server:%s' % host,
            'port:%s' % port
        ]

        db = None

        try:
            db = pymysql.connect(
                host=host,
                port=port,
                user=user,
                passwd=password,
                db=database
            )
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags=self.service_check_tags)
            yield db
        except Exception:
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags=self.service_check_tags)
            raise
        finally:
            if db:
                db.close()

    def _collect_dag_metrics(self, db):
        with closing(db.cursor(pymysql.cursors.DictCursor)) as cursor:
            cursor.execute(
                "SELECT dag_id, state, execution_date FROM "
                + self.table
                + " WHERE execution_date >= DATE(subdate(NOW(), 1))"
            )
            results = cursor.fetchall()

        return results
