# KinectGCNN

### Wymagania
- Python 3.7.9 (bądź w niższej wersji, wersje 3.8+ NIE mogą zostać zastosowane ze względu na PyKinect2 - używa ona funkcji, która w Pythonie 3.8 została usunięta)
- pipenv

### Kroki
Korzystając z Makefile:
1. make install - instalacja potrzebnych pakietów
2. make run - uruchomienie rejestracji pojedynczej klatki z Kinecta i zapisanie wyników.

Wyniki pojawią się w folderze recorded_frames w postaci plików *.ply.