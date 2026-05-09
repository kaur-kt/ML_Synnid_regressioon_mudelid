# Sünniandmestiku analüüs ja sünnikaalu prognoosiva mudeli treenimine andmestikul

## Sissejuhatus

Antud töö on koostatud reaalsete andmete baasil andmetöötluse, -analüüsi ja masinõppe eesmärgil TalTech kursuse "Masinõppe rakendamine inseneridele, 2026 kevad" lõpuprojektina.

## Andmestik

Töös kasutatud sünniandmestik koosneb ligikaudu 4+ aasta andmetest, kust on eemaldatud kõik isikuandmed, ehk tegemist on anonüümitud andmega ja mis on Tervise Arengu Instituudi sisemiseks või volitatud kasutajatele kasutamiseks.

## Eesmärk

Eesmärgiks on uurida ja teostada järgmised toimingud:

- Andmestik korrastada ja puhastada
- Analüüsida andmeid ja leida võimalikud seosed
- Luua ja treenida andmestikul põhinev mudel, mis ennustab valitud tunnuste baasil sünnikaalu, ja võimalusel ka sünnipikkust
- Luua lisaks üks või mitu alternatiivse meetodiga masinõppe mudelit ning võrrelda mudelid omavahel
- Hüpotees: suitsetamine mõjutab keskmiselt sünnikaalu

## Andmestiku struktuur

Andmestruktuur koosneb järgmistest elementidest/väljadest:

- ema perekonnaseis (kood) – kategooriline
- ema perekonnaseis – kategooriline
- suitsetamine (kood) – kategooriline
- suitsetamine – kategooriline
- raseduskestus nädalad – numbriline
- raseduskestus päevad – numbriline
- ema vanus – numbriline
- isa vanus – numbriline
- lapse sugu – kategooriline
- sündinud laste arv – numbriline
- sünnikaal – numbriline
- sünnipikkus – numbriline
- sünniviis (kood) – kategooriline
- sünniviis – kategooriline

## Andmestik.
Andmestik sisaldab algselt ja puhastamata kujul kokku 48559 kirjet, puhastatud andmestik sisaldab 47262 kirjet.

## Ema andmed
Keskmine vanus on 31,2 ja mediaan 31 aastat. Standardhälve ligi 5,36 aastat, enamik emasid jäävad vahemikku 26 kuni 36 aastat. Kvartiilidest, 25% on 28 ja 75% 35 aastat.
## Isa andmed
Keskmine vanus on 33,9 ja mediaan 33 aastat. Standardhälve ligi 6,3 aastat, enamik isasid jäävad vahemikku 28 kuni 40 aastat. Kvartiilidest, 25% on 30 ja 75% 38 aastat. Äärmustest, isa vanuse miinimum on 14 ja maksimum on 79! aastat.
## Laste andmed
Keskmine sünnikaal on 3529 ja mediaan 3564, viimane on veidi suurem keskmisest. Standardhälve on 554,8, seega sünnikaal varieerub üsna suurelt, jäädes ligikaudu vahemikku 3000 – 4100. Kvartiilidest 25% on 3234 ja 75% on 3880.
Suhe on ligikaudu 51,3% poisse ja 48,7% tüdrukuid (ligikaudu 105 poissi 100 tüdruku kohta).
Keskmine sünnipikkus on 50,87 ja mediaan 51. Standardhälve on 2,70, jaotus on üsna normaalne, jäädes ligikaudu 51 ümber, ehk varieeruvus on väike. Kvartiilidest 25% on 50 ja 75% 52.

## Sündide andmed
Keskmine raseduskestus on 277 ja mediaan 279 päeva. Standardhälve on 12,56, jaotus on normaalse lähedane, kuid veidi vasakule kaldu, millele viitab keskmisest suurem mediaan. Kvartiilidest 25% on 273 ja 75% on 285, ehk poolte raseduskestus jääb siia, suhteliselt kitsasse 12 päeva, vahemikku. Äärmustest, miinimum on 154 ja maksimum on 304.

## Seoste uurimine.
- Numbrilised väärtuste paarikaupa võrdlusgraafik.

- Tunnuste korrelatsioonid.

## Sünnistatistika.
Sündide sooline jaotus:
Sünnitusviiside ja sünnikaalude suhted, mediaanväärtustega:

## Sünnikaalu sõltuvus suitsetamisest. Hüpoteesi tõestus.
Sünnikaalu sõltuvus suitsetamisest tuleb andmestiku analüüsides kenasti välja. Kui võrrelda sünnikaalu mediaanväärtusi mittesuitsetajate ja suitsetajate puhul, siis mittesuitsetajatel on see 3570g ja suitsetajatel 3438g. Vahe 132g.
Kui võrrelda keskmiseid sünnikaale, siis erinevus on veelgi suurem, keskmine sünnikaal mittesuitsetajatel on 3539g ja suitsetajatel 3387g. Vahe 152g. Seega hüpotees sai kinnituse.
<p align="center">
  <img src="images/Võrdlus, sünnikaalu sõltuvus suitsetamisest, mediaanid.png" width="45%" />
  <img src="images/Võrdlus, sünnikaalu sõltuvus suitsetamisest, keskmised.png" width="45%" />
</p>
## Masinõpe ja mudelite treenimine 
Andmestikuga tutvumise järel langes otsus esmalt Random Forest(suvamets) kasuks. Hinnates Random Forestiga saavutatud tulemusi tekkis plaan treenida alternatiivne mudel, kasutades Gradient Boosting’ut(gradiendi võimendus), võrrelda mõlemat mudelit ja leida antud juhul parim.
Treeningul kasutatavad tunnused.
- numbrilised:
-- Raseduskestus päevades,
-- Ema vanus,
-- Isa vanus

- kategoorilised:
-- Ema perekonnaseis,
-- Suitsetamine kokku
-- Lapse sugu

- sihttunnus:
-- Sünnikaal
-- sünnipikkus

Treenimisel kasutame valdavalt pipeline’i, kuna see:
- Võimaldab käsitleda puuduvaid väärtusi automaatselt, imputeerime
- Võimaldab mugavamalt kategooriaid õigesti kodeerida, nt rakendada One-Hot-Encoder
- Võimaldab mugavamalt numbrilisi väärtusi skaleerida, rakendame vastavat skaalerit
- Töötab uute andmetega otse
- Aitab vältida andmelekkeid
Treenitud mudelite testimiseks on kasutatud kahte profiili, mis on kõiges muus identsed, välja arvatud lapse sugu, ja mis kujutavad keskmiste lähedasi väärtuseid. Täpsemalt, profiilis kasutataud tunnused testimisel: Ema vanus 30a, Isa vanus 32a, Ema perekonnaseis – abielus, ema mittesuitsetaja. Test arvutab prognoosijoone alates (raseduskestus) 175 päevast kuni 300 päevani, 5 päevase hüppega, ja arvutab välja neile päevadele vastavad sünnikaalud.

## Random Forest meetod
<p align="center">
  <img src="images/Võrdlus, mudel vs pärisandmed, tüdruk, random forest.png" width="55%" />
  <img src="images/Võrdlus, mudel vs pärisandmed, poiss, random forest.png" width="55%" />
</p>

## Gradient Boosting meetod
<p align="center">
  <img src="images/Võrdlus, mudel vs pärisandmed, tüdruk, gradient boosting.png" width="55%" />
  <img src="images/Võrdlus, mudel vs pärisandmed, poiss, gradient boost.png" width="55%" />
</p>

## Random Forest ja Gradient Boosting võrdlus
## Mudelite võrdluse tulemus ja hinnang.
Loodud ja treenitud mudelite võrdluses selgub, et Gradient Boosting’ul põhinev mudel on siin  selgelt paremate omadustega ja minu eelistus langeb selle kasuks.
## Random Forest tulemuste parendamine/tuunimine.
Hea kogemus ja õppemoment. Proovisin Random Forest tulemust parandada ja kasutada tuunimist, ehk leida parim parameetrite konfiguratsioon. Toimingu tulemuseks on esmapilgul justkui parem RMSE nii sünnikaalu, kui pikkuse osas.
Pilt muutub, kui me võrdleme mudeli prognoosimisvõimet reaalsete andmetega võrreldes.
<p align="center">
  <img src="images/Võrdlus, mudel vs pärisandmed, tüdruk, tuunitud random forest attention.png" width="70%">
  <br>
  <em>Graafikul tumepunasega märgitud alas mudel „hallutsineerib“ (sünnikaal, tüdruk)</em>
</p>

Siit joonistub välja selge probleem sünnikaalu ennustamisel lühemate rasedu##kestvuste juures. Kui pikemate raseduskestuste juures mudel üldistab paremini , kui tuunimata mudel, siis probleem on lühemate raseduskestuste korral. Graafikul tumepunasega märgitud alas mudel „hallutsioneerib“ ja sellist mudelit reaalsuses kasutada ei saa.
## Kokkuvõte.
Andmestik sai puhastatud ja korralikult analüüsitud. Loodud sai kahel erineval meetodil põhinev masinõppe mudel, Random Forest ja Gradient Boosting meetodil vastavalt. Random Forest mudeli tuunimise tulemusel RMSE tunnused justkui paranesid, kuid mudel ei ennustanud sünnikaalu osaliselt õigesti ja seda mudelit kasutada ei saa. Plaan koostada ka kolmas mudel, mis põhineks närvivõrgul jäi ajapuudusel pooleli. Viimase puhul tekkis omapärane probleem sellega, et soovitud Tensorflow paketti ei õnnestunud, teatud tehnilistel põhjustel, kasutada ja PyTorch’i baasil implementatsioon võttis minu viimase vähesema kogemuse tõttu, oodatust rohkem aega. 





