# Założenia projektu *Planner*
Projekt *planner* zakłada utworzenie discord bota, który będzie błyskawicznie zwracał ważne informację bez konieczności wchodzenia na stronę planu i doszukiwania się ich. 
Aktualnie planowane funkcjonalności (mogą ulec zmianie w dalszych etapach):
* Bot wysyła plan lekcji dla wybranej klasy w konkretny dzień
* Bot wysyła wszystkie przedmioty obowiązujące daną klasę
* Bot wysyła wolne gabinety w podanym dniu
* Bot wysyła plan lekcji dla wybranego nauczyciela na dany dzień bazując na imieniu i nazwisku, lub skrócie (potencjalnie cały tydzień)


# Narzędzia użyte w projekcie
* [PyCharm Community Edition 2024.1.1](https://www.jetbrains.com/pycharm/download/other.html)
* [Insomnia API (wersja 7.1.1)](https://insomnia.rest/download)
* [Python 3.12.0](https://www.python.org/downloads/)

# Instrukcja pozyskiwania informacji o planie
Na stronie [planu lekcji](https://zsel.edupage.org/timetable/) należy:
1. Wcisnąć `ctrl+shift+c` i wejść do zakładki *Network*, a następnie do *Fetch/XHR*
![wynik punktu pierwszego](https://media.discordapp.net/attachments/809756120125538325/1247286969176821900/discordguide-1.png?ex=6668b482&is=66676302&hm=611577a169635a7e304691609cbb2007608ea3b1b2ddd641b5ece2714ead3b36&=&format=webp&quality=lossless&width=687&height=256)
2. Odświeżyć stronę. Powinny pojawić się następujące odpowiedzi:
![wynik punktu drugiego](https://media.discordapp.net/attachments/809756120125538325/1247287332328050708/image.png?ex=665f7a59&is=665e28d9&hm=177dede9437d75d21f79554b6466d1dff60443cc46432b1719157b8a8c6dc61f&=&format=webp&quality=lossless&width=1236&height=522)
3. Wybrać odpowiedź z końcówką `regularttGetData`
![wynik punktu trzeciego](https://media.discordapp.net/attachments/809756120125538325/1247287642832502885/image.png?ex=665f7aa3&is=665e2923&hm=d600e745ed94f157c0889e2196675e25f3799551b3f9f2070631a2a949fbd0d1&=&format=webp&quality=lossless&width=1222&height=628)
Treść pliku json powinna wyświetlać się obok (patrz zdjęcie z punktu 3). Klikając na odpowiedź prawym i wybierając opcję `copy -> copy as cURL` otrzymujemy link na bazie którego można wygenerować kod requesta przez Insomnia API

# Nawigacja po pliku json
Przedstawione zostaną tylko fragmenty przydatne dla projektu. Liczby podane w nawiasach kwadratowych to numery tabeli w pliku json:
* tabela[11] `classrooms` zawiera nazwy klas i id budynku
* tabela[12] `classes` zawiera informację o klasach (nazwa klasy, id wychowawcy)
* tabela[13] `subjects` zawiera nazwy przedmiotów
* tabela[14] `teachers` zawiera id nauczycieli i skrót imienia i nazwiska
* tabela[15] 'groups' zawiera informację o grupach. Każdy element w tej tabeli jest przypisany do klasy, więc nazwy grup mogą się powtarzać
* tabela[18] `lessons` zawiera informacje o przedmiocie, klasie (id), nauczycielu (id), ilości godzin w tygodniu i długości godzin
* tabela[20] `cards` zawiera m.in. id lekcji, godzinę lekcyjną, dni podane jako 5-cyfrowa liczba (pozycja 1 oznacza dzień np. 01000 == wtorek), oraz id gabinetu
* tabela[22] `classroomsupervisions` zawiera informację o dyżurach dla gabinetów (id)

  
kolejność wczytywania planu lessons -> cards -> output


# Obsługa bot
* Skrypt powinien być uruchamiany przez jedno urządzenie (Prawdopodobne użycie hostingu w późniejszych etapach).
* Bot aktualnie ma dostęp do odczytywania i odpowiadania na komendy na każdym kanale tekstowym
* Bot używa systemu komend z prefixem `/`
* Podawane dane nie wymagają używania polskich znaków, oraz nie ma znaczenia także wielkość liter
* Zwracane przez bota dane są prezentowane w formię bloku kodu wysyłanego na czacie, z którego wysłano komendę
* Przy nieobsłużonym wyjątku bot przestanie działać. Należy uruchomić skrypt ponownie
* Token bota powinien znajdować się w pliku `.env`. W przypadku tworzenia nowego bota używającego tego kodu należy wkleić unikatowy token do tego pliku. Token nie jest zawarty w projekcie - trzeba go wygenerować samemu
* Utworzenie nowego bota należy zrobić przez stronę [developers](https://discord.com/developers/applications) discorda.

# Klasy wykorzystywane przez Bota
## classPlanner
**classPlanner** odpowiada za interpretację danych związanych z klasami pozyskanych z jsona z klasy *dataReader* i wysłanie ich w odpowiednim formacie. Klasa jest następnie wywoływana przez *main* w odpowiedniej komendzie

![Diagram UML klasy classPlanner](https://media.discordapp.net/attachments/809756120125538325/1247290242411790356/PP11IiOm48NtFKMM_S5Ue0kfLWH1YjW3X6aoIZHDoinqKSIxEzOQmMOHoBplumtfM81adMFb8Z2R_NwAa1AI-QYCdiOacB4rB7Iy2Tc3G6jyS7BCF6n_YBKX1R6sBkPL0IuxyOhIVrSz-FfYckjYwlmEjXiUrdb2EcMFo9oJMlmJnS3ocuthz8PE1gqyfSMyppGkwC9BSDhp3tE48DXdZxSnk_Tdv4KLh858bz-vij1drM7o-d5V.png?ex=6668b78f&is=6667660f&hm=9307fce4635c30eb7e1798c5e74e6823f6df68d6eaf04dae0eab9aac2022222d&=&format=webp&quality=lossless&width=420&height=287)

W klasie występują podane metody:
### getClassId
Jako dane wejściowe podane są przez użytkownika dane: nazwa klasy i dzień. Metoda najpierw odpowiednio formatuje odpowiedź, a następnie przeszukuje tabelę[12] i zwraca id (string).

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247295081564733633/FP0nSiCW44LxJl4xf2j8HTogoQJFk5XBQtib30oiHcFrEKJkuuE58Obe-0pl3uyzPQMawyEP6aptaVRdBMZOo0jZT9JpEpsuDztWPPp9oKvb-xqP9ioq1CGrwnEZlBvklKaScTG0tQ2SAXpJpZkKBknUtx2rozds1f0hckCLp9mL6-JJ-dAqvxSMUcUFHcbf3SggWb5orIkSJFQCAVpxz1Mw9AQb9FQJNF-4iDt5CPhIQqsNMDVaZrRvVOZcLFWoYXy0.png?ex=6668bc11&is=66676a91&hm=788fe4412925bca3caf884e5a984715b630a23520c18a6b6834d9a47e48cb1cc&=&format=webp&quality=lossless&width=337&height=662)

### getDayAsNumber
Format dnia zastosowany w jsonie składa się z 5 cyfr, z których jedna to 1 (dzień tygodnia), a reszta to zera. Metoda przekształca odpowiedź użytkownika do odpowiedniego formatu i zwraca jako string (jeżeli podano nieprawidłowy dzień zwracany jest pusty string).

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247296442343751720/RT512iCW40NGlQSON2MxPDiIo5Ma6Yf9DPW9eLaMUefUfxbNftKpCdMX7vp_4EmND0dNswH-GVa1Aclkq7MWvnYyixitnyEDkWQykW0Lch5M0AVaS4q1TDlGqcVbfiL1HOtlBMSsZ4dscT2qMG0eZ58vNYbQ8nNk49GT8PNMPTzCGlacuH6OFI4AS_RlvpzIegHcLB9YcWy6wmV5Cq_vpFk2SLOzPVhM3m00.png?ex=665f82d5&is=665e3155&hm=7ec0a7fe332d983e43c1ee3f9843471dd84aa3ed0d5d9577584a6e89b1d25443&=&format=webp&quality=lossless&width=1025&height=568)

### getLessonsIds
Metoda pozyskuje id lekcji przypisanych do podanej przez użytkownika klasy i zwraca je w formie listy. Metoda wykorzystuje metodę *getClassId* do pozyskania id klasy

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247299936005914785/JP0nJiGm44Lxd-9tIQwG5Am4JJew2hI5MS-oapLsv9aeIafkmNtWNeoyAq5bo_zzFSySH7tHvIEwUd7zcFWq-SYxjmEHH78QWs3orunv4QK9aKMtmVKlsvf_FdrYmZlfO_GYOsWxIvxBliqiDLgtnDS58UDq8mPNQ2Ql3kX7fL9DSzbfX_etYjzVQ6vYQGQ3-8psNiL4ebZ1hqrzuI3DyQ63NYYXLN_jZ0VwfnogspWEpT7aVwCCXb0AVBv_0-k58w4rldDz8LrA-a-BvjaTh65R-WK0.png?ex=665f8616&is=665e3496&hm=ec14cd98c3bef2c2bbe52d9ed8ff23f8707a3af6c8868a1c5bc8b9def61ccb55&=&format=webp&quality=lossless&width=328&height=662)

### getSubjectNames
Metoda wykorzystuje metodę *getLessonsIds* do pozyskania id lekcji i wyszukuje w tabeli[13] nazwy przedmiotów, a następnie zwraca je jako lista

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247298674825101393/VP0_JiCm5CPtd-BRabuXKKK7bae8iJ4W1hTvfKuSE_9xLfICt8BxmBqmYLMWGcI9xU_Fxzax5XqazbOj2rKzJgF_UDNE45v8xeZPEzutN6vgLJs4UHeCB-euETD5D1vsCILFSkoTERRQcbcd7pWUMZhAlUw9qUhEOuWirC8QbgbMWGRIee1gBnIMo11ccY7wGFRz3SNQpKMTJEQ4qZmLfYcUqH8Bnc_qpGPo9eTITBTHID-b6_YdFq-u0e0LqcR8Tel4ovQlasjABh_rpV8aAUTqJodP-5ztho_UGo3TvHsvnfn-p8hnR2oXJ5MfFCj_I5KWYS5T4LZye7Of57lx2G00.png?ex=665f84e9&is=665e3369&hm=56b536f9e63340fd8944e887e4710e043ece9dc8f046dd302363c58343e6dd3c&=&format=webp&quality=lossless&width=290&height=661)

### getLessonsForSpecificDay
Metoda wykorzystuje wyniki poprzednich metod do skonstruowania i zwrócenia listy zawierającej wszystkie nazwy lekcji w odpowiedniej kolejności (uwzględniając okienka) dla podanego dnia.

![Diagram aktywności](https://cdn-0.plantuml.com/plantuml/png/xLbHJzim47xFhx3wqdWLZFPfeke44c93GapQU8lGv3PkQzecbUq8AEA_pxcKrEaLmgcBqD3y57pE-RiltzaVwecnGjjiCG_W8JYUffasRC2E-iNpfJBM_MdaV7muaVPx7Wwv2vfiU2j7zaeifF4M_FAcOLqi7hpmcNWuDLVPOYWrH2SwpPONiP_Xstfg4y-JeHMR7URIc3If9hc4ERDE4sYvbC86p8tZ2okr6DqAjjGhkIhUqDB4megehTitKJiUgjFHAC-WVqgJprWndCDJxoYFkwM_TNhd9lgGKurPgFBv1pV51WEM5osIcBd90fsANK0bhCJAcPtAX8LMp7Z0riE32MDlkDql66uv0BQF4A3VHcru1FY9pHSifLQfc-FiAmDz8F3-A2M4tkx0bDiWphImAasAaCbZ1wnR1IUJM8stc65tKpMNB4oKP3C7MOvui5dxyffdZPZpL5zFvHb8Cch_c2cPp59NxAUYhdz7AQYWQ9ljWwxBpyQjyF6vZNSjUUAinJhCR-OeBBS-L4aixyEgI3ZdhXXVG_LOUb1hQqru2vNqrh90ABtwmdhFXRq5MZz0cdkFRZosSh64euqvgjXdrY9sgtk6urB5-MP7e2AOs2qY8kjEJfsSTXOzRWxb21utIjc6m6-URbfzlE4upPBObNakvaRYE6OUHYDDYGSmlIgh1vuzCe3hbT_3PKFlP9bGNFCosrtiFQW8Qbdv2eDIxr-HLS75YqSNX4EK84cjMuRrcchtQb9P3tTEbzSJkxkHEeFgqRPzibMWyngcYArIegZD2j_0rTnjb-pLxa1WX8oynLnVzt3ZuY7dfhXgcy7GhS603cqqy95phJDPaxJcCAxf96HkGC6apzM0YEcC3RKKitv0JrJlsKYvW5VuUeX40coq1H4cl4k-ZybQWAoUzjRYGw-GBXLyeMYHJ6JugXld_M2FDkwmMPrBWqLlCw1L_rcLEAQFv8FshV6lUIAAFoBQYUPzKws7EbGcLXDbGrx-O-b5ERWep6-NxhNeHBs_1_iWVkozhpLw-r9z6ispeTtehD4helatefVR7nl1rz4T2ztlxU_zwCQ9NXlTKD7te1ijN38P1hr4Gav2BYpz_-RgmvghFQw6vg-2vez-fFVcZtRShyrsC-HexhS4BMscyOVk1yQco-349SX_J_i3)

### createCodeBlockResponse
Metoda formuje dane przekazane z jakiejkolwiek listy jako `discord code block` (string) w formie kolumny (możliwe przeniesienie metody do osobnej klasy w przyszłości).
Mieści się także w innych klasach, lecz nie ma między nimi zbyt wielkiej różnicy.

## classroomPlanner
**classroomPlanner** odpowiada za interpretację danych związanych z gabinetami pozyskanych z jsona z klasy *dataReader* i wysłanie ich w odpowiednim formacie. Klasa jest następnie wywoływana przez *main* w odpowiedniej komendzie.

![Diagram UML klasy classPlanner](https://images-ext-1.discordapp.net/external/E8kcn_6FDg7rJtDsrrhUM_zMdlj7AxVT9yIXjqzxk9A/https/cdn-0.plantuml.com/plantuml/png/RO_DIiKm48NtUOfPzgA-G5UNUrS54N4h4iRCK8FvaPd9eeZlheqjM70JCjzt3icSrL2ivUHSIAWA_PHQipucB8K5FXt07GWheU4858DrGhYC4Clly5QRZA0cVNfjCL4iyqvkmFjOeda_xAtRhTAlX_of5sQsoqOd6axTxEAw_d4YNV5zL7l-SIy7kIxmW9d_YGHXDBvMuakguVs9zQCMvG55SFaJtfxySkxCXLfEtm00?format=webp&width=457&height=267)

W klasie występują podane metody:
### getBuildingId
Podana przez użytkownika w konstruktorze nazwa budynku jest konwertowana do ID (do wyboru możliwe: główny (main), gimnazjum)

![Diagram aktywności](https://images-ext-1.discordapp.net/external/n1EhjzzgDTRwrAL-GMJFCce_uFm9XMvyDF9In1VbZDk/https/cdn-0.plantuml.com/plantuml/png/VP2nJeSm4CRtUufB9t0mqH52mkRcucPSshHWeRsIqeP0c5ny83PNvBr4msBoX_7kTx_lag_i0_SXMWCmFsqVwpBGECFV4hANplD1Rb_edPnuWoBAaTgOWwumwPMfxaNKHcggiIYGrOVFq4JnHZSEZBl2bcjYAOPtHPW4tgQ0cBqEVbs-Fv7TFR0SbEdLoNDjYKzDj1S9ZzS9tWd3p_L3neIq-aUU7QcTaTJLtfph0Cfz-Etq1m00?format=webp&width=911&height=351)

### getClassroomIds
Metoda tworzy listę, do której dodawane są ID gabinetów wykorzystywanych w podanym przez użytkownika dniu i godzinie.

![Diagram aktywności](https://images-ext-1.discordapp.net/external/IFgvuUCeoiyOOYhh7g-Ujq0hf8Uz2q3YwBu-0vbeLw0/https/cdn-0.plantuml.com/plantuml/png/NL0zZl8m5EnzYYd35K93yKcVwEXMelF6XhpWF4TvZY97LAjTxHau1qSWt6jD2D9k6akU6S-FDn9q6xhQANN-V_-uNNkEPpM1AjzhOYgghe8Z2UC5XTCYhVVrriXQzIKvYsmRR9iaZKTFjfL15oMCvbYKAv0Wwscy5BQQsVZY593l_7i21x1-s3SSPz6iMIk03iZUdc2ZfQiiZ8TXqY0SlHc8umgXj8miwDF35SZ_UQChaB4Sue5EElWMeXsbjzEKk5W2M2SM6PET7NQ-flidWkMvqYHYGmULpccvUbJxxOFAIa3JIR2BIlc-Rs_NyJkHKpYDNqSCh4_flzVgJ_PBkcZuZ9RW6wKswTBLxWS0?format=webp&width=647&height=628)

### getClassroomNames
Metoda tworzy listę, do której dodawane są nazwy klas nieznajdujące się w liście z metody *getClassroomIds*, ale zgodne z poprzednimi kryteriami. Zwracana jest lista z gabinetami nie użytkowanymi w danym dniu o danej godzinie.

![Diagram aktywności](https://images-ext-1.discordapp.net/external/CHhiEFSD1Mu8hbsSWSGyHNn9vmwwGPt0MflR_Bs8pi8/https/cdn-0.plantuml.com/plantuml/png/TL4nRiCm3Dpr2ex95vmbGu72Iv6bIz15iPIQjamPfWn1HgQYGD-GTsJj5kTVPGmNBU3MWmVUKNV7stBGNUWRfzJfyVPslKHA9pKDLRRNI5XKVGKEEOndA9ncxhnlddHZUQEovo5nhIj0Ooca8zOw-0uElKbKz__X2LWxtAXOehEmoeFjHABr4D5sFEYY1ACf5UKQa64LSJmNjfhHz8qfW6pd3p8SWFJTNajf9isSZN3mA0g_rITn8BIovUpjCu7nFy5omo-4aF-L1rhDVMM5BnDq1karDsi8fILO1LsB9Vco1syaCUaXZkT9J1OMbmEmZYMy-9ZNThx1spi4IyiGbWmUbVodaodXifVMgcKX-zXTB-F70k3WMwMsyiIzwoy0?format=webp&width=645&height=662)


# Dodatkowe informacje
Instrukcja, podobnie jak cały program, jest nadal w procesie budowy i nie jest finalną wersją. W razie konieczności treść instrukcji będzie aktualizowana.

# Autorzy
Krzysztof Solarczyk, Szymon Rozwoda - klasa 4TP
