import re
import requests
import orodja
import os


vzorec_stevila_vrstic = re.compile(
    r'(?P<stevilo><tr><th>Finančni podatki</th></tr>.*?(<tr><td.*?>.*?</td></tr>.*?)*?<tr><td.*?>Promet</td></tr>)',
    flags= re.DOTALL
    )

def izloci_podatke_st_vrstic(blok):
    podjetje = vzorec_podjetja.search(blok).groupdict()
    stevilo = vzorec_stevila_vrstic.search(blok)
    if stevilo:
        podjetje['stevilo'] = stevilo['stevilo']
    else:
        podjetje['stevilo'] = 0    
    return podjetje

def podjetja_na_strani_st_vrstic(datoteka):
    vsebina = orodja.vsebina_datoteke(datoteka)
    for blok in vzorec_podjetja.finditer(vsebina):
        yield izloci_podatke_st_vrstic(blok.group(0))

def stetje_vrstic(datoteka):
    podjetja1 = []
    for podjetje in podjetja_na_strani_st_vrstic(datoteka):
        podjetja1.append(podjetje)
    if 'stevilo' in podjetja1[0]:    
        kakec = podjetja1[0]['stevilo']
        kakec = str(kakec)
        stevilo_vrstic = 0
        for i in range(len(kakec)):
            if kakec[i] == '<' and kakec[i+1] == 't' and kakec[i+2] == 'r':
                stevilo_vrstic += 1
        return(stevilo_vrstic)



ime_dejavnosti = "Kmetijstvo in lov, gozdarstvo, ribištvo"
url ="https://www.stop-neplacniki.si/podjetja-v-ljubljani/"
vzorec = (
    r"besedilo: '.*?', link: '(?P<naslov>.*?)'"
    )

vzorec_podjetja = re.compile(
    r"<title>\n\n\s*(?P<ime>.*?)\n.*",
    flags=re.DOTALL
)



def nalozi_stran(url):
    print(f'Nalagam {url}...')
    odziv = requests.get(url)
    return odziv.text

naslovi = []

#vsebina = nalozi_stran(url)
#with open('podjetja.html', 'w') as f:
#    f.write(vsebina)

with open('podjetja.html') as f:
        vsebina = f.read()
        for zadetek in re.finditer(vzorec, vsebina):
            naslovi.append(zadetek.groupdict()) 

#os.remove('podjetja.html')


def izloci_podatke(blok, stevilo):
    podjetje = vzorec_podjetja.search(blok).groupdict()
    stevilovrstic = stevilo 
    vzorec_prometa = re.compile(
    r'<div class="Revenue">\s*<table.*?>.*?' + str('<tr>.*?</tr>'*(stevilovrstic - 1)) + r'<tr>(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?(<td.*?>.*?</td>)?<td.*?>(?P<promet>\d*?\.?\d*?\.?\d*?,?\d*?) &euro;</td></tr>',
    flags=re.DOTALL
    )
    promet = vzorec_prometa.search(blok)
    if promet:
        podjetje['promet'] = promet['promet']
    return podjetje     



def podjetja_na_strani():
    count = 0
    for naslov in naslovi:
        for a in naslov:
            url1 = (naslov[a])
            url = f"https://www.stop-neplacniki.si{url1}"
            count += 1
            ime_datoteke = f'{count}.html'
            orodja.shrani_spletno_stran(url, ime_datoteke)
            vsebina = orodja.vsebina_datoteke(ime_datoteke)
            st_vrstic = stetje_vrstic(ime_datoteke)
            print(st_vrstic)
            for blok in vzorec_podjetja.finditer(vsebina):
                yield izloci_podatke(blok.group(0), st_vrstic)
            os.remove(ime_datoteke)    

podjetja = []
for podjetje in podjetja_na_strani():
        podjetja.append(podjetje)


orodja.zapisi_csv(
    podjetja,
    ['ime', 'promet'], f'{ime_dejavnosti}.csv'
)
                      