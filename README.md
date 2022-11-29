
# Projeto Empirica Backend

Este projeto foi um desafio proposto pela empresa Empirica, no qual tem o objetivo de fazer um post na api em que indica qual o s3 bucket e a chave do arquivo no qual será indicado para inserir todos os dados dentro de um banco de dados.

Para executar o projeto é necessário instalar a CLI do Serverless Amazon Service (SAM)
Pode se adiquirir neste link https://docs.aws.amazon.com/pt_br/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

Logo após a instalação é necessário já ter uma conta na AWS e assim poderá executar os seguintes comandos:

`sam build`

`sam deploy --guided`

Nesse caso ele irá fazer o deploy da aplicação dentro da sua conta AWS e assim poderá ver todo o processo funcionando observando as lambdas, dynamodb e o bucket s3.

