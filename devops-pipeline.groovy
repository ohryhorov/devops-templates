common = new com.mirantis.mk.Common()

/**
 * Creates env according to input params by DevOps tool
 * 
 * @param path Path to dos.py 
 * @param type Path to template having been created
 */
def createDevOpsEnv(path, tpl){
    echo "${path} ${tpl}"
    return sh(script:"""
    export ENV_NAME=${params.ENV_NAME} &&
    ${path} create-env ${tpl}
    """, returnStdout: true)
}

/**
 * Erases the env 
 *
 * @param path Path to dos.py  
 * @param env name of the ENV have to be deleted 
  */
def eraseDevOpsEnv(path, env){
    echo "${env} will be erased"
}

/**
 * Starts the env 
 * 
 * @param path Path to dos.py 
 * @param env name of the ENV have to be brought up 
  */
def startupDevOpsEnv(path, env){
    return sh(script:"""
    ${path} start ${env}
    """, returnStdout: true)
}

node {
    stage ('creating environmet') {
        if ("${params.ENV_NAME}" == '') {
            error("ENV_NAME have to be defined")
        }
        echo "${params.ENV_NAME} ${params.TEMPLATE}"
        if ("${params.TEMPLATE}" == 'Single') {
            echo "Single"
            tpl = '/var/fuel-devops-venv/tpl/clound-init-single.yaml'
        } else if ("${params.TEMPLATE}" == 'Multi') {
            echo "Multi"
        }
        try {
            createDevOpsEnv('/var/fuel-devops-venv/fuel-devops-venv/bin/dos.py',"${tpl}")
        } catch (err) {
            error("${err}")
//            eraseDevOpsEnv("${params.ENV_NAME}")   
        }
        try {
            startupDevOpsEnv('/var/fuel-devops-venv/fuel-devops-venv/bin/dos.py',"${params.ENV_NAME}")
        } catch (err) {
            error("${params.ENV_NAME} has not been managed to bring up")
        }        
    }
}

