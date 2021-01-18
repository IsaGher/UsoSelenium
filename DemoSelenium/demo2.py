from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#Autor: Sara Garcia, Colaborador:Dennis Aguirre

#el driver se descarga previamente y se ubica en program files (x86)
Path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(Path)
driver.implicitly_wait(15)
driver.maximize_window()

#funcion para obtener los links de noticias y guardarlos en una lista
def llenadoDeListasLinks(l):
    i=0
    listaNoticias = []
    for li in l:
       listaNoticias.append(li.find_element_by_tag_name("a").get_attribute("href"))
       i+=1
       if(i>4):
            break
    return listaNoticias

driver.get("https://actualidad.rt.com/")

#se accesa al buscador de la pagina
search_button = driver.find_element_by_class_name("Search-button")
search_button.click()
search_field = driver.find_element_by_class_name("Input-root.Input-size_m.Input-fill_grey.Input-hasIconRight")
search_field.clear()

search_field.send_keys("Covid")
search_field.submit()

#lista para obtener todos los elementos de esta clase
list3 = driver.find_elements_by_class_name("Search-cardInfo")

#se obtienen los links de las noticias por medio del metodo anterior
rtLinks = llenadoDeListasLinks(list3)

driver.get(rtLinks[0])
rtNoticia = ""

#se extrae titulo y cuerpo de la primera noticia
#tomar en cuenta que la estructura de la pagina puede cambiar, y los nombres de las clases y los elementos o el id ya no pueden ser el mismo
texto = driver.find_element_by_class_name("HeadLine-root.HeadLine-type_2").text
#guardamos el titulo en una variable auxiliar para comparar después
titulo1 = texto
rtNoticia += "*"
rtNoticia += texto
rtNoticia += "*"
rtNoticia += "\n"

cuerpo = driver.find_element_by_class_name("Text-root.Text-type_5.ArticleView-text.ViewText-root ").find_elements_by_tag_name("p")
for c in cuerpo:
    rtNoticia += c.text

#funcion para enviar la noticia en WhatsApp
def envioNoticias (mensaje):
    search_field.send_keys(mensaje)
    search_button = driver.find_element_by_class_name("_2Ujuu")
    search_button.click()

#despues de phone= se pone el codigo de pais y el numero al que se enviara la noticia
driver.get("https://api.whatsapp.com/send?phone=")
search_button = driver.find_element_by_class_name("_whatsapp_www__block_action").find_element_by_tag_name("a").get_attribute("href")
driver.get(search_button)
driver.implicitly_wait(20)

search_field = driver.find_element_by_tag_name("footer").find_element_by_class_name("_1awRl.copyable-text.selectable-text")
search_field.clear()

encabezado = "*Noticia mas reciente sobre el Covid*"
envioNoticias(encabezado)
envioNoticias(rtNoticia)
aviso = "*Buscando Noticia nueva...*"
envioNoticias(aviso)

busqueda = 0
while (busqueda<3):
    #tiempo de espera en que estara verificando si cambio la noticia
    time.sleep(1800)
    second_driver = webdriver.Chrome(Path)
    second_driver.implicitly_wait(15)
    second_driver.maximize_window()
    second_driver.get("https://actualidad.rt.com/")

    search_button = second_driver.find_element_by_class_name("Search-button")
    search_button.click()
    search_field = second_driver.find_element_by_class_name("Input-root.Input-size_m.Input-fill_grey.Input-hasIconRight")
    search_field.clear()

    search_field.send_keys("Covid")
    search_field.submit()

    list3 = second_driver.find_elements_by_class_name("Search-cardInfo")

    rtLinks = llenadoDeListasLinks(list3)

    second_driver.get(rtLinks[0])
    rtNoticia = ""
    texto = second_driver.find_element_by_class_name("HeadLine-root.HeadLine-type_2").text

    #comparo el titulo de la noticia anterior con la que esta actualmente
    if (titulo1 == texto):
        second_driver.quit()
        print(driver.title)
        #despues de phone= se pone el codigo de pais y el numero al que se enviara la noticia
        driver.get("https://api.whatsapp.com/send?phone=")
        search_button = driver.find_element_by_class_name("_whatsapp_www__block_action").find_element_by_tag_name("a").get_attribute("href")
        driver.get(search_button)
        driver.implicitly_wait(20)

        search_field = driver.find_element_by_tag_name("footer").find_element_by_class_name("_1awRl.copyable-text.selectable-text")
        search_field.clear()
        aviso = "*No se ha encontrado Noticia mas reciente*"
        envioNoticias(aviso)
    else:
        titulo1 = texto
        rtNoticia += "*"
        rtNoticia += texto
        rtNoticia += "*"
        rtNoticia += "\n"

        cuerpo = second_driver.find_element_by_class_name("Text-root.Text-type_5.ArticleView-text.ViewText-root ").find_elements_by_tag_name("p")
        for c in cuerpo:
            rtNoticia += c.text

        second_driver.quit()
        print(driver.title)
        #despues de phone= se pone el codigo de pais y el numero al que se enviara la noticia
        driver.get("https://api.whatsapp.com/send?phone=")
        search_button = driver.find_element_by_class_name("_whatsapp_www__block_action").find_element_by_tag_name("a").get_attribute("href")
        driver.get(search_button)
        driver.implicitly_wait(20)

        search_field = driver.find_element_by_tag_name("footer").find_element_by_class_name("_1awRl.copyable-text.selectable-text")
        search_field.clear()
        aviso = "*Nueva noticia*"
        envioNoticias(aviso)
        envioNoticias(rtNoticia)

    busqueda +=1

button_exit = driver.find_elements_by_class_name("_2wfYK")
button_exit[2].click()

button_exit = driver.find_element_by_class_name("_1OwwW._3oTCZ")
button_exit.click()

driver.quit()