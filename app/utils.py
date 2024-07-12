from datetime import datetime
import xml.etree.ElementTree as ET
from flask import Response, jsonify
from app.data.zodiac_signs import zodiac_signs

def get_zodiac(birthdate):
    month_day = int(birthdate[4:])
    for sign in zodiac_signs:
        datefrom = int(sign["datefrom"].replace("-", ""))
        dateto = int(sign["dateto"].replace("-", ""))
        if datefrom <= month_day <= dateto:
            return sign
    return None

def generate_xml_response(zodiac, result_texts, date):
    root = ET.Element("announce", lastAnnounce=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), astroDate=date)
    astro = ET.SubElement(root, "astro", code=zodiac["code"], name=zodiac["name"], datefrom=zodiac["datefrom"], dateto=zodiac["dateto"])
    ET.SubElement(astro, "astrotext_s").text = result_texts["s"]
    ET.SubElement(astro, "astrotext_m").text = result_texts["m"]
    ET.SubElement(astro, "astrotext_l").text = result_texts["l"]
    
    xml_str = ET.tostring(root, encoding="utf-8")
    return Response(xml_str, mimetype='application/xml')

def generate_json_response(zodiac, result_texts, date):
    response = {
        "announce": {
            "lastAnnounce": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fortuneDate": date,
            "astro": [
                {
                    "code": zodiac["code"],
                    "name": zodiac["name"],
                    "datefrom": zodiac["datefrom"],
                    "dateto": zodiac["dateto"],
                    "astrotext_s": result_texts["s"],
                    "astrotext_m": result_texts["m"],
                    "astrotext_l": result_texts["l"]
                }
            ]
        }
    }
    return jsonify(response)
