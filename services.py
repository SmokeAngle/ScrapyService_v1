from twisted.application import service
from twisted.internet.defer import Deferred
from utils import log,getTaskConfig
from config import *
from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


project_settings =get_project_settings()

class taskRootService(service.MultiService):

    name = 'taskRootService'
    
    def __init__(self):
        service.MultiService.__init__(self)
        
    def startService(self):
        self.startTask(1)
        service.MultiService.startService(self)
        log.msg("taskRootService->startService")

    def startTask(self, taskId):
        taskConfigDefer = getTaskConfig(taskId)
        if not isinstance(taskConfigDefer, Deferred):
            return  None
        def addTask(data, taskId):
            taskName = self.getTaskName(taskId)
            if taskName not in self.namedServices:
                _taskService = taskService(taskId=taskId, taskName=taskName, setting = data)
                self.addService(_taskService)
                log.msg(format='add task success taskId=%(taskId)s taskName=%(taskName)s', taskId=taskId, taskName=taskName)
                return True
            else :
                log.msg('add task error task is existed taskId=%(taskId)s taskName=%(taskName)s', taskId=taskId, taskName=taskName)
                return False
        def configErr(msg, taskId):
            log.msg('get config error taskid= %s ' % taskId )
            log.msg('error: ')
            log.msg(msg)

        taskConfigDefer.addCallback(addTask, taskId=taskId)
        taskConfigDefer.addErrback(configErr, taskId=taskId)

    def removeTask(self, taskId):
        if taskId is None:
            log.msg('remove task error , taskid is None')
            return None    
        taskName = self.getTaskName(taskId)
        if taskName in self.namedServices:
            self.removeService(self.getServiceNamed(taskName))
            log.msg(format='remove task success taskId=%(taskId)s taskName=%(taskName)s', taskId=taskId, taskName=taskName)
            return True
        else :
            log.msg('remove task error , taskid is not existed')
            return False
    
    def getTaskName(self, taskId):
        return 'task_%s' % taskId



class taskService(service.MultiService)  :
    def __init__(self, taskId, taskName, setting):
        service.MultiService.__init__(self)
        self.taskId = taskId
        self.name = taskName
        self.setting = setting
        self._crawlerProcess = CrawlerProcess(project_settings)
        self._crawlerProcess.create_crawler('start_page_crawler')
#         self._crawlerProcess.create_crawler('list_page_crawler')
#         self._crawlerProcess.create_crawler('content_page_crawler')
#         self._crawlerProcess.create_crawler('extra_page_crawler')
        
        # 
        # self._listPageService = listPageService()
        # self._contentPageService = contentPageService()
        # self._extraPageService = extraPageService()



    def startService(self):
        _spider_start_page_setting =  self.setting.get(SPIDER_TYPE_START_PAGE)
        if _spider_start_page_setting is not None:
            _spider_start_page_setting['szStartUrl']=self.setting.get('szStartUrl')
            _spider_start_page_setting['szRegStartUrl']=self.setting.get('szRegStartUrl')
#             self._startStartPageSpider(_spider_start_page_setting)
            
        
        self._crawlerProcess.start()
#     sService = startPageService(self)
        lSeevice = listPageService(self)
        cService = contentPageService(self)
        # eService = extraPageService(self)
#         self.addService(sService)
        self.addService(lSeevice)
        self.addService(cService)
        # self.addService(eService)
        service.MultiService.startService(self)
        log.msg('taskService->startService')

    def _startStartPageSpider(self, config):
        startPageCrawler = self._crawlerProcess.crawlers.get('start_page_crawler')
        
        print '======>'
        print startPageCrawler
        
#         startPageSpider = load_object(config.get('szSnameSpace'))
#         startPageCrawler.crawl(startPageSpider)
        

    def stopService(self):
        service.MultiService.stopService(self)
        log.msg('taskService->stopService')


class startPageService(service.Service):
    def __init__(self, taskService, config):
        self.taskService = taskService
        self.config = config
        spiderNameSpace = self.config.get('szSnameSpace')
        self.spider = load_object(spiderNameSpace)
         
        
         
         
    def startService(self):
        service.Service.startService(self)
        log.msg('startPageService->%s' % self.taskService.taskId)
 
    def stopService(self):
        service.Service.stopService(self)
 
 
class listPageService(service.Service):
    def __init__(self, taskService):
        self.taskService = taskService
    def startService(self):
        service.Service.startService(self)
        log.msg('listPageService->%s' % self.taskService.taskId)
    def stopService(self):
        service.Service.stopService(self)
     
class contentPageService(service.Service):
    def __init__(self, taskService):
        self.taskService = taskService
    def startService(self):
        service.Service.startService(self)
        log.msg('contentPageService->%s' % self.taskService.taskId)
    def stopService(self):
        service.Service.stopService(self)
 
class extraPageService(service.Service):
    def __init__(self, taskService):
        self.taskService = taskService
    def startService(self):
        service.Service.startService(self)
    def stopService(self):
        service.Service.stopService(self)
# class pageService():
#     def __init__(self):
#         pass