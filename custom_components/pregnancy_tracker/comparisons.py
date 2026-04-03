"""Size comparison data for pregnancy tracker."""
import json
import logging
import os
from pathlib import Path

_LOGGER = logging.getLogger(__name__)

# Week-by-week comparisons (weeks 1-42)
COMPARISONS = {
    1: {"veggie": "Mohnsamen", "dad": "Papas Parfümprobe"},
    2: {"veggie": "Sesamsamen", "dad": "Papas Krawattenklammer"},
    3: {"veggie": "Pfefferkorn", "dad": "Papas Kragenstäbchen"},
    4: {"veggie": "Linse", "dad": "Papas Manschettenknopf"},
    5: {"veggie": "Apfelsamen", "dad": "Papas Plektrum"},
    6: {"veggie": "Zuckerschote", "dad": "Papas Würfel"},
    7: {"veggie": "Blaubeere", "dad": "Papas USB-Stick"},
    8: {"veggie": "Himbeere", "dad": "Papas Golftee"},
    9: {"veggie": "Kirsche", "dad": "Papas Flaschenverschluss"},
    10: {"veggie": "Erdbeere", "dad": "Papas Hausschlüssel"},
    11: {"veggie": "Rosenkohl", "dad": "Papas Pokerchip"},
    12: {"veggie": "Pflaume", "dad": "Papas AirPods-Hülle"},
    13: {"veggie": "Zitrone", "dad": "Papas Fernbedienung"},
    14: {"veggie": "Pfirsich", "dad": "Papas Kaffeebecher"},
    15: {"veggie": "Apfel", "dad": "Papas Baseball"},
    16: {"veggie": "Avocado", "dad": "Papas Lieblingsbier"},
    17: {"veggie": "Steckrübe", "dad": "Papas Spielecontroller"},
    18: {"veggie": "Paprika", "dad": "Papas Geldbörse"},
    19: {"veggie": "Mango", "dad": "Papas Laufschuh"},
    20: {"veggie": "Banane", "dad": "Papas Laptop-Ladegerät"},
    21: {"veggie": "Karotte", "dad": "Papas Tablet"},
    22: {"veggie": "Papaya", "dad": "Papas Sneaker"},
    23: {"veggie": "Grapefruit", "dad": "Papas iPad"},
    24: {"veggie": "Honigmelone (Cantaloupe)", "dad": "Papas Laptop"},
    25: {"veggie": "Blumenkohl", "dad": "Papas Werkzeugkasten"},
    26: {"veggie": "Kopf-Salat", "dad": "Papas Aktenkoffer"},
    27: {"veggie": "Kohlkopf", "dad": "Papas Basketball"},
    28: {"veggie": "Aubergine", "dad": "Papas Bowlingkugel"},
    29: {"veggie": "Butternuss-Kürbis", "dad": "Papas Rucksack"},
    30: {"veggie": "Großer Kohlkopf", "dad": "Papas Monitor"},
    31: {"veggie": "Kokosnuss", "dad": "Papas Gitarre"},
    32: {"veggie": "Jicama (Mexikanische Yambohne)", "dad": "Papas Golftasche"},
    33: {"veggie": "Ananas", "dad": "Papas Grillabdeckung"},
    34: {"veggie": "Honigmelone", "dad": "Papas Kühlbox"},
    35: {"veggie": "Große Honigmelone", "dad": "Papas Angelkasten"},
    36: {"veggie": "Römersalat", "dad": "Papas Rasenmäher"},
    37: {"veggie": "Mangold", "dad": "Papas Werkzeugschrank"},
    38: {"veggie": "Lauch", "dad": "Papas Fernsehsessel"},
    39: {"veggie": "Mini-Wassermelone", "dad": "Papas Fernseher"},
    40: {"veggie": "Kleiner Kürbis", "dad": "Papas Grill"},
    41: {"veggie": "Kürbis", "dad": "Papas Werkbank"},
    42: {"veggie": "Wassermelone", "dad": "Papas Autoreifen"},
}

def _image_path(mode: str, week: int) -> str:
    """Build an image path for a given mode/week.

    Images are bundled with the integration and automatically copied to:
    /config/www/pregnancy_tracker/{mode}/week_{week}.png
    
    Users can override by placing their own images at these paths.
    """
    return f"/local/pregnancy_tracker/{mode}/week_{week}.png"

# Weekly development summaries (weeks 1-42)
WEEKLY_SUMMARIES = {
    1: "Die Befruchtung findet statt. Die befruchtete Eizelle beginnt ihre Reise.",
    2: "Die Blastozyste nistet sich in der Gebärmutterwand ein.",
    3: "Das Herz und das Nervensystem des Babys beginnen sich zu bilden.",
    4: "Der Neuralrohr entwickelt sich – daraus entstehen Gehirn und Rückenmark des Babys.",
    5: "Das Herz des Babys beginnt zu schlagen! Die wichtigsten Organe bilden sich.",
    6: "Gesichtszüge entstehen. Erste Arm- und Beinansätze sind sichtbar.",
    7: "Das Gehirn des Babys wächst schnell. Augenlider und Nase formen sich.",
    8: "Finger und Zehen entwickeln sich – noch leicht verwachsen. Das Baby beginnt sich zu bewegen!",
    9: "Der Herzschlag ist per Ultraschall hörbar. Die Organe entwickeln sich weiter.",
    10: "Die wichtigsten Organe sind gebildet und beginnen zu funktionieren.",
    11: "Die Knochen des Babys verhärten sich. Fingernägel beginnen zu wachsen.",
    12: "Reflexe entwickeln sich. Das Baby kann seine Fäuste öffnen und schließen.",
    13: "Stimmbänder und Fingerabdrücke entstehen.",
    14: "Das Baby kann Gesichtsausdrücke machen, vielleicht sogar blinzeln oder die Stirn runzeln.",
    15: "Das Skelett entwickelt sich weiter. Das Baby ist jetzt sehr aktiv!",
    16: "Die Augen des Babys können sich bewegen. Vielleicht spürst du die ersten Tritte!",
    17: "Das Baby kann Geräusche von außen hören.",
    18: "Die Ohren sind nun richtig positioniert. Das Baby kann gähnen und Schluckauf bekommen!",
    19: "Die Haut des Babys wird von der schützenden Käseschmiere (Vernix caseosa) bedeckt.",
    20: "Halbzeit! Das Baby hört deine Stimme und reagiert auf Geräusche.",
    21: "Die Bewegungen des Babys werden koordinierter und spürbarer.",
    22: "Augenbrauen und Wimpern sind sichtbar. Die Sinne entwickeln sich.",
    23: "Die Lungen bereiten sich auf das Atmen vor, funktionieren aber noch nicht selbstständig.",
    24: "Wichtiger Meilenstein: Das Baby wäre im Falle einer Frühgeburt überlebensfähig.",
    25: "Das Baby reagiert auf deine Stimme und Berührungen. Haare können beginnen zu wachsen.",
    26: "Die Augen öffnen sich langsam. Das Baby kann Licht wahrnehmen.",
    27: "Das dritte Trimester beginnt! Das Gehirn wächst nun besonders schnell.",
    28: "Das Baby kann träumen – die REM-Schlafphase hat begonnen.",
    29: "Muskeln und Lungen reifen schnell weiter.",
    30: "Das Gehirn bildet Milliarden von neuen Nervenzellen.",
    31: "Die fünf Sinne des Babys sind nun voll entwickelt und funktionsfähig.",
    32: "Das Baby übt das Atmen, indem es Fruchtwasser ein- und ausatmet.",
    33: "Die Knochen werden fester, aber der Schädel bleibt weich und flexibel.",
    34: "Das zentrale Nervensystem reift weiter aus.",
    35: "Die Nieren sind vollständig entwickelt. Die Leber verarbeitet Abfallstoffe.",
    36: "Das Baby verliert die Käseschmiere und die feinen Härchen (Lanugo). Es ist fast bereit!",
    37: "Termingerecht! Das Baby kann nun jederzeit geboren werden.",
    38: "Das Baby hat einen festen Griff und verfeinert seine Reflexe.",
    39: "Gehirn und Lungen entwickeln sich weiter und werden leistungsfähiger.",
    40: "Der errechnete Geburtstermin! Das Baby ist vollständig entwickelt und bereit, dich zu treffen.",
    41: "Das Warten geht weiter. Das Baby nimmt weiter an Gewicht zu.",
    42: "Überfällig – der Arzt könnte eine Einleitung empfehlen.",
}

def get_comparison(week: int, mode: str = "veggie") -> dict[str, str]:
    """Get size comparison data for a given week.

    Returns a dict with 'label' and 'image' keys (no emoji).
    """
    if week < 1 or week > 42:
        week = max(1, min(42, week))

    data = COMPARISONS.get(week, {})

    if mode == "dad":
        return {
            "label": data.get("dad", f"Week {week}"),
            "image": _image_path("dad", week),
        }
    else:  # Default to veggie
        return {
            "label": data.get("veggie", f"Week {week}"),
            "image": _image_path("veggie", week),
        }


def get_all_comparisons(week: int) -> dict[str, dict[str, str]]:
    """Get all comparison modes for a given week with images."""
    if week < 1 or week > 42:
        week = max(1, min(42, week))

    data = COMPARISONS.get(week, {})

    return {
        "veggie": {
            "label": data.get("veggie", f"Week {week}"),
            "image": _image_path("veggie", week),
        },
        "dad": {
            "label": data.get("dad", f"Week {week}"),
            "image": _image_path("dad", week),
        },
    }


def get_weekly_summary(week: int) -> str:
    """Get developmental summary for a given week."""
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    return WEEKLY_SUMMARIES.get(week, f"Week {week} of pregnancy.")


# Weekly Bible verses (weeks 1-42)
BIBLE_VERSES = {
    1: {"text": "Noch ehe ich dich im Mutterleib formte, habe ich dich erkannt; noch bevor du geboren wurdest, habe ich dich erwählt.", "reference": "Jeremia 1,5"},
    2: {"text": "Du hast mein Innerstes geschaffen; du hast mich im Leib meiner Mutter gebildet.", "reference": "Psalm 139,13"},
    3: {"text": "Ich danke dir, dass ich so wunderbar erschaffen bin; wunderbar sind deine Werke – das erkennt meine Seele wohl.", "reference": "Psalm 139,14"},
    4: {"text": "Deine Augen sahen mich schon, als ich noch ungeformt war; alle Tage meines Lebens standen in deinem Buch, bevor auch nur einer von ihnen begann.", "reference": "Psalm 139,16"},
    5: {"text": "Kinder sind eine Gabe des HERRN, Frucht des Leibes ist eine Belohnung.", "reference": "Psalm 127,3"},
    6: {"text": "Kann eine Mutter ihr Kindlein vergessen und sich nicht erbarmen über den Sohn ihres Leibes? Und selbst wenn sie es vergäße – ich vergesse dich nicht!", "reference": "Jesaja 49,15"},
    7: {"text": "Du hast mich aus dem Mutterschoß hervorgebracht, mich vertrauen gelehrt an meiner Mutter Brust.", "reference": "Psalm 22,10"},
    8: {"text": "Sei stark und mutig! Fürchte dich nicht und verzage nicht, denn der HERR, dein Gott, ist mit dir, wohin du auch gehst.", "reference": "Josua 1,9"},
    9: {"text": "Der HERR ist meine Stärke und mein Schild; auf ihn vertraut mein Herz, und mir ist geholfen.", "reference": "Psalm 28,7"},
    10: {"text": "All eure Sorgen werft auf ihn, denn er sorgt für euch.", "reference": "1. Petrus 5,7"},
    11: {"text": "Denn ich weiß, was ich mit euch vorhabe, spricht der HERR: Gedanken des Friedens und nicht des Unheils, um euch Zukunft und Hoffnung zu geben.", "reference": "Jeremia 29,11"},
    12: {"text": "Alle guten und vollkommenen Gaben kommen von oben, vom Vater des Lichts.", "reference": "Jakobus 1,17"},
    13: {"text": "Der HERR segne dich und behüte dich; der HERR lasse sein Angesicht über dir leuchten und sei dir gnädig.", "reference": "4. Mose 6,24–25"},
    14: {"text": "Alles vermag ich durch den, der mich stark macht.", "reference": "Philipper 4,13"},
    15: {"text": "Der HERR, dein Gott, ist in deiner Mitte, ein starker Retter. Er wird sich über dich freuen, in Liebe erneuern und mit Jubel über dich singen.", "reference": "Zefanja 3,17"},
    16: {"text": "Wir wissen aber, dass denen, die Gott lieben, alle Dinge zum Guten mitwirken.", "reference": "Römer 8,28"},
    17: {"text": "Frieden lasse ich euch, meinen Frieden gebe ich euch – nicht wie die Welt ihn gibt. Euer Herz erschrecke nicht und fürchte sich nicht.", "reference": "Johannes 14,27"},
    18: {"text": "Dies ist der Tag, den der HERR gemacht hat; lasst uns jubeln und uns an ihm freuen.", "reference": "Psalm 118,24"},
    19: {"text": "Vertraue auf den HERRN von ganzem Herzen und verlass dich nicht auf deinen Verstand.", "reference": "Sprüche 3,5"},
    20: {"text": "Ihr werdet in Freude ausziehen und in Frieden geleitet werden; Berge und Hügel werden vor euch jubeln.", "reference": "Jesaja 55,12"},
    21: {"text": "Der Gott der Hoffnung erfülle euch mit aller Freude und allem Frieden im Glauben.", "reference": "Römer 15,13"},
    22: {"text": "Der HERR ist mein Hirte, mir wird nichts mangeln. Er lässt mich lagern auf grünen Auen und führt mich zu stillen Wassern.", "reference": "Psalm 23,1–3"},
    23: {"text": "Denn er befiehlt seinen Engeln, dich zu behüten auf all deinen Wegen.", "reference": "Psalm 91,11"},
    24: {"text": "Jünglinge werden müde und matt, und junge Männer straucheln; aber die auf den HERRN hoffen, gewinnen neue Kraft.", "reference": "Jesaja 40,30–31"},
    25: {"text": "Meine Gnade genügt dir; denn meine Kraft kommt in der Schwachheit zur Vollendung.", "reference": "2. Korinther 12,9"},
    26: {"text": "Der HERR ist nahe denen, die zerbrochenen Herzens sind, und hilft denen, deren Geist zerschlagen ist.", "reference": "Psalm 34,19"},
    27: {"text": "Gewöhne den Knaben an seinen Weg, so weicht er auch im Alter nicht davon.", "reference": "Sprüche 22,6"},
    28: {"text": "Gott ist uns Zuflucht und Stärke, als Beistand in Nöten wohl bewährt.", "reference": "Psalm 46,2"},
    29: {"text": "Kommt her zu mir, alle, die ihr mühselig und beladen seid; ich will euch erquicken.", "reference": "Matthäus 11,28"},
    30: {"text": "Gesegnet ist der Mensch, der auf den HERRN vertraut und dessen Zuversicht der HERR ist.", "reference": "Jeremia 17,7"},
    31: {"text": "Der HERR behüte deinen Ausgang und Eingang von nun an bis in Ewigkeit.", "reference": "Psalm 121,8"},
    32: {"text": "Danket dem HERRN, denn er ist gütig; denn seine Gnade währt ewig.", "reference": "Psalm 107,1"},
    33: {"text": "Ich bin gewiss, dass der, der in euch das gute Werk begonnen hat, es auch vollenden wird.", "reference": "Philipper 1,6"},
    34: {"text": "Kraft und Würde sind ihr Gewand, und sie lacht über die kommende Zeit.", "reference": "Sprüche 31,25"},
    35: {"text": "Der HERR selbst zieht vor dir her; er ist mit dir, er wird dich nicht aufgeben noch dich verlassen.", "reference": "5. Mose 31,8"},
    36: {"text": "Er schenke dir, was dein Herz begehrt, und lasse all deine Pläne gelingen.", "reference": "Psalm 20,5"},
    37: {"text": "Sorgt euch also nicht um den morgigen Tag; denn der morgige Tag wird für sich selbst so


def get_bible_verse(week: int, custom_path: str | None = None) -> dict[str, str]:
    """Get Bible verse for a given week.
    
    Args:
        week: The pregnancy week (1-42)
        custom_path: Optional path to custom Bible verses JSON file
    
    Returns a dict with 'text' and 'reference' keys.
    """
    if week < 1 or week > 42:
        week = max(1, min(42, week))
    
    # Try to load custom verses if path is provided
    if custom_path:
        custom_verses = _load_custom_bible_verses(custom_path)
        if custom_verses and str(week) in custom_verses:
            custom_data = custom_verses[str(week)]
            # Support both full dict format and simple text format
            if isinstance(custom_data, dict):
                return {
                    "text": custom_data.get("text", ""),
                    "reference": custom_data.get("reference", ""),
                }
            elif isinstance(custom_data, str):
                # If only text is provided, reference will be empty
                return {
                    "text": custom_data,
                    "reference": "",
                }
    
    # Fall back to default verses
    verse_data = BIBLE_VERSES.get(week, {})
    return {
        "text": verse_data.get("text", ""),
        "reference": verse_data.get("reference", ""),
    }


def parse_bible_reference(reference: str) -> dict[str, str]:
    """Parse a Bible verse reference into its components.
    
    Args:
        reference: Bible reference like "Psalm 139:13" or "Numbers 6:24-25"
    
    Returns:
        A dict with 'book', 'chapter', 'verse', and 'book_and_chapter' keys.
    """
    if not reference:
        return {
            "book": "",
            "chapter": "",
            "verse": "",
            "book_and_chapter": "",
        }
    
    # Split on the last colon to separate book+chapter from verse
    parts = reference.rsplit(":", 1)
    
    if len(parts) == 2:
        book_and_chapter = parts[0].strip()
        verse = parts[1].strip()
        
        # Further split book_and_chapter on the last space to get book and chapter
        book_chapter_parts = book_and_chapter.rsplit(" ", 1)
        
        if len(book_chapter_parts) == 2:
            book = book_chapter_parts[0].strip()
            chapter = book_chapter_parts[1].strip()
        else:
            # No space found, treat whole thing as book
            book = book_and_chapter
            chapter = ""
    else:
        # No colon found
        book_and_chapter = reference.strip()
        verse = ""
        
        # Try to split on last space
        book_chapter_parts = book_and_chapter.rsplit(" ", 1)
        if len(book_chapter_parts) == 2:
            book = book_chapter_parts[0].strip()
            chapter = book_chapter_parts[1].strip()
        else:
            book = book_and_chapter
            chapter = ""
    
    return {
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "book_and_chapter": book_and_chapter,
    }


def _load_custom_bible_verses(file_path: str) -> dict:
    """Load custom Bible verses from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing custom verses
        
    Returns:
        Dictionary with week numbers as keys and verse data as values,
        or empty dict if file cannot be loaded.
    """
    try:
        # Handle both absolute and relative paths
        path = Path(file_path)
        
        # If path is relative, try to resolve it from common Home Assistant locations
        if not path.is_absolute():
            # Try current directory first (for testing)
            if path.exists():
                pass  # Use the path as is
            # Try /config directory (standard Home Assistant config directory)
            elif (Path("/config") / file_path).exists():
                path = Path("/config") / file_path
            else:
                _LOGGER.warning(
                    "Custom Bible verses file not found at relative path: %s", 
                    file_path
                )
                return {}
        
        if not path.exists():
            _LOGGER.warning(
                "Custom Bible verses file not found: %s", 
                path
            )
            return {}
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Validate the structure
        if not isinstance(data, dict):
            _LOGGER.error(
                "Custom Bible verses file has invalid format. Expected a dictionary."
            )
            return {}
        
        _LOGGER.info(
            "Successfully loaded %d custom Bible verses from %s", 
            len(data), 
            path
        )
        return data
        
    except json.JSONDecodeError as err:
        _LOGGER.error(
            "Failed to parse custom Bible verses JSON file %s: %s",
            file_path,
            err
        )
        return {}
    except Exception as err:
        _LOGGER.error(
            "Failed to load custom Bible verses from %s: %s",
            file_path,
            err
        )
        return {}
