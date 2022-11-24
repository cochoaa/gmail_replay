import datetime

class MailScript():
    def __init__(self,fecha: datetime, msgid, subject, sender, area, solicitante, dependencia, motivo, script):
        self.fecha = fecha
        self.msgid = msgid
        self.subject = subject
        self.sender = sender
        self.area = area
        self.solicitante = solicitante
        self.dependencia = dependencia
        self.motivo = motivo
        self.script = script

    def __repr__(self):
        return f"MailScript(\n" \
               f"fecha={self.fecha!r},\n" \
               f"msgid={self.msgid!r}, \n" \
               f"subject={self.subject!r}, \n" \
               f"sender={self.sender!r}, \n" \
               f"area={self.area!r}, \n" \
               f"solicitante={self.solicitante!r}, \n" \
               f"dependencia={self.dependencia!r}, \n" \
               f"motivo={self.motivo!r}, \n" \
               f"script={self.script!r}) \n" \
               f")"

if __name__ == '__main__':
    mail=MailScript('id','Fwd: SOLICITUD DE EJECUCIÓN DE SCRIPT - PROYECTO QUIPUCAMAYOC- ANULACIÓN DE EXPEDIENTE DE OS',
                    'helpdesk.quipucamayoc@unmsm.edu.pe','HD','Diana Tolentino','PROYECTO QUIPUCAMAYOC','Anulacion de exp de OC',
                    '''SELECT * FROM  bytsscom_bytsig.contrato where id_contrato in ('119403','119415','118924');

SELECT * FROM  bytsscom_bytsig.reg_adquisicion where id_reg_adquisicion in ('90303','90314','89948');


SELECT * FROM  bytsscom_bytsig.memo_requerimiento where id_memo_requerimiento in ('317392','317394','309815');

SELECT * FROM  bytsscom_bytsig.memo_requerimiento_item where id_memo_requerimiento in ('317392','317394','309815');


UPDATE bytsscom_bytsig.contrato set est_cont = 'X' where id_contrato in ('119403','119415','118924');

UPDATE bytsscom_bytsig.reg_adquisicion set esta_reg_adq = 3 where id_reg_adquisicion in ('90303','90314','89948');

UPDATE bytsscom_bytsig.memo_requerimiento set esta_requ = 'X' where id_memo_requerimiento in ('317392','317394','309815');

UPDATE bytsscom_bytsig.memo_requerimiento_item set estado_memo_item='X' where id_memo_requerimiento in ('317392','317394','309815');''')
    print(mail)