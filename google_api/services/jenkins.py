from api4jenkins import Jenkins
import time

class JenkinsService():
    def __init__(self,url,username,password):
        self.jenkins=Jenkins(url,auth=( username, password))

    def ejecutar_job(self,job_name,parameters):
        job=self.jenkins.get_job(job_name)
        print(job)
        print(job.parent)
        item = job.build()
        while not item.get_build():
            time.sleep(1)
        build = item.get_build()
        print(build)
        for line in build.progressive_output():
            print(line)
        print(build.building)
        print(build.result)

if __name__ == '__main__':
    parameters = None
    service=JenkinsService('http://localhost:9090/','admin','admin')
    jenkins=service.jenkins
    print(jenkins.version)
    job_name='Ejemplo'
    parameters =  None
    service.ejecutar_job('Ejemplo',parameters)