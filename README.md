# Multi-Robot Formasyon Kontrolü (A* ve Q-Learning ile)

## Giriş

Çoklu robot sistemleri; depo otomasyonu, otonom navigasyon, arama-kurtarma ve gözetleme gibi birçok alanda kullanılmaktadır.

Bu sistemlerde birden fazla robotun koordineli şekilde hareket etmesi önemli bir problemdir. Bu problemlerden biri de **formasyon kontrolüdür**. Formasyon kontrolünde robotlar hareket ederken belirli bir geometrik düzeni (örneğin üçgen, kare veya çizgi) korumaya çalışırlar.

Bu projede, basitleştirilmiş bir **2 boyutlu grid ortamında**, lider robotun A* algoritması ile hedefe ulaşması ve diğer robotların Q-learning kullanarak belirli bir formasyonu koruması amaçlanmaktadır.

---

## Problem Tanımı

Bu projenin amacı, 2D grid ortamında çalışan bir çoklu robot sistemi simüle etmektir:

- Bir robot **lider** olarak seçilir
- Lider robot hedefe gitmek için **A\*** algoritmasını kullanır
- Diğer robotlar **takipçi (follower)** olarak hareket eder
- Takipçiler, liderin etrafında belirli bir **formasyonu korumaya çalışır**
- Sistem çarpışmalardan ve engellerden kaçınır

Bu problem hem **yol planlama (path planning)** hem de **formasyon kontrolünü** birlikte ele almaktadır.

---

## Arka Plan

### Formasyon Kontrolü

Formasyon kontrolü, çoklu robot sistemlerinde robotların hareket ederken aralarındaki göreli pozisyonları korumasını sağlar.

Yaygın yöntemler:
- Leader-Follower (Lider-Takipçi)
- Virtual Structure
- Davranış tabanlı yöntemler
- Consensus tabanlı yöntemler

Bu projede basitliği nedeniyle **leader-follower yaklaşımı** kullanılacaktır.

---

###  A* Algoritması

A* algoritması, grid tabanlı ortamlarda en kısa yolu bulmak için kullanılan yaygın bir arama algoritmasıdır.

Temel mantığı:

f(n) = g(n) + h(n)

- g(n): başlangıçtan mevcut noktaya kadar olan maliyet
- h(n): hedefe olan tahmini uzaklık

Bu projede lider robot, hedefe ulaşmak için A* algoritmasını kullanacaktır.

---

###  Pekiştirmeli Öğrenme (Q-Learning)

Pekiştirmeli öğrenme, bir ajanın çevresiyle etkileşime girerek öğrenmesini sağlar.

Q-learning, durum-eylem çiftleri için değer (Q-table) öğrenen bir algoritmadır:

Q(durum, eylem)

Amaç, ajanların maksimum ödül elde edecek şekilde davranmayı öğrenmesidir.

Bu projede takipçi robotlar:
- formasyonu korumayı
- lideri takip etmeyi
- çarpışmalardan kaçınmayı

Q-learning ile öğrenmeye çalışacaktır.

---

##  Literatür Taraması

Çoklu robot formasyon kontrolü ve yol planlama problemleri, robotik ve yapay zeka alanında geniş şekilde çalışılmıştır.

Tong ve arkadaşları, A* algoritması ile yapay potansiyel alan yöntemini birleştirerek formasyon bazlı yol planlama üzerine çalışmalar yapmıştır. Bu çalışma, global yol planlama ile formasyon kontrolünün birlikte ele alınabileceğini göstermektedir.

Bae ve arkadaşları, çoklu robot yol planlama problemleri için Deep Q-Learning tabanlı bir yaklaşım önermiştir. Bu yaklaşım, öğrenme tabanlı yöntemlerin karmaşık ortamlarda etkili olabileceğini göstermektedir.

Rawat ve Karlapalem, çoklu robot formasyon kontrolünü çok ajanlı pekiştirmeli öğrenme problemi olarak ele almıştır. Bu çalışmada robotların birlikte hareket ederek formasyonu koruması hedeflenmiştir.

Son yıllarda Multi-Agent Reinforcement Learning (MARL) alanında yapılan çalışmalar, robotların merkezi olmayan şekilde koordinasyon sağlayabildiğini göstermektedir.

Bu çalışmalar, klasik algoritmalar (A*) ile öğrenme tabanlı yöntemlerin (Q-learning, DRL) birlikte kullanılmasının uygun ve etkili bir yaklaşım olduğunu göstermektedir.

---

##  Önerilen Yaklaşım

Bu projede hibrit bir yaklaşım kullanılacaktır:

- Lider robot → A* algoritması ile hedefe gider
- Takipçi robotlar → Q-learning ile formasyonu korur
- Ortam → 2D grid (ızgara)

Desteklenen formasyonlar:
- Üçgen formasyon
- Kare formasyon

Takipçi robotlar aşağıdaki kriterlere göre ödül alır:

- Formasyona yakın olmak → pozitif ödül
- Formasyondan uzaklaşmak → negatif ödül
- Çarpışma → büyük ceza
- Engellere çarpma → ceza
- Gereksiz hareket → küçük ceza

---

##  Beklenen Çıktılar

Bu proje sonucunda:

- 2D bir simülasyon ortamı oluşturulacaktır
- Lider robot A* ile hedefe ulaşacaktır
- Takipçi robotlar formasyonu korumaya çalışacaktır
- Robot hareketleri görselleştirilecektir
- Ödül (reward) ve performans grafikleri elde edilecektir

---

##  Kullanılan Teknolojiler

- Python
- NumPy
- Matplotlib / Pygame
- A* algoritması
- Q-learning

---

##  Gelecek Çalışmalar

- Deep Q-Network (DQN) kullanımı
- Dinamik engeller
- Multi-agent reinforcement learning
- Sürekli (continuous) ortamlar
- ROS2 / Gazebo entegrasyonu

---

##  Not

Bu proje, klasik yol planlama algoritmaları ile pekiştirmeli öğrenmenin birlikte kullanımını anlamaya yönelik basitleştirilmiş bir prototip olarak tasarlanmıştır. Amaç, kavramsal anlayışı geliştirmek ve temel bir simülasyon oluşturmaktır.
