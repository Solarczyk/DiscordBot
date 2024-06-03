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
![wynik punktu pierwszego](https://media.discordapp.net/attachments/809756120125538325/1247286969176821900/discordguide-1.png?ex=665f7a02&is=665e2882&hm=8e25f11dbaccff4d9e43ab695f3c6d85a37356d8bc6347739aa56bd42b52773d&=&format=webp&quality=lossless&width=1440&height=535)
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


# Obsługa bota
* Skrypt powinien być uruchamiany przez jedno urządzenie (Prawdopodobne użycie hostingu w późniejszych etapach).
* Bot aktualnie ma dostęp do odczytywania i odpowiadania na komendy na każdym kanale tekstowym
* Bot używa systemu komend z prefixem `/`
* Podawane dane nie wymagają używania polskich znaków, oraz nie ma znaczenia także wielkość liter
* Zwracane przez bota dane są prezentowane w formię bloku kodu wysyłanego na czacie, z którego wysłano komendę
* Przy nieobsłużonym wyjątku bot przestanie działać. Należy uruchomić skrypt ponownie

# Klasy wykorzystywane przez Bota
## classPlanner
**classPlanner** odpowiada za interpretację danych pozyskanych z jsona z klasy *dataReader* i wysłanie ich w odpowiednim formacie. Klasa jest następnie wywoływana przez *main* w odpowiedniej komendzie

![Diagram UML klasy classPlanner](https://media.discordapp.net/attachments/809756120125538325/1247290242411790356/PP11IiOm48NtFKMM_S5Ue0kfLWH1YjW3X6aoIZHDoinqKSIxEzOQmMOHoBplumtfM81adMFb8Z2R_NwAa1AI-QYCdiOacB4rB7Iy2Tc3G6jyS7BCF6n_YBKX1R6sBkPL0IuxyOhIVrSz-FfYckjYwlmEjXiUrdb2EcMFo9oJMlmJnS3ocuthz8PE1gqyfSMyppGkwC9BSDhp3tE48DXdZxSnk_Tdv4KLh858bz-vij1drM7o-d5V.png?ex=665f7d0f&is=665e2b8f&hm=7858b142fc90775dcbf31977e3487c3e287740b4801965bba5b59793661c8e99&=&format=webp&quality=lossless&width=420&height=287)

W klasie występują podane metody:
### getClassId
Jako dane wejściowe podane są przez użytkownika dane: nazwa klasy i dzień. Metoda najpierw odpowiednio formatuje odpowiedź, a następnie przeszukuje tabelę[12] i zwraca id (string).

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247295081564733633/FP0nSiCW44LxJl4xf2j8HTogoQJFk5XBQtib30oiHcFrEKJkuuE58Obe-0pl3uyzPQMawyEP6aptaVRdBMZOo0jZT9JpEpsuDztWPPp9oKvb-xqP9ioq1CGrwnEZlBvklKaScTG0tQ2SAXpJpZkKBknUtx2rozds1f0hckCLp9mL6-JJ-dAqvxSMUcUFHcbf3SggWb5orIkSJFQCAVpxz1Mw9AQb9FQJNF-4iDt5CPhIQqsNMDVaZrRvVOZcLFWoYXy0.png?ex=665f8191&is=665e3011&hm=d6d5d9637f4fe2c7775e874d5bbfc1826eaa5918742fd52cd72711925465b1a7&=&format=webp&quality=lossless&width=337&height=662)

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

![Diagram aktywności](https://media.discordapp.net/attachments/809756120125538325/1247301527060615238/nLJ1YjH04BtdAzujCuZWNYVike880w8U50_37cgcQtSgoNI7xWuXVHpm8sG_mqzmyrzsqgiEHXP5P4zfwbNLUw-goANpP7rxgBFfaQtMMdObrH8eVh0thNKegJ9uLcIhZtrdXYDfOTomVqdz2_UcFMpPBfOHVMT3tuYRuAxNKhLG1ehwMULhTivejrRkWS9wIeevHMQvOV8Pi5fxjfEonWOEyBJb-kupyXrPvV8Y0-GQ2zdaaTRbLpW_7mN0M0g8qTHJL4HATXxTJvRdI_WzQomyLSiC07wm0WymfmQ96qZy9qn9Gxd9fsVIeVsOqR0L4uDBNAGvpnGauW_EKoUiXK_NCMloP0f58jLQyc9qWjo8FSNPTtcibLoVs4EtbvgnqC8ZPuBdqA-7SU_wbR7lznmF8Ocg9Mg5WHgExOqPRdToBpcC3YoLTvzs16KE_N1RwnukLC8rUuHjgqn7CHGORZX-_T8XVnj1NPdyiVP_ClcPtyri_d76LsaAHZKc..png?ex=665f8791&is=665e3611&hm=420a490a0377274fd6ad9bf5043ea8adfe51f9bde37b28dc7bf509475116c739&=&format=webp&quality=lossless&width=322&height=662)

### createCodeBlockResponse
Metoda formuje dane przekazane z jakiejkolwiek listy jako `discord code block` (string) w formie kolumny (możliwe przeniesienie metody do osobnej klasy w przyszłości). 

# Dodatkowe informacje
Instrukcja, podobnie jak cały program, jest nadal w procesie budowy i nie jest finalną wersją. W razie konieczności treść instrukcji będzie aktualizowana.

# Autorzy
Krzysztof Solarczyk, Szymon Rozwoda - klasa 4TP
