from twisted.application import service,internet
from twisted.web import server,static
from services import taskRootService
from config import APP_NAME,WEB_SERVICE_PORT


def createApplication():
    app = service.Application(name=APP_NAME)
    appSrv = service.IServiceCollection(app)
    
    _taskRootService = taskRootService()
    _taskRootService.setServiceParent(appSrv)
    
    _webService = internet.TCPServer(WEB_SERVICE_PORT, server.Site(static.File('.')))
    _webService.setServiceParent(appSrv)
    
    return app

application = createApplication()
