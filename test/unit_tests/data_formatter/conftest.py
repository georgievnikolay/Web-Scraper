"""
Configuration for pytest.

NOTE: This file is automatically included when running pytest.
      There is no need to import it explicitly in the test files.
"""

import os
import sys

import pytest

from module.data_formatter import DataFormatter

import pandas as pd

# allow the contents to be found automatically as if we were in that directory
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

test_data_path = os.path.dirname(__file__)


@pytest.fixture
def example_data_formatter():
    data_formatter = DataFormatter()
    return data_formatter


@pytest.fixture
def example_input_data():
    data = {
        'date': pd.Timestamp("2021-06-15T05:50:24+00:00"),
        'content':  "\nПолети до Милано\nРезервирайте много изгодни полети до Милано "
                    "за пролетта и лятото с тръгване от София или Варна и си организирайте "
                    "един много приятен дълъг уикенд или почивка.\nПроверете изискванията за "
                    "влизане в Итлаия, когато пътуването Ви наближи. Повече информация за "
                    "източниците на информация за Covid-19 изисквания можете да намерите в "
                    "специалната ни статия.\nАко обичате модата и дизайна, то Милано е Вашият град. "
                    "Милано не е от градовете, които научаваш от един поглед; той има много "
                    "съкровища, които чакат да бъдат открити. Като вътрешните дворове в италианските "
                    "сгради – прекрасни, но някак скрити от погледа минувачите. Модата, дизайна, "
                    "музеите, църквите, италианската кухня и събитията на града поетапно разкриват "
                    "богатият му дух и многото му лица. Ако се вълнувате от мода задължително се "
                    "разходете „златните улици” на Милано или „Il Quadrilatero d’Oro” – районът "
                    "разположен между via Monte Napoleone, via Manzoni, via della Spiga и corso "
                    "Venezia, където е и сърцето на столицата на модата с бутиците на най-важните "
                    "модни марки. Витрините им са произведение на изкуството и винаги любопитна "
                    "гледка – разходете се и вечер! Отбележете си и тези места: Armani/Silos и "
                    "Fondazione Prada, музеи посветени на историческите дизайнерски къщи.\nТези "
                    "от Вас фенове на съвременното изкуство: Pirelli HangarBicocca е важна спирка "
                    "за Вас – впечатляващо с размерите си индустриално пространство (бивша фабрика "
                    "за влакове), което помещава не по-малко впечатляващи с мащаба си инсталации. "
                    "Pinacoteca di Brera пък е отличаваща се художествена галерия с висока световна "
                    "оценка на колекцията си от италиански картини, която е разположена в красивия "
                    "исторически квартал на Милано – Brera. Тук ще откриете множество малки бутици "
                    "и работилници наред с кафенета, барове и ресторанти.\n",
        'authors': [ "\nКремена\n\t\t\t\t\t\t5 ноември, 2019 в 17:58-Отговори ",
                     "\nEmil Daskalov\n\t\t\t\t\t\t5 юли, 2018 в 12:34-Отговори ",
                     "\nTravelSmart\n\t\t\t\t\t\t9 юли, 2018 в 11:42-Отговори " ],
        'comments' : [  "\nНещо не е съвсем така с цените на полетите! 😀\n",
                        "\nЗдравейте Емил,\nКакто вече Ви отговорихме във Фейсбук\n",
                        "\nИнтересува ме каква е цената на полета за 3.09 София-Санторинина и връщане Санторини- София 10.09?\n"
        ]
    }
    
    return data


@pytest.fixture
def example_expected_data():
    data = {
        'date': "15/6/2021",
        'content' : "Резервирайте много изгодни полети до Милано "
                    "за пролетта и лятото с тръгване от София или Варна и си организирайте "
                    "един много приятен дълъг уикенд или почивка.\nПроверете изискванията за "
                    "влизане в Итлаия, когато пътуването Ви наближи. Повече информация за "
                    "източниците на информация за Covid-19 изисквания можете да намерите в "
                    "специалната ни статия.\nАко обичате модата и дизайна, то Милано е Вашият град. "
                    "Милано не е от градовете, които научаваш от един поглед; той има много "
                    "съкровища, които чакат да бъдат открити. Като вътрешните дворове в италианските "
                    "сгради – прекрасни, но някак скрити от погледа минувачите. Модата, дизайна, "
                    "музеите, църквите, италианската кухня и събитията на града поетапно разкриват "
                    "богатият му дух и многото му лица. Ако се вълнувате от мода задължително се "
                    "разходете „златните улици” на Милано или „Il Quadrilatero d’Oro” – районът "
                    "разположен между via Monte Napoleone, via Manzoni, via della Spiga и corso "
                    "Venezia, където е и сърцето на столицата на модата с бутиците на най-важните "
                    "модни марки. Витрините им са произведение на изкуството и винаги любопитна "
                    "гледка – разходете се и вечер! Отбележете си и тези места: Armani/Silos и "
                    "Fondazione Prada, музеи посветени на историческите дизайнерски къщи.\n",
        'word_occurences' : { 'милано' : '6', 'много' : '3', 'модата' : '3'},
        'authors' : [ "Кремена_1", "Emil Daskalov_2", "TravelSmart_3" ],
        'comments' : {
            "Кремена_1" : "\nНещо не е съвсем така с цените на полетите! 😀\n",
            "Emil Daskalov_2" : "\nЗдравейте Емил,\nКакто вече Ви отговорихме във Фейсбук\n",
            "TravelSmart_3" : "\nИнтересува ме каква е цената на полета за 3.09 София-Санторинина и връщане Санторини- София 10.09?\n"
        }
    }

    return data


@pytest.fixture
def example_data_frame():
    return pd.read_json(test_data_path + '/example_out.json', orient='records')


@pytest.fixture
def example_comment_frame():
    in_data = { 'comment-author' : [ [
                    "\nКремена\n\t\t\t\t\t\t5 ноември, 2019 в 17:58-Отговори ",
                    "\nEmil Daskalov\n\t\t\t\t\t\t5 юли, 2018 в 12:34-Отговори ",
                    "\nTravelSmart\n\t\t\t\t\t\t9 юли, 2018 в 11:42-Отговори " ], None ],
                'comment-text' : [ [
                    "\nНещо не е съвсем така с цените на полетите! 😀\n",
                    "\nЗдравейте Емил,\nКакто вече Ви отговорихме във Фейсбук\n",
                    "\nИнтересува ме каква е цената на полета за 3.09 София-Санторинина и връщане Санторини- София 10.09?\n"
                    ], None ]
                }
    
    exp_data = {'comment-author': [ {
                    "Кремена_1" : "\nНещо не е съвсем така с цените на полетите! 😀\n",
                    "Emil Daskalov_2" : "\nЗдравейте Емил,\nКакто вече Ви отговорихме във Фейсбук\n",
                    "TravelSmart_3" : "\nИнтересува ме каква е цената на полета за 3.09 София-Санторинина и връщане Санторини- София 10.09?\n"
                    }, None ],
                'comment-text': [ [
                    "\nНещо не е съвсем така с цените на полетите! 😀\n",
                    "\nЗдравейте Емил,\nКакто вече Ви отговорихме във Фейсбук\n",
                    "\nИнтересува ме каква е цената на полета за 3.09 София-Санторинина и връщане Санторини- София 10.09?\n"
                    ], None ] 
                }
    
    return {'input': pd.DataFrame(in_data),
            'expected': pd.DataFrame(exp_data)}
