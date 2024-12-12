pipeline {
    agent any

    environment {
        // Replace this with your SonarQube server details
        SONAR_URL = 'http://localhost:9000'
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
                withSonarQubeEnv('SONAR-KEY') { // Jenkins needs a SonarQube server setup in "Manage Jenkins"
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey='SONAR-KEY' \
                      -Dsonar.sources=. \
                      -Dsonar.host.url='http://localhost:9000' \
                      -Dsonar.login='sqa_0efceaee176c2f4597209d9290c145bb473d8c9c'
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
