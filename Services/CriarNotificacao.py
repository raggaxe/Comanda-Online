from Services.playersAPI import *

def criar_Notificacao(tipo,emissor_auth,receptor_auth,squadName):
    dataInsert = {
        'tipo': tipo,
        'emissor': emissor_auth,
        'receptor':receptor_auth,
        'squadName': squadName
    }
    CheckuserRedis(auth=receptor_auth).CreateNotify(dataInsert,tipo)
