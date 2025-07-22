# Managrid

**Managrid** ist ein strategisches, rundenbasiertes Spiel, das auf dem klassischen Käsekästchen ("Dots and Boxes") basiert – erweitert um Mana, Bauelemente, Fähigkeiten und einen computergesteuerten Gegner.

## Features

- **Zufallsgenerierte Spielfelder**: In jedem Level erwartet dich ein neues Muster.
- **Bauelemente**: Fülle mit speziellen Formen ganze Bereiche auf einmal aus (später auch drehbar).
- **Mana-System**: Schließe Kästchen, um Mana zu sammeln – benötigst du, um Bauelemente einzusetzen!
- **Gegner-KI**: Der Computer erhält Mana und kann ab höheren Schwierigkeitsgraden selbst Linien setzen oder mit Spezialfähigkeiten Spieler-Kästchen zerstören oder sich heilen.
- **Rundenbasiert**: Spieler und Computer wechseln sich ab.
- **Koop-Modus (geplant)**: Spiele später gemeinsam mit bis zu 4 Freunden gegen den Computer.

## Erste Schritte

### Voraussetzungen

- Python 3.8+
- [tkinter](https://wiki.python.org/moin/TkInter) (meist bereits in Python enthalten)
- [Pillow](https://python-pillow.org/) (`pip install pillow`) für den Startbildschirm

### Installation & Start

```bash
git clone https://github.com/DEINUSERNAMEx/Managrid.git
cd managrid
python managrid.py
```

## Bedienung

- **Linksklick** auf eine Linie: Linie vorläufig setzen (rot)
- **Rechtsklick** auf eine vorläufige Linie: Linie wieder entfernen
- **Zug bestätigen**: Alle roten Linien werden endgültig gezogen, der Zug wechselt zum Computer
- Der Computer erhält pro Runde Mana. Ab einer bestimmten Menge kann er Spezialfähigkeiten nutzen (z.B. Spieler-Kästchen entfernen).

## Projektstruktur

```plaintext
managrid/
├── managrid.py
├── gui/
│   ├── startscreen.py
│   └── board.py
├── README.md
├── Managrid.jpg
```

## Mitmachen

Du hast Ideen, möchtest Bugs melden oder mitentwickeln?  
Erstelle ein Issue oder einen Pull Request – jeder Beitrag ist willkommen!

---

**Viel Spaß beim Tüfteln und Taktieren in Managrid!**