#!groovy
pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                echo 'Cleaning up existing Containers and Images'
                sh 'docker rm -f $(docker ps -aq) || true'
                sh 'docker rmi -f $(docker images -q) || true'
                
            }
        }
        stage('Build') {
            steps {
                sh 'docker network create jenkinsnetwork || true'
                sh 'docker build -t pyapp-image .'
                sh 'docker build -t mynginx -f Dockerfile.nginx'
                 
            }
        }
        stage('Run') {
            steps {
                sh 'docker run -d --name pythonapp --network jenkinsnetwork pyapp-image'
                sh 'docker run -d --name nginx --network jenkinsnetwork -p 80:80 mynginx:latest'
            }
        }
        stage('Test') {
            steps {
                sh 'curl -f http://localhost:5500 || echo "Test failed"' 
                sh 'curl -f http://localhost:80 || echo "Nginx test failed"'
            }
        }
    }
}

