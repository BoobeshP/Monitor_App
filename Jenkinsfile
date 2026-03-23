pipeline {
    agent any

    environment {
        VENV = "venv"
        BUILD_BRANCH = "unknown"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    BUILD_BRANCH = sh(
                        script: "git rev-parse --abbrev-ref HEAD",
                        returnStdout: true
                    ).trim()
                }
                echo "🔹 Building branch: ${BUILD_BRANCH}"
            }
        }

        stage('Install OS Dependencies') {
            steps {
                sh '''
                sudo apt update
                sudo apt install -y python3.10-venv python3-pip
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV}
                . ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Branch Specific Validation') {
            steps {
                sh '''
                echo "Running branch-specific checks..."

                if [ "${BUILD_BRANCH}" = "feature_Monitor" ]; then
                    echo "✅ feature_Monitor branch detected"
                else
                    echo "✅ main branch detected – skipping feature checks"
                fi
                '''
            }
        }

        stage('Package & Archive') {
            steps {
                sh '''
                tar -czf monitoring-dashboard-${BUILD_BRANCH}.tar.gz app.py templates requirements.txt
                ls -l monitoring-dashboard-${BUILD_BRANCH}.tar.gz
                '''
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
