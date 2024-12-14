pipeline {
    agent any

    environment {
        SONAR_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = 'sqa_0efceaee176c2f4597209d9290c145bb473d8c9c'
        SONAR_PROJECT_KEY = 'SONAR-KEY'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SONAR-KEY') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=SONAR-KEY \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_URL \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
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
