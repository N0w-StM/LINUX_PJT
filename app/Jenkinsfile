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

        stage('Install Dependencies') {
            steps {
                echo 'Installing Requirements'
                sh '''
                cd app
                pip install --upgrade pip
                pip install pylint
                pip install -r requirements.txt || true
                '''
            }
        }

        stage('Code Analysis with SonarQube') {
            steps {
                echo 'Running SonarQube code analysis...'
                withSonarQubeEnv('SONAR-KEY') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_URL \
                      -Dsonar.login=$SONAR_TOKEN \
                      -Dsonar.python.version=3 \
                      -Dsonar.sourceEncoding=UTF-8 \
                      -Dsonar.exclusions=**/__pycache__/**,**/venv/**,**/*.test.py
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Checking SonarQube quality gate results...'
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
