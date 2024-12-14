pipeline {
    agent any

    environment {
        SONAR_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = 'sqa_7379f9bca1669323bdcec5b722ff87079b18b61d'
        SONAR_PROJECT_KEY = 'SONAR-KEY'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Run in Docker Container') {
            steps {
                echo '[+] Installing Requirements ....'
                sh '''
                    cd app
                    python3 -m venv ./venv
                    source ./venv/bin/activate
                    pip install -r requirements.txt
                    echo 'installed successfully!'
                "
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SONAR-KEY') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=$SONAR_URL \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
