pipeline {
    agent any

    environment {
        SONAR_URL = 'http://localhost:9000'
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
        stage('Sonar Check') {
            def Scanner = tool 'sonar';
            withSonarQubeEnv(){
                sh '${Scanner}/bin/sonar-scanner --version'
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
