

from contextlib import suppress #supressão de erros
import googlemaps #api do google
import credenciais_google #azquivo pra ocultar API KEY
import time #Biblioteca nativa: utilizada pra freezar o tempo

#coordenadas  -12.9704,-38.5124

#entradas
localizacao = str(input('Digite as coordenadas:'))
raio = int(input('Digite o raio:'))
palavrachave = str(input('Digite o estabelecimento desejado:'))
i = 0
k = 0
rep = "Y"

#Registro de pesquisa
with open('banco.txt', 'a') as save:
    print('*'*60, file=save)
    print('Pesquisa sobre: ', palavrachave, '/   Localização: ', localizacao, '/    Raio: ', raio, file=save)
    print('*'*60, file=save)

#autenticação api places
gmaps = googlemaps.Client(key=credenciais_google.google_api_token)

#request dados da pesquisa
resultados = gmaps.places_nearby(location=localizacao, radius=raio, open_now=False, keyword=palavrachave)


#sistemas pra varer arquivo jason solicitado pela api
for c in range(0, 20):
    with suppress(Exception): #ignorar excessões (caso o resultado não tenha telefone e etc
        i += 1
        place_id = resultados['results'][c]['place_id']
        name = resultados['results'][c]['name']
        address = resultados['results'][c]['vicinity']
        number = gmaps.place(place_id=place_id, fields=['formatted_phone_number'])
        website = gmaps.place(place_id=place_id, fields=['website'])
        rating = str(resultados['results'][c]['rating'])

        #metodo para escrever os dados no arquivo de texto

        with open("banco.txt", "a") as stream:
            print('='*60, file=stream)
            print("resultado nº", i, file=stream )
            print('Name: ' + name, file=stream)
            print('Address: ' + address, file=stream)
            print('Phone Number: ', number['result']['formatted_phone_number'], file=stream)
            print('Website: ', website['result']['website'], file=stream)
            print('Rating: ' + rating, file=stream)
            print('='*60, file=stream)

        #metodo para imprimir dados obtidos na tela

        print('=' * 60)
        print("resultado nº", i)
        print('Name: ' + name)
        print('Address: ' + address)
        print('Phone Number: ', number['result']['formatted_phone_number'])
        print('Website: ', website['result']['website'])
        print('Rating: ' + rating)
        print('=' * 60)

#Repetição para solicitar proximas paginas de resultados
while rep == 'Y':
    rep = input(str('Deseja Solicitar mais 20 resultados? [Y/N]'))[0].strip().upper()
    if rep == 'N':
        pass
    else:
        time.sleep(3)
        resultados = gmaps.places_nearby(page_token=resultados['next_page_token'])
        for c in range(0, 20):
            with suppress(Exception):  #ignorar excessões (caso o resultado não tenha telefone e etc
                i += 1
                place_id = resultados['results'][c]['place_id']
                name = resultados['results'][c]['name']
                address = resultados['results'][c]['vicinity']
                number = gmaps.place(place_id=place_id, fields=['formatted_phone_number'])
                website = gmaps.place(place_id=place_id, fields=['website'])
                rating = str(resultados['results'][c]['rating'])

                # metodo para escrever os dados no arquivo de texto

                with open("banco.txt", "a") as stream:
                    print('=' * 60, file=stream)
                    print("resultado nº", i, file=stream)
                    print('Name: ' + name, file=stream)
                    print('Address: ' + address, file=stream)
                    print('Phone Number: ', number['result']['formatted_phone_number'], file=stream)
                    print('Website: ', website['result']['website'], file=stream)
                    print('Rating: ' + rating, file=stream)
                    print('=' * 60, file=stream)

                # metodo para imprimir dados obtidos na tela

                print('=' * 60)
                print("resultado nº", i)
                print('Name: ' + name)
                print('Address: ' + address)
                print('Phone Number: ', number['result']['formatted_phone_number'])
                print('Website: ', website['result']['website'])
                print('Rating: ' + rating)
                print('=' * 60)
else:
    pass
#Mensagem final informando sobre arquivo de armazenamento
print('TODOS OS DADOS FORAM SALVOS NO ARQUIVO BANCO.TXT')


