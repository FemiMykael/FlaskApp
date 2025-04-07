pipeline {
    agent { label 'Jenkins' }

    environment {
        JENKINS_WORKSPACE = "${env.WORKSPACE}"
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'dev', url: 'https://github.com/FemiMykael/FlaskApp.git'
            }
        }

        stage('Package App') {
            steps {
                sh '''
                    tar -czf app.tar.gz flaskapp
                    sha256sum app.tar.gz > hash.txt
                    mkdir -p artifacts
                    mv app.tar.gz hash.txt artifacts/
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'artifacts/*'
            }
        }

        stage('Run Ansible') {
            steps {
                sh '''
                    ansible-playbook -i inventory.ini playbook.yml -e "jenkins_workspace=${JENKINS_WORKSPACE}"
                '''
            }
        }
    }

    /*
    post {
        success {
            mail to: 'femimykael@yahoo.com',
                subject: ':white_check_mark: Secure Flask Deploy Success',
                body: 'Artifact verified & app deployed via HTTPS!'
        }
        failure {
            mail to: 'femimykael@yahoo.com',
                subject: ':x: Secure Flask Deploy FAILED',
                body: 'Check Jenkins logs for details.'
        }
    }
    */
}
