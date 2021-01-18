from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

#primera pagina
driver.get("https://cnnespanol.cnn.com/")

#se accesa al buscador de la pagina
search_field = driver.find_element_by_name("s")
search_field.clear()

search_field.send_keys("Covid")
search_field.submit()

#lista para obtener todos los elementos de esta clase
list1 = driver.find_elements_by_class_name("news__title")

#se obtienen los links de las noticias por medio del metodo anterior
cnnLinks = llenadoDeListasLinks(list1)

driver.get(cnnLinks[0])
cnnNoticia = ""

#se extrae titulo y cuerpo de la primera noticia
texto = driver.find_element_by_class_name("news__title").text
cnnNoticia += texto
cnnNoticia += "\n"

texto = driver.find_element_by_class_name("news__excerpt").find_element_by_tag_name("p").text
cnnNoticia += texto
cnnNoticia += " "

buttonVideo = driver.find_element_by_class_name("pui_center-controls_big-play-toggle.sc-iAyFgw.cnBpEa")
buttonVideo.click()
texto = driver.find_element_by_id("player-fave-video1").find_elements_by_tag_name("video")
cnnNoticia += texto[1].get_attribute("src")

#para el resto de paginas es el mismo proceso
#tomar en cuenta que la estructura de la pagina puede cambiar, y los nombres de las clases y los elementos o el id ya no pueden ser el mismo
#segunda pagina
driver.get("https://es.euronews.com/noticias/internacional")

search_field = driver.find_element_by_class_name("c-search-form__input.awesomplete")
search_field.clear()

search_field.send_keys("Covid")
search_button = driver.find_element_by_class_name("c-search-form__button")
search_button.click()

list2 = driver.find_elements_by_class_name("m-object__title.qa-article-title")

euLinks = llenadoDeListasLinks(list2)

driver.get(euLinks[1])
euNoticia = ""

texto = driver.find_element_by_class_name("c-article-title.u-padding-x-large-10").text
euNoticia += texto
euNoticia += "\n"

cuerpo = driver.find_element_by_class_name("c-article-content.js-article-content.article__content").find_elements_by_tag_name("p")
for c in cuerpo:
    euNoticia += c.text

#tercera pagina
driver.get("https://actualidad.rt.com/")

search_button = driver.find_element_by_class_name("Search-button")
search_button.click()
search_field = driver.find_element_by_class_name("Input-root.Input-size_m.Input-fill_grey.Input-hasIconRight")
search_field.clear()

search_field.send_keys("Covid")
search_field.submit()

list3 = driver.find_elements_by_class_name("Search-cardInfo")

rtLinks = llenadoDeListasLinks(list3)

driver.get(rtLinks[0])
rtNoticia = ""

texto = driver.find_element_by_class_name("HeadLine-root.HeadLine-type_2").text
rtNoticia += texto
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
driver.implicitly_wait(15)

search_field = driver.find_element_by_tag_name("footer").find_element_by_class_name("_1awRl.copyable-text.selectable-text")
search_field.clear()

encabezado = "_Busqueda \"Covid\"_\n*Primera noticia de CNN*"
envioNoticias(encabezado)
envioNoticias(cnnNoticia)

encabezado = "*Primera noticia de EuroNews*"
envioNoticias(encabezado)
envioNoticias(euNoticia)

encabezado = "*Primera noticia de RT en español*"
envioNoticias(encabezado)
envioNoticias(rtNoticia)

button_exit = driver.find_elements_by_class_name("_2wfYK")
button_exit[2].click()

button_exit = driver.find_element_by_class_name("_1OwwW._3oTCZ")
button_exit.click()

driver.quit()