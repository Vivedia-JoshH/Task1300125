#!groovy
pipeline {
    agent any

    stages  {
        stage('Cleanup'){
            steps{
                echo 'Cleaning up existing Containers and Images'
                sh docker rm -f -qa $(docker ps -a)
                sh docker rmi $(docker images)
                sh docker ps -a
                sh docker images
               
            }
        }
        stage('Build'){
            steps{
                sh docker build -t pyapp-image .
                sh docker network create jenkinsnetwork
                
            }
        }
        stage('Run'){
            steps{
                sh docker run -d --name pythonapp --network jenkinsnetwork pyapp-image
                sh docker run -d --name nginx --network jenkinsnetwork -p 80:80 -v /$(pwd)/nginx.conf:/etc/nginx/nginx.conf nginx:latest
            }
        }
        stage('Test'){
            steps{
                sh curl localhost
                sh curl localhost:5500
            }
        }
    }
}
