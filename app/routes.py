from flask import request, jsonify, Response
from datetime import datetime
import random
import xml.etree.ElementTree as ET
from app import app
from app.utils import get_zodiac, generate_xml_response, generate_json_response
from app.data.horoscopes import horoscopes

def get_random_message(messages, date):
    # 日付に基づいてシードを設定し、乱数を生成
    seed = int(date)
    random.seed(seed)
    return random.choice(messages)

@app.route('/')
def horoscope():
    userids = request.args.getlist('userid')
    dates = request.args.getlist('date')
    births = request.args.getlist('birth')
    resulttype = request.args.get('resulttype')

    if not (userids and dates and births and resulttype):
        return "Missing parameters", 400

    if not (len(userids) == len(dates) == len(births)):
        return "Parameter lists must be of the same length", 400

    responses = []
    for userid, date, birth in zip(userids, dates, births):
        birthdate = birth if len(birth) == 8 else f"{date[:4]}{birth.zfill(4)}"
        zodiac = get_zodiac(birthdate)
        if not zodiac:
            return "Invalid birth date", 400

        result_texts = horoscopes[zodiac["name"]]

        # 占いメッセージを日付ベースでランダムに選択
        result_texts_s = get_random_message(result_texts["s"], date)
        result_texts_m = get_random_message(result_texts["m"], date)
        result_texts_l = get_random_message(result_texts["l"], date)

        if resulttype.lower() == 'xml':
            response = generate_xml_response(zodiac, result_texts_s, result_texts_m, result_texts_l, date)
            responses.append(response)
        elif resulttype.lower() == 'json':
            response = {
                "userid": userid,
                "announce": {
                    "lastAnnounce": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "fortuneDate": date,
                    "astro": {
                        "code": zodiac["code"],
                        "name": zodiac["name"],
                        "datefrom": zodiac["datefrom"],
                        "dateto": zodiac["dateto"],
                        "astrotext_s": result_texts_s,
                        "astrotext_m": result_texts_m,
                        "astrotext_l": result_texts_l
                    }
                }
            }
            responses.append(response)
        else:
            return "Invalid result type", 400

    if resulttype.lower() == 'xml':
        return Response("".join(responses), mimetype='application/xml')
    else:
        return jsonify(responses)

def generate_xml_response(zodiac, text_s, text_m, text_l, date):
    root = ET.Element("announce", lastAnnounce=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), astroDate=date)
    astro = ET.SubElement(root, "astro", code=zodiac["code"], name=zodiac["name"], datefrom=zodiac["datefrom"], dateto=zodiac["dateto"])
    ET.SubElement(astro, "astrotext_s").text = text_s
    ET.SubElement(astro, "astrotext_m").text = text_m
    ET.SubElement(astro, "astrotext_l").text = text_l
    
    return ET.tostring(root, encoding="utf-8").decode("utf-8")

def generate_json_response(zodiac, text_s, text_m, text_l, date):
    return {
        "announce": {
            "lastAnnounce": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fortuneDate": date,
            "astro": {
                "code": zodiac["code"],
                "name": zodiac["name"],
                "datefrom": zodiac["datefrom"],
                "dateto": zodiac["dateto"],
                "astrotext_s": text_s,
                "astrotext_m": text_m,
                "astrotext_l": text_l
            }
        }
    }
