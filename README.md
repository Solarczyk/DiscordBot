# Nawigacja po pliku json:
* tabela cards zawiera informacje o tym, kiedy odbywa się dana lekcja itd
* tabela lessons zawiera informacje o przedmiocie, klasie (id), nauczycielu (id), ilości godzin w tygodniu i długości godzin
* tabela subjects zawiera nazwy przedmiotów
  
kolejność wczytywania planu lessons -> cards -> output


# Obsługa bota
* Skrypt powinien być uruchamiany przez jedno urządzenie (Prawdopodobne użycie hostingu w późniejszych etapach).
* Bot aktualnie ma dostęp do odczytywania i odpowiadania na komendy na każdym kanale tekstowym (TODO: Ograniczyć dostęp bota)
* Bot używa systemu komend z prefixem "/"
* Podawane dane nie wymagają używania polskich znaków, oraz nie ma znaczenia także wielkość liter
* Zwracane przez bota dane są prezentowane w formię bloku kodu
* Przy nieobsłużonym wyjątku bot przestanie działać. Należy uruchomić skrypt ponownie


