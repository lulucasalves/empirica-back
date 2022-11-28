import json
import os
import boto3
import uuid
import io
import csv

def changeColumnName(headerName, cell):
    if (headerName == 'Originador'):
        return {'headerName': 'ORIGINADOR', 'cell': cell, 'cellType': 'S'}

    elif (headerName == 'Doc Originador'):
        return {'headerName': 'DOC_ORIGINADOR', 'cell': formatDocument(cell), 'cellType': 'N'}

    elif (headerName == 'Cedente'):
        return {'headerName': 'CEDENTE', 'cell': cell, 'cellType': 'S'}

    elif (headerName == 'Doc Cedente'):
        return {'headerName': 'DOC_CEDENTE', 'cell': formatDocument(cell), 'cellType': 'S'}

    elif (headerName == 'CCB'):
        return {'headerName': 'CCB', 'cell': cell, 'cellType': 'N'}

    elif (headerName == 'Id'):
        return {'headerName': 'ID_EXTERNO', 'cell': cell, 'cellType': 'N'}

    elif (headerName == 'Cliente'):
        return {'headerName': 'CLIENTE', 'cell': cell, 'cellType': 'S'}

    elif (headerName == 'CPF/CNPJ'):
        return {'headerName': 'CPF_CNPJ', 'cell': formatDocument(cell), 'cellType': 'S'}

    elif (headerName == 'Endereço'):
        return {'headerName': 'ENDERECO', 'cell': cell, 'cellType': 'S'}

    elif (headerName == 'Cidade'):
        return {'headerName': 'CIDADE', 'cell': cell, 'cellType': 'S'}

    elif (headerName == 'Valor do Empréstimo'):
        return {'headerName': 'VALOR_DO_EMPRESTIMO', 'cell': formatFloat(cell), 'cellType': 'N'}

    elif (headerName == 'Parcela R$'):
        return {'headerName': 'VALOR_PARCELA', 'cell': formatFloat(cell), 'cellType': 'N'}

    elif (headerName == 'Total Parcelas'):
        return {'headerName': 'TOTAL_PARCELAS', 'cell': cell, 'cellType': 'N'}

    elif (headerName == 'Parcela'):
        return {'headerName': 'PARCELA', 'cell': cell, 'cellType': 'N'}

    elif (headerName == 'Data de Emissão'):
        return {'headerName': 'DATA_DE_EMISSAO', 'cell': formatDate(cell), 'cellType': 'S'}

    elif (headerName == 'Data de Vencimento'):
        return {'headerName': 'DATA_DE_VENCIMENTO', 'cell': formatDate(cell), 'cellType': 'S'}

    elif (headerName == 'Preço de Aquisição'):
        return {'headerName': 'PRECO_DE_AQUISICAO', 'cell': formatFloat(cell), 'cellType': 'N'}

    elif (headerName == 'CEP' or headerName == 'UF'):
        return {'headerName': headerName, 'cell': cell, 'cellType': 'S'}

    else:
        return {'headerName': '', 'cell': '', 'cellType': ''}


def formatDocument(currentRow):
    return currentRow.replace('.', '').replace('/', '').replace('-', '')


def formatDate(currentRow):
    day, month, year = currentRow.split('/')
    return f'{year}-{month}-{day}'


def formatFloat(currentRow):
    return currentRow.replace(' ', '').replace(',', '.')

client = boto3.client('dynamodb')

def postItemHandler(event, context):
    if event["httpMethod"] != "POST":
        raise Exception(
            f"putItemHandler only accept POST method, you tried: {event.httpMethod}")

    body = json.loads(event["body"])
    name = body["bucket_name"]
    key = body["object_key"]

    s3Object = boto3.client('s3').get_object(
        Bucket=name, Key=key)

    s3Data = io.StringIO(s3Object['Body'].read().decode('ISO-8859-1'))

    s3DataReader = csv.reader(s3Data)

    headersColumns = []
    currentNumber = 0

    for row in s3DataReader:
        rows = str(row).replace("'", '').replace(
            '[', '').replace(']', '').split(';')
        rowsLength = len(rows)-1
        id = uuid.uuid4()

        for cell in rows:
            if (currentNumber == 0):
                headersColumns.append(cell)

        objectsList = [{'ID_SESSAO': {"S": str(id)}}]

        for i in range(rowsLength):
            if currentNumber != 0:
                updatedData = changeColumnName(headersColumns[i], rows[i])

                if (len(updatedData['headerName'])):
                    objectsList.append(
                        {updatedData['headerName']: {updatedData['cellType']: updatedData['cell']}})

                    putItemObject = {'ID_SESSAO': {"S": str(id)}}

                    for item in objectsList:
                        putItemObject.update(item)

                    client.put_item(
                        TableName=os.environ["SAMPLE_TABLE"], Item=putItemObject)

        currentNumber += 1

    response = {
        "statusCode": 200,
        "body": json.dumps({'message': 'success'})
    }

    return response
