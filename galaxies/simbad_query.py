from numpy import loadtxt
from astroquery.simbad import Simbad    # Импорт модуля для работы с Simbad
import astropy.coordinates as coord     # Импорт модуля для работы с координатами
import astropy.units as u               # Импорт единиц измерения из AstroPy

# Загрузим координаты наших галактик
ra, dec = loadtxt('Edgeon.csv', unpack=True,
                  usecols=[1,2], delimiter=',',
                  skiprows=1)

# Посмотрим список полей, которые можно запросить в Simbad
# print(Simbad.list_votable_fields())

# Нас интересуют поля fluxdata(filter), добавим их в запрос
Simbad.add_votable_fields('fluxdata(r)', 'fluxdata(B)')

# Теперь будем искать наши галактики в Simbad внутри радиуса field_radius
# относительно точки с координатами ra, dec
for i in range(len(ra)):
    field_radius = 0.05 * u.deg   # Зададим начальный радиус поиска

    # Сделаем запрос в Simbad и запишем результаты поиска в таблицу result_table
    result_table = Simbad.query_region(coord.SkyCoord(ra=ra[i], dec=dec[i],
                                       unit=(u.deg, u.deg), frame='icrs'),
                                       radius=field_radius)

    # Наша галактика -- первый найденный объект (потому result_table[0])
    # Если для неё нашлись звёздные величины в фильтрах B и R -- выведем
    # показатель цвета B-R
    if result_table[0]['FLUX_r'] and result_table[0]['FLUX_B']:
        color = float(result_table[0]['FLUX_B']) - float(result_table[0]['FLUX_r'])
        color = round(color, 3)
        print(f'{ra[i]}, {dec[i]}, {color}')
