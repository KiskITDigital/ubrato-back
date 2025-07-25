INSERT INTO objects_groups (name)
VALUES
    ( 'Жилая недвижимость' ),
    ( 'Объект здравоохранения' ),
    ( 'Объекты культурного наследия' ),
    ( 'Объекты образования' ),
    ( 'Офисная недвижимость' ),
    ( 'Природные объекты' ),
    ( 'Производственная недвижимость' ),
    ( 'Складская недвижимость' ),
    ( 'Спортивно-оздоровительные объекты' ),
    ( 'Территория' ),
    ( 'Торговая недвижимость' ),
    ( 'Транспорт' ),
    ( 'Транспортная инфраструктура' ),
    ( 'HoReCa' );

INSERT INTO objects_types (object_group_id, name)
VALUES
    ( 1, 'Дом' ),
    ( 1, 'Квартира' ),
    ( 1, 'Общежитие' ),
    ( 1, 'Коттедж' ),
    ( 1, 'Дача' ),
    ( 1, 'Апартаменты' ),
    ( 2, 'Больница' ),
    ( 2, 'Клиника' ),
    ( 2, 'Лечебный комлекс' ),
    ( 2, 'Поликлиника' ),
    ( 3, 'Памятник' ),
    ( 3, 'Мемориал' ),
    ( 3, 'Музей' ),
    ( 3, 'Архитектурный ансамбль' ),
    ( 4, 'Детский сад' ),
    ( 4, 'Ясли' ),
    ( 4, 'Школа' ),
    ( 4, 'ВУЗ' ),
    ( 5, 'Офис открытого типа (open spaсe)' ),
    ( 5, 'Кабинетная планировка офиса' ),
    ( 5, 'Комбинированный тип' ),
    ( 5, 'Кабинетно-коридорная планировка офиса' ),
    ( 5, 'Коворкинг' ),
    ( 6, 'Заповедник' ),
    ( 6, 'Парк' ),
    ( 7, 'Фабрика' ),
    ( 7, 'Завод' ),
    ( 7, 'Мастерская' ),
    ( 7, 'Цех' ),
    ( 8, 'Складской комплекс' ),
    ( 8, 'Склад индивидуального хранения' ),
    ( 8, 'Склад временного хранения (СВХ)' ),
    ( 8, 'Склад горюче-смазочных материалов (ГСМ)' ),
    ( 8, 'Теплый склад' ),
    ( 8, 'Холодильный склад' ),
    ( 8, 'Производственный склад' ),
    ( 8, 'Открытые склады' ),
    ( 8, 'Полуоткрытые склады' ),
    ( 8, 'Закрытые склады' ),
    ( 9, 'Стадион' ),
    ( 9, 'Спортзал' ),
    ( 9, 'Спортплощадка' ),
    ( 9, 'Бассейн' ),
    ( 9, 'Ледовый каток' ),
    ( 9, 'Корт' ),
    ( 9, 'Санаторий' ),
    ( 9, 'Туристическая база' ),
    ( 9, 'Баня' ),
    ( 9, 'Сауна' ),
    ( 9, 'Спортивно-оздоровительный комплекс' ),
    ( 9, 'Спортшкола' ),
    ( 9, 'Теннисный корт' ),
    ( 10, 'Земельный участок' ),
    ( 10, 'Водный участок' ),
    ( 10, 'Прибрежный участок' ),
    ( 10, 'Кейтиринг' ),
    ( 10, 'Тротуар' ),
    ( 10, 'Открытая парковка' ),
    ( 10, 'Газон' ),
    ( 11, 'Магазин' ),
    ( 11, 'Торговый центр' ),
    ( 11, 'Торгово-развлекательный центр' ),
    ( 11, 'Ритейл' ),
    ( 11, 'Гипермаркет' ),
    ( 11, 'Супермаркет' ),
    ( 12, 'Автомобильный' ),
    ( 12, 'Железнодорожный' ),
    ( 12, 'Авиационный' ),
    ( 12, 'Речной' ),
    ( 12, 'Морской' ),
    ( 13, 'Трубопровод' ),
    ( 13, 'Дорога' ),
    ( 13, 'Вокзал' ),
    ( 13, 'Транспортно-пересадочный узел (ТПУ)' ),
    ( 13, 'Станция' ),
    ( 13, 'Аэропорт' ),
    ( 13, 'Парковка' ),
    ( 13, 'Гараж' ),
    ( 13, 'Гаражно-строительный кооператив' ),
    ( 14, 'Гостиница' ),
    ( 14, 'Ресторан' ),
    ( 14, 'Кафе' ),
    ( 14, 'Отель' ),
    ( 14, 'Мотель' ),
    ( 14, 'Хостел' ),
    ( 14, 'Бар' ),
    ( 14, 'Столовая' ),
    ( 14, 'Буфет' ),
    ( 14, 'Кейтеринг' );

INSERT INTO services_groups (name)
VALUES
    ('Вывоз'),
    ('Дезинсекция'),
    ('Дезинфекция'),
    ('Дератизация'),
    ('Замена оборудования и инвентаря'),
    ('Комплексное обслуживание'),
    ('Мойка'),
    ('Мытье'),
    ('Очистка'),
    ('Полировка и укреплений покрытий'),
    ('Поставка товаров и расходных материалов'),
    ('Предоставление доп. персонала'),
    ('Промышленный альпинизм'),
    ('Уборка'),
    ('Услуги прачечной'),
    ('Химчистка'),
    ('Чистка');

INSERT INTO services_types (service_group_id, name)
VALUES
    (1, 'Твердых бытовых отходов (ТБО)'),
    (1, 'Твердых коммунальных отходов (ТКО)'),
    (1, 'Мусора'),
    (1, 'Строительного мусора'),
    (1, 'Снега'),
    (1, 'Вторсырья'),
    (1, 'Опасных отходов'),
    (2, 'Насекомых'),
    (2, 'Клещей'),
    (2, 'Мух'),
    (2, 'Комаров'),
    (2, 'Тараканов'),
    (2, 'Муравьев'),
    (2, 'Клопов'),
    (2, 'Постельных клопов'),
    (2, 'Блох'),
    (3, 'От коронавируса'),
    (3, 'От туберкулеза'),
    (3, 'После смерти'),
    (4, 'Дератизация'),
    (5, 'Замена грязезащитных покрытий'),
    (6, 'Комплексное обслуживание'),
    (7, 'Окон'),
    (7, 'Фасада'),
    (7, 'Вывески'),
    (7, 'Высотная'),
    (7, 'Промышленный альпинизм'),
    (7, 'Наружной рекламы и баннеров'),
    (7, 'Витрин'),
    (8, 'Посуды'),
    (8, 'Холодильного оборудования'),
    (9, 'Бассейна'),
    (9, 'Улиц от снега и льда'),
    (9, 'Зданий от снега и льда'),
    (9, 'Подметание улиц'),
    (9, 'От пыли'),
    (10, 'Полировка и восстановление каменных поверхностей'),
    (10, 'Кристаллизация мрамора'),
    (11, 'Антигололедный реагент'),
    (11, 'Гранитная крошка'),
    (11, 'Мешки для мусора'),
    (11, 'Урны'),
    (12, 'Предоставление доп. персонала'),
    (13, 'Промышленный альпинизм'),
    (14, 'Генеральная уборка'),
    (14, 'Ежедневная уборка'),
    (14, 'Интенсивная уборка'),
    (14, 'Основная уборка'),
    (14, 'Первичная уборка'),
    (14, 'Поддерживающая уборка'),
    (14, 'Уборка после ремонта'),
    (14, 'Послестроительная уборка'),
    (14, 'Уборка по графику'),
    (14, 'Уборка снега'),
    (14, 'Уборка прилегающей территории'),
    (14, 'Зимняя уборка'),
    (14, 'Летняя уборка'),
    (14, 'Уборка коммерческих помещений'),
    (14, 'Уборка всех видов помещений'),
    (14, 'Экоуборка'),
    (14, 'Поддерживающая'),
    (14, 'После пожара'),
    (14, 'После потопа и затопления канализацией'),
    (14, 'Снега'),
    (14, 'Дезодорация (устранение неприятных запахов)'),
    (14, 'Профилактика плесени'),
    (14, 'После установки окон'),
    (14, 'Влажная'),
    (14, 'Мусора'),
    (14, 'Механическая уборка (мехуборка)'),
    (14, 'Промышленным пылесосом'),
    (14, 'Уборка офиса'),
    (14, 'Уборка ТЦ'),
    (14, 'Уборка склада'),
    (14, 'Уборка ресторана'),
    (15, 'Услуги прачечной'),
    (16, 'Ковров'),
    (16, 'Мебели'),
    (16, 'Офисной мебели'),
    (16, 'Кресел'),
    (16, 'Диванов'),
    (16, 'Матрасов'),
    (16, 'Вискозных ковров'),
    (16, 'Шерстяных ковров'),
    (16, 'Сухая химчистка ковров'),
    (16, 'Кожаной мебели'),
    (16, 'Паласа'),
    (16, 'Штор'),
    (16, 'Жалюзи'),
    (16, 'Ковролина'),
    (16, 'Стриппинг'),
    (17, 'Аквачистка'),
    (17, 'Системы защиты от грязи на входе в помещение'),
    (17, 'Бластинг'),
    (17, 'Стриппинг'),
    (17, 'Ковров'),
    (17, 'Ковролина'),
    (17, 'Напольных покрытий'),
    (17, 'Текстильных покрытий'),
    (17, 'Офисной мебели'),
    (17, 'Мебели'),
    (17, 'Пароструйная очистка фасадов зданий'),
    (17, 'Пескоструйная очистка фасадов зданий'),
    (17, 'Чистка занавесей и штор'),
    (17, 'Дымоходов, печных труб, каминов'),
    (17, 'Плит и печей'),
    (17, 'Мусоросжигателей'),
    (17, 'Бойлеров'),
    (17, 'Вентиляционных шахт и вытяжных вентиляторов');
