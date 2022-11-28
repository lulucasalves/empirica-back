import json
import os
import boto3
import uuid
import io
import csv

client = boto3.client('dynamodb')


def postItemHandler(event, context):
    if event["httpMethod"] != "POST":
        raise Exception(
            f"putItemHandler only accept POST method, you tried: {event.httpMethod}")

    body = json.loads(event["body"])
    name = body["bucket_name"]
    key = body["object_key"]

    obj = boto3.client('s3').get_object(
        Bucket=name, Key=key)

    data = io.StringIO(obj['Body'].read().decode('ISO-8859-1'))

    my_reader = csv.reader(data)

    columns = []
    num = 0

    def changeColumnName(current_name):
        if (current_name == 'Originador'):
            return 'ORIGINADOR'
        elif (current_name == 'Doc Originador'):
            return 'DOC_ORIGINADOR'
        elif (current_name == 'Cedente'):
            return 'CEDENTE'
        elif (current_name == 'Doc Cedente'):
            return 'DOC_CEDENTE'
        elif (current_name == 'CCB'):
            return 'CCB'
        elif (current_name == 'Id'):
            return 'ID_EXTERNO'
        elif (current_name == 'Cliente'):
            return 'CLIENTE'
        elif (current_name == 'CPF/CNPJ'):
            return 'CPF_CNPJ'
        elif (current_name == 'Endereço'):
            return 'ENDERECO'
        elif (current_name == 'Cidade'):
            return 'CIDADE'
        elif (current_name == 'Valor do Empréstimo'):
            return 'VALOR_DO_EMPRESTIMO'
        elif (current_name == 'Parcela R$'):
            return 'VALOR_PARCELA'
        elif (current_name == 'Total Parcelas'):
            return 'TOTAL_PARCELAS'
        elif (current_name == 'Parcela'):
            return 'PARCELA'
        elif (current_name == 'Data de Emissão'):
            return 'DATA_DE_EMISSAO'
        elif (current_name == 'Data de Vencimento'):
            return 'DATA_DE_VENCIMENTO'
        elif (current_name == 'Preço de Aquisição'):
            return 'PRECO_DE_AQUISICAO'
        elif (current_name == 'CEP' or current_name == 'UF'):
            return current_name
        else:
            return ''

    def formatCpf(current_row):
        return current_row.replace('.', '').replace('/', '').replace('-', '')

    def formatDate(current_row):
        day, month, year = current_row.split('/')
        return f'{year}-{month}-{day}'

    for row in my_reader:
        x = str(row).replace("'", '').replace(
            '[', '').replace(']', '').split(';')
        numberof = len(x)-1
        id = uuid.uuid4()

        for column in x:
            if (num == 0):
                columns.append(column)

        objectList = [{'ID_SESSAO': {"S": str(id)}}]

        for i in range(numberof):
            columnName = changeColumnName(columns[i])
            if (len(columnName) and num != 0):
                if (i == 1 or i == 7):
                    objectList.append({columnName: {"S": formatCpf(x[i])}})
                elif (i == 24 or i == 23):
                    objectList.append({columnName: {"S": formatDate(x[i])}})
                else:
                    objectList.append({columnName: {"S": x[i]}})

                objects = {'ID_SESSAO': {"S": str(id)}}

                for o in objectList:
                    objects.update(o)

                client.put_item(
                    TableName=os.environ["SAMPLE_TABLE"], Item=objects)
        num += 1

    response = {
        "statusCode": 200,
        "body": json.dumps({'message': 'success'})
    }

    return response
