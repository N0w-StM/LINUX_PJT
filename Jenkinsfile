pipeline {
    agent any

    environment {
        // Replace this with your SonarQube server details
        SONAR_URL = 'http://your-sonarqube-server:9000'
        SONAR_TOKEN = 'sqa_0efceaee176c2f4597209d9290c145bb473d8c9c' // Replace with your SonarQube token
        SONAR_PROJECT_KEY = 'SONAR-KEY' // Replace with your SonarQube project key
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out the source code...'
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') { // Jenkins needs a SonarQube server setup in "Manage Jenkins"
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=${SONAR_URL} \
                      -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Checking SonarQube Quality Gate...'
                script {
                    def qualityGate = waitForQualityGate()
                    if (qualityGate.status != 'OK') {
                        error "Quality Gate failed: ${qualityGate.status}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
