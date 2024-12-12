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
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SONAR-KEY') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=SONAR-KEY \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.token=sqp_c3bad8f21d9f1f4cf65632dd43d710aac3d82bfc
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
