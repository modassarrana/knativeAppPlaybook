## This document covers step for knative application deployment & uninstallation
Jenkin Job has been written to execute playbook automatically whenever there is code submit
Update the  command in jenkin job for knative application ansible playbook path (git clone)
```
cmd -> sudo ansible-plybook <path of ansible plybook on there server> <path of inventory file>  
Ex->
sudo ansible-playbook /home/centos/FAAS/ansibleAutomation/knative-app.yml -i /home/centos/FAAS/ansibleAutomation/hosts.ini 
```

## update app_config.json file before faas application deployment
```
   "env": "default",  # environment in which this application will be deployed or removed from
   "docker_artifactory_repo_url": "clna-prototype-docker.apro.nbnco.net.au", # docker artifactory repo
   "domain": "example.com",
   "action": "create", # update it with delete , if you want to uninstall knative application
  # "delete_list": [ping,getuptime],  #uncomment it only incase of delete
   "knative_version": "0.11.0", # determine & update knative version 
   "app_detail": [
    {
        "app_name": "ping",
        "app_docker_image": "checkpingconn",
        "app_url": "/ping", # Keep this same as you have defined in your application code
        "docker_tag": "v1",
        "description": "Knative application details",
        "package": [ flask ]
    },

#knative version can be determined by using below command on knative cluster & update values accordingly
#kubectl get namespace knative-serving -o 'go-template={{index .metadata.labels "serving.knative.dev/release"}}' | sed 's/v//'    
```
