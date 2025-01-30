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
                sh 'docker build -t mynginx -f Dockerfile.nginx .'
                 
            }
        }
        stage("Security Scan") {
            steps {
                sh "trivy fs --format json -o trivy-report.json ."
            }
            post {
                always {
                    // Archive the Trivy report
                    archiveArtifacts artifacts: 'trivy-report.json', onlyIfSuccessful: true
                }
            }
        }
        stage('Run') {
            steps {
                sh 'docker run -d --name flask-app --network jenkinsnetwork pyapp-image'
                sh 'docker run -d --name nginx --network jenkinsnetwork -p 80:80 mynginx:latest'
            }
        }
        stage('Simple Test') {
            steps {                 
                sh 'curl -f http://localhost:80 || echo "Nginx test failed"'
            }
        }
        stage('Execute Tests') {
         //   options {
        //allowFailure true
           // timeout(time: 30, unit: 'MINUTES')
            //disableConcurrentBuilds()
    //}
            steps {
                script {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE'/*failure/success/aborted*/){
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                python3 -m unittest discover -s tests .
                deactivate
                '''
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
