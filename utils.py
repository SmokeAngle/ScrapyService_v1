from twisted.python.log import theLogPublisher
from config import *
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor


class log():
    
    @staticmethod
    def msg(*message, **kw):
        if APP_DEBUG is True:
            theLogPublisher.msg(system=APP_NAME, *message, **kw)



def getTaskConfig(taskId):
    if taskId is None:
        return None
    def getRowConfig(tx):
        tx.execute('SELECT p.szName,pt.szTaskName,pt.iPid,pt.iTaskId,pt.szRegStartUrl,pt.szStartUrl,pt.szRegListUrl ' 
                   ' FROM project p LEFT JOIN project_task pt ON p.iPid = pt.iPid WHERE p.iPid = %d' % taskId)
        projectSetting = tx.fetchone()
        if isinstance(projectSetting, dict):
            tx.execute('SELECT ps.szStype,ps.szSnameSpace '
                       'FROM project_spider_to_task pstt '
                       'LEFT JOIN project_spider ps ON ps.iSid = pstt.iSid '
                       'WHERE pstt.iTaskId = %d' % taskId)
            taskConfig = tx.fetchall()
#             projectSetting.update(taskConfig)
            for config in taskConfig:
                projectSetting['%s' % config.get('szStype')] = config
        return projectSetting
              
        
    dbPool = adbapi.ConnectionPool('MySQLdb', db=PROJECT_DB_NAME, user=PROJECT_DB_USER,passwd=PROJECT_DB_PASS, 
                                   host=PROJECT_DB_HOST, use_unicode=PROJECT_DB_UNICODE, charset=PROJECT_DB_CHARSET, 
                                   cursorclass=DictCursor)
    return dbPool.runInteraction(getRowConfig)