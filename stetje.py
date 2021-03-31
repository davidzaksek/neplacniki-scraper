import re
import orodja

vzorec_stevila_vrstic = re.compile(
    r'(?P<stevilo><tr><th>Finančni podatki</th></tr>.*?(<tr><td.*?>.*?</td></tr>.*?)*?<tr><td.*?>Promet</td></tr>)',
    flags= re.DOTALL
    )

vzorec_podjetja = re.compile(
    r"<title>\n\n\s*(?P<ime>.*?)\n.*",
    flags=re.DOTALL
)

vzorec_test = re.compile(
    r'<th>Finančni podatki(?P<neki>.*?)</tr>',
    flags=re.DOTALL
)



def izloci_podatke(blok):
    podjetje = vzorec_podjetja.search(blok).groupdict()
    stevilo = vzorec_stevila_vrstic.search(blok)
    podjetje['stevilo'] = stevilo['stevilo']
    return podjetje


datoteka = "33.html"
def podjetja_na_strani():
    vsebina = orodja.vsebina_datoteke(datoteka)
    for blok in vzorec_podjetja.finditer(vsebina):
        yield izloci_podatke(blok.group(0))

podjetja = []
for podjetje in podjetja_na_strani():
    podjetja.append(podjetje)

kakec = podjetja[0]['stevilo']
stevilo_vrstic = 0

for i in range(len(kakec)):
    if kakec[i] == '<' and kakec[i+1] == 't' and kakec[i+2] == 'r':
        stevilo_vrstic += 1

