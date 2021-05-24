
#       
# -------- PIILOSANAN RAKENTAMINEN ----------        
# -------------------------------------------

import math
import pygame
import random
import re
import pickle
import sys


# ----- UUSI KOODI ALKAA ------

class Ruudukko():
    def __init__(self,xx,yy):
        self.x = xx
        self.y = yy
        self.kirjain = ''
        self.musta = False
        self.kursori = ''
        self.numero = ''

    def kirjainruutu(self,k):
        self.kirjain = k
        self.musta = False
        self.kursori = ''
        self.numero = ''

    def mustaruutu(self):
        self.musta = True
        self.kirjain = ''
        self.kursori = ''
        self.numero = ''

    def kursoriruutu(self, suunta):
        self.kursori = suunta
        self.musta = False
        self.kirjain = ''
        self.numero = ''

    def numeroruutu(self, nro):
        self.numero = nro
        self.kursori = ''
        self.musta = False
        self.kirjain = ''

    def tyhjaruutu(self):
        self.numero = ''
        self.kursori = ''
        self.musta = False
        self.kirjain = ''

    # Funktio: piirretään ruutujen sisältö ruudukkoon
    def ruutupiirto(self):
        blank(xyk(self.x,self.y)[0],xyk(self.x,self.y)[1]) # Ruutu valkoiseksi
        if self.kirjain:
            text = tyyli(24,'Verdana').render(self.kirjain,True,BLACK)   
            screen.blit(text, [xyk(self.x,self.y)[0] + 7,xyk(self.x,self.y)[1] + 2])
        elif self.musta:
            pygame.draw.rect(screen,BLACK,[xyk(self.x,self.y)[0]+3,xyk(self.x,self.y)[1]+3,25,25])
        elif self.kursori == 'oikea':
            kur_oik(xyk(self.x,self.y)[0]+8,xyk(self.x,self.y)[1]+1)
        elif self.kursori == 'alas':
            kur_alas(xyk(self.x,self.y)[0]+8,xyk(self.x,self.y)[1]+1)
        elif self.numero:
            # Piirretään nrot        
            nro = tyyli(10,'Verdana').render(self.numero,True,BLACK)   
            screen.blit(nro, [xyk(self.x,self.y)[0] + 1,xyk(self.x,self.y)[1]])

    # Funktio, joka palauttaa ruudun tilan
    def ruutucheck(self):
        if self.kirjain != "":
            return self.kirjain
        elif self.musta:
            return 'musta'
        elif self.kursori == 'oikea' or self.kursori == 'alas':
            return self.kursori
        elif self.numero != '':
            return 'numero'
        else:
            return ''
            
        
# Ruudukon piirto -funktio
def ruudukko(lkm):
    rx = 30
    ry = 120
    pygame.draw.rect(screen,BLACK,[rx-4,ry-4,lkm*30+8,lkm*30+8],4) # Ruudukon kehys
    for i in range(lkm - 1):
        pygame.draw.line(screen,BLACK,[rx+30+i*30,ry],[rx+30+i*30,ry+lkm*30],1)
        pygame.draw.line(screen,BLACK,[rx,ry+30+i*30],[rx+lkm*30,ry+30+i*30],1)

# Ruudun tyhjennys
def blank(x,y):
    pygame.draw.rect(screen,WHITE,[x+1,y+1,29,29])

# Piirtokoordinaatit
def xyk(x,y): # Ruudukon vasen ylänurkka aina pisteessä (30,90)
    return [x*30,90 + y*30]

# Funktiot: kursori oikealle tai alas
def kur_oik(x,y):
    pygame.draw.rect(screen,GREY,[x-5,y+3,8,21])
    pygame.draw.polygon(screen,GREY,[[x+2,y],[x+18,y+13],[x+2,y+26]],0)

def kur_alas(x,y):
    pygame.draw.rect(screen,GREY,[x-3,y+1,21,8])
    pygame.draw.polygon(screen,GREY,[[x-6,y+8],[x+7,y+24],[x+20,y+8]],0)

# Funktiot: siirtävät kursorin paikkaa, jos se on laitettu ruudukkoon,
# ei siirrä mustaan
# eikä ruudukosta ulos
def kur_siirto_edel(ruudussa, ind, lkm, x, y):
    kur_pois()
    if ruudussa == 'oikea':
        if ind-1 >= 0 and (x-1) > 0:
            if ruudut[ind-1].musta == False:
                 return [-1,0]
    elif ruudussa == 'alas':
        if ind-lkm >= 0:
            if ruudut[ind-lkm].musta == False:
                 return [0,-1]
    return [0,0]

def ekavapaaruutu(lkm, kur):
    nn = 0
    while (ruudut[nn].kirjain or ruudut[nn].musta) and nn < len(ruudut)-1:
        nn += 1
        if nn == len(ruudut):
            print('Ei vapaita ruutuja')
            return [0,0]
    ruudut[nn].kursoriruutu(kur)
    return[nn%lkm + 1,nn//lkm + 1]

def kur_siirto_seur(ruudussa, ind, lkm, x, y):
    kur_pois()
    if ind == len(ruudut)-1:
        print('Olit viimeisessä ruudussa')
        return [0,0]
    elif ruudussa == 'oikea' and ind+1 < len(ruudut)-1:
        if not (ruudut[ind+1].musta or ruudut[ind+1].kirjain):
            return [x+1,y]
        elif (x < lkm-1):
            if (ruudut[ind+1].kirjain and not(ruudut[ind+2].kirjain)): 
                return [x+2,y]
        else:
            return ekavapaaruutu(lkm,'oikea')
    elif ruudussa == 'alas' and ind+lkm < len(ruudut)-1:
        if not (ruudut[ind+lkm].musta or ruudut[ind+lkm].kirjain):
            return [x,y+1]
        elif (y < lkm-1):
            if (ruudut[ind+lkm].kirjain and not(ruudut[ind+2*lkm].kirjain)):
                return [x,y+2]
        else:
            return ekavapaaruutu(lkm,'alas')    
    return ekavapaaruutu(lkm,'oikea')

# Poistetaan kursori sieltä missä se on 
def kur_pois():
    for r in range (0,len(ruudut)-1):
        if ruudut[r].kursori:
            ruudut[r].tyhjaruutu()
            blank(xyk(ruutu.x,ruutu.y)[0],xyk(ruutu.x,ruutu.y)[1])
            

# Fontin ja kirjaintyypin asetus
def tyyli(fnt,kir):
    return pygame.font.SysFont(kir, fnt, False, False)

# Ehdotusten max 5 kpl kirjoitus ruudulle
def teksti(lkm,t):
    # pyyhitään edelliset sanat pois
    pygame.draw.rect(screen,WHITE,[lkm*30+60,110,lkm*30,10*25])
    # listataan max 5 (satunnaista) sanaa
    count = 0
    for s in t:
        sana = s
        if len(t) > 5:
            sana = t[random.randint(0,len(t))-1]
        rivi = tyyli(18,'Courier').render(sana, True, BLACK)
        screen.blit(rivi, [lkm*30+60, 115 + count*20])
        count += 1
        if count == 5:
            break

# Merkki autosanan riville/sarakkeelle
def as_m(vir_x,vir_y, color):
    pygame.draw.circle(screen,color,[xyk(vir_x,vir_y)[0]+13,xyk(vir_x,vir_y)[1]+13],4)
    
# Automaattisten sanojen haku ja listaus
def autosana(vir_x, vir_y, kur, xy_lkm, suomensanat):
    # Katsotaan ensin mitä rivillä/sarakkeessa jo on
    kir_lkm = 0
    kirjaimet = {}
    autosanat = []
    if kur == 'oikea' or vir_x == 0:
        seur = 1
        ind = (vir_y-1)*xy_lkm + vir_x
    elif kur == 'alas' or vir_y == 0:
        seur = xy_lkm
        ind = vir_y*xy_lkm + vir_x-1
    
    while not (vir_y > xy_lkm or vir_x >= xy_lkm or ind > xy_lkm*xy_lkm - 1): # kunnes vastaan
        # tulee ruudukon reuna
        if ruudut[ind].kirjain: # jos ruudussa kirjain, tallentaan kirjaimet-hakulistaan
            kirjaimet[kir_lkm] = ruudut[ind].kirjain
        elif ruudut[ind].musta:
            break
        if seur == 1:
            vir_x += 1
        else: 
            vir_y += 1
        kir_lkm += 1
        ind += seur

    if kir_lkm <= 1:
        return autosanat
    for sana in suomensanat:
        # jos sanan pituus on sama kuin ruutujen määrä, katsotaan, osuuko kirjaimet
        if len(sana) == kir_lkm: 
            osuu = True
            for k in kirjaimet:
                if not (sana[k].upper() == kirjaimet[k]):
                    osuu = False
                    break
            if osuu:
                autosanat.append(sana)
    return autosanat
    
    
# ---------------------------------------------------------------------------
# Pääohjelma 
def main(ruudut, xy_lkm):

    # Luodaan tarpeelliset listat
    merkit = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
                "R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7",
                "8","9",'musta','oikea','alas','pois','sanaehdotus']
    keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,
        pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,
        pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,
        pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,
        pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,
        pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3, pygame.K_4,pygame.K_5,
        pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_RSHIFT,
        pygame.K_RIGHT,pygame.K_DOWN,pygame.K_BACKSPACE,pygame.K_SPACE]


    # Sanojen pituudet
    sanapituus = []

    '''# Vihjelista
    vihjeet = ['Vaakasuoraan:','1.Phil, onko täällä sitä paljesoitinta? Ei oo, ei tuu, eikä tilata. (11)',\
    '2.SAMOS... (5)','3.Mis on se kaikista söpöin? (5)'\
    ,'4.SIIAT... (5)'\
    ,'5.Tässäkin on yksi paikka leikattu ja liimattu. (3)','6.TATU...(4)'\
    ,'7.AHKERA...(6)','8.Se mikä pienenä pyörii ja hyörii, noin parhain. (13)'\
    ,'9.Jano soimaa, kun tekee kaikenlaista taitavasti. (10)','','Pystysuoraan:'\
    ,'1.F-9 ote:"Rapia ois kunto, jos sitä käyttäis." (12)'\
    ,'6.Ota jatsi, kommunistimiehiä tai elämän vastoinkäymisiä. (8)'\
    ,'10.Äläpä Mel sekoile, järjestät vain uudestaan kotisi. (8)'\
    ,'11.Nelosasia in, yksinolo out. (11)','12.Mi kuiski mun korvaani säveliä. (8)'\
    ,'13.SELUS... (5)','14.NAMIT... (5)'\
    ,'16.Akin napinaa:"Taas väärään suuntaan! Ja Saarikolle ja Haavistolle'\
    ,'ihan sama." (7)','17.Onpa sporttinen ja monipuolinen se Luihu Ysirele. (12)']'''

    suomensanat = []
    # Avataan Suomen sanalista ja tallennetaan haravoidut listaan
    flista = open('kotus_sanalista_v1.xml','r')
    for rivi in flista:
        sana = re.search('s>([a-z]+)<', rivi)
        if sana:
            s = sana.group(1)
            suomensanat.append(s)
    flista.close()

    # Piirretään ruudukko
    ruudukko(xy_lkm)
    pygame.display.flip()

    # Lähtötilanteen alkuarvot
    done = False
    x = 1
    y = 1
    vir_x = 0
    vir_y = 0
    ruutuind = 0
    
    # Loopataan, kunnes käyttäjä klikkaa sulje-painiketta
    while not done:
        
        for event in pygame.event.get():# käyttäjä teki jonkin tapahtuman
       
            if event.type == pygame.QUIT: # jos klikattiin close
                done = True # tällä asetuksella looppi lopetetaan

    # Hiiren klikkaus alkaa -------------------------------------------------------
            # Onko hiirtä klikattu
            if event.type == pygame.MOUSEBUTTONDOWN:

                as_m(vir_x,vir_y,WHITE)
                kur_pois()
                
                # Kursorin sijainti
                pos = pygame.mouse.get_pos()
                if (pos[0] > 30 and pos[0] < 30+xy_lkm*30) and (pos[1] > 120 and pos[1] < 120+xy_lkm*30):
                    x = vir_x = (pos[0]//30)  # ruudun x-numero
                    y = vir_y = ((pos[1]-90)//30)  # ruudun y-numero
                    ruutuind = (y-1)*xy_lkm+x-1 # ruudun uusi indeksi
                    
                    
                # jos klikkaus ruudukon vas. tai yläpuolella
                elif (pos[0] <= 30 and pos[1] > 120 and pos[1] < 120+xy_lkm*30):
                    vir_x = 0 # virtuaaliruudun x-numero
                    vir_y = ((pos[1]-90)//30) # virtuaaliruudun y-numero
                    as_m(vir_x,vir_y, GREY)

                elif (pos[1] <= 120 and pos[0] > 30 and pos[0] < 30+xy_lkm*30):
                    vir_x = (pos[0]//30)
                    vir_y = 0
                    as_m(vir_x,vir_y, GREY)
                
                # Minkälaisen ruudun päällä klikkaus
                if not (vir_x == 0 or vir_y == 0):
                    # Skandit
                    for ruutu in ruudut:
                        if ruutu.x == x and ruutu.y == y:
                            ruudussa = ruutu.ruutucheck()
                            if ruudussa == 'A':
                                ruutu.kirjainruutu('Ä')
                            elif ruudussa == 'Ä':
                                ruutu.kirjainruutu('Å')
                            elif ruudussa == "O":
                                ruutu.kirjainruutu('Ö')
                            # jos ruudukon ulkopuolelle klikkaus
                            elif vir_x != 0 and vir_y != 0:
                                blank(xyk(x,y)[0],xyk(x,y)[1])
                                ruutu.kursoriruutu('oikea') # default-suunta oikealle

    # Hiiren klikkaus loppuu --- Näppäin alas alkaa --------------------
    
            if event.type == pygame.KEYDOWN:
                ekey = event.key # muuttujaan näppäintapahtuma

                if ekey in keys:
                    print(x,y)
                    indeksi = keys.index(ekey) # mikä indeksi merkit-listassa
                    nappain = merkit[indeksi]
                    ruudussa = ruudut[ruutuind].ruutucheck()
                        
                    if indeksi < 26 and ruutuind < len(ruudut)-1: # kirjain
                        ruudut[ruutuind].kirjainruutu(nappain)
                        siirto = kur_siirto_seur(ruudussa, ruutuind, xy_lkm, x, y)
                        x = siirto[0]
                        y = siirto[1]
                        ruutuind = (y-1)*xy_lkm+x-1
                        ruudut[ruutuind].kursoriruutu(ruudussa)
                    elif indeksi < 36 and len(ruudut[ruutuind].numero) < 2: # numerot 99 asti
                        edNro = ''
                        if ruudut[ruutuind].numero != '':
                            edNro = ruudut[ruutuind].numero
                        ruudut[ruutuind].numeroruutu(edNro+nappain)
                    elif indeksi == 36: # SHIFT (oikean puolen) musta
                        ruudut[ruutuind].mustaruutu()
                        x = ekavapaaruutu(xy_lkm, ruudussa)[0]
                        y = ekavapaaruutu(xy_lkm, ruudussa)[1]
                        ruutuind = (y-1)*xy_lkm+x-1
                        ruudut[ruutuind].kursoriruutu(ruudussa)
                    elif indeksi < 39: # (kursori) nuoli oikea tai alas
                        ruudut[ruutuind].kursoriruutu(nappain)
                    elif indeksi == 39: # backspace
                        siirto = kur_siirto_edel(ruudussa, ruutuind, xy_lkm, x, y)
                        x += siirto[0]
                        y += siirto[1]
                        ruutuind = (y-1)*xy_lkm+x-1
                        ruudut[ruutuind].kursoriruutu(ruudussa)
                    elif indeksi == 40: # SPACE -> sanaehdotukset näkyviin
                        if vir_x == 0 or vir_y == 0:
                            as_m(vir_x,vir_y,WHITE)
                        ehdotukset = autosana(vir_x, vir_y, ruudussa, xy_lkm, suomensanat)
                        teksti(xy_lkm,ehdotukset)
                          
                        
                        
    # Tähän asti näppäinten käyttö ----------------------------------
                
        # Ruutujen päivitys
        c = 1
        for ruutu in ruudut:
            if (len(ruudut)-c): #jätetään viimeinen piirtämättä, ettei printtaa ruudukon kulmaan
                ruutu.ruutupiirto()
            c += 1
           
        # Näytön päivitys 
        pygame.display.flip()
     
        # 10 framea sekunnissa.
        clock.tick(10)

    #        
    # Pääohjelman määrittely LOPPUU -----------------------------------------------
    # -----------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# OHJELMA ALKAA 
#----------------------------------------------------------------------------------

# Luodaa lista ruudukon objekteille
ruudut = []

# Kysytään ruudukon koko ja piirretään ruudukko:
kysymys = input("Montako ruutua x-y-suunnissa? ")
xy_lkm = int(kysymys)

# Jos vastaus 0, niin kysytään tiedoston nimi ja jatketaan sen sisällöllä
# muutoin piirretään uusi ruudukko
if kysymys == '0':
    tiedosto = input("Mikä tiedosto? ")
    file = open('%s.dat'%(tiedosto),'rb')
    ruudut = pickle.load(file)
    file.close()
    xy_lkm = int((len(ruudut))**0.5)

else: # Luodaan ruutu-objektit ja laitetaan ruudut-listaan
    for ry in range(1,xy_lkm + 1):
        for rx in range(1,xy_lkm + 1):
            ruutu = Ruudukko(rx,ry)
            ruudut.append(ruutu)
    # kursori vasempaan ylänurkkaruutuun
    ruudut[0].kursori = 'oikea'
    ruudut[0].missa = 'tässä'
    ruutu = Ruudukko(0,0) # alkusijainti ja loppusijainti
    ruudut.append(ruutu)

BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
GREY =  ( 215, 215, 215)

pygame.init()
size = (xy_lkm*70, xy_lkm*60)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Piilosanan rakentaminen")

# Näytön päivityksen asetus
clock = pygame.time.Clock()

# Näyttö valkoiseksi
screen.fill(WHITE)
pygame.display.flip()

# Pääfunktion käynnistys
if __name__ == "__main__":
    main(ruudut, xy_lkm)

# ------ LOPETUS -----------

# Grafiikkanäytön sulkeminen
pygame.quit()

# Kirjoitetaan lopuksi lista tiedostoon (pickle)
tall = input("Millä numerolla tallennetaan? ")
file = open('ruudut%s.dat'%(tall),'wb')
pickle.dump(ruudut,file)
file.close()

