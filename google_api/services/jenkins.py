from jenkinsapi.jenkins import Jenkins

class JenkinsService():
    def __init__(self,url,username,password):
        self.jenkins=Jenkins(url, username, password)

    def ejecutar_job(self,job_name,parameters):
        self.jenkins.build_job(job_name, params=parameters)
        #self.jenkins.build_job(job_name)

if __name__ == '__main__':
    parameters = None
    service=JenkinsService('http://localhost:9090/','admin','admin')
    jenkins=service.jenkins
    job_name='Ejemplo'
    parameters =  {'token': '123456789',
                   'fecha': 'hola'}
    service.ejecutar_job('Ejemplo',parameters)